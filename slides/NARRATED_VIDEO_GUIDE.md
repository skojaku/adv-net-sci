# Narrated video guide

How the Module 05 deck becomes a video in which a small figure lying down types short notes as terminal lines, with typing sound
(`slides/m05/remotion/out/m05-narrated.mp4`). The slides are **not touched**: everything is in `slides/m05/remotion/src/video/` and
two scripts, and the video has its own Remotion entry point (`src/video/entry.ts`). Deck authoring is in `REMOTION_DECK_GUIDE.md`.
Shell commands and file paths only.

## Make it

```sh
cd slides/m05/remotion
node scripts/extract_mechvibes.mjs --pack=cherrymx-red-abs --release=0.5   # typing samples, once (sounds/, not committed)
npm run video:prose                  # the slides' own sentences -> src/video/prose.json (committed); again whenever a slide's sentences change
npm run video:audio                  # out/video-public/typing.wav, from the same keystrokes the video shows
npm run video                        # out/m05-narrated.mp4 (about 12 minutes of rendering for 26 minutes of video)
npm run video:sampler                # a listening test of all ten keyboard packs: then render_video.mjs --id=M05-sampler --out=out/sound-packs.mp4
node scripts/render_video.mjs --frames=1890-2145 --out=out/clip.mp4        # a part
node scripts/render_video.mjs --still=1900,2000 --dir=out/video-stills     # single frames
```

Run `npm run video:audio` again after **any** change to the narration, to a slide's `marks`, to `src/video/prose.json` or to the sound: the timeline
(and so every key time) changes, and the audio must follow.

## What the video is

One continuous talk, not chapters: the three section dividers (S1, S8, S22) are left out (`SKIP` in `src/video/timeline.ts`), the chat is never cleared at a slide
change, and the bridge from one part to the next is in the first lines of the next slide (S9, S23). Each slide plays stage by stage as in the click-through deck.
After a stage's animation **has finished** the picture is held while the narrator types that stage's lines, then the next stage starts. The figure sits a little left of centre (x about 150 to 400; the first version had it at the edge), the terminal lines to its right; all of it stays in the free band under the slides (below y = 920).

### The slides' sentences move into the chat

The lecturer: text appearing on a slide while a comment is being read ("bang bang bang") is hard to follow, so the slide's words should go into the chat.
So in the video the slides are drawn with `ProseContext = 'hide'` (`src/components/Text.tsx`): a `Box`, `Cap` or `Tag` with **at least five words and no formula** is not drawn.
Labels (under five words), numbers, figures and formulas stay on the slide. `npm run video:prose` finds those sentences: it renders every slide at the end of every
stage with `ProseContext = 'collect'`, reads what the page logs (`onBrowserLog`), keeps the ones visible at the stage end that were not visible at the end of the stage
before, in reading order, and writes `src/video/prose.json`. The video types them first in their stage (cut into lines that fit, capitalized). The default
mode is `'show'`, so the deck, the review stills and the student html are unchanged. The slide files are never edited.

## Writing the narration (`src/video/narration.ts`)

`narration[slide number][stage index] = [line, ...]`; one line is one terminal line. The lines **add** to the slide's own sentences (which come first, or where the line
`'@mirror'` stands): why, how to read the picture, what to compare, the bridge to the next idea. Lecturer: "writing what can be seen is fine, but add some supplement".
- A line is one short plain sentence, at most 64 characters (`MAX_CHARS` in `src/video/timeline.ts`; longer throws). One or two lines per stage, not every stage. No em dash, no rhetoric.
- **A question slide gets no answer**: its notes end with a prompt ("Take a moment to guess.").
- Length: about 190 lines (60 sentences from the slides, about 120 written lines) is 26 minutes with the reading pauses. Typing time dominates (about 8,000 keystrokes). Trim lines, not typing speed: past
  about 12 characters a second the typing stops looking like typing.
- English, like the slides. The text in the repo is a draft by the agent; the lecturer edits it.

## Typing (`src/video/typing.ts`, pure, deterministic)

Keys come in uneven bursts (interval about 58 ms times a random factor 0.62 to 1.5, two keys in quick succession 12% of the time), slower after a space
(+18 to 73 ms) and after punctuation (+110 to 250 ms), with an occasional hesitation. A wrong neighbouring key (QWERTY adjacency) is typed with
probability 1.2% per eligible letter, at most 2 per line, only in lines of 14+ characters; the typist carries on for 0 to 2 letters, notices after
190 to 420 ms, backspaces quickly, and types the letter again. The seed is the text and its place, so a render is repeatable.

## Timeline (`src/video/timeline.ts`, no React so that node can import it)

`SKIP` the dividers; `stageLines` puts a stage's slide sentences and written lines in order; `LEAD` 40 frames after a stage's animation before the first key (time to look at the slide first); `POP` 9 frames from the line starting to the first key; `GAP` 44 between lines; `READ`
72 after the last key (time to finish reading and to look at the slide); `HOLD` 48 after a stage without narration. The lecturer asked for room to read and to look at the slide: raise these, not the typing speed. `buildTimeline(marks, narration)` returns slides, stages (`anim` frames of play,
`hold` frames frozen), lines (`Bubble` in the code) with the global frame of each keystroke, and all key times (used for the sound).
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

## The figure and the terminal lines (`src/video/Loafer.tsx`, `Narrator.tsx`)

The lecturer asked for something simpler than the first cat: a person lying on the stomach, chin on one hand, feet in the air (thick black lines, flat colours; the
reference image was only the "touch", the drawing is our own), and **plain terminal lines instead of message boxes**: white page, no frame, a prompt (`$ `, blue) before
each line, monospace type (JetBrains Mono), a block cursor on the line being typed. A new line starts at the bottom; the older lines move up one line and fade (three
lines at most, `FADE` in `Narrator.tsx`). The figure's pose is a pure function of the frame: a nod and tilt on each key, the feet kick alternately (faster while typing), a blink
every 112 frames, the ribbon sways, a breathing movement. Position: figure at x 150 to 400, text from x 440, all below y = 920: **two lines** of 46 px with **72 px of margin under the last** (the lecturer found text near the bottom edge hard to see; three lines would need a taller band).
(The first version, a cat with speech bubbles, is in the git history: commits before this change.)

### Character art from an image model (optional)

`python3 scripts/gen_character.py [--only 1,3] [--model google/gemini-3.1-flash-image]` makes candidates for the figure with a Gemini image model through OpenRouter (key in `$OPENROUTER_API_KEY`, never
written to a file; a few cents per image; `out/character/cand-N.png` and the prompt in `cand-N.txt`). The prompt describes the touch in words (thick uniform black outlines, flat pastel fills,
no shading, big round head with straight bangs, dot eyes, a small smile, lying on the stomach with the head on one hand and the feet in the air, white background); **a reference image is not uploaded**,
so the result is an original character. Models that can output images are listed by `GET https://openrouter.ai/api/v1/models` (`output_modalities` contains `image`); the request is a chat completion with
`modalities: ["image", "text"]` and `image_config.aspect_ratio`, and the image comes back as a base64 data URL in `choices[0].message.images[0]`. To use a candidate in the video, cut the white background
away (or draw it on white) and replace `Loafer.tsx` with an `<Img>` plus small CSS movements (nod, breathing), keeping the pose a pure function of the frame.

## Checks before handing it over

`npx remotion ffprobe out/m05-narrated.mp4` (duration, 1920x1080 30 fps, AAC audio); stills of a few narrated frames (figure, terminal lines, nothing above y = 920);
onsets against key times; `git status` shows no change under `src/slides/`.
