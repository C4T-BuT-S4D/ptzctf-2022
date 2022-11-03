package main

import (
	"bytes"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"runtime"
	"sync"

	"data-grinder/algos"
)

type Processed struct {
	HashName  string `json:"hash"`
	Size      int    `json:"size"`
	HexDigest string `json:"digest"`
}

var (
	algorithms map[string]*algos.Algorithm
	tables     map[string]map[string][]byte
)

func init() {
	// Initialize algorithms
	algorithms = make(map[string]*algos.Algorithm)
	for i := range algos.Algorithms {
		a := &algos.Algorithms[i]
		algorithms[a.Name] = a
	}

	// Initialize rainbow tables
	tables = make(map[string]map[string][]byte)
	for k, v := range algorithms {
		tables[k] = make(map[string][]byte)
		b := make([]byte, 2)
		h := v.InstancePool.Get()
		defer v.InstancePool.Put(h)

		for {
			h.Reset()
			if _, err := h.Write(b); err != nil {
				panic("hashing: " + err.Error())
			}

			result := h.Sum(nil)
			tables[k][string(result)] = append([]byte(nil), b...)

			if increment(b) {
				break
			}
		}
	}
}

func increment(b []byte) bool {
	for i := len(b) - 1; i >= 0; i-- {
		b[i]++
		if b[i] != 0 {
			return false
		}
	}
	return true
}

func bruteforce(p Processed) []byte {
	a := algorithms[p.HashName]
	need, err := hex.DecodeString(p.HexDigest)
	if err != nil {
		panic(p)
	}

	// Try simple table lookup first
	if b, ok := tables[p.HashName][string(need)]; ok {
		return b
	}

	b := make([]byte, p.Size)
	h := a.InstancePool.Get()
	defer a.InstancePool.Put(h)
	for {
		h.Reset()
		if _, err := h.Write(b); err != nil {
			panic("hashing: " + err.Error())
		}

		got := h.Sum(nil)
		if bytes.Equal(need, got) {
			return b
		}
		if increment(b) {
			break
		}
	}
	panic(fmt.Sprintf("couldn't find match for %+v", p))
}

func main() {
	// Initialize workers
	nWorkers := runtime.NumCPU()

	type job struct {
		Processed
		Out chan<- []byte
	}
	jobs := make(chan job, nWorkers)

	var wg sync.WaitGroup
	for i := 0; i < nWorkers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for job := range jobs {
				job.Out <- bruteforce(job.Processed)
			}
		}()
	}

	// Initialize result combiner
	output := make(chan chan []byte, nWorkers)
	wg.Add(1)
	go func() {
		defer wg.Done()
		for out := range output {
			b := <-out
			os.Stdout.Write(b)
		}
	}()

	// Parse all chunks
	d := json.NewDecoder(os.Stdin)
	var p Processed
	for {
		if err := d.Decode(&p); err != nil {
			if err == io.EOF {
				break
			}
			panic(err)
		}
		out := make(chan []byte)
		jobs <- job{p, out}
		output <- out
	}

	close(jobs)
	close(output)
	wg.Wait()
}
