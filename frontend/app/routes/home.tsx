import { HeroSection } from "../components/marketing/HeroSection";
import { TrackingSection } from "../components/marketing/TrackingSection";
import { FeaturesSection } from "../components/marketing/FeaturesSection";
import { HowItWorksSection } from "../components/marketing/HowItWorksSection";
import { StatsSection } from "../components/marketing/StatsSection";
import { SellerCTASection } from "../components/marketing/SellerCTASection";

export default function Home() {
  return (
    <>
      <HeroSection />
      <TrackingSection />
      <FeaturesSection />
      <HowItWorksSection />
      <StatsSection />
      <SellerCTASection />
    </>
  );
}
