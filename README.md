# timelock
Implementation of the Time Lock Puzzle as described by Rivest, Shamir
and Wagner in [0].

## Caveat
This is **a testing ground**. This code does not work (mainly because it's unclear from the paper how the key `K` is generated and used with `C_K = K + 2^a^t (mod n)`. The only possible way I can think of is generating and using a 160+bit integer). It is also extremely inefficient.

## References
[0] http://www.hashcash.org/papers/time-lock.pdf (2.1)

## License
CC0 1.0 (https://creativecommons.org/publicdomain/zero/1.0)
