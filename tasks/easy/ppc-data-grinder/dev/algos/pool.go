package algos

import (
	"hash"
	"sync"
)

type HashPool struct {
	pool sync.Pool
	New  func() hash.Hash
}

func (p *HashPool) Get() hash.Hash {
	if p.pool.New == nil {
		p.pool.New = func() any {
			return p.New()
		}
	}
	return p.pool.Get().(hash.Hash)
}

func (p *HashPool) Put(h hash.Hash) {
	h.Reset()
	p.pool.Put(h)
}
