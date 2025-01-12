const avatar = document.getElementById("avatar");
const user_menu = document.getElementById("user_menu");
if (avatar) {
    avatar.addEventListener("click", () => {
        user_menu.classList.toggle("hidden")
        console.log("Haii")
    })

}
const avatar2 = document.getElementById("avatar2");
const user_menu2 = document.getElementById("user_menu2");
if (avatar2) {
    avatar2.addEventListener("click", () => {
        user_menu2.classList.toggle("hidden")
        console.log("Haii")
    })
}