// news-image-20261119 — entry program.
//
// The entry image is the file entry.png beside this program. This program
// reads it and writes it, byte for byte, to /output/entry.png (or to the
// directory named by MAKEFUN_OUTPUT_DIR when run outside the grader).
// It touches nothing else: no network, no clock, no randomness, so two
// runs always produce identical bytes.
//
// The image itself is composed by compose.py (PIL) from four editorial
// illustrations in assets/ plus text and icons drawn by that script.
// Run it first:  python3 compose.py
// Then test this program:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(outDir, { recursive: true });
const bytes = readFileSync(join(here, 'entry.png'));
writeFileSync(join(outDir, 'entry.png'), bytes);
