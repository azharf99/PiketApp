const openMobileNav = document.getElementById("openMobileNav");
const mobileNav = document.getElementById("mobileNav");
const closeMobileNav = document.getElementById("closeMobileNav");
const toggle = document.getElementById("AcceptConditions");
const toggle2 = document.getElementById("AcceptConditions2");
const html = document.querySelector("html");

const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)').matches;

if (prefersDarkScheme) {
  toggle.checked = true;
  toggle2.checked = true;
  html.classList.add("dark")
} else {
    toggle.checked = false;
    toggle2.checked = false;
    html.classList.remove("dark")
}

openMobileNav.addEventListener('click', (e)=> {
  mobileNav.classList.remove('hidden');
  closeMobileNav.classList.remove('hidden');
  openMobileNav.classList.add('hidden');
});
closeMobileNav.addEventListener('click', ()=> {
  mobileNav.classList.add('hidden');
  closeMobileNav.classList.add('hidden');
  openMobileNav.classList.remove('hidden');

});
toggle.addEventListener('click', () => toggle.checked ? html.classList.add("dark") : html.classList.remove("dark"));
toggle2.addEventListener('click', () => toggle2.checked ? html.classList.add("dark") : html.classList.remove("dark"));


