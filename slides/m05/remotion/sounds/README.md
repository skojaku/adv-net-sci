# Recorded typing sounds (optional)

`npm run video:audio` uses the WAV files in this folder when they are here, and the synthesized sound for any kind that has none.

| file name | what | how many |
| --- | --- | --- |
| `key-1.wav`, `key-2.wav`, ... | one press of an ordinary key (down and up in one clip) | 6 to 10, each a little different |
| `space-1.wav`, ... | one press of the space bar | 2 to 4 |
| `back-1.wav`, ... | one press of the backspace key | 2 to 4 |

- WAV (PCM 16 or 24 bit, or 32 bit float), mono or stereo, any sample rate.
- One keystroke per file, 0.15 to 0.4 s long, dry (no music, no room noise, no key repeating).
- The script cuts the silence before the click, so a little room before it does no harm; it levels every file itself.
