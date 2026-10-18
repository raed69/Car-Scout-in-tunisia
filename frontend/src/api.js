// The two calls the page makes to the Python backend.

export async function askQuestion(question, conversationId) {
  let response;
  try {
    response = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, conversation_id: conversationId }),
    });
  } catch {
    throw new Error("Could not reach Car Scout. Check that the app is still running in the terminal.");
  }
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(typeof data.detail === "string" ? data.detail : "Something went wrong. Try again.");
  }
  return data;
}

export async function loadPreferences() {
  try {
    const response = await fetch("/api/preferences");
    return response.ok ? (await response.json()).preferences : null;
  } catch {
    return null;
  }
}
