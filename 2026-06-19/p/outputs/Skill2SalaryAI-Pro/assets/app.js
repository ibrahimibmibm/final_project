const skillCatalog = {
  Python: ["python"], SQL: ["sql"], JavaScript: ["javascript", "js"], React: ["react"],
  "Machine Learning": ["machine learning", "ml", "sklearn", "scikit"], "Deep Learning": ["deep learning", "neural"],
  NLP: ["nlp", "natural language"], "Generative AI": ["generative ai", "llm", "prompt"],
  Pandas: ["pandas"], NumPy: ["numpy"], Docker: ["docker"], Kubernetes: ["kubernetes", "k8s"],
  AWS: ["aws"], Azure: ["azure"], GCP: ["gcp"], MLOps: ["mlops", "deployment", "monitoring"],
  FastAPI: ["fastapi"], Streamlit: ["streamlit"], "Power BI": ["power bi"], Tableau: ["tableau"],
  Statistics: ["statistics", "statistical"], "A/B Testing": ["a/b", "ab testing"],
  Leadership: ["leadership", "mentor", "stakeholder"], "Product Strategy": ["product strategy", "roadmap"]
};

const roleNeeds = {
  "AI Engineer": ["Python", "Generative AI", "NLP", "MLOps", "Docker", "FastAPI", "AWS"],
  "Data Scientist": ["Python", "SQL", "Machine Learning", "Statistics", "Pandas", "NLP"],
  "ML Engineer": ["Python", "Machine Learning", "MLOps", "Docker", "Kubernetes", "AWS"],
  "Full-Stack Developer": ["JavaScript", "React", "SQL", "Docker", "FastAPI", "AWS"],
  "Data Analyst": ["SQL", "Python", "Power BI", "Tableau", "Statistics", "Pandas"],
  "Product Manager": ["Product Strategy", "SQL", "A/B Testing", "Leadership", "Statistics"]
};

const baseSalary = {
  "AI Engineer": 132000,
  "Data Scientist": 118000,
  "ML Engineer": 128000,
  "Full-Stack Developer": 106000,
  "Data Analyst": 76000,
  "Product Manager": 122000
};

const state = {
  name: "",
  role: "AI Engineer",
  skills: [],
  ats: 0,
  experience: 3,
  depth: 6,
  proof: 4
};

const $ = (id) => document.getElementById(id);
const money = (value) => `$${Math.round(value).toLocaleString()}`;

function saveState() {
  localStorage.setItem("s2s-profile", JSON.stringify(state));
}

function loadState() {
  const saved = localStorage.getItem("s2s-profile");
  if (!saved) return false;
  Object.assign(state, JSON.parse(saved));
  return true;
}

function showDashboard() {
  $("authView").classList.add("hidden");
  $("dashboardView").classList.remove("hidden");
  $("welcomeText").textContent = `Welcome, ${state.name}`;
  $("roleTitle").textContent = `${state.role} Career Intelligence`;
  renderAll();
}

function extractSkills(text) {
  const clean = text.toLowerCase();
  return Object.entries(skillCatalog)
    .filter(([, aliases]) => aliases.some((alias) => clean.includes(alias)))
    .map(([skill]) => skill);
}

function calculateAts(text, skills) {
  const checks = [
    /@|email|phone|linkedin/i.test(text),
    /\d+%|\$\d+|\b\d+\b/.test(text),
    /project|github|portfolio|demo/i.test(text),
    /experience|work|intern|engineer|analyst/i.test(text),
    /impact|improved|reduced|increased|built|launched/i.test(text),
    skills.length >= 5
  ];
  return Math.round((checks.filter(Boolean).length / checks.length) * 100);
}

function skillMatch() {
  const needs = roleNeeds[state.role] || roleNeeds["AI Engineer"];
  const have = new Set(state.skills);
  return Math.round((needs.filter((skill) => have.has(skill)).length / needs.length) * 100);
}

function salary() {
  const base = baseSalary[state.role] || 100000;
  return base + state.experience * 5200 + state.depth * 2400 + state.proof * 2800 + skillMatch() * 180;
}

function careerScore() {
  return Math.min(98, Math.round(state.ats * 0.35 + skillMatch() * 0.35 + state.proof * 3 + state.experience * 1.5 + 18));
}

function missingSkills() {
  const have = new Set(state.skills);
  return (roleNeeds[state.role] || []).filter((skill) => !have.has(skill));
}

function renderMetrics() {
  const sal = salary();
  $("careerScore").textContent = careerScore();
  $("salaryEstimate").textContent = `${Math.round(sal / 1000)}k`;
  $("skillMatch").textContent = `${skillMatch()}%`;
  $("nextAction").textContent = missingSkills()[0] || "Apply";
  $("focusText").textContent = missingSkills().length
    ? `Close ${missingSkills().slice(0, 3).join(", ")} and add one measurable portfolio project.`
    : "Your core role skills are strong. Focus on senior-level proof: architecture, ownership, and outcomes.";
}

function renderSkillCloud() {
  $("skillCount").textContent = `${state.skills.length} found`;
  $("skillCloud").innerHTML = state.skills.length
    ? state.skills.map((skill) => `<span>${skill}</span>`).join("")
    : `<span>Paste a resume to detect skills</span>`;
  const offset = 314 - (314 * state.ats) / 100;
  $("atsRing").style.strokeDashoffset = offset;
  $("atsScore").textContent = `${state.ats}%`;
}

function renderTips() {
  const gaps = missingSkills();
  const tips = [
    gaps.length ? `Add proof for ${gaps.slice(0, 3).join(", ")} using projects, metrics, or certifications.` : "You match the core role skills. Upgrade bullets with ownership and business impact.",
    "Rewrite resume bullets in this format: action + technical method + measurable result.",
    "Add one portfolio case study with problem, architecture, screenshots, and outcome.",
    state.ats < 70 ? "Add contact links, project links, numbers, and a clear skills section." : "Your ATS base is healthy. Make the top third of the resume sharper."
  ];
  $("resumeTips").innerHTML = tips.map((tip) => `<li>${tip}</li>`).join("");
}

function renderRoadmap() {
  const gaps = missingSkills();
  const plan = [
    { day: "01-15", title: gaps[0] || "Portfolio proof", text: `Build a focused ${gaps[0] || state.role} mini-project with measurable output.` },
    { day: "16-35", title: gaps[1] || "Resume upgrade", text: "Rewrite top resume bullets with metrics, keywords, and project links." },
    { day: "36-60", title: gaps[2] || "Interview practice", text: "Practice technical stories, salary negotiation, and system-design style explanations." },
    { day: "61-90", title: "Market push", text: "Apply to matched roles, publish the portfolio case study, and track callbacks weekly." }
  ];
  $("roadmapList").innerHTML = plan.map((item) => `
    <div class="roadmap-item">
      <strong>${item.day}</strong>
      <div><b>${item.title}</b><p>${item.text}</p></div>
    </div>
  `).join("");
}

function drawRadar() {
  const canvas = $("radarChart");
  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);
  const labels = ["Skills", "ATS", "Salary", "Portfolio", "Fit"];
  const values = [state.skills.length * 7, state.ats, Math.min(100, salary() / 1800), state.proof * 10, skillMatch()].map((v) => Math.min(100, v));
  const cx = w / 2;
  const cy = h / 2;
  const radius = 120;
  ctx.strokeStyle = "rgba(148,163,184,.22)";
  ctx.fillStyle = "#cbd5e1";
  ctx.font = "15px Segoe UI";
  for (let ring = 1; ring <= 4; ring++) {
    polygon(ctx, cx, cy, radius * ring / 4, labels.length, false);
  }
  ctx.beginPath();
  values.forEach((value, i) => {
    const angle = -Math.PI / 2 + i * (Math.PI * 2 / labels.length);
    const r = radius * value / 100;
    const x = cx + Math.cos(angle) * r;
    const y = cy + Math.sin(angle) * r;
    i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
  });
  ctx.closePath();
  const gradient = ctx.createLinearGradient(0, 0, w, h);
  gradient.addColorStop(0, "rgba(34,211,238,.55)");
  gradient.addColorStop(1, "rgba(139,92,246,.55)");
  ctx.fillStyle = gradient;
  ctx.fill();
  ctx.strokeStyle = "#22d3ee";
  ctx.lineWidth = 3;
  ctx.stroke();
  labels.forEach((label, i) => {
    const angle = -Math.PI / 2 + i * (Math.PI * 2 / labels.length);
    ctx.fillStyle = "#e0f2fe";
    ctx.fillText(label, cx + Math.cos(angle) * 155 - 28, cy + Math.sin(angle) * 155 + 5);
  });
}

function polygon(ctx, cx, cy, r, sides, fill) {
  ctx.beginPath();
  for (let i = 0; i < sides; i++) {
    const angle = -Math.PI / 2 + i * (Math.PI * 2 / sides);
    const x = cx + Math.cos(angle) * r;
    const y = cy + Math.sin(angle) * r;
    i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
  }
  ctx.closePath();
  fill ? ctx.fill() : ctx.stroke();
}

function drawLineChart(canvasId, points, color = "#22d3ee") {
  const canvas = $(canvasId);
  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;
  const pad = 42;
  ctx.clearRect(0, 0, w, h);
  ctx.strokeStyle = "rgba(148,163,184,.18)";
  ctx.lineWidth = 1;
  for (let i = 0; i < 5; i++) {
    const y = pad + i * ((h - pad * 2) / 4);
    ctx.beginPath();
    ctx.moveTo(pad, y);
    ctx.lineTo(w - pad, y);
    ctx.stroke();
  }
  const min = Math.min(...points) * 0.92;
  const max = Math.max(...points) * 1.04;
  const coords = points.map((p, i) => ({
    x: pad + i * ((w - pad * 2) / (points.length - 1)),
    y: h - pad - ((p - min) / (max - min)) * (h - pad * 2)
  }));
  ctx.beginPath();
  coords.forEach((p, i) => i ? ctx.lineTo(p.x, p.y) : ctx.moveTo(p.x, p.y));
  ctx.strokeStyle = color;
  ctx.lineWidth = 4;
  ctx.stroke();
  coords.forEach((p, i) => {
    ctx.fillStyle = "#050509";
    ctx.strokeStyle = color;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(p.x, p.y, 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = "#cbd5e1";
    ctx.font = "14px Segoe UI";
    ctx.fillText(i === 0 ? "Now" : `Y${i}`, p.x - 12, h - 12);
  });
}

function drawGrowth() {
  const start = salary();
  const growth = 1.045 + Math.min(0.08, skillMatch() / 1600 + state.proof / 1000);
  const points = Array.from({ length: 6 }, (_, i) => start * Math.pow(growth, i));
  drawLineChart("growthChart", points, "#8b5cf6");
}

function renderSalaryLab() {
  state.experience = Number($("experience").value);
  state.depth = Number($("skillDepth").value);
  state.proof = Number($("proof").value);
  $("expValue").textContent = `${state.experience} yrs`;
  $("depthValue").textContent = state.depth;
  $("proofValue").textContent = state.proof;
  const sal = salary();
  $("salaryLive").textContent = money(sal);
  $("salaryRange").textContent = `${money(sal * 0.88)} - ${money(sal * 1.14)} likely range`;
  drawLineChart("salaryChart", [sal * 0.88, sal * 0.94, sal, sal * 1.07, sal * 1.14], "#22d3ee");
}

function renderAll() {
  renderMetrics();
  renderSkillCloud();
  renderTips();
  renderRoadmap();
  renderSalaryLab();
  drawRadar();
  drawGrowth();
  saveState();
}

function addMessage(role, text) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.textContent = text;
  $("chatLog").appendChild(div);
  $("chatLog").scrollTop = $("chatLog").scrollHeight;
}

function coachReply(message) {
  const lower = message.toLowerCase();
  const gaps = missingSkills();
  if (lower.includes("salary") || lower.includes("money") || lower.includes("package")) {
    return `For ${state.role}, your fastest salary lever is proof. Add ${gaps[0] || "a senior-level project"} and one quantified case study. Your current model estimate is ${money(salary())}; strong portfolio proof could move it toward ${money(salary() * 1.12)}.`;
  }
  if (lower.includes("resume")) {
    return `Make your resume sharper by placing ${state.role} keywords in the top third, adding measurable bullets, and showing links. Missing high-value signals: ${gaps.slice(0, 3).join(", ") || "architecture, ownership, and impact"}.`;
  }
  if (lower.includes("interview")) {
    return "Use this answer structure: context, technical decision, tradeoff, measurable result, lesson. Practice two stories: one debugging story and one project ownership story.";
  }
  return `Your next best move is: ${gaps[0] ? `learn and prove ${gaps[0]}` : "apply with a stronger proof-of-impact portfolio"}. Keep it simple: one project, one metric, one clean story.`;
}

function initNavigation() {
  document.querySelectorAll("[data-panel]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const panel = btn.dataset.panel;
      document.querySelectorAll(".panel").forEach((p) => p.classList.remove("active-panel"));
      document.querySelectorAll(".nav-btn").forEach((n) => n.classList.remove("active"));
      $(panel).classList.add("active-panel");
      document.querySelectorAll(`.nav-btn[data-panel="${panel}"]`).forEach((n) => n.classList.add("active"));
      setTimeout(renderAll, 60);
    });
  });
}

function initNetwork() {
  const canvas = $("network");
  const ctx = canvas.getContext("2d");
  const nodes = Array.from({ length: 58 }, () => ({ x: Math.random(), y: Math.random(), vx: (Math.random() - 0.5) * 0.0008, vy: (Math.random() - 0.5) * 0.0008 }));
  function resize() {
    canvas.width = innerWidth * devicePixelRatio;
    canvas.height = innerHeight * devicePixelRatio;
  }
  addEventListener("resize", resize);
  resize();
  function frame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    nodes.forEach((n) => {
      n.x += n.vx; n.y += n.vy;
      if (n.x < 0 || n.x > 1) n.vx *= -1;
      if (n.y < 0 || n.y > 1) n.vy *= -1;
    });
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const a = nodes[i], b = nodes[j];
        const ax = a.x * canvas.width, ay = a.y * canvas.height;
        const bx = b.x * canvas.width, by = b.y * canvas.height;
        const d = Math.hypot(ax - bx, ay - by);
        if (d < 170 * devicePixelRatio) {
          ctx.strokeStyle = `rgba(34,211,238,${(1 - d / (170 * devicePixelRatio)) * 0.22})`;
          ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(bx, by); ctx.stroke();
        }
      }
    }
    nodes.forEach((n) => {
      ctx.fillStyle = "rgba(255,255,255,.72)";
      ctx.beginPath();
      ctx.arc(n.x * canvas.width, n.y * canvas.height, 1.8 * devicePixelRatio, 0, Math.PI * 2);
      ctx.fill();
    });
    requestAnimationFrame(frame);
  }
  frame();
}

function bindEvents() {
  $("loginForm").addEventListener("submit", (event) => {
    event.preventDefault();
    state.name = $("nameInput").value.trim() || "Friend";
    state.role = $("roleInput").value;
    showDashboard();
  });

  $("resetBtn").addEventListener("click", () => {
    localStorage.removeItem("s2s-profile");
    location.reload();
  });

  $("sampleBtn").addEventListener("click", () => {
    $("resumeText").value = "AI Engineer with 3 years experience building Python, FastAPI, SQL and Generative AI applications. Created LLM support bot, improved ticket resolution by 32%, deployed Docker services on AWS, built dashboards with Pandas and React, mentored interns, GitHub portfolio with demos.";
  });

  $("analyzeBtn").addEventListener("click", () => {
    const text = $("resumeText").value;
    state.skills = extractSkills(text);
    state.ats = calculateAts(text, state.skills);
    state.depth = Math.max(1, Math.min(15, state.skills.length));
    $("skillDepth").value = state.depth;
    renderAll();
  });

  ["experience", "skillDepth", "proof"].forEach((id) => $(id).addEventListener("input", renderAll));

  $("chatForm").addEventListener("submit", (event) => {
    event.preventDefault();
    const text = $("chatInput").value.trim();
    if (!text) return;
    addMessage("user", text);
    $("chatInput").value = "";
    setTimeout(() => addMessage("ai", coachReply(text)), 280);
  });
}

initNetwork();
bindEvents();
initNavigation();
if (loadState()) showDashboard();
addMessage("ai", "Hi. I am your career coach. Ask me about salary, resume, interview prep, or what to learn next.");
