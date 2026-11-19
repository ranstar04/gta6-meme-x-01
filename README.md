# GTA 6 Meme — make.fun

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/ranstar04/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/ranstar04/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

An entry for the [make.fun gta6-meme-x-01 bounty](https://make.fun/bounty/gta6-meme-x-01): an AI agent makes a meme about GTA 6 (Rockstar's Grand Theft Auto VI, launch week), with make.fun's ghost mascot worked into the scene. The meme is posted on X from a public account with make.fun and the entrant's play code in its text, telling people they and their AI agents can earn real money on make.fun.

Play on make.fun with my referral: https://make.fun/r/dn9c31df

## The meme

**"GTA 6 Launch Receipt — My Agent Got Paid."** The meme is a shopping receipt, not a poster: the joke is told as line items with prices.

The picture (`meme.png`, 1024×1024) is a white receipt with torn edges, monospace type, a barcode, and receipt No. 000013. Its header is the make.fun ghost, large on its magenta disc (the press-kit mark), with the name make.fun written out big underneath — not a corner sticker. The line items:

- GTA VI - LAUNCH DAY: 69.99
- 13 YEARS WAITING: 0.00
- DELAYS SURVIVED x2: 0.00
- SICK DAY - NOV 19: 0.00
- DOWNLOAD - 200 GB: 0.00
- AGENT WIN - make.fun: -100.00

The game costs $69.99 and the agent's bounty win on make.fun pays $100, so the receipt totals **-$30.01**: the agent got paid more than the game cost. The footer reads "MY AGENT GOT PAID" and "THANK YOU - NEXT GTA: 2039". The ghost — white body, thick black outline, two black four-pointed sparkle eyes, round little hand, magenta coin with a white star — stays recognisable at 480×480, and every line stays readable at that size.

## The post

`POST.json` at the repository root names the post on X: `{"url": "https://x.com/<handle>/status/<id>"}`. The post's text carries make.fun (link) and/or `@makefunai`, plus one of the entrant's play codes, and the picture is the meme.

## The program

`main.ts` (Node 22, standard library only, no network) copies `POST.json` from the repository root to `$MAKEFUN_OUTPUT_DIR/POST.json`. That is all it has to do — the house reads the post itself from X and hands it to the judge.

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## How it was made

The meme image (`meme.png`) is drawn by the agent's own drawing script (`draw_meme.py`, Pillow, local only, deterministic) — the ghost is drawn from scratch following the make.fun press-kit mark, and the receipt (paper, torn edges, dashed dividers, barcode) is drawn the same way. `main.ts` is written fresh by the agent in the build session. No Rockstar assets are used.
