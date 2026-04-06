export async function analyzeMessage(message) {
  const API_URL = "http://localhost:8000/analyze";
  
  console.log(`[PEG] Sending message for analysis: "${message}"`);
  
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
      throw new Error(`Server responded with ${res.status}: ${errorText}`);
    }

    const data = await res.json();
    console.log("[PEG] Analysis result received:", data);
    return data;

  } catch (error) {
    console.error("[PEG] Connection failed:", error.message);
    
    // Explicitly fail to ensure frontend uses REAL backend
    return {
      risk_score: 0,
      decision: "ERROR",
      action: "NONE",
      signals: ["Connection Error"],
      recommendation: "Failed to connect to PEG Engine. Ensure backend is running.",
      trace: ["[System] API Connection Failed: " + error.message]
    };
  }
}