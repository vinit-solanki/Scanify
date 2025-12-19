export async function analyzeProduct({ labelText, mode = "general" }) {
  const response = await fetch("http://localhost:5000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      label_text: labelText,
      mode: mode,
    }),
  });

  if (!response.ok) {
    throw new Error("Backend analysis failed");
  }

  return response.json();
}

export async function analyzeProductImage({ image, mode = "general" }) {
  const formData = new FormData();
  formData.append("image", image);
  formData.append("mode", mode);

  const response = await fetch("http://localhost:5000/analyze", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Backend image analysis failed");
  }

  return response.json();
}
