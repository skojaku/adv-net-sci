import React, {createContext, useContext, useEffect, useState} from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';

/**
 * Two clocks.
 *  1. useCurrentFrame(): the "stage timeline". In the app it is driven by clicks.
 *  2. useIdle(): a free-running wall clock (seconds) for motion that should keep
 *     going while the stage timeline is paused (rotating circles and so on).
 * Outside the app (Remotion Studio or render) there is no provider, so useIdle()
 * falls back to frame / fps and everything stays deterministic.
 */
export const IdleContext = createContext<number | null>(null);

export const useIdle = (): number => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const wall = useContext(IdleContext);
  return wall ?? frame / fps;
};

export const IdleProvider: React.FC<{children: React.ReactNode}> = ({children}) => {
  const [t, setT] = useState(0);
  useEffect(() => {
    let raf = 0;
    const t0 = performance.now();
    const tick = (now: number) => {
      setT((now - t0) / 1000);
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, []);
  return <IdleContext.Provider value={t}>{children}</IdleContext.Provider>;
};
