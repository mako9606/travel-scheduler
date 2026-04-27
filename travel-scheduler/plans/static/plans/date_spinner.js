// plan_create・editの年月日スピナー 

document.addEventListener("DOMContentLoaded", function () {
    const DEFAULT_YEAR_MIN = new Date().getFullYear() - 10;
    const YEAR_MAX = new Date().getFullYear() + 60;

    function getInput(prefix, field) {
        return document.querySelector(`input[name="${prefix}_${field}"]`);
    }

    function getYearMin(prefix) {
        const yearInput = getInput(prefix, "year");
        const yearMin = yearInput ? parseInt(yearInput.dataset.yearMin, 10) : NaN;

        if (Number.isNaN(yearMin)) {
            return DEFAULT_YEAR_MIN;
        }

        return yearMin;
    }

    function getDisplay(prefix, field) {
        return document.querySelector(`.spinner-value[data-prefix="${prefix}"][data-field="${field}"]`);
    }

    function getGroup(prefix, field) {
        return document.querySelector(`.date-spinner-group[data-prefix="${prefix}"][data-field="${field}"]`);
    }

    function getDaysInMonth(year, month) {
        return new Date(year, month, 0).getDate();
    }

    function clampDay(prefix) {
        const year = parseInt(getInput(prefix, "year").value, 10);
        const month = parseInt(getInput(prefix, "month").value, 10);
        const dayInput = getInput(prefix, "day");

        if (!year || !month) {
            dayInput.value = "";
            return;
        }

        const maxDay = getDaysInMonth(year, month);
        const currentDay = parseInt(dayInput.value, 10);

        if (!currentDay) {
            return;
        }

        if (currentDay > maxDay) {
            dayInput.value = String(maxDay);
        }

        if (currentDay < 1) {
            dayInput.value = "1";
        }
    }

    function render(prefix) {
        const yearInput = getInput(prefix, "year");
        const monthInput = getInput(prefix, "month");
        const dayInput = getInput(prefix, "day");

        const year = yearInput.value;
        const month = monthInput.value;
        const day = dayInput.value;

        getDisplay(prefix, "year").textContent = year || "年";
        getDisplay(prefix, "month").textContent = month || "月";
        getDisplay(prefix, "day").textContent = day || "日";

        const dayGroup = getGroup(prefix, "day");
        if (dayGroup) {
            if (year && month) {
                dayGroup.classList.remove("is-disabled");
            } else {
                dayGroup.classList.add("is-disabled");
            }
        }
    }

    function step(prefix, field, direction) {
        const input = getInput(prefix, field);
        let value = input.value ? parseInt(input.value, 10) : null;

        if (field === "year") {
            const yearMin = getYearMin(prefix);

            if (value === null) {
                value = yearMin;
            } else {
                value += direction;
                if (value < yearMin) value = yearMin;
                if (value > YEAR_MAX) value = YEAR_MAX;
            }

            input.value = String(value);
            clampDay(prefix);
        }

        if (field === "month") {
            if (value === null) {
                value = direction > 0 ? 1 : 12;
            } else {
                value += direction;
                if (value < 1) value = 12;
                if (value > 12) value = 1;
            }
            input.value = String(value);
            clampDay(prefix);
        }

        if (field === "day") {
            const year = parseInt(getInput(prefix, "year").value, 10);
            const month = parseInt(getInput(prefix, "month").value, 10);

            if (!year || !month) {
                return;
            }

            const maxDay = getDaysInMonth(year, month);

            if (value === null) {
                value = direction > 0 ? 1 : maxDay;
            } else {
                value += direction;
                if (value < 1) value = maxDay;
                if (value > maxDay) value = 1;
            }

            input.value = String(value);
        }

        render(prefix);
    }

    document.querySelectorAll(".spinner-btn").forEach(function (btn) {
        btn.addEventListener("click", function () {
            const prefix = btn.dataset.prefix;
            const field = btn.dataset.field;
            const direction = btn.classList.contains("spinner-up") ? 1 : -1;
            step(prefix, field, direction);
        });
    });

    ["start", "end"].forEach(function (prefix) {
        render(prefix);
    });
});