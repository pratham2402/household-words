(() => {
  const search = document.querySelector("#search");
  const cards = [...document.querySelectorAll("[data-search]")];
  const count = document.querySelector("#search-count");

  if (search && count) {
    const total = cards.length;
    const update = () => {
      const query = search.value.trim().toLowerCase();
      let visible = 0;
      for (const card of cards) {
        const match = !query || card.dataset.search.includes(query);
        card.hidden = !match;
        if (match) visible += 1;
      }
      if (!query) {
        count.textContent = `${total} ${total === 1 ? "entry" : "entries"}`;
      } else if (visible === 0) {
        count.textContent = "No matches";
      } else {
        count.textContent = `${visible} of ${total}`;
      }
    };
    search.addEventListener("input", update);
    update();
  }

  for (const form of document.querySelectorAll("form[data-loading]")) {
    form.addEventListener("submit", () => {
      const button = form.querySelector("button[type='submit']");
      if (!button || button.disabled) return;
      button.disabled = true;
      button.dataset.original = button.textContent;
      button.textContent = form.dataset.loading || "Working…";
      form.setAttribute("aria-busy", "true");
    });
  }
})();
