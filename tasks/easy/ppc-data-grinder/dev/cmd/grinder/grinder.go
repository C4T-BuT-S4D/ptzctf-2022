package main

import (
	"bufio"
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"math/big"
	"os"

	"data-grinder/algos"
)

type Processed struct {
	HashName  string `json:"hash"`
	Size      int    `json:"size"`
	HexDigest string `json:"digest"`
}

func pickAlgorithm() (*algos.Algorithm, error) {
	b, err := rand.Int(rand.Reader, big.NewInt(int64(len(algos.Algorithms))))
	if err != nil {
		return nil, fmt.Errorf("getting random data: %w", err)
	}
	return &algos.Algorithms[b.Int64()], nil
}

func processChunk(b []byte) (Processed, error) {
	a, err := pickAlgorithm()
	if err != nil {
		return Processed{}, err
	}

	h := a.InstancePool.Get()
	defer a.InstancePool.Put(h)
	if _, err := h.Write(b); err != nil {
		return Processed{}, fmt.Errorf("hashing %s: %w", hex.EncodeToString(b), err)
	}
	return Processed{HashName: a.Name, Size: len(b), HexDigest: hex.EncodeToString(h.Sum(nil))}, nil
}

func processFile(name string, chunkSize int) error {
	f, err := os.Open(name)
	if err != nil {
		return fmt.Errorf("opening file: %w", err)
	}

	e := json.NewEncoder(os.Stdout)
	r := bufio.NewReader(f)
	b := make([]byte, chunkSize)

	for {
		n, err := r.Read(b)
		if n != 0 {
			chunk, err := processChunk(b[:n])
			if err != nil {
				return fmt.Errorf("processing chunk: %w", err)
			}

			if err := e.Encode(chunk); err != nil {
				return fmt.Errorf("encoding chunk: %w", err)
			}
		}

		if err != nil {
			if err == io.EOF {
				break
			}
			return fmt.Errorf("reading file: %w", err)
		}
	}
	return nil
}

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintf(os.Stderr, "Usage: %s file\n", os.Args[0])
		return
	}

	if err := processFile(os.Args[1], 2); err != nil {
		fmt.Fprintf(os.Stderr, "Error while processing file: %s", err.Error())
	}
}
