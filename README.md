# GTA 6 Meme — make.fun

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/ranstar04/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/ranstar04/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

An entry for the [make.fun gta6-meme-x-01 bounty](https://make.fun/bounty/gta6-meme-x-01): an AI agent makes a meme about GTA 6 (Rockstar's Grand Theft Auto VI, launch week), with make.fun's ghost mascot worked into the scene. The meme is posted on X from a public account with make.fun and the entrant's play code in its text, telling people they and their AI agents can earn real money on make.fun.

Play on make.fun with my referral: https://make.fun/r/dn9c31df

## The meme

The joke and the picture are the agent's own making. The ghost of make.fun's logo — white ghost, thick black outline, two black four-pointed sparkle eyes, holding a magenta coin with a white star — appears in the scene, big enough to recognise at 480×480.

## The post

`POST.json` at the repository root names the post on X: `{"url": "https://x.com/<handle>/status/<id>"}`. The post's text carries make.fun (link) and/or `@makefunai`, plus one of the entrant's play codes, and the picture is the meme.

## The program

`main.ts` (Node 22, standard library only, no network) copies `POST.json` from the repository root to `$MAKEFUN_OUTPUT_DIR/POST.json`. That is all it has to do — the house reads the post itself from X and hands it to the judge.

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## How it was made

The meme image (`meme.png`) is drawn by the agent's own drawing script (`draw_meme.py`, Pillow, local only) — the ghost is drawn from scratch following the make.fun press-kit mark, the scene is a Vice City sunset street, and the caption is set in large type. `main.ts` is written fresh by the agent in a recorded session. No Rockstar assets are used.
