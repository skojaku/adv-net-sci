# Narrated video guide

How a Remotion click-through deck becomes a video in which a small figure lying down types short notes as terminal lines, with typing sound.
Module 05 (`slides/m05/remotion`, `out/m05-narrated.mp4`) is the worked example; **the video code is shared**, and any other deck made as
`REMOTION_DECK_GUIDE.md` says can have a video of its own: see "Making the video of another deck". The slides are **not touched**: everything is in
`src/video/` and a few scripts, and the video has its own Remotion entry point (`src/video/entry.ts`). Shell commands and file paths only.

## Make it

```sh
cd slides/m05/remotion
node scripts/extract_mechvibes.mjs --pack=cherrymx-red-abs --release=0.5   # typing samples, once (sounds/, not committed)
npm run video:prose                  # the slides' own sentences -> src/video/prose.json (committed); again whenever a slide's sentences change
npm run video:skeleton               # a skeleton of src/video/narration.ts: every slide and stage, the slide's sentences as comments; `-- --out=src/video/narration.ts` writes it, never over an existing file
npm run video:lengths                # how long the typed lines are: the font must let the longest one fit (see "The figure and the terminal lines")
npm run video:audio                  # out/video-public/typing.wav, from the same keystrokes the video shows; also lists the frames of every reaction
npm run video                        # out/<`out` of src/video/video.config.json>, here m05-narrated.mp4 (about 12 minutes of rendering for 26 minutes of video)
npm run video:sampler                # a listening test of all ten keyboard packs: then render_video.mjs --id=<id>-sampler --out=out/sound-packs.mp4
node scripts/render_video.mjs --frames=1890-2145 --out=out/clip.mp4        # a part
node scripts/render_video.mjs --still=1900,2000 --dir=out/video-stills     # single frames
```

Run `npm run video:audio` again after **any** change to the narration, to a slide's `marks`, to `src/video/prose.json` or to the sound: the timeline
(and so every key time) changes, and the audio must follow.

## Starting a new topic (no deck yet)

The video needs a Remotion deck. For a new topic the deck is most of the work (the modularity video: 21 slides, written first, then 149 lines). Check first whether a deck exists: `slides/*/remotion*/src/slides/index.ts`.

1. **The story as a table**: from the lecturer's brief, one row per slide and stage, what appears on screen and what picture is left at the end (`DECK_SPEC.md` of the new project; the modularity one is the model). Pitch it as pictures, not algorithm names. Show it and ask the questions that change what is drawn (the lecturer invites them); get the answers before drawing.
2. **One command**, from `slides/m05/remotion`: `node scripts/new_deck.mjs ../remotion-<topic> --name=<topic> --ids=slide-one,slide-two,... --video-id=<ID> [--title=... --subtitle=... --kicker=...]`. It copies the shared deck parts, writes a stub slide per id, `src/slides/index.ts` and `TOTAL`, and ports the video code (`port_video.mjs`). It refuses a directory that is not empty. Then `npm install` there.
3. **Numbers before pictures**: `scripts/make_data.py` writes `src/data/data.ts` (every number and random choice), `scripts/verify_numbers.py` recomputes them with an independent library (a number that no script computed is a bug). Check a claim from a paper at its source (an arXiv abstract) before it goes on a slide. A **constructed** example is never captioned as an algorithm's real run: say in the spec that it is constructed.
4. **Slides**: agents can write slide ranges in parallel once the shared files are frozen (data, shared libs, index, stubs); each edits only its own slides and helper files with its own prefix (`a_`, `b_`, `c_`), never the shared ones. `node scripts/review.mjs --only=1-8` renders a range. Look at every still yourself (contact sheets of 9 to 12 stills per image save effort), then `check_bottom.py`.
5. **Then the video**, steps 2 to 7 of the next section. Commit after each round (the project directory only).

What the second video taught:
- **A line costs about 7.5 seconds**: plan the length by counting lines before writing (149 lines = 18.7 minutes); cut lines, not typing speed.
- The lecturer reads a long derivation as wordy: **one straight line per step**; a slide whose information is scattered is cut and replaced by one sentence; no closing recap slide; an example whose values differ clearly (every node with the same degree makes the matrix of expected edges teach nothing); an expected count is not called a probability.
- Cutting or inserting a slide shifts the slide files, `index.ts`, `TOTAL`, the narration keys, `moods.ts` and the spec: do it with a script, then `npm run video:prose` and `npm run video:audio`.
- The introduction's layout and the order of its move are per-video knobs (`INTRO` in `Narrator.tsx`, `introMove` in `timeline.ts`); in the modularity video the typed lines are above the narrator, who moves up after them. `port_video.mjs --update` would overwrite a changed copy.
- Render the full video only after the lecturer has seen the stills and says so (about 11 minutes in the background); for a changed introduction render a clip: `--frames=0-1700 --out=out/intro-clip.mp4`.

## Making the video of another deck

**What is specific to one video** is four files in `src/video/`: `video.config.json` (`id` of the compositions, `out` the file name, `skip` the slides left out, normally the section
dividers, `intro` the title of the introduction), `narration.ts` (the written lines), `moods.ts` (where the figure reacts) and `prose.json` (generated by `npm run video:prose`). **Everything else is shared**: the timeline, the typing
model, `Narrator.tsx` (the band and the terminal lines), `Character.tsx` and the frames in `src/video/character/`, the sound, the scripts. **The deck must provide**: `src/slides/index.ts` listing
`{n: 1, id: 'name', marks, Component}`, every slide file exporting `marks`, `ProseContext` in `src/components/Text.tsx`, the colour table `C` in `src/theme.ts`, a free band below y = 920, `@remotion/google-fonts`
and `@remotion/cli` in `package.json`. A deck made by copying the Module 05 project has all of it; a deck that is not a Remotion deck cannot use this pipeline (build it first: `REMOTION_DECK_GUIDE.md`).

1. From the Module 05 project: `node scripts/port_video.mjs <the new project> --id=M06 --skip=1,8` (the section dividers to leave out; `--out=` the file name). It copies the shared code, the character frames and the typing
   samples, writes the four stubs, completes `package.json` (scripts) and `.gitignore`, and **lists what the target lacks** (do that first). Nothing is overwritten; `--update` refreshes the shared code later, never the four files.
2. In the new project: `npm install`, then `npm run video:prose` (the slides' own sentences).
3. `npm run video:skeleton -- --out=src/video/narration.ts` and write the lines (the rules in the next section), **and the introduction**: `narration[0][0]` (a greeting and what the module covers, about eight lines) with `intro` in `video.config.json` (`kicker`, `title`, `subtitle`; `port_video.mjs` takes `--kicker --title --subtitle`). A question slide gets no answer. Draft it, run step 5, and let the lecturer edit.
4. `moods.ts`: five to ten reactions in 25 minutes (`worry` where something goes wrong or misleads, `shrug` where there is no single answer); the stage after which each one comes.
5. `npm run video:lengths` (no line may be wider than the lines' width), `npm run video:audio` (the key times, the reaction frames and the frames of the introduction's move), then **stills** of the frames that matter: `node scripts/render_video.mjs --still=<frames> --dir=out/video-stills`.
6. Show the lecturer the stills (layout, figure, a long line, one reaction), correct, and only then `npm run video` in the background.
7. Checks below. Commit the project directory only (never the unrelated files that `git status` may list).

**Second worked example: `slides/m05/remotion-modularity`** (modularity, Louvain, Leiden; id `M05MOD`, 23 slides, 186 lines, 8,079 keystrokes = 23.1 minutes, no section dividers so `skip` is empty). The deck did not exist, so most of the work was the deck: `DECK_SPEC.md` (the table of slides, shown to the lecturer first), `scripts/make_data.py` (every number and random choice, written to `src/data/data.ts`), `scripts/verify_numbers.py` (recomputes them with networkx), then the slides. Rule of thumb from both videos: **a line costs about 7.5 seconds**, so count the lines before writing and cut lines, not typing speed. The shared deck parts were copied from the Module 05 project (`Frame`, `Text`, `Tex`, `FormulaStack`, `Network`, `anim`, `look`, `theme`), not re-written.

The character is reused as it is (the lecturer chose it). A new character or new frames: "Character art from an image model". New typing sound: `extract_mechvibes.mjs` (the port copies the extracted samples).
**Knobs** the lecturer has already turned: `BAND`, `TOP`, `BX`, `WIDTH`, `FONT`, `LINE`, `FIG_H` and the figure's `left` in `Narrator.tsx` (the introduction's layout is the `INTRO` object there, its title is `IntroTitle.tsx`); `TYPE_SEQ`, `FADE`, `TYPING_AGE` in `Character.tsx`; `LEAD`, `GAP`, `READ`, `HOLD` (the pauses), `INTRO_LEAD`, `INTRO_HOLD`, `TRANS` (the introduction), `introMove` (the order of the move) and `REACT_*`
in `timeline.ts`. After changing a pause, a mark or a line, run `npm run video:audio` again.

## What the video is

One continuous talk, not chapters: the three section dividers (S1, S8, S22) are left out (`skip` in `src/video/video.config.json`), the chat is never cleared at a slide
change, and the bridge from one part to the next is in the first lines of the next slide (S9, S23). Each slide plays stage by stage as in the click-through deck.
After a stage's animation **has finished** the picture is held while the narrator types that stage's lines, then the next stage starts. **The narrator is in a band at the TOP** (228 px, `BAND` in `src/video/Narrator.tsx`; the figure starts 52 px below the top edge): the figure at the left (x 120 to 432), the terminal lines to its right (from x 520). **The slide is shown under it**: `NarratedDeck.tsx` scales the slide's first 920 px (its own bottom 160 px, kept empty for subtitles, are cut off) to the room that is left (scale 0.926), so the slide's page number is not in the video. (Lecturer: character and text on top, slide below, easier to see.)

### The introduction (`narration[0][0]`, `intro` in `video.config.json`)

The lecturer: the opening has the **title large at the top and the narrator in the middle of the screen**, who says hello and explains what the module covers; when the main part starts, **the narrator moves to the top, smoothly**.
So the video opens with the title alone (`IntroTitle.tsx`: kicker, title, subtitle), the figure centred under it (440 px wide) and the chat at 40 px with up to five lines, the older ones fading; the lines are typed like any others (same keystrokes, same sound).
After the last line and `INTRO_HOLD` frames the layout moves into the band over `TRANS` frames. The parts move **one after the other so that nothing overlaps** (`introMove` in `timeline.ts`): the title leaves first (up and out), then the figure moves, then the lines
(their font shrinks from 40 to 34 px and the old ones fade), and last the first slide's opening picture fades in; its animation starts when the move is done. The chat is not cleared, as everywhere else. Without lines in `narration[0][0]` there is no introduction and the video opens on the first slide.
The introduction's lines are slide 0 in `narration.ts`; the 64-character limit applies. A draft for Module 05 is there: greeting, what a community is, the three parts, "I will type short notes here while each slide plays", "Let's start with modularity."

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
- Start from `npm run video:skeleton`: every slide and stage with the slide's own sentences as comments, so you see what is already typed.
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

`SKIP` (= `skip` of `video.config.json`) the slides left out; `stageLines` puts a stage's slide sentences and written lines in order; `LEAD` 40 frames after a stage's animation before the first key (time to look at the slide first); `POP` 9 frames from the line starting to the first key; `GAP` 44 between lines; `READ`
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

## The figure and the terminal lines (`src/video/Character.tsx`, `Narrator.tsx`)

The lecturer asked for **plain terminal lines instead of message boxes**: white page, no frame, a prompt (`$ `, blue) before each line, monospace type (JetBrains Mono), a block cursor on
the line being typed. A new line starts at the bottom; the older lines move up one line and fade (`FADE` in `Narrator.tsx`). Position: figure at x 120 to 432 (top 52, 166 px high), text from x 520
(top 85): **two lines** of 50 px, 34 px JetBrains Mono (`FONT`, `LINE`, `WIDTH` in `Narrator.tsx`), in the band at the top of the video. A line never wraps (`white-space: pre`): the longest line, 63 characters plus the prompt and the cursor, is 1360 px of the 1390 px of `WIDTH` (a wrapped line grows upward over the line above); `node scripts/line_lengths.mjs` prints the line lengths, so check it before raising the font again. (Lecturer: more margin above the figure; the narration a little to the right.)

The figure is a boy lying flat on his stomach, seen from the side and facing right toward the text, knees bent and feet in the air (chosen P2), drawn by a Gemini image model (below) in the
touch of the lecturer's reference images (thick black outlines, soft off-white fills, a hint of pale lavender shading). (The first design, D1, had the face to the viewer and the body lying
sideways: the lecturer found the body too twisted; it is in `out/character/`.) `Character.tsx` swaps five frames (`src/video/character/*.png`, committed; the head and the keyboard are at the same pixels in all of them):
`rest` (hands on the keys), `typeA` / `typeC` / `typeB` / `typeC` (in turn, one step every two keystrokes while keys are being pressed: A lifts the far hand, C the **near** hand, B the far hand higher, so both hands visibly strike; with only A and B the near hand never moved and it did not look like typing), `worry` (a troubled face with a sweat drop, **still at the keys**) and
`shrug` (eyes closed, palms up). The frame is a pure function of the frame number; groups blend over 6 frames, A to B is a hard cut; the whole figure breathes and dips 1.5 px on each key.

**Reactions** (`src/video/moods.ts`): after the last line of a named stage is typed he shows the mood (worry: the face changes; shrug: the hands leave the keys) for about 3 s (until 6 frames before the next line,
`reactionsOf` in `timeline.ts`). A rule is `{slide, stage (0-based), mood}`; a stage without lines throws. Keep them few: now 5 worry (the random networks all score high, the reordered table,
no diagonal, Rand fooled, K = 8) and 3 shrug (a high Q proves nothing, NMI and ARI disagree, one group at the end). `npm run video:audio` prints the frames of every reaction, for looking.

### Character art from an image model (`scripts/gen_character.py`, `scripts/prep_character.py`)

`python3 scripts/gen_character.py --set <name> [--ref a.png,b.png] [--only 1,3]` calls a Gemini image model through OpenRouter (`google/gemini-3.1-flash-image`; key in `$OPENROUTER_API_KEY`,
never written to a file; a few cents per image; `out/character/<set>-N.png` and the prompt in `<set>-N.txt`). The request is a chat completion with `modalities: ["image", "text"]` and
`image_config.aspect_ratio`; reference images go in as `image_url` parts (the first is the character to keep, the others only the touch); the image comes back as a base64 data URL in
`choices[0].message.images[0]`. The sets are the steps of the design: `words` (touch described in words), `ref`, `white`, `boy`, `glasses`, `lines`, `b4` (restyle), `gaze`, `touch`, `both`
(both hands on the keyboard: D1 = `both-1`), `pose` (typing A/B, troubled, happy, shrug, from D1; `--ref out/character/base.png`, the expression references in `out/character/expr/`), `prone` (four side-view prone candidates, `--ref out/character/base.png`; P2 = `prone-2`, copied to `base2.png`), `pframe` (the frames of the chosen P2: typing A/B, two troubled faces, two shrugs; `--ref out/character/base2.png`; used: `pframe-1`, `-2`, `-3`, `-5`, and `-21`). The model kept lifting the far hand however the near hand was named in words (UPPER/LOWER hand, an annotated picture with a red arrow, a picture of the opposite state: all failed); what worked for the near hand (`pframe-21`, typing C) was a **rough collage of my own**: the near hand cut out (polygon) and rotated 16 degrees about the wrist in `out/character/collage-a.png`, then `--ref out/character/collage-a.png` with a prompt asking the model to clean it up (keep the lifted hand where it is, join the wrist, redraw the keys under it): 1 of 3 samples kept the hand lifted.
Lessons: ask for **the same camera and the same place of the head** (then the frames swap without a jump: the head outline came out pixel-identical), and say explicitly that **the keyboard stays on
the floor at the same place in every frame** (otherwise it disappears or moves).
`python3 scripts/prep_character.py` makes the video frames (its `FRAMES` table says which picture is which): the white page is flood-filled from the border (the outline is closed) and made transparent, each frame is shifted so that the head matches
the rest frame (it found 0 px of shift for all five), all are cropped to one box and saved at 640 px width, with `size.json` (the aspect of the frames, read by `Character.tsx`). It needs numpy and Pillow.

## Order of work that succeeded (Module 05)

1. Decide the look on **stills** and short clips, never on a full render (about 12 minutes): `render_video.mjs --still=...` (a few frames, 0.75 scale is enough) and `--frames=a-b --out=out/clip.mp4`.
2. The character: images only first (a gallery page), one change per round, the lecturer picks; then the frames. Layout changes (a band at the top, a margin, the narration to the right, a bigger font) were each asked for after seeing a still.
3. After every change: `npx tsc --noEmit`, then stills at the frames that matter: a typing burst (frames 3 apart, cropped and enlarged: the hands are small), the longest line (`video:lengths` prints its frame), each reaction (`video:audio` prints them).
4. Commit, then render in the background (`npm run video > out/render.log 2>&1 &`) and wait with a loop on "wrote" in the log. **Never `pkill -f` a pattern that also appears in your own command line**: it kills the waiting shell too (use `pgrep -f "[r]ender_video.mjs"`); to stop a render, kill the node process by its pid, then the `chrome-headless-shell`.
5. Verify the **file**, not only the stills (below), report what could not be verified (the sound), then take the lecturer's next remarks.
6. A script that writes into the source tree must refuse to overwrite an existing file, and be tested on a copy: `narration_skeleton.mjs --out=` once overwrote the real narration (restored from git).

## Checks before handing it over

`npx remotion ffprobe out/<out>` (duration, 1920x1080, 30 fps, AAC audio); a few frames **taken out of the mp4** (`npx remotion ffmpeg -ss <s> -i out/<out> -frames:v 1 f.png`): a worry and a shrug frame, a typing frame, the longest line,
no overlap of lines; the sound of a typing stretch (`ffmpeg -ss 225 -t 12 -i out/<out> -vn -ac 1 -ar 44100 a.wav`, then peak and rms with Python: Remotion's ffmpeg has no `volumedetect`); onsets against key times;
`git status` shows no change under `src/slides/`. An agent cannot hear: say so, and name what to listen to (the loudness, the feel of the typing, the timing of the frame changes).
