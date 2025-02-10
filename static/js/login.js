
const toggle = document.getElementById("AcceptConditions");
const html = document.querySelector("html");

/**
 * Updates dark mode state.
 * @param {boolean} isDark - Whether dark mode should be enabled.
 */
function setDarkMode(isDark) {
  if (isDark) {
    html.classList.add("dark");
    toggle.checked = true;
    localStorage.setItem("theme", "dark");
  } else {
    html.classList.remove("dark");
    toggle.checked = false;
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

// Dark mode toggle event listeners
toggle.addEventListener("click", () => setDarkMode(toggle.checked));
