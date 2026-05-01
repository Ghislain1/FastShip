import { createFileRoute } from '@tanstack/react-router'
import Hero from "~/components/ui/Hero";

export const Route = createFileRoute('/')({
    component: HomePage,
})

export default function HomePage() {
    return (
        <>
            <Hero />
            <h2>Unsere Plattform</h2>
            <p>
                Faship verbindet E-Commerce mit intelligenter Versandlogik.
            </p>
        </>
    );
}