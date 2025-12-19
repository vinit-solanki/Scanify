import { Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import ProductScan from "./pages/ProductScan";

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/scan" element={<ProductScan />} />
    </Routes>
  );
}

export default App;
