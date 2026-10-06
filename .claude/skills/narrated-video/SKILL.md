---
name: narrated-video
description: Make or change the narrated video of a Remotion deck, for any module: a small figure lying down types short English notes as terminal lines with mechanical-keyboard sound, the slides' own sentences moved into the chat, a few reactions (worry, shrug). Covers porting the video code to another deck, writing the narration, the figure and its Gemini-drawn frames, the typing sound, rendering and checking. Use when the lecturer asks for narration, a video of a deck, the typing sound or the character.
---

# Narrated video

The substance is in plain markdown so that any agent can follow it: read `slides/NARRATED_VIDEO_GUIDE.md` and do what it says. Deck authoring and the Remotion pitfalls are in `slides/REMOTION_DECK_GUIDE.md`.

- **A video of another deck (another module)**: the guide's section "Making the video of another deck". The video code is shared; one video is four files in `src/video/` (`video.config.json`, `narration.ts`, `moods.ts`, `prose.json`).
  From `slides/m05/remotion`: `node scripts/port_video.mjs <new project> --id=M06 --skip=<slides to leave out>` copies the rest, writes the four stubs and **lists what the target deck lacks**; then `npm run video:prose`, `npm run video:skeleton -- --out=src/video/narration.ts`, write the lines and `moods.ts`.
  The target must be a Remotion click-through deck made as the deck guide says.
- **Change the Module 05 video** (a line, the layout, the font, the figure's frames, a reaction, the pauses, the sound): the matching section of the guide; the knobs are listed in "Making the video of another deck".
- **Always**: decide on stills (`node scripts/render_video.mjs --still=...`), not on a full render; render in the background; check the mp4 itself (ffprobe, frames, the sound of a stretch); say what an agent cannot judge (it cannot hear the sound). Run `npm run video:audio` again after any change to narration, marks, prose or pauses.
- The slides are never edited for the video. Commit only the deck's project directory (`slides/m05/remotion` for Module 05); `git status` may list unrelated changes.

Commands (in the deck's project): `npm run video:prose | video:skeleton | video:lengths | video:audio | video | video:sampler`. Code: `src/video/` and `scripts/` (`make_typing_audio.mjs`, `render_video.mjs`, `collect_prose.mjs`, `narration_skeleton.mjs`, `port_video.mjs`, `extract_mechvibes.mjs`, `gen_character.py`, `prep_character.py`).
