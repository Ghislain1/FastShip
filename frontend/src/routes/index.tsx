import { useEffect, useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { useInView } from "../hooks/use-in-view";
import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  return (
    <div className="relative flex min-h-screen flex-col overflow-x-hidden bg-background">
      <FloatingParticles />
      <GridOverlay />
      <Navbar />
      <main className="relative z-10">
        <HeroSection />
        <TrackingSection />
        <FeaturesSection />
        <HowItWorksSection />
        <StatsSection />
        <SellerCTASection />
      </main>
      <Footer />
    </div>
  );
}

function FloatingParticles() {
  const particles = Array.from({ length: 120 }, (_, i) => i);
  return (
    <div className="pointer-events-none fixed inset-0 z-0">
      {particles.map((i) => {
        const size = Math.random() * 4 + 2;
        const left = Math.random() * 100;
        const top = Math.random() * 100;
        const delay = Math.random() * 6;
        const dur = Math.random() * 8 + 6;
        return (
          <div
            key={i}
            className="absolute rounded-full bg-primary/30"
            style={{
              width: size,
              height: size,
              left: `${left}%`,
              top: `${top}%`,
              animation: `float ${dur}s ease-in-out ${delay}s infinite`,
            }}
          />
        );
      })}
    </div>
  );
}

function GridOverlay() {
  return <div className="pointer-events-none fixed inset-0 z-0 opacity-30 grid-bg" />;
}

function HeroSection() {
  const { ref, isInView } = useInView();

  return (
    <section ref={ref} className="relative overflow-hidden py-32 sm:py-40">
      <div className="pointer-events-none absolute inset-0 -z-10">
        <div className="absolute left-1/2 top-0 h-96 w-96 -translate-x-1/2 rounded-full bg-primary/10 blur-3xl" />
        <div className="absolute right-0 top-1/4 h-64 w-64 rounded-full bg-accent/5 blur-3xl" />
      </div>

      <div className="container mx-auto max-w-6xl px-4 text-center">
        <div
          className={`mx-auto mb-8 inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-5 py-2 text-sm text-primary transition-all duration-700 ${isInView ? "animate-reveal" : "opacity-0"
            }`}
        >
          <span className="relative flex h-2.5 w-2.5">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-primary opacity-75" />
            <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-primary" />
          </span>
          Real-time shipment tracking
        </div>

        <h1
          className={`mx-auto max-w-4xl text-5xl font-bold tracking-tight text-foreground sm:text-6xl lg:text-8xl transition-all duration-700 delay-150 ${isInView ? "animate-reveal" : "opacity-0"
            }`}
        >
          Ship{" "}
          <span className="relative">
            <span className="animate-gradient bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent">
              faster.
            </span>
          </span>{" "}
          <br />
          Track{" "}
          <span className="relative">
            <span className="animate-gradient bg-gradient-to-r from-accent via-primary to-accent bg-clip-text text-transparent">
              smarter.
            </span>
          </span>
        </h1>

        <p
          className={`mx-auto mt-6 max-w-2xl text-lg text-muted-foreground sm:text-xl transition-all duration-700 delay-300 ${isInView ? "animate-reveal" : "opacity-0"
            }`}
        >
          The all-in-one platform for sellers and customers to manage orders,
          track shipments in real-time, and deliver with confidence.
        </p>

        <div
          className={`mt-12 flex flex-col items-center justify-center gap-4 sm:flex-row transition-all duration-700 delay-500 ${isInView ? "animate-reveal" : "opacity-0"
            }`}
        >
          <Link
            to="/register"
            className="group relative inline-flex h-14 items-center justify-center overflow-hidden rounded-xl bg-primary px-10 text-base font-medium text-primary-foreground shadow-lg shadow-primary/20 transition-all hover:shadow-xl hover:shadow-primary/30"
          >
            <span className="relative z-10">Start selling free</span>
            <div className="animate-shimmer absolute inset-0" />
          </Link>
          <a
            href="#track"
            className="group inline-flex h-14 items-center justify-center rounded-xl border border-border bg-background/50 px-10 text-base font-medium text-foreground backdrop-blur transition-all hover:border-primary/40 hover:bg-background/80"
          >
            Track a package
            <svg
              className="ml-2 h-4 w-4 transition-transform group-hover:translate-y-0.5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path d="M12 5v14M5 12l7 7 7-7" />
            </svg>
          </a>
        </div>

        <div
          className={`mx-auto mt-20 max-w-4xl transition-all duration-700 delay-700 ${isInView ? "animate-reveal" : "opacity-0"
            }`}
        >
          <div className="relative glass rounded-2xl p-1 glow-box">
            <div className="overflow-hidden rounded-xl">
              <div className="flex items-center gap-2 border-b border-border bg-secondary/40 px-5 py-3">
                <div className="flex gap-2">
                  <div className="h-3 w-3 rounded-full bg-destructive/60" />
                  <div className="h-3 w-3 rounded-full bg-muted-foreground/30" />
                  <div className="h-3 w-3 rounded-full bg-primary/60" />
                </div>
                <span className="ml-3 rounded-md bg-secondary px-3 py-0.5 text-xs text-muted-foreground">
                  fastship.app/dashboard
                </span>
              </div>
              <div className="grid grid-cols-3 gap-4 bg-card/50 p-6">
                <DashboardStat label="Active Shipments" value="142" change="+12%" />
                <DashboardStat label="Delivered Today" value="38" change="+5%" />
                <DashboardStat label="Avg. Delivery Time" value="2.4d" change="-8%" />
              </div>
            </div>
            <div className="pointer-events-none absolute -right-12 -top-12 h-24 w-24 rounded-full bg-primary/20 blur-2xl" />
          </div>
        </div>
      </div>
    </section>
  );
}

function DashboardStat({
  label,
  value,
  change,
}: {
  label: string;
  value: string;
  change: string;
}) {
  return (
    <div className="group rounded-xl border border-border bg-secondary/20 p-5 transition-all hover:border-primary/30 hover:bg-secondary/30">
      <p className="text-xs font-medium text-muted-foreground">{label}</p>
      <p className="mt-2 text-3xl font-bold tracking-tight text-foreground glow-text">
        {value}
      </p>
      <p
        className={`mt-1 text-xs font-medium ${change.startsWith("-") ? "text-primary" : "text-accent"
          }`}
      >
        {change} this week
      </p>
    </div>
  );
}

function TrackingSection() {
  const { ref, isInView } = useInView();

  return (
    <section id="track" ref={ref} className="relative py-28 sm:py-32">
      <div className="neon-line absolute left-0 right-0 top-0" />
      <div className="container mx-auto max-w-6xl px-4">
        <div className="mx-auto max-w-2xl text-center">
          <h2
            className={`text-3xl font-bold tracking-tight text-foreground sm:text-5xl transition-all duration-700 ${isInView ? "animate-reveal" : "opacity-0"
              }`}
          >
            Track any shipment{" "}
            <span className="animate-gradient bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              instantly
            </span>
          </h2>
          <p
            className={`mt-4 text-lg text-muted-foreground transition-all duration-700 delay-150 ${isInView ? "animate-reveal" : "opacity-0"
              }`}
          >
            Enter your tracking number to get real-time updates.
          </p>
        </div>

        <div
          className={`mx-auto mt-12 max-w-xl transition-all duration-700 delay-300 ${isInView ? "animate-reveal" : "opacity-0"
            }`}
        >
          <div className="relative group">
            <div className="absolute -inset-0.5 rounded-xl bg-gradient-to-r from-primary/50 to-accent/50 opacity-0 blur transition-opacity group-hover:opacity-100" />
            <div className="relative flex gap-3 rounded-xl border border-border bg-card p-2">
              <input
                type="text"
                placeholder="FS-2026-XXXXX"
                className="flex-1 rounded-lg bg-secondary/50 px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground/50 focus:bg-secondary/70 focus:outline-none focus:ring-2 focus:ring-primary/30"
              />
              <button className="inline-flex items-center rounded-lg bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground transition-all hover:bg-primary/90 hover:shadow-lg hover:shadow-primary/25">
                <svg
                  className="mr-2 h-4 w-4"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth={2.5}
                >
                  <circle cx="11" cy="11" r="8" />
                  <path d="m21 21-4.3-4.3" />
                </svg>
                Track
              </button>
            </div>
          </div>
        </div>

        <div
          className={`mx-auto mt-16 max-w-lg transition-all duration-700 delay-500 ${isInView ? "animate-reveal" : "opacity-0"
            }`}
        >
          <TrackingTimeline />
        </div>
      </div>
    </section>
  );
}

function TrackingTimeline() {
  const [activeStep, setActiveStep] = useState(0);
  const steps = [
    { status: "Order confirmed", time: "Apr 28, 10:30 AM", done: true },
    { status: "Picked up by carrier", time: "Apr 29, 2:15 PM", done: true },
    { status: "In transit", time: "Apr 30, 8:00 AM", done: true },
    { status: "Out for delivery", time: "Est. May 1", done: false },
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveStep((p) => (p < steps.length - 1 ? p + 1 : 0));
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="glass rounded-2xl p-6 glow-box">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold text-foreground">FS-2026-78432</p>
          <p className="mt-0.5 text-xs text-muted-foreground">DHL Express</p>
        </div>
        <span className="inline-flex items-center rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
          In Transit
        </span>
      </div>
      <div className="mt-6 space-y-0">
        {steps.map((step, i) => (
          <div
            key={i}
            className={`flex items-center gap-3 transition-opacity duration-500 ${i === activeStep ? "opacity-100" : "opacity-60"
              }`}
          >
            <div className="flex flex-col items-center">
              <div
                className={`h-3.5 w-3.5 rounded-full transition-all duration-500 ${step.done
                  ? "bg-primary shadow-lg shadow-primary/40"
                  : "border-2 border-border bg-transparent"
                  }`}
              />
              {i < steps.length - 1 && (
                <div
                  className={`w-0.5 transition-all duration-500 ${step.done ? "h-10 bg-primary/40" : "h-10 bg-border"
                    }`}
                />
              )}
            </div>
            <div className="flex-1 pb-4">
              <p
                className={`text-sm font-medium transition-colors ${step.done ? "text-foreground" : "text-muted-foreground"
                  }`}
              >
                {step.status}
              </p>
              <p className="text-xs text-muted-foreground">{step.time}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function FeaturesSection() {
  const { ref, isInView } = useInView();
  const features = [
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
  feature: {
    icon: string;
    title: string;
    description: string;
    color: string;
  };
  index: number;
}) {
  const { ref, isInView } = useInView();
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

function HowItWorksSection() {
  const { ref, isInView } = useInView();
  const steps = [
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

function StatsSection() {
  const { ref, isInView } = useInView();
  const stats = [
    { value: "10K+", label: "Active sellers" },
    { value: "2M+", label: "Shipments delivered" },
    { value: "99.5%", label: "On-time delivery" },
    { value: "50+", label: "Carriers supported" },
  ];

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

function SellerCTASection() {
  const { ref, isInView } = useInView();

  return (
    <section id="for-sellers" ref={ref} className="relative py-28 sm:py-32">
      <div className="neon-line absolute left-0 right-0 top-0" />
      <div className="container mx-auto max-w-6xl px-4">
        <div
          className={`reveal-on-scroll relative overflow-hidden rounded-3xl border border-primary/20 bg-gradient-to-br from-primary/10 via-card to-accent/10 p-10 sm:p-16 lg:p-20 glow-box transition-all duration-700 ${isInView ? "" : ""
            }`}
        >
          <div className="pointer-events-none absolute -right-20 -top-20 h-80 w-80 rounded-full bg-primary/20 blur-3xl" />
          <div className="pointer-events-none absolute -bottom-20 -left-20 h-64 w-64 rounded-full bg-accent/15 blur-3xl" />

          <div className="relative z-10 mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-5xl">
              Ready to grow your{" "}
              <span className="animate-gradient bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                business
              </span>
              ?
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Join thousands of sellers who trust FastShip. No setup fees, no monthly commitments.
            </p>
            <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Link
                to="/register"
                className="group relative inline-flex h-14 items-center justify-center overflow-hidden rounded-xl bg-primary px-10 text-base font-semibold text-primary-foreground shadow-lg shadow-primary/20 transition-all hover:shadow-xl hover:shadow-primary/30"
              >
                <span className="relative z-10">Create seller account</span>
                <div className="animate-shimmer absolute inset-0" />
              </Link>
              <a
                href="#features"
                className="inline-flex h-14 items-center justify-center rounded-xl border border-border bg-transparent px-10 text-base font-medium text-foreground transition-all hover:border-primary/40 hover:bg-primary/5"
              >
                Learn more
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
