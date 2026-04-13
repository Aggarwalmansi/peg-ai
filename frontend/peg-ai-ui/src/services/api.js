export async function analyzeMessage(message) {
  // Use Vite environment variable for API URL
  const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
  const API_URL = `${BASE_URL}/analyze`;
  
  console.log(`[PEG] Requesting analysis from: ${API_URL}`);
  
  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    if (!res.ok) {
      const errorText = await res.text();
      console.error(`[PEG] Backend Error (${res.status}):`, errorText);
      throw new Error(`Server Error (${res.status}): ${errorText}`);
    }

    const data = await res.json();
    console.log("[PEG] Analysis success:", data);
    return data;

  } catch (error) {
    console.error("[PEG] Connection failed:", error.message);
    
    // Throw error to be handled by the UI component's catch block
    throw error;
  }
}