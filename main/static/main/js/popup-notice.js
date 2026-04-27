(function () {
  var DISMISS_KEY = "sbgh_free_healing_popup_dismissed";

  function getDismissed() {
    try {
      return localStorage.getItem(DISMISS_KEY) === "1";
    } catch (error) {
      return false;
    }
  }

  function setDismissed() {
    try {
      localStorage.setItem(DISMISS_KEY, "1");
    } catch (error) {
      // Ignore storage errors silently.
    }
  }

  function createPopup() {
    var overlay = document.createElement("div");
    overlay.className = "site-popup-overlay";
    overlay.setAttribute("aria-hidden", "true");

    var popup = document.createElement("div");
    popup.className = "site-popup";
    popup.setAttribute("role", "dialog");
    popup.setAttribute("aria-modal", "true");
    popup.setAttribute("aria-label", "Free healing sessions notice");
    popup.innerHTML =
      '<div class="site-popup-inner">' +
      '<button type="button" class="site-popup-close" aria-label="Close notification">&times;</button>' +
      '<h3 class="site-popup-title">Community Announcement</h3>' +
      '<p class="site-popup-message">Free healing sessions every Friday, 5 PM to 6 PM</p>' +
      "</div>";

    function closePopup() {
      overlay.classList.remove("is-visible");
      popup.classList.remove("is-visible");
      setTimeout(function () {
        overlay.remove();
        popup.remove();
      }, 220);
      setDismissed();
    }

    overlay.addEventListener("click", closePopup);
    var closeButton = popup.querySelector(".site-popup-close");
    if (closeButton) {
      closeButton.addEventListener("click", closePopup);
    }

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && popup.classList.contains("is-visible")) {
        closePopup();
      }
    });

    document.body.appendChild(overlay);
    document.body.appendChild(popup);

    requestAnimationFrame(function () {
      overlay.classList.add("is-visible");
      popup.classList.add("is-visible");
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (getDismissed()) {
      return;
    }
    createPopup();
  });
})();
