// Program details modal
(function () {
  const modal = document.querySelector("[data-program-modal]");
  const overlay = document.querySelector("[data-program-modal-overlay]");
  const closeBtn = document.querySelector("[data-program-modal-close]");
  const triggers = document.querySelectorAll("[data-program-trigger]");

  // Elements inside the modal
  const visual = modal?.querySelector("[data-program-modal-visual]");
  const titleEl = modal?.querySelector("#program-modal-title");
  const introEl = modal?.querySelector(".program-modal-intro");
  const listEl = modal?.querySelector(".program-modal-list");

  if (
    !modal ||
    !overlay ||
    !closeBtn ||
    !visual ||
    !titleEl ||
    !introEl ||
    !listEl ||
    triggers.length === 0
  ) {
    return;
  }

  // Content for each coaching option
  const programDetails = {
    personal: {
      title: "1:1 Personal Training",
      intro:
        "Work one-to-one with one of our Precision Performance coaches and enjoy fully tailored sessions built around your goals. Here the full attention is on you and helping you move closer to ypur goals",
      bullets: [
        "Comprehensive in person assessments looking at movement, strength and mobility.",
        "Access to our client portal and dashboard to analyze body metrics and performance",
        "Real-time accoutabilty/coaching on performance and technique",
        "Progress tracking and session reviews to keep you moving forward.",
        "Training plans refined over time to match progress, recovery and performance."
      ],
      visualClass: "program-card--personal"
    },
    smallGroup: {
      title: "Small Group Coaching",
      intro:
        "Train in a focused group of 4–7 people for extra motivation accountability and fun!. Perfect for those who enjoy a high-energy atmosphere with like-minded people.",
      bullets: [
        "Coach-led sessions with a strong emphasis on form and safety.",
        "Small group atmosphere that keeps sessions motivating without losing personal guidance.",
        "Well-structured sessions designed to build strength and confidence over time.",
        "Consistent accountability from both the coach and the group."
      ],
      visualClass: "program-card--small-group"
    },
    largeGroup: {
      title: "Larger Group Classes",
      intro:
        "High-energy classes designed to deliver a fun, intense and effective workout. Perfect for those who thrive in a motivating group environment",
      bullets: [
        "Fast-paced strength and conditioning in a motivating environment.",
        "Coaching cues to help you get the most from every rep.",
        "Great option if you enjoy training with others and pushing the pace.",
        "Scalable exercises so all fitness levels can train together."
      ],
      visualClass: "program-card--large-group"
    },
    online: {
      title: "Online Coaching",
      intro:
        "Remote coaching that fits around busy work and family schedules. Train when it suits you, with the support you need.",
      bullets: [
        "Structured training plan you can follow from home or your local gym.",
        "Access to our client portal and dashboard to analyze body metrics and performance",
        "Regular check-ins and form reviews to keep you on track.",
        "Accountability and support without needing to be in the gym in person."
      ],
      visualClass: "program-card--online"
    }
  };

 let currentVisualClass = null;
  let lastFocusedElement = null;

  function setContent(programId) {
    const data = programDetails[programId];
    if (!data) return;

    titleEl.textContent = data.title;
    introEl.textContent = data.intro;

    listEl.innerHTML = "";
    data.bullets.forEach((text) => {
      const li = document.createElement("li");
      li.textContent = text;
      listEl.appendChild(li);
    });

    if (currentVisualClass) {
      visual.classList.remove(currentVisualClass);
    }
    if (data.visualClass) {
      visual.classList.add(data.visualClass);
      currentVisualClass = data.visualClass;
    }
  }

  function openModal(programId) {
    setContent(programId);

    // Remember where focus was, then move it to the close button
    lastFocusedElement = document.activeElement;

    overlay.classList.add("is-open");
    modal.classList.add("is-open");

    closeBtn.focus();
  }

  function closeModal() {
    overlay.classList.remove("is-open");
    modal.classList.remove("is-open");

    // Return focus to the thing that opened the modal, if possible
    if (lastFocusedElement && typeof lastFocusedElement.focus === "function") {
      lastFocusedElement.focus();
    }
  }

  triggers.forEach((btn) => {
    btn.addEventListener("click", (event) => {
      event.preventDefault();
      const programId = btn.getAttribute("data-program-trigger");
      if (!programId) return;
      openModal(programId);
    });
  });

  closeBtn.addEventListener("click", closeModal);
  overlay.addEventListener("click", closeModal);

  // Allow closing with the Escape key
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && modal.classList.contains("is-open")) {
      closeModal();
    }
  });
})();