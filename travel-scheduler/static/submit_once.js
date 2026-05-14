document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll('form[data-submit-once="true"]');

    forms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            if (form.dataset.submitted === "true") {
                event.preventDefault();
                return;
            }

            form.dataset.submitted = "true";

            const submitButtons = form.querySelectorAll('button[type="submit"], input[type="submit"]');
            submitButtons.forEach(function (button) {
                button.disabled = true;
            });
        });
    });
});