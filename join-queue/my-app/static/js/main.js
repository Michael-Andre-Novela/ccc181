// Prevent double submissions on the join form
const joinForm = document.getElementById("join-form");
if (joinForm) {
  joinForm.addEventListener("submit", () => {
    const button = joinForm.querySelector("button[type=submit]");
    if (button) {
      button.disabled = true;
      button.textContent = "Getting your ticket…";
    }
  });
}

// Confirm destructive actions before submitting
document.querySelectorAll("form[data-confirm]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    if (!confirm(form.dataset.confirm)) {
      event.preventDefault();
    }
  });
});