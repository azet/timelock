#!/usr/bin/env python3
#
# Time-Lock Puzzle as described by Rivest, Shamir & Wagner
# ref.: http://www.hashcash.org/papers/time-lock.pdf
#
# Author:   Aaron Zauner <azet@azet.org>
# License:  CC0 1.0 (https://creativecommons.org/publicdomain/zero/1.0)
# Depends:  `pip3 install cryptography`
#
import os, random
from cryptography.hazmat.backends               import default_backend
from cryptography.hazmat.primitives.asymmetric  import rsa
from cryptography.hazmat.primitives.ciphers     import (
                                                    Cipher,
                                                    algorithms,
                                                    modes
                                                )

class TimeLockPuzzle:
    def __init__(self, message, seconds, squarings='1000', keysize='2048'):
        self.M = bytes(message)
        self.T = int(seconds)
        self.S = int(squarings)
        rsa_   = rsa.generate_private_key(
            public_exponent = 65537,
            key_size        = keysize,
            backend         = default_backend()
        )
        self.n = rsa_.private_numbers().public_numbers.n
        self.t = self.T * self.S
        self.K = os.urandom(32)

    def __exit__(self):
        rsa_   = None
        self.n = None
        self.K = None

    def encrypt(self):
        self.a  = random.SystemRandom().randint(1, self.n)
        self.iv = os.urandom(16)
        enc = Cipher(
            algorithms.AES(self.K),
            modes.OFB(self.iv),
            backend = default_backend()
        ).encryptor()
        self.C_M = enc.update(self.M) + enc.finalize()
        self.C_K = self.K + (pow(self.a, pow(2, self.t)) % self.n)
        return self.C_M, self.iv, self.C_K, self.a, self.t, self.n

def test():
    timelock = TimeLockPuzzle(
        message=b'hello gracious world',
        seconds=3600,
        squarings=4,
        keysize=512
    )
    print(timelock.encrypt())

def main():
    test()

if __name__ == '__main__':
    main()

