# Recorded typing sounds (optional)

The samples here are generated (not committed): `node scripts/extract_mechvibes.mjs --pack=cherrymx-blue-abs` cuts them out of a Mechvibes sound pack installed with MechvibesDX (see `SOURCE.txt`; other packs: `cherrymx-brown-abs`, `topre-purple-hybrid-pbt`, `cherrymx-red-abs`, ...). Your own recordings go here too, in the same file names; commit those with `git add -f`.

`npm run video:audio` uses the WAV files in this folder when they are here, and the synthesized sound for any kind that has none (the space bar is silent unless `--space-sound` is given; see `slides/NARRATED_VIDEO_GUIDE.md`).

| file name | what | how many |
| --- | --- | --- |
| `key-1.wav`, `key-2.wav`, ... | one press of an ordinary key (down and up in one clip) | 6 to 10, each a little different |
| `space-1.wav`, ... | one press of the space bar | 2 to 4 |
| `back-1.wav`, ... | one press of the backspace key | 2 to 4 |

- WAV (PCM 16 or 24 bit, or 32 bit float), mono or stereo, any sample rate.
- One keystroke per file, 0.15 to 0.4 s long, dry (no music, no room noise, no key repeating).
- The script cuts the silence before the click, so a little room before it does no harm; it levels every file itself.
