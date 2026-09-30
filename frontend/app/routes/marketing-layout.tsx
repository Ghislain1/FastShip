import { Outlet } from "react-router";
import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";
import { FloatingParticles } from "../components/marketing/FloatingParticles";
import { GridOverlay } from "../components/marketing/GridOverlay";

export default function MarketingLayout() {
  return (
    <div className="relative flex min-h-screen flex-col overflow-x-hidden bg-background">
      <FloatingParticles />
      <GridOverlay />
      <Navbar />
      <main className="relative z-10 flex-1">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
