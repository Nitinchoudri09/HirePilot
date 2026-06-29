import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import PricingSection from "@/components/landing/PricingSection";

export default function PricingPage() {
  return (
    <>
      <Navbar />
      <main className="pt-24">
        <PricingSection />
      </main>
      <Footer />
    </>
  );
}
