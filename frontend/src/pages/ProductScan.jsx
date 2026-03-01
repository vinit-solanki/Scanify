import React, { useState } from 'react'
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { SparklesCore } from "../components/ui/sparkles";
import { BackgroundBeams } from "../components/ui/background-beams";
import { Card } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { analyzeProduct, analyzeProductImage } from "../lib/api";
import { transformAnalysisToScanResult } from "../lib/transformResponse";
import { formatExplanation, getHealthColor } from "../lib/formatExplanation";

const getInsightSectionStyle = (title = "") => {
  const normalized = title.toLowerCase();

  if (normalized.includes("summary")) {
    return {
      icon: "🧠",
      badge: "Overview",
      border: "border-cyan-400/25",
      bg: "bg-cyan-500/10",
      title: "text-cyan-200",
    };
  }

  if (normalized.includes("positive")) {
    return {
      icon: "✅",
      badge: "Strengths",
      border: "border-emerald-400/25",
      bg: "bg-emerald-500/10",
      title: "text-emerald-200",
    };
  }

  if (normalized.includes("concern")) {
    return {
      icon: "⚠️",
      badge: "Watchouts",
      border: "border-amber-400/25",
      bg: "bg-amber-500/10",
      title: "text-amber-200",
    };
  }

  if (normalized.includes("recommend")) {
    return {
      icon: "🎯",
      badge: "Action Plan",
      border: "border-violet-400/25",
      bg: "bg-violet-500/10",
      title: "text-violet-200",
    };
  }

  if (normalized.includes("confidence")) {
    return {
      icon: "📎",
      badge: "Context",
      border: "border-neutral-500/35",
      bg: "bg-neutral-500/10",
      title: "text-neutral-200",
    };
  }

  return {
    icon: "✨",
    badge: "Insight",
    border: "border-white/15",
    bg: "bg-white/5",
    title: "text-emerald-200",
  };
};

const modeOptions = [
  { value: "general", label: "🍽️ General", desc: "Overall health" },
  { value: "diabetes", label: "💉 Diabetes", desc: "Sugar control" },
  { value: "weight_loss", label: "⚖️ Weight Loss", desc: "Calorie tracking" },
];

function ProductScan() {
  const [productData, setProductData] = useState("");
  const [scanResult, setScanResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [imagePreview, setImagePreview] = useState(null);
  const [error, setError] = useState(null);
  const [mode, setMode] = useState("general"); // general, diabetes, weight_loss
  const [uploadedFile, setUploadedFile] = useState(null); // Store the uploaded file

  const handleFileUpload = async (file) => {
    if (!file) return;

    // Store the file for re-analysis
    setUploadedFile(file);

    // Create image preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result);
    };
    reader.readAsDataURL(file);

    setLoading(true);
    setError(null);
    setScanResult(null);

    try {
      const data = await analyzeProductImage({ image: file, mode });
      const transformed = transformAnalysisToScanResult(data);
      setScanResult(transformed);
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.message || 'Failed to analyze image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleTextAnalyze = async () => {
    if (!productData.trim()) return;

    setLoading(true);
    setError(null);
    setScanResult(null);

    try {
      const data = await analyzeProduct({ labelText: productData, mode });
      const transformed = transformAnalysisToScanResult(data);
      setScanResult(transformed);
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.message || 'Failed to analyze product data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Auto re-analyze when mode changes if there's existing data
  const handleModeChange = async (newMode) => {
    setMode(newMode);
    
    // If there's already a result, re-run the analysis with the new mode
    if (scanResult) {
      if (uploadedFile) {
        // Re-analyze with image
        setLoading(true);
        setError(null);
        setScanResult(null);
        
        try {
          const data = await analyzeProductImage({ image: uploadedFile, mode: newMode });
          const transformed = transformAnalysisToScanResult(data);
          setScanResult(transformed);
        } catch (err) {
          console.error('Analysis error:', err);
          setError(err.message || 'Failed to re-analyze image.');
        } finally {
          setLoading(false);
        }
      } else if (productData.trim()) {
        // Re-analyze with text
        setLoading(true);
        setError(null);
        setScanResult(null);
        
        try {
          const data = await analyzeProduct({ labelText: productData, mode: newMode });
          const transformed = transformAnalysisToScanResult(data);
          setScanResult(transformed);
        } catch (err) {
          console.error('Analysis error:', err);
          setError(err.message || 'Failed to re-analyze text.');
        } finally {
          setLoading(false);
        }
      }
    }
  };

  const processSteps = [
    {
      title: "OCR & Text Extraction",
      description: "Extract text from label images or parse input data"
    },
    {
      title: "Nutrition Analysis",
      description: "Parse and normalize nutrition facts per 100g"
    },
    {
      title: "Ingredient Intelligence",
      description: "Identify additives, allergens, and processing level"
    },
    {
      title: "Health Scoring",
      description: "AI-powered health assessment with personalized insights"
    }
  ];

  return (
    <div className="relative min-h-screen bg-gradient-to-b from-black via-neutral-950 to-black text-white">
      <div className="pointer-events-none absolute inset-0 opacity-[0.06]" style={{ backgroundImage: 'linear-gradient(to right, #ffffff 1px, transparent 1px), linear-gradient(to bottom, #ffffff 1px, transparent 1px)', backgroundSize: '56px 56px' }} />
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-24 pb-20">
        <div className="absolute inset-0">
          <div className="absolute -left-20 top-10 h-72 w-72 rounded-full bg-emerald-500/25 blur-3xl" />
          <div className="absolute bottom-0 right-0 h-96 w-96 rounded-full bg-cyan-500/20 blur-3xl" />
          <BackgroundBeams className="opacity-30" />
          <SparklesCore
            id="scan-sparkles"
            background="transparent"
            minSize={0.6}
            maxSize={1.4}
            particleDensity={120}
            className="absolute inset-0 h-full w-full"
            particleColor="#10b981"
          />
        </div>

        <div className="relative z-10 mx-auto max-w-6xl px-6">
          <Card className="relative border-white/10 bg-white/5 backdrop-blur-xl p-7 md:p-10 mb-10 overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/10 via-cyan-500/5 to-violet-500/10" />
            <div className="relative text-center space-y-6">
              <div className="flex items-center justify-center gap-2 flex-wrap">
                <Badge className="bg-white/10 border-white/20 text-neutral-200 text-xs px-3 py-1">AI Nutrition Intelligence</Badge>
                <Badge className="bg-emerald-500/20 border-emerald-400/30 text-emerald-200 text-xs px-3 py-1">Realtime Health Insights</Badge>
              </div>

              <h1 className="text-white text-3xl md:text-5xl font-black leading-tight tracking-tight">
                Food Label <span className="bg-gradient-to-r from-emerald-400 via-cyan-300 to-cyan-600 bg-clip-text text-transparent">
                  Health Analyzer
                </span>
              </h1>

              <p className="max-w-3xl mx-auto text-base md:text-lg text-neutral-300 leading-relaxed">
                Scan labels to instantly evaluate nutrition quality, ingredient risks, and personalized health impact.
                Designed for fast decisions with clinically-inspired clarity.
              </p>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-left">
                {[
                  { title: "OCR Ready", desc: "Image + text input" },
                  { title: "Per 100g", desc: "Normalized analysis" },
                  { title: "Risk Signals", desc: "Additives & allergens" },
                  { title: "AI Insights", desc: "Actionable guidance" },
                ].map((item) => (
                  <div key={item.title} className="rounded-xl border border-white/10 bg-black/30 p-3.5">
                    <p className="text-xs text-neutral-400 uppercase tracking-wider">{item.title}</p>
                    <p className="text-sm text-neutral-100 mt-1 font-medium">{item.desc}</p>
                  </div>
                ))}
              </div>

              {/* Mode Selection */}
              <div className="inline-flex items-center gap-2 rounded-xl border border-white/10 bg-black/40 p-2 flex-wrap justify-center">
                {modeOptions.map(({ value, label, desc }) => (
                  <Button
                    key={value}
                    onClick={() => handleModeChange(value)}
                    disabled={loading}
                    className={`${
                      mode === value
                        ? "bg-gradient-to-r from-emerald-500 to-cyan-500 text-white shadow-lg shadow-emerald-500/35"
                        : "bg-transparent text-neutral-300 hover:bg-white/10"
                    } px-4 py-2.5 text-sm font-semibold transition-all rounded-lg group disabled:opacity-50 disabled:cursor-not-allowed`}
                    title={desc}
                  >
                    {label}
                  </Button>
                ))}
              </div>
            </div>
          </Card>
            
            {/* Mode Change Indicator */}
            {scanResult && loading && (
              <p className="text-xs text-emerald-400 animate-pulse">
                Re-analyzing with {mode === "general" ? "General" : mode === "diabetes" ? "Diabetes" : "Weight Loss"} mode...
              </p>
            )}
          

          {/* Input Section */}
          <div className="grid lg:grid-cols-2 gap-6 mb-10">
            {/* Image Upload */}
            <Card className="relative border-white/10 bg-white/5 p-6 backdrop-blur-xl hover:border-emerald-500/30 transition-all group shadow-2xl shadow-emerald-500/5">
              <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-emerald-500/10 via-cyan-400/5 to-transparent opacity-80" />
              <div className="relative space-y-4">
                <div>
                  <div className="flex items-center justify-between gap-2 flex-wrap mb-2">
                    <h3 className="text-xl font-bold text-white flex items-center gap-2">
                      <span>📸</span>
                    Upload Food Label Image
                    </h3>
                    <Badge className="text-[11px] bg-emerald-500/15 text-emerald-200 border-emerald-400/30">Camera Input</Badge>
                  </div>
                  <p className="text-sm text-neutral-400">Take a photo or upload a clear image of the food label</p>
                </div>

                <div className="border-2 border-dashed border-white/20 rounded-xl p-10 text-center hover:border-emerald-400/60 transition-all cursor-pointer bg-black/30">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => handleFileUpload(e.target.files[0])}
                    className="hidden"
                    id="file-input"
                    disabled={loading}
                  />
                  <label htmlFor="file-input" className="cursor-pointer block">
                    {imagePreview ? (
                      <div className="space-y-4">
                        <img src={imagePreview} alt="Preview" className="mx-auto max-h-56 rounded-lg shadow-lg border border-white/20" />
                        <div className="flex items-center justify-center gap-2">
                          {loading ? (
                            <>
                              <div className="animate-spin h-4 w-4 border-2 border-emerald-400 border-t-transparent rounded-full"></div>
                              <p className="text-sm font-semibold text-emerald-400">Analyzing image...</p>
                            </>
                          ) : (
                            <>
                              <span className="text-emerald-400">✓</span>
                              <p className="text-sm font-semibold text-emerald-400">Image uploaded! Click to change</p>
                            </>
                          )}
                        </div>
                      </div>
                    ) : (
                      <>
                        <div className="text-6xl mb-4">📷</div>
                        <p className="text-lg font-semibold text-white mb-2">Click to upload or drag & drop</p>
                        <p className="text-sm text-neutral-400">Supports JPG, PNG (max 10MB)</p>
                        <p className="text-xs text-neutral-500 mt-3">Best results with clear, well-lit labels</p>
                      </>
                    )}
                  </label>
                </div>
              </div>
            </Card>

            {/* Text Input */}
            <Card className="relative border-white/10 bg-white/5 p-6 backdrop-blur-xl hover:border-cyan-500/30 transition-all group shadow-2xl shadow-cyan-500/5">
              <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-cyan-500/10 via-blue-400/5 to-transparent opacity-80" />
              <div className="relative space-y-4">
                <div>
                  <div className="flex items-center justify-between gap-2 flex-wrap mb-2">
                    <h3 className="text-xl font-bold text-white flex items-center gap-2">
                      <span>📝</span>
                    Paste Label Text
                    </h3>
                    <Badge className="text-[11px] bg-cyan-500/15 text-cyan-200 border-cyan-400/30">Manual Input</Badge>
                  </div>
                  <p className="text-sm text-neutral-400">Enter ingredients list and nutrition facts manually</p>
                </div>

                <textarea
                  className="w-full h-56 rounded-xl border border-white/20 bg-black/60 p-4 text-sm text-white placeholder:text-neutral-500 focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20 focus:outline-none resize-none transition-all"
                  placeholder="Example:&#10;&#10;Ingredients: Wheat flour, sugar, palm oil, salt, artificial flavor, cocoa powder, soy lecithin&#10;&#10;Nutrition Facts (per 100g):&#10;Calories: 480&#10;Total Fat: 23g&#10;Saturated Fat: 12g&#10;Sodium: 350mg&#10;Carbohydrates: 65g&#10;Sugars: 28g&#10;Protein: 6g"
                  value={productData}
                  onChange={(e) => setProductData(e.target.value)}
                  disabled={loading}
                />

                <Button
                  onClick={handleTextAnalyze}
                  disabled={loading || !productData.trim()}
                  className="w-full bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 text-white font-semibold py-6 text-base disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-cyan-500/50 transition-all"
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-2">
                      <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
                      Analyzing...
                    </span>
                  ) : (
                    <span className="flex items-center justify-center gap-2">
                      Analyze Label
                      <span>→</span>
                    </span>
                  )}
                </Button>
              </div>
            </Card>
          </div>

          {/* Error State */}
          {error && (
            <Card className="border-red-500/40 bg-red-500/10 p-6 backdrop-blur mb-6 shadow-lg shadow-red-500/20">
              <div className="flex items-start gap-4 text-red-300">
                <span className="text-3xl flex-shrink-0">⚠️</span>
                <div className="flex-1">
                  <p className="font-bold text-lg text-red-200 mb-1">Analysis Failed</p>
                  <p className="text-sm text-red-300/90 leading-relaxed">{error}</p>
                  <p className="text-xs text-red-400/70 mt-2">Try uploading a clearer image or checking your input text.</p>
                </div>
              </div>
            </Card>
          )}

          {/* Loading State */}
          {loading && !scanResult && (
            <Card className="border-white/10 bg-white/5 p-12 backdrop-blur text-center shadow-xl shadow-emerald-500/10">
              <div className="space-y-4">
                <div className="inline-block animate-spin rounded-full h-16 w-16 border-4 border-emerald-400 border-t-transparent" />
                <div>
                  <p className="text-xl font-bold text-emerald-400">Analyzing Food Label...</p>
                  <p className="text-sm text-neutral-400 mt-2">This may take a few seconds</p>
                </div>
                <div className="flex justify-center gap-2 text-xs text-neutral-500">
                  <span className="animate-pulse">• Extracting text</span>
                  <span className="animate-pulse delay-75">• Analyzing nutrition</span>
                  <span className="animate-pulse delay-150">• Generating insights</span>
                </div>
              </div>
            </Card>
          )}

          {/* Results Section */}
          {scanResult && (
            <div className="grid lg:grid-cols-12 gap-6">
              {/* AI Insights - Left Side */}
              {scanResult.rawData?.explanation && (
                <Card className="relative border-white/10 bg-white/5 backdrop-blur-xl overflow-hidden h-fit lg:col-span-7 shadow-2xl shadow-violet-500/10">
                  <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-violet-500/15 via-cyan-400/10 to-transparent" />
                  <div className="relative p-6 space-y-5">
                    <div className="flex items-center justify-between gap-3 border-b border-white/10 pb-4 flex-wrap">
                      <div className="flex items-center gap-3">
                        <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-gradient-to-br from-violet-500/30 to-cyan-500/20 border border-white/10 shadow-lg shadow-violet-500/20">
                        <span className="text-2xl">🤖</span>
                        </div>
                        <div>
                          <h3 className="text-xl font-bold text-white">AI Health Insights</h3>
                          <p className="text-xs text-neutral-400 mt-0.5">Generated from nutrition, ingredients, and risk signals</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge className="bg-violet-500/20 text-violet-200 border-violet-400/30 text-[11px] px-2.5 py-1">OpenRouter</Badge>
                        <Badge className="bg-cyan-500/20 text-cyan-200 border-cyan-400/30 text-[11px] px-2.5 py-1">AI Summary</Badge>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 pr-2 custom-scrollbar">
                      {formatExplanation(scanResult.rawData.explanation)?.map((section, idx) => {
                        const sectionStyle = getInsightSectionStyle(section.title);

                        return (
                        <div key={idx} className={`rounded-xl border ${sectionStyle.border} ${sectionStyle.bg} p-4 space-y-3 backdrop-blur-sm`}>
                          <div className="flex items-center justify-between gap-2 flex-wrap">
                            {section.title ? (
                              <h4 className={`text-[15px] font-bold ${sectionStyle.title} flex items-center gap-2`}>
                                <span>{sectionStyle.icon}</span>
                                {section.title}
                              </h4>
                            ) : (
                              <h4 className={`text-[15px] font-bold ${sectionStyle.title} flex items-center gap-2`}>
                                <span>{sectionStyle.icon}</span>
                                Insight
                              </h4>
                            )}
                            <Badge variant="outline" className="text-[10px] border-white/15 bg-black/20 text-neutral-300 px-2 py-0.5">
                              {sectionStyle.badge}
                            </Badge>
                          </div>

                          <div className="space-y-2.5">
                            {section.content.map((item, cidx) => {
                              if (item.type === 'bullet') {
                                return (
                                  <div key={cidx} className="flex items-start gap-2.5">
                                    <span className="mt-1 h-1.5 w-1.5 rounded-full bg-white/70"></span>
                                    <p className="text-sm text-neutral-200 leading-relaxed">{item.text}</p>
                                  </div>
                                );
                              }

                              if (item.type === 'break') {
                                return <div key={cidx} className="h-1"></div>;
                              }

                              return (
                                <p key={cidx} className="text-sm text-neutral-200 leading-relaxed">
                                  {item.text}
                                </p>
                              );
                            })}
                          </div>
                        </div>
                        );
                      }) || (
                        <div className="text-sm text-neutral-300 leading-relaxed whitespace-pre-line">
                          {scanResult.rawData.explanation}
                        </div>
                      )}
                    </div>
                  </div>
                </Card>
              )}

              {/* Health Analysis - Right Side */}
              <Card className="relative border-white/10 bg-white/5 backdrop-blur-xl overflow-hidden h-fit lg:col-span-5 lg:sticky lg:top-24 shadow-2xl shadow-emerald-500/10">
                <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-emerald-500/10 via-cyan-400/5 to-transparent" />
                <div className="relative p-6 space-y-6">
                  <div className="flex items-center justify-between flex-wrap gap-3">
                    <h2 className="text-xl font-bold text-white">Health Analysis</h2>
                    <Badge className="bg-emerald-500/20 text-emerald-300 border-emerald-400/30 px-4 py-2 text-sm font-semibold">
                      {scanResult.confidence}% Confidence
                    </Badge>
                  </div>

                  <div className="space-y-2">
                    <div className="h-2 w-full rounded-full bg-white/10 overflow-hidden">
                      <div className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-cyan-400" style={{ width: `${Math.max(5, Math.min(100, scanResult.confidence || 0))}%` }} />
                    </div>
                    <p className="text-xs text-neutral-400">Model confidence reflects extraction completeness and signal quality.</p>
                  </div>

                  {/* Primary Category */}
                  <div className="space-y-3">
                    <p className="text-xs uppercase tracking-wider text-neutral-400 font-semibold">Health Category</p>
                    <div className={`bg-gradient-to-r ${getHealthColor(scanResult.category).gradient} p-[2px] rounded-xl shadow-lg`}>
                      <div className="bg-black rounded-xl p-5">
                        <div className="flex items-center gap-3">
                          <span className="text-3xl">{getHealthColor(scanResult.category).icon}</span>
                          <div>
                            <p className="text-2xl font-bold text-white">{scanResult.category}</p>
                            <p className="text-xs text-neutral-400 mt-1">Overall Rating</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Key Indicators */}
                  <div className="space-y-3">
                    <p className="text-xs uppercase tracking-wider text-neutral-400 font-semibold">Key Indicators</p>
                    <div className="flex flex-wrap gap-2">
                      {scanResult.labels.length > 0 ? (
                        scanResult.labels.map((label, idx) => (
                          <Badge key={idx} variant="outline" className="border-cyan-400/40 bg-cyan-500/15 text-cyan-200 px-3 py-1.5 text-xs font-medium">
                            {label}
                          </Badge>
                        ))
                      ) : (
                        <p className="text-sm text-neutral-500 italic">No specific indicators detected</p>
                      )}
                    </div>
                  </div>

                  {/* Nutritional Profile */}
                  <div className="space-y-3">
                    <p className="text-xs uppercase tracking-wider text-neutral-400 font-semibold">Nutritional Profile</p>
                    <div className="grid grid-cols-2 gap-3">
                      {Object.entries(scanResult.attributes).map(([key, value]) => (
                        <div key={key} className="bg-white/5 border border-white/10 rounded-lg p-3 hover:bg-white/10 transition-colors">
                          <p className="text-xs text-neutral-400 mb-1.5 font-medium">{key}</p>
                          <p className="text-sm font-bold text-white">{value}</p>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Detailed Analysis */}
                  <div className="space-y-3">
                    <p className="text-xs uppercase tracking-wider text-neutral-400 font-semibold">Detailed Breakdown</p>
                    <div className="space-y-2 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
                      {scanResult.signals.map((signal, idx) => (
                        <div key={idx} className="bg-white/5 border border-white/10 rounded-lg p-3.5 hover:bg-white/8 transition-all">
                          <div className="flex justify-between items-start gap-3">
                            <span className="text-xs font-semibold text-emerald-300 min-w-fit">{signal.key}</span>
                            <span className="text-xs text-neutral-200 text-right">{signal.value}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          )}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="relative py-20 overflow-hidden">
        <div className="absolute inset-0 opacity-40">
          <SparklesCore
            id="process-sparkles"
            background="transparent"
            minSize={0.4}
            maxSize={1}
            particleDensity={80}
            className="h-full w-full"
            particleColor="#06b6d4"
          />
        </div>

        <div className="relative z-10 mx-auto max-w-6xl px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">How It Works</h2>
            <p className="text-neutral-400 max-w-2xl mx-auto">
              Our AI system analyzes food labels using OCR, ingredient parsing, and nutrition science
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {processSteps.map((step, idx) => (
              <Card key={idx} className="border-white/10 bg-white/5 p-6 backdrop-blur hover:bg-white/10 hover:border-emerald-400/25 transition-all group">
                <div className="space-y-3">
                  <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-500 to-cyan-500 text-white font-bold text-lg group-hover:scale-105 transition-transform">
                    0{idx + 1}
                  </div>
                  <h3 className="text-lg font-bold text-white leading-snug">{step.title}</h3>
                  <p className="text-sm text-neutral-400">{step.description}</p>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="relative p-3 bg-gradient-to-b from-black to-neutral-950">
        <div className="mx-auto max-w-6xl px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Use Cases</h2>
            <p className="text-neutral-400">Make informed food choices based on your health goals</p>
          </div>

          <div className="mb-7 grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            {[
              { icon: "🏃", title: "Weight Management", desc: "Track calories and macros" },
              { icon: "💉", title: "Diabetes Care", desc: "Monitor sugar and carbs" },
              { icon: "❤️", title: "Heart Health", desc: "Control sodium and fats" },
              { icon: "🌱", title: "Clean Eating", desc: "Avoid additives and processing" }
            ].map((useCase, idx) => (
              <div key={idx} className="bg-gradient-to-br from-white/5 to-white/0 border border-white/10 rounded-xl p-6 hover:border-emerald-400/30 hover:bg-white/10 transition-all">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-lg bg-white/10 border border-white/15 text-2xl mb-3">{useCase.icon}</div>
                <h3 className="text-lg font-bold text-white mb-2 leading-snug">{useCase.title}</h3>
                <p className="text-sm text-neutral-400">{useCase.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}

export default ProductScan
