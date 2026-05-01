import { createFileRoute } from "@tanstack/react-router";
import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";
import {
  FloatingParticles,
  GridOverlay,
  HeroSection,
  TrackingSection,
  FeaturesSection,
  HowItWorksSection,
  StatsSection,
  SellerCTASection,
} from "../components/ui/sections";

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