// News-image entry for make.fun news-image-20261121 (Node 22, standard
// library only). The finished image is entry.png beside this file: a
// one-page newspaper front page drawn in code (see draw.py) summing up
// the world's news of Saturday 21 November 2026. The program copies it
// to /output/entry.png. Outside the grader's container,
// MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const image = new URL("./entry.png", import.meta.url);
if (!existsSync(image)) {
  throw new Error("entry.png is missing next to main.ts; nothing to copy.");
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(image, join(outDir, "entry.png"));
