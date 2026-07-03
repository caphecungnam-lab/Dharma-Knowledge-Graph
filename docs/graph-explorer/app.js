(function () {
  const graphScopes = window.DHARMA_GRAPH_SCOPES || {
    default_mode: "giac_khang",
    modes: {
      giac_khang: window.DHARMA_GRAPH,
    },
  };
  let graph = graphScopes.modes[graphScopes.default_mode] || window.DHARMA_GRAPH;

  if (!graph) {
    throw new Error("Graph data is missing. Run scripts/build_graph.py first.");
  }

  const canvas = document.getElementById("graphCanvas");
  const ctx = canvas.getContext("2d");
  const statsEl = document.getElementById("stats");
  const searchInput = document.getElementById("searchInput");
  const dataModeToggle = document.getElementById("dataModeToggle");
  const languageFilter = document.getElementById("languageFilter");
  const typeFilter = document.getElementById("typeFilter");
  const relationshipFilter = document.getElementById("relationshipFilter");
  const resetButton = document.getElementById("resetButton");
  const languageToggle = document.getElementById("languageToggle");
  const detailTitle = document.getElementById("detailTitle");
  const detailType = document.getElementById("detailType");
  const detailDescription = document.getElementById("detailDescription");
  const propertyList = document.getElementById("propertyList");
  const relationshipList = document.getElementById("relationshipList");

  const colors = {
    Concept: "#1f6f52",
    Person: "#9a496b",
    School: "#c47a24",
    Text: "#2f6f9f",
    Place: "#6d5b9a",
    Term: "#5d6b2f",
    Citation: "#6b6258",
    Corpus: "#174f3c",
    Source: "#6b6258",
    Document: "#2f6f9f",
    Evidence: "#b45b2d",
    Work: "#5d6b2f",
  };

  const badgeColors = {
    corpus: "#174f3c",
    pilot: "#6d5b9a",
    seed: "#6b6258",
    processed: "#2f6f9f",
    reviewed: "#b45b2d",
    curated: "#1f6f52",
  };

  const badgeDisplayLabels = {
    corpus: "COR",
    pilot: "PILOT",
    seed: "SEED",
    processed: "PROC",
    reviewed: "REV",
    curated: "CUR",
  };

  const modeTranslationKeys = {
    giac_khang: "giacKhang",
    seeds_only: "seeds",
    all_data: "allData",
  };

  const languageOptions = ["All", "vi", "en", "pali", "sanskrit"];

  const languageKey = "dkg_language";
  const translations = {
    en: {
      brand: "Dharma Knowledge Graph",
      explorerTitle: "Graph Explorer v0.1",
      search: "Search",
      searchPlaceholder: "Concept, text, school...",
      dataScope: "Data",
      giacKhang: "Giác Khang",
      seeds: "Seeds",
      allData: "All",
      languageFilter: "Language",
      type: "Type",
      relationship: "Relationship",
      reset: "Reset",
      selectedNode: "Selected Node",
      selectNode: "Select a node",
      noSelection: "No selection",
      noSelectionDescription: "Click a node in the graph to inspect its metadata and relationships.",
      noDescription: "No description yet.",
      properties: "Properties",
      relationshipsHeader: "Relationships",
      nodes: "Nodes",
      relationshipsStat: "Relationships",
      concepts: "Concepts",
      seedFiles: "Seed files",
      all: "All",
      switchLanguage: "Switch language",
      to: "to",
      from: "from",
      noRelationshipsYet: "No relationships yet.",
      sourceBadge: "Source badge",
    },
    vi: {
      brand: "Dharma Knowledge Graph",
      explorerTitle: "Graph Explorer v0.1",
      search: "Tìm kiếm",
      searchPlaceholder: "Khái niệm, văn bản, trường phái...",
      dataScope: "Dữ liệu",
      giacKhang: "Giác Khang",
      seeds: "Seeds",
      allData: "Tất cả",
      languageFilter: "Ngôn ngữ",
      type: "Loại",
      relationship: "Quan hệ",
      reset: "Đặt lại",
      selectedNode: "Nút đang chọn",
      selectNode: "Chọn một nút",
      noSelection: "Chưa chọn",
      noSelectionDescription: "Bấm vào một nút trong đồ thị để xem metadata và các quan hệ.",
      noDescription: "Chưa có mô tả.",
      properties: "Thuộc tính",
      relationshipsHeader: "Quan hệ",
      nodes: "Nút",
      relationshipsStat: "Quan hệ",
      concepts: "Khái niệm",
      seedFiles: "Tệp nguồn",
      all: "Tất cả",
      switchLanguage: "Đổi ngôn ngữ",
      to: "đến",
      from: "từ",
      noRelationshipsYet: "Chưa có quan hệ.",
      sourceBadge: "Nhãn nguồn",
    },
  };
  let language = localStorage.getItem(languageKey) === "vi" ? "vi" : "en";

  const state = {
    selectedId: graph.nodes[0] ? graph.nodes[0].id : null,
    hoveredId: null,
    draggingId: null,
    dataMode: graphScopes.default_mode || "giac_khang",
    languageFilter: "All",
    search: "",
    type: "All",
    relationship: "All",
    width: 0,
    height: 0,
  };

  let nodeById = new Map();
  let adjacency = new Map();
  let layoutNodes = [];
  let layoutById = new Map();

  function t(key) {
    return translations[language][key] || translations.en[key] || key;
  }

  function applyLanguage() {
    document.documentElement.lang = language;
    document.querySelectorAll("[data-i18n]").forEach((element) => {
      element.textContent = t(element.dataset.i18n);
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
      element.setAttribute("placeholder", t(element.dataset.i18nPlaceholder));
    });

    if (languageToggle) {
      languageToggle.textContent = language === "vi" ? "EN" : "VI";
      languageToggle.setAttribute("aria-label", t("switchLanguage"));
    }

    populateStats();
    populateFilters();
    renderDetails();
  }

  function setGraph(nextGraph) {
    graph = nextGraph;
    state.selectedId = graph.nodes[0] ? graph.nodes[0].id : null;
    state.hoveredId = null;
    state.draggingId = null;

    nodeById = new Map(graph.nodes.map((node) => [node.id, node]));
    adjacency = new Map(graph.nodes.map((node) => [node.id, []]));
    graph.relationships.forEach((relationship) => {
      adjacency.get(relationship.source)?.push({ direction: "out", ...relationship });
      adjacency.get(relationship.target)?.push({ direction: "in", ...relationship });
    });

    layoutNodes = graph.nodes.map((node, index) => {
      const angle = (index / Math.max(graph.nodes.length, 1)) * Math.PI * 2;
      const ring = 170 + (index % 4) * 36;
      return {
        ...node,
        x: Math.cos(angle) * ring,
        y: Math.sin(angle) * ring,
        vx: 0,
        vy: 0,
        radius: node.type === "Concept" ? 8 : 10,
      };
    });
    layoutById = new Map(layoutNodes.map((node) => [node.id, node]));
  }

  function populateStats() {
    statsEl.innerHTML = [
      [t("nodes"), graph.summary.node_count],
      [t("relationshipsStat"), graph.summary.relationship_count],
      [t("concepts"), graph.summary.node_type_counts.Concept || 0],
      [t("seedFiles"), graph.metadata.source_files.length],
    ]
      .map(([label, value]) => `<div class="stat"><strong>${value}</strong><span>${label}</span></div>`)
      .join("");
  }

  function populateDataModeToggle() {
    if (!dataModeToggle) return;

    dataModeToggle.querySelectorAll("button").forEach((button) => {
      const isActive = button.dataset.mode === state.dataMode;
      button.classList.toggle("active", isActive);
      button.setAttribute("aria-pressed", String(isActive));
      const translationKey = modeTranslationKeys[button.dataset.mode];
      button.textContent = translationKey ? t(translationKey) : button.dataset.mode;
    });
  }

  function populateFilters() {
    const nodeTypes = ["All", ...Object.keys(graph.summary.node_type_counts).sort()];
    const relationshipTypes = ["All", ...Object.keys(graph.summary.relationship_type_counts).sort()];

    languageFilter.innerHTML = languageOptions
      .map((option) => {
        const label = option === "All" ? t("all") : option;
        return `<option value="${option}">${label}</option>`;
      })
      .join("");
    typeFilter.innerHTML = nodeTypes
      .map((type) => `<option value="${type}">${type === "All" ? t("all") : type}</option>`)
      .join("");
    relationshipFilter.innerHTML = relationshipTypes
      .map((type) => `<option value="${type}">${type === "All" ? t("all") : type}</option>`)
      .join("");
    languageFilter.value = state.languageFilter;
    typeFilter.value = state.type;
    relationshipFilter.value = state.relationship;
    populateDataModeToggle();
  }

  function normalizeLanguage(value) {
    if (!value) return "";
    const normalized = String(value).trim().toLowerCase();
    if (normalized === "vietnamese") return "vi";
    if (normalized === "english") return "en";
    return normalized;
  }

  function filteredNodeIds() {
    const search = state.search.trim().toLowerCase();
    const ids = new Set();

    graph.nodes.forEach((node) => {
      const matchesType = state.type === "All" || node.type === state.type;
      const matchesLanguage =
        state.languageFilter === "All" ||
        normalizeLanguage(node.language) === state.languageFilter;
      const searchable = [
        node.id,
        node.name,
        node.description,
        node.evidence_text,
        node.reviewed_evidence_text,
        node.original_evidence_text,
        node.pali,
        node.sanskrit,
        node.category,
        node.tradition,
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      const matchesSearch = !search || searchable.includes(search);

      if (matchesType && matchesLanguage && matchesSearch) {
        ids.add(node.id);
      }
    });

    if (state.relationship === "All") {
      return ids;
    }

    const relatedIds = new Set();
    graph.relationships.forEach((relationship) => {
      if (relationship.type !== state.relationship) {
        return;
      }
      if (ids.has(relationship.source) || ids.has(relationship.target)) {
        relatedIds.add(relationship.source);
        relatedIds.add(relationship.target);
      }
    });

    return relatedIds;
  }

  function visibleRelationships(visibleIds) {
    return graph.relationships.filter((relationship) => {
      const matchesType =
        state.relationship === "All" || relationship.type === state.relationship;
      return (
        matchesType &&
        visibleIds.has(relationship.source) &&
        visibleIds.has(relationship.target)
      );
    });
  }

  function resizeCanvas() {
    const rect = canvas.parentElement.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    state.width = Math.max(320, rect.width);
    state.height = Math.max(320, rect.height);
    canvas.width = Math.floor(state.width * dpr);
    canvas.height = Math.floor(state.height * dpr);
    canvas.style.width = `${state.width}px`;
    canvas.style.height = `${state.height}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function tick(visibleIds, relationships) {
    const visibleNodes = layoutNodes.filter((node) => visibleIds.has(node.id));
    const centerStrength = 0.006;
    const linkStrength = 0.015;
    const repelStrength = visibleNodes.length > 40 ? 1450 : 1120;

    visibleNodes.forEach((node) => {
      node.vx += (0 - node.x) * centerStrength;
      node.vy += (0 - node.y) * centerStrength;
    });

    relationships.forEach((relationship) => {
      const source = layoutById.get(relationship.source);
      const target = layoutById.get(relationship.target);
      if (!source || !target) return;

      const dx = target.x - source.x;
      const dy = target.y - source.y;
      const distance = Math.max(1, Math.hypot(dx, dy));
      const desired = visibleNodes.length > 40 ? 132 : 122;
      const force = (distance - desired) * linkStrength;
      const fx = (dx / distance) * force;
      const fy = (dy / distance) * force;

      source.vx += fx;
      source.vy += fy;
      target.vx -= fx;
      target.vy -= fy;
    });

    for (let i = 0; i < visibleNodes.length; i += 1) {
      for (let j = i + 1; j < visibleNodes.length; j += 1) {
        const a = visibleNodes[i];
        const b = visibleNodes[j];
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const distance = Math.max(8, Math.hypot(dx, dy));
        const force = repelStrength / (distance * distance);
        const fx = (dx / distance) * force;
        const fy = (dy / distance) * force;

        a.vx -= fx;
        a.vy -= fy;
        b.vx += fx;
        b.vy += fy;
      }
    }

    visibleNodes.forEach((node) => {
      if (state.draggingId === node.id) {
        node.vx = 0;
        node.vy = 0;
        return;
      }

      node.vx *= 0.86;
      node.vy *= 0.86;
      node.x += node.vx;
      node.y += node.vy;
    });
  }

  function toScreen(node) {
    return {
      x: state.width / 2 + node.x,
      y: state.height / 2 + node.y,
    };
  }

  function fromScreen(point) {
    return {
      x: point.x - state.width / 2,
      y: point.y - state.height / 2,
    };
  }

  function drawArrow(sourcePoint, targetPoint, color) {
    const angle = Math.atan2(targetPoint.y - sourcePoint.y, targetPoint.x - sourcePoint.x);
    const arrowLength = 8;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(targetPoint.x, targetPoint.y);
    ctx.lineTo(
      targetPoint.x - Math.cos(angle - Math.PI / 6) * arrowLength,
      targetPoint.y - Math.sin(angle - Math.PI / 6) * arrowLength,
    );
    ctx.lineTo(
      targetPoint.x - Math.cos(angle + Math.PI / 6) * arrowLength,
      targetPoint.y - Math.sin(angle + Math.PI / 6) * arrowLength,
    );
    ctx.closePath();
    ctx.fill();
  }

  function badgeLabel(node) {
    return node.source_badge || (node.type === "Corpus" ? "corpus" : "seed");
  }

  function truncateLabel(value, maxLength = 32) {
    const normalized = String(value || "").trim();
    if (normalized.length <= maxLength) {
      return normalized;
    }
    return `${normalized.slice(0, maxLength - 1)}…`;
  }

  function nodeFullLabel(node) {
    if (node.type === "Evidence" && node.evidence_text) {
      return String(node.evidence_text).trim();
    }
    return node.name || node.id;
  }

  function nodeCanvasLabel(node) {
    return truncateLabel(nodeFullLabel(node), 32);
  }

  function drawNodeBadge(point, node) {
    const badge = badgeLabel(node);
    const label = badgeDisplayLabels[badge] || badge.slice(0, 3).toUpperCase();
    const width = Math.max(20, ctx.measureText(label).width + 6);
    const height = 12;
    const x = point.x + node.radius - 1;
    const y = point.y - node.radius - 6;

    ctx.fillStyle = badgeColors[badge] || "#6b6258";
    ctx.beginPath();
    ctx.roundRect(x, y, width, height, 4);
    ctx.fill();
    ctx.fillStyle = "#ffffff";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(label, x + width / 2, y + height / 2 + 0.5);
  }

  function draw() {
    const visibleIds = filteredNodeIds();
    const labelFontSize = visibleIds.size > 40 ? 10 : visibleIds.size > 24 ? 11 : 12;
    const relationships = visibleRelationships(visibleIds);
    tick(visibleIds, relationships);

    ctx.clearRect(0, 0, state.width, state.height);
    ctx.lineWidth = 1.2;
    ctx.font = `${labelFontSize}px Inter, system-ui, sans-serif`;

    relationships.forEach((relationship) => {
      const source = layoutById.get(relationship.source);
      const target = layoutById.get(relationship.target);
      if (!source || !target) return;

      const start = toScreen(source);
      const end = toScreen(target);
      const dx = end.x - start.x;
      const dy = end.y - start.y;
      const distance = Math.max(1, Math.hypot(dx, dy));
      const targetRadius = target.radius + 4;
      const endTrimmed = {
        x: end.x - (dx / distance) * targetRadius,
        y: end.y - (dy / distance) * targetRadius,
      };

      const selected =
        state.selectedId === relationship.source ||
        state.selectedId === relationship.target;
      const stroke = selected ? "rgba(31, 111, 82, 0.64)" : "rgba(23, 32, 27, 0.18)";
      ctx.strokeStyle = stroke;
      ctx.beginPath();
      ctx.moveTo(start.x, start.y);
      ctx.lineTo(endTrimmed.x, endTrimmed.y);
      ctx.stroke();
      drawArrow(start, endTrimmed, stroke);
    });

    layoutNodes.forEach((node) => {
      if (!visibleIds.has(node.id)) return;

      const point = toScreen(node);
      const isSelected = state.selectedId === node.id;
      const isHovered = state.hoveredId === node.id;
      const fill = colors[node.type] || "#6b6258";

      ctx.beginPath();
      ctx.arc(point.x, point.y, node.radius + (isSelected ? 5 : isHovered ? 3 : 0), 0, Math.PI * 2);
      ctx.fillStyle = isSelected ? "rgba(31, 111, 82, 0.16)" : isHovered ? "rgba(196, 122, 36, 0.18)" : "rgba(255, 255, 255, 0.72)";
      ctx.fill();

      ctx.beginPath();
      ctx.arc(point.x, point.y, node.radius, 0, Math.PI * 2);
      ctx.fillStyle = fill;
      ctx.fill();
      ctx.strokeStyle = "#ffffff";
      ctx.lineWidth = 2;
      ctx.stroke();
      drawNodeBadge(point, node);

      const labelVisible = isSelected || isHovered || node.type !== "Concept";
      if (labelVisible) {
        ctx.fillStyle = "#17201b";
        ctx.textAlign = "center";
        ctx.textBaseline = "top";
        ctx.fillText(nodeCanvasLabel(node), point.x, point.y + node.radius + 8, 132);
      }
    });

    requestAnimationFrame(draw);
  }

  function pointerPosition(event) {
    const rect = canvas.getBoundingClientRect();
    return {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top,
    };
  }

  function findNodeAt(point) {
    const visibleIds = filteredNodeIds();
    let found = null;

    layoutNodes.forEach((node) => {
      if (!visibleIds.has(node.id)) return;
      const screen = toScreen(node);
      const distance = Math.hypot(point.x - screen.x, point.y - screen.y);
      if (distance <= node.radius + 8) {
        found = node;
      }
    });

    return found;
  }

  function renderDetails() {
    const node = nodeById.get(state.selectedId);

    if (!node) {
      detailTitle.textContent = t("selectNode");
      detailType.textContent = t("noSelection");
      detailDescription.textContent = t("noSelectionDescription");
      propertyList.innerHTML = "";
      relationshipList.innerHTML = "";
      return;
    }

    detailTitle.textContent = nodeFullLabel(node);
    detailType.innerHTML = `${escapeHtml(node.type)} <span class="badge-pill">${escapeHtml(badgeLabel(node))}</span>`;
    detailDescription.textContent = node.description || t("noDescription");

    const hiddenProperties = new Set(["id", "name", "type", "description"]);
    const properties = Object.entries(node).filter(([key, value]) => {
      return !hiddenProperties.has(key) && value !== null && value !== undefined && value !== "";
    });

    propertyList.innerHTML = [
      ["id", node.id],
      ...properties,
    ]
      .map(([key, value]) => {
        const label = key.replaceAll("_", " ");
        return `<div><dt>${escapeHtml(label)}</dt><dd>${escapeHtml(String(value))}</dd></div>`;
      })
      .join("");

    const relationships = adjacency.get(node.id) || [];
    relationshipList.innerHTML = relationships.length
      ? relationships
          .map((relationship) => {
            const otherId = relationship.direction === "out" ? relationship.target : relationship.source;
            const other = nodeById.get(otherId);
            const direction = relationship.direction === "out" ? t("to") : t("from");
            return `<li><span class="relationship-type">${escapeHtml(relationship.type)}</span>${direction} ${escapeHtml(other ? nodeFullLabel(other) : otherId)}</li>`;
          })
          .join("")
      : `<li>${t("noRelationshipsYet")}</li>`;
  }

  function escapeHtml(value) {
    return value
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  canvas.addEventListener("pointermove", (event) => {
    const point = pointerPosition(event);
    const node = findNodeAt(point);
    state.hoveredId = node ? node.id : null;
    canvas.style.cursor = node ? "grab" : "default";

    if (state.draggingId) {
      const dragged = layoutById.get(state.draggingId);
      const graphPoint = fromScreen(point);
      dragged.x = graphPoint.x;
      dragged.y = graphPoint.y;
      canvas.style.cursor = "grabbing";
    }
  });

  canvas.addEventListener("pointerdown", (event) => {
    const node = findNodeAt(pointerPosition(event));
    if (!node) return;

    state.selectedId = node.id;
    state.draggingId = node.id;
    canvas.setPointerCapture(event.pointerId);
    renderDetails();
  });

  canvas.addEventListener("pointerup", (event) => {
    state.draggingId = null;
    canvas.releasePointerCapture(event.pointerId);
  });

  canvas.addEventListener("pointerleave", () => {
    state.hoveredId = null;
    state.draggingId = null;
  });

  searchInput.addEventListener("input", () => {
    state.search = searchInput.value;
  });

  dataModeToggle.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-mode]");
    if (!button) return;

    const nextMode = button.dataset.mode;
    const nextGraph = graphScopes.modes[nextMode];
    if (!nextGraph) return;

    state.dataMode = nextMode;
    state.search = "";
    state.type = "All";
    state.relationship = "All";
    searchInput.value = "";
    setGraph(nextGraph);
    populateStats();
    populateFilters();
    renderDetails();
  });

  languageFilter.addEventListener("change", () => {
    state.languageFilter = languageFilter.value;
  });

  typeFilter.addEventListener("change", () => {
    state.type = typeFilter.value;
  });

  relationshipFilter.addEventListener("change", () => {
    state.relationship = relationshipFilter.value;
  });

  resetButton.addEventListener("click", () => {
    state.search = "";
    state.type = "All";
    state.relationship = "All";
    state.languageFilter = "All";
    searchInput.value = "";
    languageFilter.value = "All";
    typeFilter.value = "All";
    relationshipFilter.value = "All";
  });

  if (languageToggle) {
    languageToggle.addEventListener("click", () => {
      language = language === "vi" ? "en" : "vi";
      localStorage.setItem(languageKey, language);
      applyLanguage();
    });
  }

  window.addEventListener("resize", resizeCanvas);

  setGraph(graph);
  applyLanguage();
  resizeCanvas();
  requestAnimationFrame(draw);
})();
