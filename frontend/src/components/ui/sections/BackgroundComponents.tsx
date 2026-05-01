import { useMemo } from "react";
import { generateFloatingParticles } from "../../../lib/particles";

export function FloatingParticles() {
  const particles = useMemo(() => generateFloatingParticles(), []);

  return (
    <div className="pointer-events-none fixed inset-0 z-0">
      {particles.map((p) => (
        <div
          key={p.id}
          className="absolute rounded-full bg-primary/30"
          style={{
            width: p.size,
            height: p.size,
            left: `${p.left}%`,
            top: `${p.top}%`,
            animation: `float ${p.duration}s ease-in-out ${p.delay}s infinite`,
          }}
        />
      ))}
    </div>
  );
}

export function GridOverlay() {
  return <div className="pointer-events-none fixed inset-0 z-0 opacity-30 grid-bg" />;
}