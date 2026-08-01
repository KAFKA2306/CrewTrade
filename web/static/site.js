(() => {
  const search = document.querySelector("[data-case-search]");
  const cards = [...document.querySelectorAll("[data-case-card]")];
  const count = document.querySelector("[data-result-count]");

  if (search && cards.length) {
    const filter = () => {
      const query = search.value.trim().toLocaleLowerCase("ja");
      let visible = 0;
      cards.forEach((card) => {
        const match = !query || card.dataset.search.includes(query);
        card.hidden = !match;
        visible += Number(match);
      });
      if (count) count.textContent = `${visible}件`;
    };
    search.addEventListener("input", filter);
    filter();
  }

  const reportSelect = document.querySelector("[data-report-select]");
  if (reportSelect) {
    reportSelect.addEventListener("change", (event) => {
      window.location.href = event.target.value;
    });
  }
})();
