# tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/CHEN19840723/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/CHEN19840723/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A 4 KB Python chess engine: iterative-deepening PVS, quiescence, a transposition table, null-move pruning, killers and history, packed into 2823 bytes. In the local 20-game R8-vs-R7 match it scored 20/20 (10/10 with each colour), with zero timeouts or illegal moves; maximum move time was 8.182 seconds.

## Validation

- Depth acceptance: three middlegames reached depths 7, 7 and 8 (mean 7.33).
- Search speed: 21,388–31,639 nodes/s (mean 27,715).
- Engine source: `engine.py`; match details: `tools/match-results.json` and `R8-REPORT.md`.

## Run it

```sh
python3 -P -s main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=be3a1ry7&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
