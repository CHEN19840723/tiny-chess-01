# tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/CHEN19840723/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/CHEN19840723/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A 4 KB Python chess engine: iterative-deepening PVS, quiescence, a transposition table, null-move pruning, killers and history, packed into 2754 bytes with makefun compress. The strength-tuned R8 engine scored 18.0/20 against R7 (16 wins, 4 draws, 0 losses), with zero timeouts or illegal moves; maximum move time was 8.773 seconds. See the untracked R8-STRENGTH-TAIL-REPORT.md for validation details.

## Validation

- Depth acceptance: three middlegames reached depths 8, 8 and 8 (mean 8.00).
- Search speed: 24,884–31,955 nodes/s (mean 28,887).
- Readable engine source and validation details remain in the working tree, outside this compact commit.

## Run it

```sh
python3 -P -s main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=be3a1ry7&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
