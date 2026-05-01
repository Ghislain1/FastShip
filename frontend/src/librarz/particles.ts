export interface Particle {
  id: number;
  size: number;
  left: number;
  top: number;
  delay: number;
  duration: number;
}

function generateParticles(count: number): Particle[] {
  return Array.from({ length: count }, (_, i) => ({
    id: i,
    size: Math.random() * 4 + 2,
    left: Math.random() * 100,
    top: Math.random() * 100,
    delay: Math.random() * 6,
    duration: Math.random() * 8 + 6,
  }));
}

export function generateFloatingParticles(): Particle[] {
  return generateParticles(120);
}