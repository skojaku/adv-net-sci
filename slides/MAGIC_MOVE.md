# Magic move in Marp

How to make an object slide, resize or recolour between two slides (Keynote's Magic Move).
Worked example: `slides/m06/morph-demo/build.py` (an 11-node network, five slides; the
lecturer checked it by eye and called it good). Nothing here is needed for an ordinary deck;
read it when a slide pair should show *the same thing changing* rather than a new picture.

## What it is

Marp CLI 4.x HTML output runs `document.startViewTransition` on every slide change. The
browser pairs elements that carry the **same `view-transition-name` on both slides** and
animates position, size and colour between the two. Elements with no partner (or an
unnamed element) just cross-fade with the rest of the slide.

## Rules that decided whether it worked

1. **Draw the objects as HTML boxes, never SVG shapes.** Chrome captures a box for an HTML
   `div`, but not for an SVG `<circle>`, `<line>` or `<text>`; an SVG figure only cross-fades,
   and no error says why. A node is a round `div` (`border-radius:50%`, the letter inside);
   an edge is a thin `div` of the edge's length, `transform-origin:0 50%`, `rotate(angle)`.
   Absolute-position all of them in one `position:relative` container.
2. **One name per object, identical on both slides** (`n_E`, `e_EF`), set inline:
   `style="view-transition-name:n_E"`. A name used twice on one slide breaks the whole
   transition. An object missing on the next slide fades out (a closed road); a new one fades in.
3. **Raw HTML needs `marp --html`.** Emit the figure as one unbroken HTML block in the
   markdown (a blank line inside it ends the block).
4. **Change only what the point is about.** Move, resize or recolour a few objects per step;
   keep the layout fixed otherwise, so the cost of each slide is what is new on it. Size on a shared
   scale across the slides being compared, or the shrinking the slide is about is hidden.

## Timing, per slide

- Transition per slide: `<!-- _transition: fade 1.6s -->` (name, then duration) for one slide,
  `<!-- transition: fade -->` for that slide and all later ones. The YAML-object form
  (`name:` / `duration:`) is accepted but **drops the duration**.
- Duration of the named objects' motion, honouring the slide's own value (Marp exposes it as
  `--marp-bespoke-transition-animation-duration`, `-1s` when unset):

      ::view-transition-group(*) { animation-duration: max(.8s, var(--marp-bespoke-transition-animation-duration)); animation-timing-function: ease-in-out; }

- The transition a slide uses is the one declared on the slide being *entered*.

## Limits

- **Chrome / Edge only**; Firefox is behind. PDF, PPTX and PNG exports show still slides and
  keep only the final state of each. A deck that goes through the render gate and exports
  should keep its morph slides in a **separate HTML-only build**, as the demo does.
- A slide with `prefers-reduced-motion` set shows no morph (Marp turns the names off).
- Diagonal edges stretch rather than pivot while the ends move; fine for short moves. For
  exact edges that follow nodes through long moves, use a stage (`DECK_BUILD_GUIDE.md`,
  "Density from motion") instead.
- Text inside a resizing box scales as a picture during the move; keep labels short.

## Checking it

A **hidden browser tab skips view transitions entirely** (`document.hidden` is true), and a
screenshot tool shows only the finished state, so an automated browser cannot see the motion.
Serve the folder (`python3 -m http.server`, since `file://` is blocked in some setups), open
it in a visible Chrome window and step through with the right arrow. Static checks (layout,
clipping, that each slide's end state is right) can be done by screenshot.
