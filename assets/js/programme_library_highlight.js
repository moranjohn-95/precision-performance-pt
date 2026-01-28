document.addEventListener("DOMContentLoaded", function () {
    if (!window.location.hash) {
        return;
    }

    var targetId = window.location.hash.slice(1);
    if (!targetId) {
        return;
    }

    var el = document.getElementById(targetId);
    if (!el) {
        return;
    }

    el.scrollIntoView({ behavior: "smooth", block: "start" });
    el.classList.add("is-highlight");

    setTimeout(function () {
        el.classList.remove("is-highlight");
    }, 2500);
});
