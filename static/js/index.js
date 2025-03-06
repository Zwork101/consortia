const wicsButton = document.querySelector(".wics .wicscomsbutton");
const comsButton = document.querySelector(".coms .wicscomsbutton");

wicsButton.addEventListener("mouseenter", function () {
    wicsButton.style.filter = "brightness(80%)";
    wicsButton.style.border = "2px solid #7D55C7";
    wicsButton.style.outline = "none"
    wicsButton.style.color = "#7D55C7";
});

wicsButton.addEventListener("mouseleave", function () {
    wicsButton.style.filter = "brightness(100%)";
    wicsButton.style.border = "";
    wicsButton.style.color = "";
});

wicsButton.addEventListener("click", function () {
    window.location.href = "/wics-profile"; // need proper page link
});

comsButton.addEventListener("mouseenter", function () {
    comsButton.style.filter = "brightness(80%)";
    comsButton.style.border = "2px solid #009CBD";
    comsButton.style.outline = "none"
    comsButton.style.color = "#009CBD";
});

comsButton.addEventListener("mouseleave", function () {
    comsButton.style.filter = "brightness(100%)";
    comsButton.style.border = "";
    comsButton.style.color = "";
});

comsButton.addEventListener("click", function () {
    window.location.href = "/coms-profile"; // need proper page link
});