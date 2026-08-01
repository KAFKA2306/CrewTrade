(() => {
  const search = document.querySelector("[data-case-search]");
  const caseItems = [...document.querySelectorAll("[data-case-item]")];
  const count = document.querySelector("[data-result-count]");
  const viewButtons = [...document.querySelectorAll("[data-view-button]")];
  const views = [...document.querySelectorAll("[data-case-view]")];

  const caseGroups = new Map();
  caseItems.forEach((item) => {
    const slug = item.dataset.caseSlug;
    if (!slug) return;
    if (!caseGroups.has(slug)) caseGroups.set(slug, []);
    caseGroups.get(slug).push(item);
  });

  const filterCases = () => {
    if (!caseGroups.size) return;
    const query = search?.value.trim().toLocaleLowerCase("ja") ?? "";
    let visible = 0;

    caseGroups.forEach((items) => {
      const searchable = items[0]?.dataset.search ?? "";
      const match = !query || searchable.includes(query);
      items.forEach((item) => {
        item.hidden = !match;
      });
      visible += Number(match);
    });

    if (count) count.textContent = `${visible}件`;
  };

  const setView = (viewName) => {
    if (!views.length) return;
    const selected = views.some((view) => view.dataset.caseView === viewName)
      ? viewName
      : "table";

    views.forEach((view) => {
      view.hidden = view.dataset.caseView !== selected;
    });
    viewButtons.forEach((button) => {
      button.setAttribute(
        "aria-pressed",
        String(button.dataset.viewButton === selected),
      );
    });

    try {
      window.localStorage.setItem("crewtrade-case-view", selected);
    } catch {
      // Storage can be disabled; the table remains the deterministic default.
    }
  };

  if (search && caseGroups.size) {
    search.addEventListener("input", filterCases);
  }

  if (viewButtons.length && views.length) {
    let initialView = "table";
    try {
      initialView = window.localStorage.getItem("crewtrade-case-view") || "table";
    } catch {
      initialView = "table";
    }

    viewButtons.forEach((button) => {
      button.addEventListener("click", () => {
        setView(button.dataset.viewButton || "table");
      });
    });
    setView(initialView);
  }

  filterCases();

  const reportSelect = document.querySelector("[data-report-select]");
  if (reportSelect) {
    reportSelect.addEventListener("change", (event) => {
      window.location.href = event.target.value;
    });
  }
})();
