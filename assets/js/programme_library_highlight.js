/* jshint esversion: 11 */
/* Programme library anchor highlight for the client programme library page. */
document.addEventListener("DOMContentLoaded", function () {
    // Only run when the URL includes a hash target.
    if (!window.location.hash) {
        return;
    }

    // Use the hash as the element id to highlight.
    var targetId = window.location.hash.slice(1);
    if (!targetId) {
        return;
    }

    var el = document.getElementById(targetId);
    if (!el) {
        return;
    }

    // Scroll the target into view and add a temporary highlight.
    el.scrollIntoView({ behavior: "smooth", block: "start" });
    el.classList.add("is-highlight");

    // Remove the highlight after a short delay.
    setTimeout(function () {
        el.classList.remove("is-highlight");
    }, 2500);
});
