import React, {useCallback, useEffect, useRef, useState} from 'react';
import {Player, PlayerRef} from '@remotion/player';
import {slides} from './slides';
import {FPS} from './lib/anim';
import {IdleProvider} from './lib/idle';

type Pos = {slide: number; stage: number};

/** Going back plays the animation in reverse at this speed (1 = normal). */
const BACK_SPEED = 2;

const LABEL: React.CSSProperties = {
  position: 'fixed',
  bottom: 10,
  font: '12px ui-monospace, Menlo, monospace',
  color: '#fff',
  background: 'rgba(0,0,0,0.6)',
  padding: '3px 10px',
  borderRadius: 6,
  pointerEvents: 'none',
  transition: 'opacity 400ms ease',
};

export const App: React.FC = () => {
  const [pos, setPos] = useState<Pos>({slide: 0, stage: 0});
  const posRef = useRef<Pos>(pos);
  const playerRef = useRef<PlayerRef>(null);
  // the two small labels at the bottom show on load and whenever the mouse or a key moves, then fade after a few seconds
  const [ui, setUi] = useState(true);

  // The frame currently shown (fractional) and the frame we are heading to.
  const frameRef = useRef(0);
  const targetRef = useRef(slides[0].marks[0]);
  const shownRef = useRef(0);
  const initialRef = useRef(0);

  const move = useCallback((dir: 1 | -1) => {
    const p = posRef.current;
    const cur = slides[p.slide];
    let next: Pos | null = null;

    if (dir === 1) {
      if (p.stage < cur.marks.length - 1) next = {slide: p.slide, stage: p.stage + 1};
      else if (p.slide < slides.length - 1) next = {slide: p.slide + 1, stage: 0};
    } else if (p.stage > 0) {
      next = {slide: p.slide, stage: p.stage - 1};
    } else if (p.slide > 0) {
      next = {slide: p.slide - 1, stage: slides[p.slide - 1].marks.length - 1};
    }
    if (!next) return;

    const ns = slides[next.slide];
    if (next.slide !== p.slide) {
      // New slide: forward starts from frame 0 and plays stage 0. Backward lands on the last stage.
      const start = dir === 1 ? 0 : ns.marks[ns.marks.length - 1];
      frameRef.current = start;
      shownRef.current = start;
      initialRef.current = start;
    }
    targetRef.current = ns.marks[next.stage];
    posRef.current = next;
    setPos(next);
  }, []);

  // Drives the Player by seeking, so we can stop at any frame and also run backwards.
  useEffect(() => {
    let raf = 0;
    let last = performance.now();
    const tick = (now: number) => {
      const dt = Math.min(0.1, (now - last) / 1000);
      last = now;
      const cur = frameRef.current;
      const target = targetRef.current;
      if (cur !== target) {
        const d = FPS * dt * (target > cur ? 1 : BACK_SPEED);
        const nxt = target > cur ? Math.min(target, cur + d) : Math.max(target, cur - d);
        frameRef.current = nxt;
        const shown = Math.round(nxt);
        if (shown !== shownRef.current) {
          shownRef.current = shown;
          playerRef.current?.seekTo(shown);
        }
      }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, []);

  useEffect(() => {
    let timer = 0;
    const wake = () => {
      setUi(true);
      window.clearTimeout(timer);
      timer = window.setTimeout(() => setUi(false), 4000);
    };
    wake();
    window.addEventListener('mousemove', wake);
    window.addEventListener('keydown', wake);
    window.addEventListener('click', wake);
    return () => {
      window.clearTimeout(timer);
      window.removeEventListener('mousemove', wake);
      window.removeEventListener('keydown', wake);
      window.removeEventListener('click', wake);
    };
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter'].includes(e.key)) {
        e.preventDefault();
        move(1);
      } else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].includes(e.key)) {
        e.preventDefault();
        move(-1);
      } else if (e.key === 'f') {
        if (document.fullscreenElement) void document.exitFullscreen();
        else void document.documentElement.requestFullscreen();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [move]);

  const slide = slides[pos.slide];
  const lastMark = slide.marks[slide.marks.length - 1];
  const progress = (pos.slide + (pos.stage + 1) / slide.marks.length) / slides.length;

  return (
    <>
      <div
        onClick={() => move(1)}
        style={{
          width: 'min(100vw, calc(100vh * 16 / 9))',
          aspectRatio: '16 / 9',
          position: 'relative',
          cursor: 'pointer',
          userSelect: 'none',
        }}
      >
        <IdleProvider>
          <Player
            key={pos.slide}
            ref={playerRef}
            component={slide.Component}
            durationInFrames={lastMark + 1}
            fps={FPS}
            compositionWidth={1920}
            compositionHeight={1080}
            initialFrame={initialRef.current}
            controls={false}
            clickToPlay={false}
            doubleClickToFullscreen={false}
            spaceKeyToPlayOrPause={false}
            allowFullscreen={false}
            style={{width: '100%', height: '100%'}}
          />
        </IdleProvider>
      </div>

      <div
        style={{
          position: 'fixed',
          left: 0,
          bottom: 0,
          height: 4,
          width: `${progress * 100}%`,
          background: '#c8402a',
          transition: 'width 300ms ease',
        }}
      />
      <div style={{...LABEL, right: 12, opacity: ui ? 1 : 0}}>
        slide {pos.slide + 1}/{slides.length} · step {pos.stage + 1}/{slide.marks.length}
      </div>
      <div style={{...LABEL, left: 12, opacity: ui ? 1 : 0}}>click or → : next · ← : back · f : full screen</div>
    </>
  );
};
