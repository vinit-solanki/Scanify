export async function analyzeProduct({ labelText, mode = "general" }) {
  const response = await fetch("https://scanify-rd8p.onrender.com/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      label_text: labelText,
      mode: mode,
    }),
  });

  let data;
  try {
    data = await response.json();
  } catch (err) {
    data = null;
  }

  if (!response.ok) {
    throw new Error(data?.error || "Backend analysis failed");
  }

  return data;
}

export async function analyzeProductImage({ image, mode = "general" }) {
  const formData = new FormData();
  formData.append("image", image);
  formData.append("mode", mode);

  const response = await fetch("https://scanify-rd8p.onrender.com/analyze", {
    method: "POST",
    body: formData,
  });

  let data;
  try {
    data = await response.json();
  } catch (err) {
    data = null;
  }

  if (!response.ok) {
    throw new Error(data?.error || "Backend image analysis failed");
  }

  return data;
}
