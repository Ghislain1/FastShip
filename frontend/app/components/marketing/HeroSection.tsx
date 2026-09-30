import { useInView } from "../../../hooks/use-in-view";

export function HeroSection() {
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
          <a
            href="/register"
            className="group relative inline-flex h-14 items-center justify-center overflow-hidden rounded-xl bg-primary px-10 text-base font-medium text-primary-foreground shadow-lg shadow-primary/20 transition-all hover:shadow-xl hover:shadow-primary/30"
          >
            <span className="relative z-10">Start selling free</span>
            <div className="animate-shimmer absolute inset-0" />
          </a>
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
                <div className="flex-1 text-center text-xs text-muted-foreground">
                  fastship.delivery
                </div>
              </div>
              <div className="flex aspect-video items-center justify-center bg-card">
                <div className="flex flex-col items-center gap-4">
                  <div className="relative">
                    <div className="h-24 w-24 rounded-full border-4 border-primary/20">
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="h-16 w-16 animate-pulse rounded-full bg-primary" />
                      </div>
                    </div>
                    <div className="absolute -right-12 top-1/2 -translate-y-1/2">
                      <svg className="h-8 w-8 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
                        <path d="M5 12h14M12 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                  <div className="flex gap-8 text-center">
                    <div>
                      <div className="text-2xl font-bold text-foreground">98%</div>
                      <div className="text-xs text-muted-foreground">On-Time</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-foreground">24h</div>
                      <div className="text-xs text-muted-foreground">Delivery</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}