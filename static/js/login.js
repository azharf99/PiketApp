
const toggle = document.getElementById("AcceptConditions");
const html = document.querySelector("html");

const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)').matches;

if (prefersDarkScheme) {
  toggle.checked = true;
  html.classList.add("dark")
} else {
    toggle.checked = false;
    html.classList.remove("dark")
}

toggle.addEventListener('click', () => toggle.checked ? html.classList.add("dark") : html.classList.remove("dark"));
