import { useInView } from "../../../hooks/use-in-view";

interface Step {
  number: string;
  title: string;
  description: string;
}

const steps: Step[] = [
  {
    number: "01",
    title: "List your products",
    description: "Create product listings with prices, descriptions, and shipping options in minutes.",
  },
  {
    number: "02",
    title: "Receive orders",
    description: "Customers browse and purchase. Get instant notifications on new orders.",
  },
  {
    number: "03",
    title: "Ship with confidence",
    description: "Generate labels, choose carriers, and track every shipment to delivery.",
  },
];

export function HowItWorksSection() {
  const { ref, isInView } = useInView();

  return (
    <section id="how-it-works" ref={ref} className="relative py-28 sm:py-32">
      <div className="neon-line absolute left-0 right-0 top-0" />
      <div className="pointer-events-none absolute inset-0 -z-10 bg-gradient-to-b from-primary/5 via-transparent to-transparent" />
      <div className="container mx-auto max-w-6xl px-4">
        <div className="mx-auto max-w-2xl text-center">
          <h2
            className={`text-3xl font-bold tracking-tight text-foreground sm:text-5xl transition-all duration-700 ${isInView ? "animate-reveal" : "opacity-0"
              }`}
          >
            How it works
          </h2>
          <p
            className={`mt-4 text-lg text-muted-foreground transition-all duration-700 delay-150 ${isInView ? "animate-reveal" : "opacity-0"
              }`}
          >
            Three simple steps to start shipping.
          </p>
        </div>

        <div className="mt-20 grid gap-8 md:grid-cols-3">
          {steps.map((step, i) => (
            <div
              key={i}
              data-delay={i}
              className={`reveal-on-scroll group relative text-center transition-all duration-500 ${isInView ? "" : ""
                }`}
            >
              <div className="relative mx-auto mb-8 flex h-20 w-20 items-center justify-center">
                <div className="absolute inset-0 rounded-full border border-primary/20 animate-pulse-glow" />
                <span className="relative text-2xl font-bold text-primary glow-text">
                  {step.number}
                </span>
              </div>
              <h3 className="text-xl font-semibold text-foreground">{step.title}</h3>
              <p className="mt-3 text-muted-foreground">{step.description}</p>
              {i < steps.length - 1 && (
                <div className="absolute -right-4 top-10 hidden md:block">
                  <svg className="h-8 w-16 text-primary/30" viewBox="0 0 64 32" fill="none" stroke="currentColor" strokeWidth={1.5}>
                    <path d="M0 16h56" strokeDasharray="4 4" />
                    <path d="m52 12 4 4-4 4" />
                  </svg>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}