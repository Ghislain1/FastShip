import { useEffect, useState } from "react";
import { useInView } from "../../../hooks/use-in-view";

export function TrackingSection() {
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
  }, [steps.length]);

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