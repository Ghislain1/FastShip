import { useInView } from "../../../hooks/use-in-view";

const stats = [
  { value: "10K+", label: "Active sellers" },
  { value: "2M+", label: "Shipments delivered" },
  { value: "99.5%", label: "On-time delivery" },
  { value: "50+", label: "Carriers supported" },
];

export function StatsSection() {
  const { ref, isInView } = useInView();

  return (
    <section ref={ref} className="relative py-28 sm:py-32">
      <div className="neon-line absolute left-0 right-0 top-0" />
      <div className="container mx-auto max-w-6xl px-4">
        <div className="grid grid-cols-2 gap-12 md:grid-cols-4">
          {stats.map((stat, i) => (
            <div
              key={i}
              data-delay={i}
              className={`reveal-on-scroll text-center transition-all duration-500 ${isInView ? "" : ""
                }`}
            >
              <p className="text-5xl font-bold tracking-tight text-primary sm:text-6xl glow-text">
                {stat.value}
              </p>
              <p className="mt-3 text-sm font-medium uppercase tracking-wider text-muted-foreground">
                {stat.label}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}