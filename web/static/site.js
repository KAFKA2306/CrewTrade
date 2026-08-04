(() => {
  const search = document.querySelector("[data-case-search]");
  const purposeFilter = document.querySelector("[data-purpose-filter]");
  const freshnessFilter = document.querySelector("[data-freshness-filter]");
  const caseItems = [...document.querySelectorAll("[data-case-item]")];
  const count = document.querySelector("[data-result-count]");
  const summary = document.querySelector("[data-filter-summary]");
  const emptyState = document.querySelector("[data-empty-state]");
  const clearButtons = [
    document.querySelector("[data-clear-filters]"),
    document.querySelector("[data-empty-clear]"),
  ].filter(Boolean);
  const viewButtons = [...document.querySelectorAll("[data-view-button]")];
  const views = [...document.querySelectorAll("[data-case-view]")];
  const purposeSections = [...document.querySelectorAll("[data-purpose-section]")];

  const caseGroups = new Map();
  caseItems.forEach((item) => {
    const slug = item.dataset.caseSlug;
    if (!slug) return;
    if (!caseGroups.has(slug)) caseGroups.set(slug, []);
    caseGroups.get(slug).push(item);
  });

  const validView = (value) =>
    views.some((view) => view.dataset.caseView === value) ? value : "table";

  const readState = () => {
    const params = new URLSearchParams(window.location.search);
    return {
      q: params.get("q") || "",
      purpose: params.get("purpose") || "all",
      freshness: params.get("freshness") || "all",
      view: validView(params.get("view") || "table"),
    };
  };

  const currentState = () => ({
    q: search?.value.trim() || "",
    purpose: purposeFilter?.value || "all",
    freshness: freshnessFilter?.value || "all",
    view:
      viewButtons.find((button) => button.getAttribute("aria-pressed") === "true")
        ?.dataset.viewButton || "table",
  });

  const writeState = (state, { push = false } = {}) => {
    const params = new URLSearchParams();
    if (state.q) params.set("q", state.q);
    if (state.purpose !== "all") params.set("purpose", state.purpose);
    if (state.freshness !== "all") params.set("freshness", state.freshness);
    if (state.view !== "table") params.set("view", state.view);
    const next = `${window.location.pathname}${params.size ? `?${params}` : ""}${window.location.hash}`;
    window.history[push ? "pushState" : "replaceState"](state, "", next);
  };

  const setView = (viewName, { persist = true } = {}) => {
    if (!views.length) return;
    const selected = validView(viewName);
    views.forEach((view) => {
      view.hidden = view.dataset.caseView !== selected;
    });
    viewButtons.forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.viewButton === selected));
    });
    if (persist) writeState({ ...currentState(), view: selected });
  };

  const updatePurposeSections = () => {
    purposeSections.forEach((section) => {
      const visibleCards = [...section.querySelectorAll("[data-case-card]")].filter(
        (card) => !card.hidden,
      );
      section.hidden = visibleCards.length === 0;
      const sectionCount = section.querySelector("[data-purpose-count]");
      if (sectionCount) sectionCount.textContent = `${visibleCards.length}件`;
    });
  };

  const filterCases = ({ persist = true } = {}) => {
    if (!caseGroups.size) return;
    const state = currentState();
    const query = state.q.toLocaleLowerCase("ja");
    let visible = 0;

    caseGroups.forEach((items) => {
      const source = items[0];
      const searchable = source?.dataset.search || "";
      const purpose = source?.dataset.purpose || "";
      const freshness = source?.dataset.freshness || "";
      const matchQuery = !query || searchable.includes(query);
      const matchPurpose = state.purpose === "all" || purpose === state.purpose;
      const matchFreshness = state.freshness === "all" || freshness === state.freshness;
      const match = matchQuery && matchPurpose && matchFreshness;
      items.forEach((item) => {
        item.hidden = !match;
      });
      visible += Number(match);
    });

    if (count) count.textContent = `${visible}件`;
    if (emptyState) emptyState.hidden = visible !== 0;
    updatePurposeSections();

    const parts = [];
    if (state.q) parts.push(`検索「${state.q}」`);
    if (state.purpose !== "all") parts.push(state.purpose);
    if (state.freshness === "current") parts.push("最新基準日");
    if (state.freshness === "archive") parts.push("過去基準日");
    if (summary) summary.textContent = parts.length ? `${parts.join("・")}で絞り込み` : "全テーマを表示中";
    if (persist) writeState(state);
  };

  const applyState = (state, { persist = false } = {}) => {
    if (search) search.value = state.q;
    if (purposeFilter) {
      purposeFilter.value = [...purposeFilter.options].some((option) => option.value === state.purpose)
        ? state.purpose
        : "all";
    }
    if (freshnessFilter) {
      freshnessFilter.value = [...freshnessFilter.options].some(
        (option) => option.value === state.freshness,
      )
        ? state.freshness
        : "all";
    }
    setView(state.view, { persist: false });
    filterCases({ persist });
  };

  const clearFilters = () => {
    applyState({ q: "", purpose: "all", freshness: "all", view: currentState().view });
    search?.focus();
  };

  search?.addEventListener("input", () => filterCases());
  purposeFilter?.addEventListener("change", () => filterCases());
  freshnessFilter?.addEventListener("change", () => filterCases());
  clearButtons.forEach((button) => button.addEventListener("click", clearFilters));

  viewButtons.forEach((button) => {
    button.addEventListener("click", () => {
      setView(button.dataset.viewButton || "table");
      filterCases();
    });
  });

  window.addEventListener("popstate", () => applyState(readState()));
  applyState(readState(), { persist: true });

  const reportSelect = document.querySelector("[data-report-select]");
  if (reportSelect) {
    reportSelect.addEventListener("change", (event) => {
      window.location.href = event.target.value;
    });
  }
})();
