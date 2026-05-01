import { Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";


export default function Navbar() {
    const [scrolled, setScrolled] = useState(false);

    useEffect(() => {
        const onScroll = () => setScrolled(window.scrollY > 20);
        window.addEventListener("scroll", onScroll, { passive: true });
        return () => window.removeEventListener("scroll", onScroll);
    }, []);

    return (

        <header
            className={`fixed top-0 inset-0 z-50 h-20 justify-center transition-all duration-1000 ${scrolled ? "glass-strong border-b border-green" : "bg-transparent"
                }`}
        >
            <div className="container  mx-auto flex h-20 max-w-6xl items-center justify-center px-4">
                <div className="flex items-center gap-2 mx-12">
                    <div className="relative">
                        <svg
                            className="h-7 w-7 text-primary animate-pulse-glow rounded-md"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth={3}
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        >
                            <path d="M5 12h14" />
                            <path d="m12 5 7 7-7 7" />
                            <circle cx="4" cy="12" r="1" fill="currentColor" />
                        </svg>
                    </div>
                    <span className="text-xl font-bold tracking-tight text-foreground glow-text">
                        FastShip
                    </span>
                </div>
                <nav className="hidden items-center gap-8 md:flex flex-grow">
                    {["Track", "Features", "How it works", "For Sellers"].map((item) => (
                        <a
                            key={item}
                            href={`#${item.toLowerCase().replace(/ /g, "-")}`}
                            className="group relative text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
                        >
                            {item}
                            <span className="absolute -bottom-1 left-0 h-0.5 w-0 bg-primary transition-all group-hover:w-full" />
                        </a>
                    ))}
                </nav>
                <div className="flex items-center gap-3">
                    <Link
                        to="/login"
                        className="rounded-md px-4 py-2 text-sm font-medium text-foreground transition-colors hover:bg-accent"
                    >
                        Sign in
                    </Link>
                    <Link
                        to="/register"
                        className="relative overflow-hidden rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-all hover:shadow-lg hover:shadow-primary/25"
                    >
                        <span className="relative z-10">Get started</span>
                        <div className="animate-shimmer absolute inset-0" />
                    </Link>
                </div>
            </div>
        </header>

    );
}
