import { Link } from "@tanstack/react-router";
import { useInView } from "../../../hooks/use-in-view";

export function SellerCTASection() {
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

          <div className="relative z-10 mx-auto max-w-3xl text-center">
            <h2
              className={`text-3xl font-bold tracking-tight text-foreground sm:text-5xl transition-all duration-700 ${isInView ? "animate-reveal" : "opacity-0"
                }`}
            >
              Ready to scale your{" "}
              <span className="animate-gradient bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                business
              </span>
              {" "}?
            </h2>
            <p
              className={`mt-6 text-lg text-muted-foreground transition-all duration-700 delay-150 ${isInView ? "animate-reveal" : "opacity-0"
                }`}
            >
              Join thousands of sellers growing their e-commerce with FastShip.
              No credit card required.
            </p>
            <div
              className={`mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row transition-all duration-700 delay-300 ${isInView ? "animate-reveal" : "opacity-0"
                }`}
            >
              <Link
                to="/register"
                className="group relative inline-flex h-14 items-center justify-center overflow-hidden rounded-xl bg-primary px-10 text-base font-medium text-primary-foreground shadow-lg shadow-primary/20 transition-all hover:shadow-xl hover:shadow-primary/30"
              >
                <span className="relative z-10">Get started free</span>
                <div className="animate-shimmer absolute inset-0" />
              </Link>
              <a
                href="#"
                className="inline-flex h-14 items-center justify-center rounded-xl border border-border bg-background/50 px-10 text-base font-medium text-foreground backdrop-blur transition-all hover:border-primary/40 hover:bg-background/80"
              >
                Contact sales
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}