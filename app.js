/* =============================================
  Smart Business Idea Generator
  Local template-based idea generation
  ============================================= */

// ─── STATE ────────────────────────────────────────────────────────────────────
let ideaCount = 3;
let savedIdeas = JSON.parse(localStorage.getItem("savedIdeas") || "[]");

// ─── LOCAL GENERATOR ─────────────────────────────────────────────────────────
function generateLocalIdeas({ skills, budget, industry, audience, context, count }) {
  const skillText = skills || "your strongest skills";
  const nicheText = industry || "your chosen market";
  const audienceText = audience || "a focused customer group";
  const contextText = context ? ` It can address this goal: ${context}.` : "";
  const ideas = [
    {
      title: `${nicheText} Starter Studio`,
      description: `A practical service that helps ${audienceText} solve a recurring problem in ${nicheText} using ${skillText}. Start with a focused offer, then turn the most requested work into repeatable packages.${contextText}`,
      industry: nicheText,
      difficulty: "Easy",
      revenueModel: "Service packages",
      marketPotential: `A focused audience such as ${audienceText} can be reached through local groups, referrals, and niche communities.`,
      nextSteps: [`Interview five ${audienceText}`, "Design one fixed-price starter package", "Deliver a pilot and collect testimonials"],
    },
    {
      title: `${nicheText} Resource Hub`,
      description: `A curated library of templates, guides, and tools for ${audienceText}. Your knowledge of ${skillText} gives the hub a useful point of view and makes it easier to maintain than a generic directory.${contextText}`,
      industry: nicheText,
      difficulty: "Medium",
      revenueModel: "Membership or digital downloads",
      marketPotential: "A small, well-defined information gap can become a dependable recurring-revenue product.",
      nextSteps: ["List the ten questions customers ask most", "Publish three useful free resources", "Validate a paid bundle with early users"],
    },
    {
      title: `${audienceText} Progress Club`,
      description: `A lightweight accountability community where ${audienceText} make progress on goals related to ${nicheText}. Combine group sessions, practical challenges, and your ${skillText} expertise.${contextText}`,
      industry: "Community",
      difficulty: "Medium",
      revenueModel: "Monthly membership",
      marketPotential: "Communities become resilient businesses when members receive visible progress and a reason to return each week.",
      nextSteps: ["Invite ten founding members", "Run a two-week free challenge", "Measure attendance and define the paid membership"],
    },
    {
      title: `${nicheText} Matchmaking Service`,
      description: `A trusted matching service connecting ${audienceText} with vetted specialists, products, or opportunities in ${nicheText}. Begin manually and use your ${skillText} to improve the recommendations.${contextText}`,
      industry: nicheText,
      difficulty: "Hard",
      revenueModel: "Referral commission",
      marketPotential: "Trust and convenience create value where customers struggle to compare specialized choices.",
      nextSteps: ["Map the most common buying decision", "Recruit five trusted providers", "Test matching manually with the first customers"],
    },
    {
      title: `${nicheText} Field Kit`,
      description: `A compact physical or digital kit that helps ${audienceText} complete a specific task in ${nicheText}. Keep the first version simple and use ${skillText} to make it clearer and more useful.${contextText}`,
      industry: nicheText,
      difficulty: "Medium",
      revenueModel: "Product sales",
      marketPotential: "A narrowly defined kit is easier to explain, price, and sell than a broad product line.",
      nextSteps: ["Choose one high-friction task", "Prototype the smallest useful kit", "Pre-sell to ten interested customers"],
    },
  ];

  return ideas.slice(0, count);
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
    renderIdeas(generateLocalIdeas({ skills, budget, industry, audience, context, count: ideaCount }));
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
