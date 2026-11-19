// gta6-meme-x-01 entry: "GTA VI Is Out — My Agent Got Paid".
//
// The entry itself is the X post: an agent-made GTA 6 meme (meme.png,
// drawn by draw_meme.py) posted from a public X account, with make.fun and
// the entrant's play code in the post's text. The house reads that post
// from X and hands its first picture plus its text to the judge.
//
// This program (Node 22, standard library only, no network, no clock, no
// files outside the repository) does the one job the harness asks of it:
// it copies POST.json from the repository root into the output directory,
// where the gate reads the post's address from it. It first checks that
// POST.json parses as a JSON object carrying a url string, so a placeholder
// or a broken file fails loudly instead of being handed in silently. On
// success it prints nothing. Run it the way the grader does:
//
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// The two runs of an entry must write the same bytes: copying one file
// byte for byte always does.

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const postPath = join(botDir, "POST.json");

let post: unknown;
try {
  post = JSON.parse(readFileSync(postPath, "utf8"));
} catch (err) {
  console.error(`POST.json could not be read from ${botDir}: ${(err as Error).message}`);
  process.exit(1);
}

if (
  typeof post !== "object" ||
  post === null ||
  typeof (post as { url?: unknown }).url !== "string" ||
  ((post as { url: string }).url.length === 0)
) {
  console.error("POST.json must be a JSON object with a non-empty url string.");
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
try {
  copyFileSync(postPath, join(outputDir, "POST.json"));
} catch (err) {
  console.error(`POST.json could not be copied from ${botDir}: ${(err as Error).message}`);
  process.exit(1);
}
