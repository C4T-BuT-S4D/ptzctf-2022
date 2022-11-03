package algos

import (
	"crypto/md5"
	"crypto/sha256"
	"hash"

	"golang.org/x/crypto/blake2s"
	"golang.org/x/crypto/ripemd160"
	"golang.org/x/crypto/sha3"
)

type Algorithm struct {
	Name         string
	InstancePool HashPool
}

var Algorithms = []Algorithm{
	{"md5", HashPool{New: md5.New}},
	{"sha256", HashPool{New: sha256.New}},
	{"sha3-256", HashPool{New: sha3.New256}},
	{"ripemd160", HashPool{New: ripemd160.New}},
	{"blake2s-256", HashPool{New: func() hash.Hash {
		h, e := blake2s.New256(nil)
		if e != nil {
			panic("failed to initialize blake2s: " + e.Error())
		}
		return h
	}}},
}
