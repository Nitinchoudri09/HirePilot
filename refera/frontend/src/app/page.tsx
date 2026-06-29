import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Hero, {
  ProblemSection, HowItWorks, Features, Testimonials, FAQ, CTA,
} from "@/components/landing/Sections";
import PricingSection from "@/components/landing/PricingSection";

export default function HomePage() {
  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <ProblemSection />
        <HowItWorks />
        <Features />
        <PricingSection compact />
        <Testimonials />
        <FAQ />
        <CTA />
      </main>
      <Footer />
    </>
  );
}
