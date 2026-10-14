import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FuturePath AI — Sign in",
  description: "Sign in to your personal career intelligence workspace.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
