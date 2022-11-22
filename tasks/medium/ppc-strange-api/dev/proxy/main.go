package main

import (
	"bufio"
	"errors"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"
)

func mix[T any](slice []T) {
	for l, r := 1, 2; r < len(slice); l, r = l+r, r+l+r {
		slice[l], slice[r] = slice[r], slice[l]
	}
}

const (
	timeout         = time.Second * 10
	shutdownTimeout = time.Second * 2
)

func ioDeadline() time.Time {
	return time.Now().Add(timeout)
}

func processLine(rc net.Conn, r *bufio.Reader, wc net.Conn, w *bufio.Writer) error {
	rc.SetReadDeadline(ioDeadline())
	data, rErr := r.ReadBytes('\n')

	var wrErr error
	if len(data) > 0 {
		if data[len(data)-1] == '\n' {
			data = data[:len(data)-1]
		}
		mix(data)
		wc.SetWriteDeadline(ioDeadline())
		_, wrErr = w.Write(append(data, '\n'))
		w.Flush()
	}

	if rErr == nil && wrErr == nil {
		return nil
	} else if rErr == nil {
		return fmt.Errorf("writing line: %w", wrErr)
	} else if rErr == io.EOF {
		return io.EOF
	}
	return fmt.Errorf("reading line: %w", rErr)
}

func proxy(done <-chan struct{}, from net.Conn, to net.Conn) error {
	fromb, tob := bufio.NewReader(from), bufio.NewWriter(to)

	for {
		// Simple cancellation mechanism. Won't work immediately, but will stop the connection eventually.
		select {
		case <-done:
			return nil
		default:
		}

		if err := processLine(from, fromb, to, tob); err == io.EOF {
			return nil
		} else if err != nil {
			return err
		}
	}
}

type Proxy struct {
	Addr string
	To   string
	Log  *log.Logger

	listener     net.Listener
	shutdownCh   chan struct{}
	onceInit     sync.Once
	onceShutdown sync.Once
}

// ListenAndServe starts a net.Listener on the supplied address and immediately starts accepting new
// connections, which are then handled in their own goroutines.
func (p *Proxy) ListenAndServe() error {
	var once bool
	p.onceInit.Do(func() {
		once = true
		p.shutdownCh = make(chan struct{})

		if p.Log == nil {
			p.Log = log.Default()
		}
	})

	if !once {
		return errors.New("proxy: already started")
	}

	l, err := net.Listen("tcp", p.Addr)
	if err != nil {
		return fmt.Errorf("proxy: launching listener: %w", err)
	}
	p.listener = l

	for {
		c, err := l.Accept()
		if err != nil {
			return fmt.Errorf("proxy: accepting new connections: %w", err)
		}

		go func() {
			defer c.Close()

			addr := c.RemoteAddr().String()
			prefix := fmt.Sprintf("proxy: handling connection from %s", addr)
			p.Log.Println(prefix)
			if err := p.handle(c); err != nil {
				p.Log.Printf("%s: %s\n", prefix, err.Error())
			}
			p.Log.Printf("proxy: connection from %s done", addr)
		}()
	}
}

// Shutdown tries to gracefully shutdown the server by notifying the running goroutines about the shutdown
// and then waiting for 10 seconds before returning.
func (p *Proxy) Shutdown() {
	p.onceShutdown.Do(func() {
		p.listener.Close()
		close(p.shutdownCh)
		time.Sleep(shutdownTimeout)
	})
}

// handle handles a single connection by connecting to the upstream
// and then proxying each request and response back and forth between
// the client and the server
func (p *Proxy) handle(c net.Conn) error {
	srv, err := net.Dial("tcp", p.To)
	if err != nil {
		return fmt.Errorf("dialing upstream: %w", err)
	}
	defer srv.Close()

	connErrs := make(chan error, 2)
	done := make(chan struct{})
	oneWayProxy := func(info string, from, to net.Conn) {
		if err := proxy(done, from, to); err != nil {
			connErrs <- fmt.Errorf("%s: %w", info, err)
			return
		}
		connErrs <- nil
	}

	go oneWayProxy("proxying client to server", c, srv)
	go oneWayProxy("proxying server to client", srv, c)

	var closeOnce sync.Once
	closeDone := func() {
		closeOnce.Do(func() {
			// close after timeout to allow writers/readers to finish
			time.AfterFunc(timeout, func() {
				close(done)
			})
		})
	}

	// monitor server status to gracefully close connections
	go func() {
		select {
		case <-p.shutdownCh:
			closeDone()
		case <-done:
		}
	}()

	var savedErr error
	for i := 0; i < 2; i++ {
		err := <-connErrs
		if err == nil {
			continue
		}

		closeDone()
		if savedErr == nil {
			savedErr = err
		}
	}
	// We might've not closed done if both connections ended successfully
	closeDone()
	close(connErrs)
	return savedErr
}

func main() {
	if len(os.Args) != 3 {
		fmt.Fprintf(os.Stderr, "Usage: %s from to\n\tWill listen on 'from' and proxy the requests to 'to'.\n", os.Args[0])
		os.Exit(2)
	}

	p := Proxy{
		Addr: os.Args[1],
		To:   os.Args[2],
	}

	signals := make(chan os.Signal, 1)
	signal.Notify(signals, syscall.SIGINT, syscall.SIGQUIT, syscall.SIGTERM)

	var wg sync.WaitGroup
	wg.Add(1)
	// monitor signals for graceful shutdown
	go func() {
		<-signals
		log.Println("gracefully shutting down")
		p.Shutdown()
		wg.Done()
	}()

	if err := p.ListenAndServe(); err != nil {
		if !errors.Is(err, net.ErrClosed) {
			log.Println(err)
		}
	}
	wg.Wait()
}
