import type { Metadata } from "next";
import { Inter, Space_Grotesk } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/lib/auth";
import GoogleAuthProvider from "@/components/GoogleAuthProvider";
import AIChat from "@/components/AIChat";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const spaceGrotesk = Space_Grotesk({ subsets: ["latin"], variable: "--font-space" });

export const metadata: Metadata = {
  title: "Refera — AI Job Referral Network",
  description: "Get referred to your dream job with AI-powered resume analysis, job matching, and referral messages.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${spaceGrotesk.variable}`}>
      <body className="font-sans">
        <GoogleAuthProvider>
          <AuthProvider>{children}</AuthProvider>
        </GoogleAuthProvider>
        <AIChat />
      </body>
    </html>
  );
}
