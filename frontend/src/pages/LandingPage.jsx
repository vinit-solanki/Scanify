import React, { useState } from 'react'
import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import Features from "../components/Features";
import Modes from "../components/Modes";
import ProductInsight from "../components/ProductInsight";
import Footer from "../components/Footer";

function LandingPage() {
  const [mode, setMode] = useState("general");

  return (
    <div className="bg-black dark:bg-black text-neutral-900 dark:text-white">
      <Navbar />
      <Hero />
      <Features />
      <Modes selectedMode={mode} onSelect={setMode} />
      <Footer />
    </div>
  )
}

export default LandingPage