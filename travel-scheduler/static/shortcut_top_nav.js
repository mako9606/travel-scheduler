document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("a[href]").forEach((link) => {
        const href = link.getAttribute("href");
        if (!href || href.startsWith("#") || href.startsWith("javascript:")) {
            return;
        }
        link.setAttribute("target", "_top");
    });

    document.querySelectorAll("form").forEach((form) => {
        form.setAttribute("target", "_top");
    });
});