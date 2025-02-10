// Get DOM elements
const openMobileNav = document.getElementById("openMobileNav");
const mobileNav = document.getElementById("mobileNav");
const closeMobileNav = document.getElementById("closeMobileNav");
const toggle = document.getElementById("AcceptConditions");
const toggle2 = document.getElementById("AcceptConditions2");
const html = document.querySelector("html");

/**
 * Updates dark mode state.
 * @param {boolean} isDark - Whether dark mode should be enabled.
 */
function setDarkMode(isDark) {
  if (isDark) {
    html.classList.add("dark");
    toggle.checked = true;
    toggle2.checked = true;
    localStorage.setItem("theme", "dark");
  } else {
    html.classList.remove("dark");
    toggle.checked = false;
    toggle2.checked = false;
    localStorage.setItem("theme", "light");
  }
}

// Check for a stored dark mode preference
const storedTheme = localStorage.getItem("theme");

if (storedTheme) {
  // Use stored preference
  setDarkMode(storedTheme === "dark");
} else {
  // Fall back to the system preference
  const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)").matches;
  setDarkMode(prefersDarkScheme);
}

// Mobile navigation event listeners
openMobileNav.addEventListener("click", () => {
  mobileNav.classList.remove("hidden");
  closeMobileNav.classList.remove("hidden");
  openMobileNav.classList.add("hidden");
});

closeMobileNav.addEventListener("click", () => {
  mobileNav.classList.add("hidden");
  closeMobileNav.classList.add("hidden");
  openMobileNav.classList.remove("hidden");
});

// Dark mode toggle event listeners
toggle.addEventListener("click", () => setDarkMode(toggle.checked));
toggle2.addEventListener("click", () => setDarkMode(toggle2.checked));
