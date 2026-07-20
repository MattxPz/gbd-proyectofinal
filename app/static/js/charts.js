/* Helper genérico para renderizar gráficos de barras (Chart.js) a partir de
   los mismos datos que ya se muestran en la tabla de cada reporte.

   No consulta MongoDB ni ningún endpoint: recibe labels/data ya extraídos
   en la plantilla desde `resultados`. */

(function () {
  var UMBRAL_HORIZONTAL = 15; // más de N ítems -> barras horizontales
  var ALTURA_VERTICAL = 320;
  var ALTURA_BASE_HORIZONTAL = 120;
  var ALTURA_POR_ITEM = 24;
  var ALTURA_MAXIMA = 1000;

  var COLOR_BARRA = "#1d4ed8";
  var COLOR_BARRA_HOVER = "#1e3a8a";

  function mostrarSinDatos(wrapper) {
    wrapper.innerHTML =
      '<div class="empty-state chart-empty">' +
      '<div class="empty-icon">&#128202;</div>' +
      "Sin datos para graficar." +
      "</div>";
  }

  /**
   * @param {string} canvasId  id del <canvas> destino
   * @param {string[]} labels  etiquetas (eje de categorías)
   * @param {number[]} data    valores numéricos
   * @param {{datasetLabel?: string}} [opciones]
   */
  function renderBarChart(canvasId, labels, data, opciones) {
    var canvas = document.getElementById(canvasId);
    if (!canvas) return;

    var wrapper = canvas.closest(".chart-wrapper");

    if (!labels || labels.length === 0) {
      if (wrapper) mostrarSinDatos(wrapper);
      return;
    }

    var config = opciones || {};
    var horizontal = labels.length > UMBRAL_HORIZONTAL;

    if (wrapper) {
      var altura = horizontal
        ? Math.min(ALTURA_MAXIMA, ALTURA_BASE_HORIZONTAL + labels.length * ALTURA_POR_ITEM)
        : ALTURA_VERTICAL;
      wrapper.style.height = altura + "px";
    }

    new Chart(canvas, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: config.datasetLabel || "",
            data: data,
            backgroundColor: COLOR_BARRA,
            hoverBackgroundColor: COLOR_BARRA_HOVER,
            borderRadius: 4,
            maxBarThickness: 36,
          },
        ],
      },
      options: {
        indexAxis: horizontal ? "y" : "x",
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { enabled: true },
        },
        scales: {
          x: { grid: { display: !horizontal } },
          y: { grid: { display: horizontal } },
        },
      },
    });
  }

  window.renderBarChart = renderBarChart;
})();
