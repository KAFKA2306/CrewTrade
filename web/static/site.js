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

(() => {
  const release = "kafka-signal-v1.0.0";
  document.documentElement.dataset.kafkaSignal = release;
  const style = document.createElement("style");
  style.textContent = `:root{--ks-canvas:#FBFAF7;--ks-surface:#FFF;--ks-subtle:#F4F2EC;--ks-ink:#243653;--ks-muted:#56657A;--ks-border:#C9D0DA;--ks-primary:#4D72A8;--ks-primary-soft:#DCE8F7;--ks-focus:#174D8B}.site-header,.hero-note,.catalogue-controls,.case-table-shell,.case-card,.process-step,.notice{border-color:var(--ks-border)!important;border-radius:.5rem!important;box-shadow:0 1px 2px rgb(36 54 83/.08)!important}.brand-mark,.category-pill,.status-pill,.view-button,.clear-button{border-radius:.25rem!important}.research-toc,.recent-reading{margin:1rem 0;padding:1rem;border:1px solid var(--ks-border);border-radius:.5rem;background:var(--ks-surface)}.research-toc h2,.recent-reading h2{margin:0 0 .5rem;font-size:1.1rem}.research-toc ol,.recent-reading ol{display:flex;gap:.5rem;flex-wrap:wrap;margin:0;padding:0;list-style:none}.research-toc a,.recent-reading a{display:inline-flex;min-height:44px;align-items:center;padding:.45rem .65rem;border:1px solid var(--ks-border);border-radius:.25rem;text-decoration:none;font-weight:800}.change-label{display:block;margin-top:.25rem;color:var(--ks-primary);font-size:.875rem;font-weight:800}:where(a,button,input,select,summary):focus-visible{outline:none!important;box-shadow:0 0 0 3px var(--ks-canvas),0 0 0 6px var(--ks-focus)!important}@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}`;
  document.head.append(style);
  const catalogue = document.querySelector("#research-catalogue");
  const links = [...document.querySelectorAll("[data-case-row] .table-title")];
  if (catalogue && links.length) {
    const toc = document.createElement("nav");
    toc.className = "research-toc";
    toc.setAttribute("aria-label", "調査テーマ目次");
    const items = links.map((link, index) => {
      const row = link.closest("[data-case-row]");
      const id = `research-${row?.dataset.caseSlug || index}`;
      if (row) row.id = id;
      return `<li><a href="#${id}">${link.querySelector("strong")?.textContent || link.textContent}</a></li>`;
    }).join("");
    toc.innerHTML = `<h2>調査テーマ目次</h2><ol>${items}</ol>`;
    catalogue.insertBefore(toc, catalogue.querySelector(".catalogue-controls"));
  }
  document.querySelectorAll(".cell-secondary").forEach((node) => {
    if (node.textContent?.trim() && node.closest("td")?.querySelector(".table-date")) {
      node.classList.add("change-label");
      node.textContent = `前回差分: ${node.textContent.trim()}`;
    }
  });
  const key = "crewtrade-reading-history";
  const current = location.pathname.match(/\/([^/]+)\/(\d{4}-\d{2}-\d{2})\.html$/);
  if (current) {
    const history = JSON.parse(localStorage.getItem(key) || "[]").filter((item) => item.href !== location.pathname);
    history.unshift({ href: location.pathname, title: document.querySelector("h1")?.textContent?.trim() || document.title, date: current[2] });
    localStorage.setItem(key, JSON.stringify(history.slice(0, 8)));
  }
  if (catalogue) {
    const history = JSON.parse(localStorage.getItem(key) || "[]");
    if (history.length) {
      const panel = document.createElement("section");
      panel.className = "recent-reading";
      panel.innerHTML = `<h2>最近読んだレポート</h2><ol>${history.map((item) => `<li><a href="${item.href}">${item.title} · ${item.date}</a></li>`).join("")}</ol>`;
      catalogue.insertBefore(panel, catalogue.querySelector(".catalogue-controls"));
    }
  }
  const footer = document.querySelector(".site-footer .footer-inner");
  if (footer) footer.insertAdjacentHTML("beforeend", `<span>KAFKA SIGNAL ${release} · 6cceef70</span>`);
})();
