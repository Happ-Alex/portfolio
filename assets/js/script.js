const STORAGE_KEY = "oleksandr-portfolio-preferences";

const defaultPreferences = {
  theme: "system",
  accent: "blue",
};

const accentColors = {
  blue: "#3b82f6",
  teal: "#14b8a6",
  violet: "#8b5cf6",
  coral: "#f97360",
};

function readPreferences() {
  try {
    return {
      ...defaultPreferences,
      ...JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}"),
    };
  } catch {
    return { ...defaultPreferences };
  }
}

let preferences = readPreferences();
const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");

function resolveTheme(theme) {
  return theme === "system" ? (systemTheme.matches ? "dark" : "light") : theme;
}

function applyPreferences() {
  const resolvedTheme = resolveTheme(preferences.theme);
  const accent = accentColors[preferences.accent] || accentColors.blue;

  document.documentElement.dataset.theme = resolvedTheme;
  document.documentElement.dataset.themePreference = preferences.theme;
  document.documentElement.dataset.accent = preferences.accent;
  document.documentElement.style.setProperty("--accent", accent);

  document.querySelector('meta[name="theme-color"]')?.setAttribute(
    "content",
    resolvedTheme === "dark" ? "#0b1120" : "#f5f7fb",
  );

  document.querySelectorAll("[data-theme-option]").forEach((button) => {
    const isSelected = button.dataset.themeOption === preferences.theme;
    button.classList.toggle("is-selected", isSelected);
    button.setAttribute("aria-pressed", String(isSelected));
  });

  document.querySelectorAll("[data-accent-option]").forEach((button) => {
    const isSelected = button.dataset.accentOption === preferences.accent;
    button.classList.toggle("is-selected", isSelected);
    button.setAttribute("aria-pressed", String(isSelected));
  });
}

function savePreferences() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(preferences));
  applyPreferences();
}

applyPreferences();

systemTheme.addEventListener("change", () => {
  if (preferences.theme === "system") applyPreferences();
});

document.querySelectorAll("[data-theme-option]").forEach((button) => {
  button.addEventListener("click", () => {
    preferences.theme = button.dataset.themeOption;
    savePreferences();
  });
});

document.querySelectorAll("[data-accent-option]").forEach((button) => {
  button.addEventListener("click", () => {
    preferences.accent = button.dataset.accentOption;
    savePreferences();
  });
});

const settings = document.querySelector(".settings");
const settingsButton = document.querySelector(".settings-button");
const settingsClose = document.querySelector(".settings-close");

function setSettingsOpen(isOpen) {
  settings?.classList.toggle("is-open", isOpen);
  settingsButton?.setAttribute("aria-expanded", String(isOpen));
}

settingsButton?.addEventListener("click", () => {
  setSettingsOpen(!settings?.classList.contains("is-open"));
});

settingsClose?.addEventListener("click", () => setSettingsOpen(false));

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") setSettingsOpen(false);
});

document.addEventListener("click", (event) => {
  if (settings?.classList.contains("is-open") && !settings.contains(event.target)) {
    setSettingsOpen(false);
  }
});

const sections = [...document.querySelectorAll("[data-page]")];
const navLinks = [...document.querySelectorAll("[data-nav-target]")];
const sectionIds = sections.map((section) => section.id);

function showSection(sectionId, updateHistory = true) {
  const targetId = sectionIds.includes(sectionId) ? sectionId : "home";

  sections.forEach((section) => {
    const isActive = section.id === targetId;
    section.classList.toggle("is-active", isActive);
    section.setAttribute("aria-hidden", String(!isActive));
  });

  navLinks.forEach((link) => {
    const isActive = link.dataset.navTarget === targetId;
    link.classList.toggle("is-active", isActive);
    if (isActive) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  });

  if (updateHistory) history.replaceState(null, "", `#${targetId}`);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

navLinks.forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    showSection(link.dataset.navTarget);
    document.querySelector(".sidebar")?.classList.remove("is-open");
    document.querySelector(".mobile-overlay")?.classList.remove("is-active");
  });
});

document.querySelectorAll("[data-section-link]").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    showSection(link.dataset.sectionLink);
  });
});

window.addEventListener("hashchange", () => showSection(location.hash.slice(1), false));
showSection(location.hash.slice(1) || "home", false);

document.querySelectorAll("[data-language-link]").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    const activeSection = sections.find((section) => section.classList.contains("is-active"))?.id || "home";
    window.location.href = `${link.getAttribute("href")}#${activeSection}`;
  });
});

const menuButton = document.querySelector(".menu-button");
const sidebar = document.querySelector(".sidebar");
const mobileOverlay = document.querySelector(".mobile-overlay");

function setMobileMenuOpen(isOpen) {
  sidebar?.classList.toggle("is-open", isOpen);
  mobileOverlay?.classList.toggle("is-active", isOpen);
  menuButton?.setAttribute("aria-expanded", String(isOpen));
}

menuButton?.addEventListener("click", () => {
  setMobileMenuOpen(!sidebar?.classList.contains("is-open"));
});

mobileOverlay?.addEventListener("click", () => setMobileMenuOpen(false));

document.querySelectorAll("[data-certificate-url]").forEach((link) => {
  const url = link.dataset.certificateUrl?.trim();
  if (!url) {
    link.hidden = true;
    return;
  }
  link.href = url;
  link.target = "_blank";
  link.rel = "noreferrer";
});
