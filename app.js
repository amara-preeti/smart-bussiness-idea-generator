/* =============================================
   Smart Business Idea Generator
   IBM Granite AI (watsonx.ai) Integration
   ============================================= */

// ─── CONFIG ──────────────────────────────────────────────────────────────────
const CONFIG = {
  modelId: "ibm/granite-4-h-small",
  apiKey: "gRG0zZ5T0CkfbWvkw0I2q9xSpmTTTS9JPpGRogSczggF",
  projectId: "6df1205d-5c58-49ea-a2c2-fc392dd3c254",
};

// ─── STATE ────────────────────────────────────────────────────────────────────
let ideaCount = 3;
let savedIdeas = JSON.parse(localStorage.getItem("savedIdeas") || "[]");

// ─── PROMPT BUILDER ──────────────────────────────────────────────────────────
function buildPrompt({ skills, budget, industry, audience, context, count }) {
  return `You are an expert business strategist and entrepreneur mentor. Generate exactly ${count} unique, creative, and actionable business ideas.

User Profile:
- Skills/Expertise: ${skills || "General"}
- Startup Budget: ${budget || "Flexible"}
- Industry/Niche: ${industry || "Any"}
- Target Audience: ${audience || "General public"}
- Additional Context: ${context || "None"}

For EACH business idea, provide a structured response in the following JSON array format. Return ONLY valid JSON, no markdown, no explanation outside the JSON:

[
  {
    "title": "Business Name / Title",
    "description": "2-3 sentence description of the business idea, what problem it solves, and why it's unique.",
    "industry": "Industry tag (1-2 words)",
    "difficulty": "Easy | Medium | Hard",
    "revenueModel": "How it makes money (e.g. Subscription, Commission, B2B SaaS, etc.)",
    "marketPotential": "Brief market size / opportunity note",
    "nextSteps": [
      "First concrete action to take",
      "Second concrete action to take",
      "Third concrete action to take"
    ]
  }
]

Generate exactly ${count} ideas. Ensure they are realistic, tailored to the user's profile, and varied in approach.`;
}

// ─── MAIN GENERATE ───────────────────────────────────────────────────────────
async function generateIdeas() {
  const skills = document.getElementById("skills").value.trim();
  const budget = document.getElementById("budget").value;
  const industry = document.getElementById("industry").value.trim();
  const audience = document.getElementById("audience").value.trim();
  const context = document.getElementById("context").value.trim();

  if (!skills && !industry && !audience) {
    showError("Please fill in at least one field (Skills, Industry, or Target Audience).");
    return;
  }

  setLoading(true);
  hideError();
  hideResults();

  try {
    const prompt = buildPrompt({ skills, budget, industry, audience, context, count: ideaCount });

    const payload = {
      model_id: CONFIG.modelId,
      project_id: CONFIG.projectId,
      messages: [
        {
          role: "system",
          content: "You are a world-class business idea generator. Always respond with valid JSON only.",
        },
        {
          role: "user",
          content: prompt,
        },
      ],
      parameters: {
        max_new_tokens: 3000,
        temperature: 0.85,
        top_p: 0.95,
      },
    };

    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`API Error (${response.status}): ${errText}`);
    }

    const data = await response.json();
    const rawText = data?.choices?.[0]?.message?.content || "";

    const ideas = parseIdeas(rawText);
    if (!ideas || ideas.length === 0) {
      throw new Error("No ideas returned. Please try again with different inputs.");
    }

    renderIdeas(ideas);
  } catch (err) {
    console.error(err);
    showError(`⚠️ ${err.message}`);
  } finally {
    setLoading(false);
  }
}

// ─── PARSE IDEAS ─────────────────────────────────────────────────────────────
function parseIdeas(raw) {
  // Strip markdown code fences if present
  let text = raw.trim();
  text = text.replace(/^```json\s*/i, "").replace(/^```\s*/i, "").replace(/```\s*$/g, "").trim();

  // Find JSON array in the text
  const startIdx = text.indexOf("[");
  const endIdx = text.lastIndexOf("]");
  if (startIdx !== -1 && endIdx !== -1) {
    text = text.slice(startIdx, endIdx + 1);
  }

  try {
    const parsed = JSON.parse(text);
    return Array.isArray(parsed) ? parsed : [parsed];
  } catch (e) {
    console.warn("JSON parse failed, attempting field extraction…", e);
    return extractIdeasFallback(raw);
  }
}

// Fallback: try to extract ideas heuristically
function extractIdeasFallback(raw) {
  const ideas = [];
  const titleMatches = raw.match(/"title"\s*:\s*"([^"]+)"/g) || [];
  const descMatches = raw.match(/"description"\s*:\s*"([^"]+)"/g) || [];

  titleMatches.forEach((tm, i) => {
    const title = tm.match(/"title"\s*:\s*"([^"]+)"/)?.[1] || `Business Idea ${i + 1}`;
    const description = descMatches[i]?.match(/"description"\s*:\s*"([^"]+)"/)?.[1] || "No description available.";
    ideas.push({
      title,
      description,
      industry: "General",
      difficulty: "Medium",
      revenueModel: "TBD",
      marketPotential: "To be researched",
      nextSteps: ["Research your market", "Create a business plan", "Launch an MVP"],
    });
  });

  return ideas.length > 0 ? ideas : null;
}

// ─── RENDER IDEAS ─────────────────────────────────────────────────────────────
function renderIdeas(ideas) {
  const container = document.getElementById("ideas-container");
  container.innerHTML = "";

  ideas.forEach((idea, idx) => {
    const card = document.createElement("div");
    card.className = "idea-card";
    card.dataset.index = idx;

    const stepsHtml = (idea.nextSteps || [])
      .map((s) => `<li>${escHtml(s)}</li>`)
      .join("");

    card.innerHTML = `
      <div class="idea-header">
        <span class="idea-number">Idea #${idx + 1}</span>
        <span class="idea-title">${escHtml(idea.title || "Untitled")}</span>
        <button class="idea-save-btn" onclick="saveIdea(${idx})" data-idx="${idx}">💾 Save</button>
      </div>
      <div class="idea-body">
        <p>${escHtml(idea.description || "")}</p>
        <div class="idea-tags">
          ${idea.industry ? `<span class="tag tag-industry">🏭 ${escHtml(idea.industry)}</span>` : ""}
          ${idea.difficulty ? `<span class="tag tag-difficulty">⚡ ${escHtml(idea.difficulty)}</span>` : ""}
          ${idea.revenueModel ? `<span class="tag tag-revenue">💰 ${escHtml(idea.revenueModel)}</span>` : ""}
        </div>
        ${idea.marketPotential ? `
          <div class="idea-section-label">Market Potential</div>
          <p>${escHtml(idea.marketPotential)}</p>
        ` : ""}
        ${stepsHtml ? `
          <div class="idea-section-label">Next Steps</div>
          <ul class="idea-steps">${stepsHtml}</ul>
        ` : ""}
      </div>
    `;

    container.appendChild(card);
  });

  // Store current ideas for save/copy
  window._currentIdeas = ideas;

  document.getElementById("results-section").classList.remove("hidden");
  document.getElementById("results-section").scrollIntoView({ behavior: "smooth", block: "start" });
}

// ─── SAVE IDEA ────────────────────────────────────────────────────────────────
function saveIdea(idx) {
  const idea = window._currentIdeas?.[idx];
  if (!idea) return;

  const btn = document.querySelector(`.idea-save-btn[data-idx="${idx}"]`);
  if (btn?.classList.contains("saved")) {
    btn.textContent = "💾 Save";
    btn.classList.remove("saved");
    savedIdeas = savedIdeas.filter((i) => i.title !== idea.title);
    localStorage.setItem("savedIdeas", JSON.stringify(savedIdeas));
    renderHistory();
    return;
  }

  const entry = { ...idea, savedAt: new Date().toISOString() };
  savedIdeas.unshift(entry);
  localStorage.setItem("savedIdeas", JSON.stringify(savedIdeas));

  if (btn) {
    btn.textContent = "✅ Saved";
    btn.classList.add("saved");
  }

  renderHistory();
}

// ─── COPY ALL ─────────────────────────────────────────────────────────────────
function copyAll() {
  if (!window._currentIdeas) return;
  const text = window._currentIdeas
    .map(
      (idea, i) =>
        `Idea #${i + 1}: ${idea.title}\n${idea.description}\n` +
        `Industry: ${idea.industry} | Difficulty: ${idea.difficulty} | Revenue: ${idea.revenueModel}\n` +
        `Market: ${idea.marketPotential}\n` +
        `Next Steps:\n${(idea.nextSteps || []).map((s) => `  → ${s}`).join("\n")}`
    )
    .join("\n\n─────────────────────────────────\n\n");

  navigator.clipboard.writeText(text).then(() => {
    const btn = document.querySelector(".btn-copy");
    if (btn) {
      btn.textContent = "✅ Copied!";
      setTimeout(() => (btn.textContent = "📋 Copy All"), 2000);
    }
  });
}

// ─── HISTORY ─────────────────────────────────────────────────────────────────
function renderHistory() {
  const container = document.getElementById("history-container");
  const clearBtn = document.getElementById("clear-btn");

  if (savedIdeas.length === 0) {
    container.innerHTML = `<p class="empty-state">No ideas saved yet. Generate some above!</p>`;
    clearBtn.classList.add("hidden");
    return;
  }

  clearBtn.classList.remove("hidden");
  container.innerHTML = savedIdeas
    .map(
      (idea, idx) => `
      <div class="history-item">
        <div>
          <div class="history-item-title">${escHtml(idea.title)}</div>
          <div class="history-item-meta">${escHtml(idea.industry || "")} · ${escHtml(idea.difficulty || "")} · Saved ${new Date(idea.savedAt).toLocaleDateString()}</div>
        </div>
        <button class="history-remove-btn" onclick="removeFromHistory(${idx})" title="Remove">✕</button>
      </div>
    `
    )
    .join("");
}

function removeFromHistory(idx) {
  savedIdeas.splice(idx, 1);
  localStorage.setItem("savedIdeas", JSON.stringify(savedIdeas));
  renderHistory();
}

function clearHistory() {
  if (!confirm("Clear all saved ideas?")) return;
  savedIdeas = [];
  localStorage.removeItem("savedIdeas");
  renderHistory();
}

// ─── UI HELPERS ───────────────────────────────────────────────────────────────
function adjustCount(delta) {
  ideaCount = Math.max(1, Math.min(5, ideaCount + delta));
  document.getElementById("count-display").textContent = ideaCount;
}

function setLoading(loading) {
  const btn = document.getElementById("generate-btn");
  const btnText = document.getElementById("btn-text");
  const loader = document.getElementById("btn-loader");
  btn.disabled = loading;
  btnText.classList.toggle("hidden", loading);
  loader.classList.toggle("hidden", !loading);
}

function showError(msg) {
  const box = document.getElementById("error-box");
  box.textContent = msg;
  box.classList.remove("hidden");
}
function hideError() {
  document.getElementById("error-box").classList.add("hidden");
}
function hideResults() {
  document.getElementById("results-section").classList.add("hidden");
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

// Allow Enter key to trigger generate on text inputs
document.querySelectorAll("input[type='text']").forEach((el) => {
  el.addEventListener("keydown", (e) => {
    if (e.key === "Enter") generateIdeas();
  });
});

// ─── INIT ─────────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  renderHistory();
});
