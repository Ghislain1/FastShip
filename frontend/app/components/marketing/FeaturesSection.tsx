import { useInView } from "../../../hooks/use-in-view";

interface Feature {
  icon: string;
  title: string;
  description: string;
  color: string;
}

const features: Feature[] = [
  {
    icon: "shield",
    title: "Secure payments",
    description: "End-to-end encrypted transactions with multiple payment methods.",
    color: "from-primary to-primary/60",
  },
  {
    icon: "credit-card",
    title: "Order management",
    description: "Centralized dashboard to manage orders, returns, and communications.",
    color: "from-accent to-accent/60",
  },
  {
    icon: "tracking",
    title: "Real-time tracking",
    description: "Live shipment status updates from pickup to delivery.",
    color: "from-primary to-accent",
  },
  {
    icon: "users",
    title: "Seller tools",
    description: "Inventory management, analytics, and marketing tools.",
    color: "from-accent to-primary",
  },
  {
    icon: "globe",
    title: "Multi-carrier support",
    description: "Ship with DHL, FedEx, UPS, and local carriers from one platform.",
    color: "from-primary to-primary/60",
  },
  {
    icon: "api",
    title: "API access",
    description: "Full REST API for seamless integration with your systems.",
    color: "from-accent to-accent/60",
  },
];

const icons: Record<string, React.ReactElement> = {
  shield: (
    <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10" />
      <path d="m9 12 2 2 4-4" />
    </svg>
  ),
  "credit-card": (
    <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
      <rect x="1" y="3" width="22" height="18" rx="2" />
      <path d="M1 9h22" /><path d="M8 15h2" />
    </svg>
  ),
  tracking: (
    <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
      <path d="M5 12h14" /><path d="m12 5 7 7-7 7" />
    </svg>
  ),
  users: (
    <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
      <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M22 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" />
    </svg>
  ),
  globe: (
    <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
      <circle cx="12" cy="10" r="3" />
    </svg>
  ),
  api: (
    <svg className="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2v4" /><path d="m16.2 7.8 2.9-2.9" />
      <path d="M18 12h4" /><path d="m16.2 16.2 2.9 2.9" />
      <path d="M12 18v4" /><path d="m7.8 16.2-2.9 2.9" />
      <path d="M6 12H2" /><path d="m7.8 7.8-2.9-2.9" />
      <circle cx="12" cy="12" r="2" />
    </svg>
  ),
};

export function FeaturesSection() {
  const { ref, isInView } = useInView();

  return (
    <section id="features" ref={ref} className="relative py-28 sm:py-32">
      <div className="neon-line absolute left-0 right-0 top-0" />
      <div className="container mx-auto max-w-6xl px-4">
        <div className="mx-auto max-w-2xl text-center">
          <h2
            className={`text-3xl font-bold tracking-tight text-foreground sm:text-5xl transition-all duration-700 ${isInView ? "animate-reveal" : "opacity-0"
              }`}
          >
            Everything to ship{" "}
            <span className="text-primary glow-text">with confidence</span>
          </h2>
          <p
            className={`mt-4 text-lg text-muted-foreground transition-all duration-700 delay-150 ${isInView ? "animate-reveal" : "opacity-0"
              }`}
          >
            Powerful tools for sellers, seamless experience for customers.
          </p>
        </div>

        <div className="mt-20 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((f, i) => (
            <FeatureCard key={i} feature={f} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}

function FeatureCard({
  feature,
  index,
}: {
  feature: Feature;
  index: number;
}) {
  const { ref, isInView } = useInView();

  return (
    <div
      ref={ref}
      data-delay={index % 3}
      className={`reveal-on-scroll group relative rounded-2xl border border-border bg-card/50 p-8 transition-all duration-500 hover:border-primary/30 hover:bg-card/80 ${isInView ? "" : ""
        }`}
    >
      <div
        className={`mb-5 inline-flex h-14 w-14 items-center justify-center rounded-xl bg-gradient-to-br ${feature.color} p-0.5 transition-transform duration-500 group-hover:scale-110`}
      >
        <div className="flex h-full w-full items-center justify-center rounded-xl bg-background text-primary">
          {icons[feature.icon]}
        </div>
      </div>
      <h3 className="text-lg font-semibold text-foreground">{feature.title}</h3>
      <p className="mt-2 text-sm text-muted-foreground">{feature.description}</p>
      <div className="pointer-events-none absolute -right-8 -top-8 h-24 w-24 rounded-full bg-primary/5 blur-2xl transition-all group-hover:bg-primary/10" />
    </div>
  );
}