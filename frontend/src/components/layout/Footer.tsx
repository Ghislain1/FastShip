export default function Footer() {
  return (
    <footer className="relative border-t border-border py-16">
      <div className="neon-line absolute left-0 right-0 top-0" />
      <div className="container mx-auto max-w-6xl px-4">
        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
          <div>
            <div className="flex items-center gap-2">
              <svg className="h-6 w-6 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 12h14" /><path d="m12 5 7 7-7 7" />
                <circle cx="4" cy="12" r="1" fill="currentColor" />
              </svg>
              <span className="text-lg font-bold text-foreground glow-text">FastShip</span>
            </div>
            <p className="mt-4 text-sm text-muted-foreground">
              The all-in-one shipping and e-commerce platform for modern businesses.
            </p>
          </div>
          {[
            { title: "Product", links: ["Features", "Tracking", "Pricing", "API"] },
            { title: "Company", links: ["About", "Blog", "Careers", "Contact"] },
            { title: "Support", links: ["Help Center", "Docs", "Privacy", "Terms"] },
          ].map((col) => (
            <div key={col.title}>
              <h4 className="text-sm font-semibold text-foreground">{col.title}</h4>
              <ul className="mt-4 space-y-3">
                {col.links.map((link) => (
                  <li key={link}>
                    <a href="#" className="group text-sm text-muted-foreground transition-colors hover:text-primary">
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="mt-12 border-t border-border pt-8 text-center text-sm text-muted-foreground">
          <p>2026 FastShip. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}