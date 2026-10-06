# Narrated video guide

How the Module 05 deck becomes a video in which a small animal types short notes in speech bubbles, with typing sound
(`slides/m05/remotion/out/m05-narrated.mp4`). The slides are **not touched**: everything is in `slides/m05/remotion/src/video/` and
two scripts, and the video has its own Remotion entry point (`src/video/entry.ts`). Deck authoring is in `REMOTION_DECK_GUIDE.md`.
Shell commands and file paths only.

## Make it

```sh
cd slides/m05/remotion
node scripts/extract_mechvibes.mjs --pack=cherrymx-red-abs --release=0.5   # typing samples, once (sounds/, not committed)
npm run video:prose                  # the slides' own sentences -> src/video/prose.json (committed); again whenever a slide's sentences change
npm run video:audio                  # out/video-public/typing.wav, from the same keystrokes the video shows
npm run video                        # out/m05-narrated.mp4 (about 10 minutes of rendering for 21 minutes of video)
npm run video:sampler                # a listening test of all ten keyboard packs: then render_video.mjs --id=M05-sampler --out=out/sound-packs.mp4
node scripts/render_video.mjs --frames=1890-2145 --out=out/clip.mp4        # a part
node scripts/render_video.mjs --still=1900,2000 --dir=out/video-stills     # single frames
```

Run `npm run video:audio` again after **any** change to the narration, to a slide's `marks`, to `src/video/prose.json` or to the sound: the timeline
(and so every key time) changes, and the audio must follow.

## What the video is

One continuous talk, not chapters: the three section dividers (S1, S8, S22) are left out (`SKIP` in `src/video/timeline.ts`), the chat is never cleared at a slide
change, and the bridge from one part to the next is in the first lines of the next slide (S9, S23). Each slide plays stage by stage as in the click-through deck.
After a stage's animation **has finished** the picture is held while the narrator types that stage's lines, then the next stage starts. The animal sits at the
bottom left; two bubbles at most; a new bubble pops up at the bottom and pushes the older one up; all of it stays in the free band under the slides (below y = 920).

### The slides' sentences move into the chat

The lecturer: text appearing on a slide while a comment is being read ("bang bang bang") is hard to follow, so the slide's words should go into the chat.
So in the video the slides are drawn with `ProseContext = 'hide'` (`src/components/Text.tsx`): a `Box`, `Cap` or `Tag` with **at least five words and no formula** is not drawn.
Labels (under five words), numbers, figures and formulas stay on the slide. `npm run video:prose` finds those sentences: it renders every slide at the end of every
stage with `ProseContext = 'collect'`, reads what the page logs (`onBrowserLog`), keeps the ones visible at the stage end that were not visible at the end of the stage
before, in reading order, and writes `src/video/prose.json`. The video types them first in their stage (cut into bubble-sized lines, capitalized). The default
mode is `'show'`, so the deck, the review stills and the student html are unchanged. The slide files are never edited.

## Writing the narration (`src/video/narration.ts`)

`narration[slide number][stage index] = [line, ...]`; one line is one bubble. The lines **add** to the slide's own sentences (which come first, or where the line
`'@mirror'` stands): why, how to read the picture, what to compare, the bridge to the next idea. Lecturer: "writing what can be seen is fine, but add some supplement".
- A line is one short plain sentence, at most 64 characters (`MAX_CHARS` in `src/video/timeline.ts`; longer throws). One or two lines per stage, not every stage. No em dash, no rhetoric.
- **A question slide gets no answer**: its notes end with a prompt ("Take a moment to guess.").
- Length: about 190 bubbles (60 sentences from the slides, about 120 written lines) is 21 minutes. Typing time dominates (about 8,000 keystrokes). Trim lines, not typing speed: past
  about 12 characters a second the typing stops looking like typing.
- English, like the slides. The text in the repo is a draft by the agent; the lecturer edits it.

## Typing (`src/video/typing.ts`, pure, deterministic)

Keys come in uneven bursts (interval about 58 ms times a random factor 0.62 to 1.5, two keys in quick succession 12% of the time), slower after a space
(+18 to 73 ms) and after punctuation (+110 to 250 ms), with an occasional hesitation. A wrong neighbouring key (QWERTY adjacency) is typed with
probability 1.2% per eligible letter, at most 2 per line, only in lines of 14+ characters; the typist carries on for 0 to 2 letters, notices after
190 to 420 ms, backspaces quickly, and types the letter again. The seed is the text and its place, so a render is repeatable.

## Timeline (`src/video/timeline.ts`, no React so that node can import it)

`SKIP` the dividers; `stageLines` puts a stage's slide sentences and written lines in order; `LEAD` 20 frames after a stage's animation before the first key; `POP` 9 frames from the bubble appearing to the first key; `GAP` 26 between bubbles; `READ`
38 after the last key; `HOLD` 30 after a stage without narration. `buildTimeline(marks, narration)` returns slides, stages (`anim` frames of play,
`hold` frames frozen), bubbles with the global frame of each keystroke, and all key times (used for the sound).
`NarratedDeck.tsx` plays a stage with `<Sequence from={-slideFrom}>` inside a `<Sequence>` (the slide starts in the middle) and holds its end with `<Freeze>`.
`scripts/make_typing_audio.mjs` bundles `src/video/audio-entry.ts` with esbuild for node and reads `marks` from the slide files by regex like
`scripts/review.mjs`: **modules used there must import no React, css or pictures.**

## The sound

Each keystroke has its sound at the same frame as its letter on screen. Kinds: key, space, backspace. **The space bar is silent** by default
(`--space-sound` to turn it on): the lecturer found it distracting. Without samples the sound is synthesized (filtered noise plus a falling sine);
with WAV files in `sounds/` (`key-*.wav`, `space-*.wav`, `back-*.wav`) those are used (random pick, never the same twice in a row, pitch varied by 7%, or 12%
when a kind has fewer than three samples, relative loudness kept).

### Sampling from Mechvibes (what worked)

Mechvibes and MechvibesDX (MIT, github.com/hainguyents13/mechvibes-dx; the pre-installed packs are by "Mechvibes") ship keyboard sound packs. The packs
are on disk after installing the app: `/Applications/MechvibesDX.app/Contents/Resources/soundpacks/keyboard/<pack>/` (the classic app keeps its packs in
`~/Library/Application Support/Mechvibes/soundpacks`). The site beta.mechvibes.com itself offers no direct file links, and a web fetch of it lists
nothing reliable: use the installed app.

A pack is `config.json` plus one long audio file (`sound.ogg`, about 40 s): `definition_method: "single"`, `audio_file`, and
`definitions` = `{KeyboardEvent.code: {timing: [[pressStart, pressEnd], [releaseStart, releaseEnd]]}}` in milliseconds (`KeyA`, `Space`, `Backspace`, ...).
`scripts/extract_mechvibes.mjs --pack=NAME [--release=G] [--lowpass=HZ] [--out=DIR] [--from=DIR]` decodes it with the ffmpeg that Remotion ships,
cuts press plus release for ten letters, `Space` and `Backspace`, and writes `sounds/key-1..10.wav`, `space-1.wav`, `back-1.wav` and `SOURCE.txt`.
`--release` (default 0.6) is the gain of the key coming back up: the release click is what makes a clicky switch scratchy.

How bright each pack is (mean over the ten key samples; centroid in Hz, share of energy above 4 kHz):

| pack | centroid | > 4 kHz | feel |
| --- | --- | --- | --- |
| topre-purple-hybrid-pbt | 1,136 | 0.03 | low, soft thock |
| cherrymx-red-abs | 2,393 | 0.10 | smooth linear: the "sukosuko" the lecturer asked for (default) |
| eg-crystal-purple | 2,775 | 0.19 | tactile, mid |
| cherrymx-black-pbt / -abs | 3,109 / 3,538 | 0.15 / 0.23 | deeper linear |
| eg-oreo | 3,599 | 0.31 | thock with a bright top |
| cherrymx-brown-pbt / -abs | 3,740 / 4,576 | 0.28 / 0.35 | tactile |
| cherrymx-blue-pbt / -abs | 5,516 / 7,037 | 0.44 / 0.67 | clicky: "karikari", **too bright** for this use |

The lecturer's brief: a mechanical keyboard, a soft "sukosuko", not clicky (Blue sounded scratchy), and no space bar. To choose a pack render a short clip with
each (`--frames=` around one note) and compare: Remotion keeps the audio when it renders a frame range.
`npm run video:sampler` renders a listening test: every pack in turn types the same sentence (with one typo and a backspace) under its own name, so only the sound differs
(`src/video/SoundSampler.tsx`, `sampler.ts`); it is how the packs in the table were compared.
Own recordings: one keystroke per WAV, 0.15 to 0.4 s, dry, 6 to 10 letter keys, 2 to 4 space, 2 to 4 backspace (`sounds/README.md`); commit them with `git add -f`
(the generated Mechvibes samples are ignored by git).

### Checking the sound without ears

Extract the audio of a rendered clip (`npx remotion ffmpeg -i clip.mp4 -vn -ac 1 -ar 44100 clip.wav`) and compare the first onsets with the planned key times
(they agree to a frame); measure peak, rms and the spectrum of the loud blocks. An agent cannot hear the result: say so, and let the lecturer listen.

## The animal and the bubbles (`src/video/Critter.tsx`, `Narrator.tsx`)

An original drawing (a cream cat with a tan patch over one ear and eye), not a copy of any reference image. Its pose is a pure function of the frame: mouth
open on each key, paws alternate, a hop when a bubble pops, a blink every 104 frames, ears twitch, lines wobbled by a turbulence filter that changes seed every
7 frames. Bubbles use the deck's light blue (`C.blueSoft`), Inter 32 px, a tail on the newest one, a blinking cursor while typing. Sizes are chosen so that two
one-line bubbles and the animal fit in the 160 px band.

## Checks before handing it over

`npx remotion ffprobe out/m05-narrated.mp4` (duration, 1920x1080 30 fps, AAC audio); stills of a few narrated frames (animal, bubbles, nothing above y = 920);
onsets against key times; `git status` shows no change under `src/slides/`.
