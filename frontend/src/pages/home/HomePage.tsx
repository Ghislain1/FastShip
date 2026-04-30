import { createFileRoute } from '@tanstack/react-router'
import Hero from '~/components/Hero';

export const Route = createFileRoute('/home/HomePage')({
    component: RouteComponent,
})

function RouteComponent() {
    return <div>Hello "/home/HomePage"!</div>
}

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