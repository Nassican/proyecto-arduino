let chart;
let pieChart;
let timeData = [];
let frequencyData = [];

// Plugin para mostrar texto en el centro del gráfico de dona
const centerTextPlugin = {
  id: "centerText",
  afterDatasetsDraw(chart) {
    if (chart.config.type === "doughnut") {
      const { ctx, width, height } = chart;
      const percentage = chart.data.datasets[0].data[0];

      ctx.save();
      ctx.font = "bold 1.5em sans-serif";
      ctx.textBaseline = "middle";
      ctx.textAlign = "center";
      ctx.fillStyle = "#000";
      ctx.fillText("Notas", width / 2, height / 2 - 10);
      ctx.fillText("Correctas", width / 2, height / 2 + 10);
      ctx.fillText(percentage.toFixed(2) + "%", width / 2, height / 2 + 40);
      ctx.restore();
    }
  },
};

async function actualizarDatos() {
  const response = await fetch("/datos");
  const datos = await response.json();

  const tabla = document
    .getElementById("datos-tabla")
    .getElementsByTagName("tbody")[0];
  tabla.innerHTML = "";

  datos.forEach((dato) => {
    const row = tabla.insertRow();
    row.insertCell(0).innerText = dato.tecla;
    row.insertCell(1).innerText = dato.nota_tecla; // Mostrar el nuevo campo
    row.insertCell(2).innerText = dato.frecuencia;
    row.insertCell(3).innerText = dato.nota;
    row.insertCell(4).innerText = dato.correcta ? "Sí" : "No";
    row.insertCell(5).innerText = dato.timestamp;
    // Actualizar datos para la gráfica

    // Si la nota es correcta, resaltar la fila
    if (dato.correcta) row.classList.add("font-medium");
    else row.classList.add("text-neutral-800");

    row.classList.add(
      "border",
      "border-gray-300",
      "px-4",
      "py-2",
      "hover:bg-gray-100"
    );

    const timestamp = dato.timestamp;
    if (timeData.length === 10) {
      timeData.shift();
      frequencyData.shift();
    }
    timeData.push(timestamp);
    frequencyData.push(dato.frecuencia);
  });

  chart.data.labels = timeData;
  chart.data.datasets[0].data = frequencyData;
  chart.update("none"); // 'none' desactiva las animaciones
}

async function actualizarEstadisticas() {
  const response = await fetch("/estadisticas");
  const estadisticas = await response.json();

  document.getElementById("total-notas").innerText = estadisticas.total_notas;
  document.getElementById("total-correctas").innerText =
    estadisticas.total_correctas;
  // document.getElementById("porcentaje-correctas").innerText =
  //   estadisticas.porcentaje_correctas.toFixed(2) + "%";

  // Llamar a la función para actualizar el gráfico de dona
  actualizarGraficoCircular(estadisticas.porcentaje_correctas);
}

function actualizarGraficoCircular(porcentajeCorrectas) {
  pieChart.data.datasets[0].data = [
    porcentajeCorrectas,
    100 - porcentajeCorrectas,
  ];
  pieChart.update();
}

async function actualizarEstadisticasPorNota() {
  const response = await fetch("/notas");
  const estadisticas = await response.json();

  const tablaEfectividad = document
    .getElementById("efectividad-tabla")
    .getElementsByTagName("tbody")[0];
  tablaEfectividad.innerHTML = "";

  //Estructura de mis json
  // {
  //     "nota": "B4",
  //     "porcentaje_correctas": 100,
  //     "total_correctas": 13,
  //     "total_notas": 13
  // }

  // Ordenar el array según el orden musical
  const ordenMusical = ["C", "D", "E", "F", "G", "A", "B"];
  const ordenarPorNota = (a, b) => {
    const octavaA = parseInt(a.nota.slice(-1));
    const octavaB = parseInt(b.nota.slice(-1));
    const notaA = a.nota.slice(0, -1);
    const notaB = b.nota.slice(0, -1);

    const indexA = ordenMusical.indexOf(notaA);
    const indexB = ordenMusical.indexOf(notaB);

    if (indexA === indexB) {
      return octavaA - octavaB;
    } else {
      return indexA - indexB;
    }
  };

  estadisticas.sort(ordenarPorNota);

  estadisticas.forEach((estadistica) => {
    const row = tablaEfectividad.insertRow();
    row.insertCell(0).innerText = estadistica.nota;
    row.insertCell(1).innerText = estadistica.total_notas;
    row.insertCell(2).innerText = estadistica.total_correctas;
    row.insertCell(3).innerText =
      estadistica.porcentaje_correctas.toFixed(2) + "%";
    row.classList.add(
      "border",
      "border-gray-300",
      "px-4",
      "py-2",
      "hover:bg-gray-100"
    );
  });
}

function crearGrafica() {
  const ctx = document.getElementById("frecuenciaChart").getContext("2d");
  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: timeData,
      datasets: [
        {
          label: "Frecuencia vs Tiempo",
          data: frequencyData,
          borderColor: "rgba(75, 192, 192, 1)",
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          fill: false,
        },
      ],
    },
    options: {
      animation: {
        duration: 0, // Desactivar animaciones
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Tiempo",
          },
          reverse: true,
        },
        y: {
          title: {
            display: true,
            text: "Frecuencia (Hz)",
          },
        },
      },
    },
  });
}

function crearGraficoCircular() {
  const ctx = document
    .getElementById("porcentajeCorrectasChart")
    .getContext("2d");
  pieChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: [
        "Notas Correctas (Analizadas por el sensor)",
        "Notas Incorrectas (Error del sensor)",
      ],
      datasets: [
        {
          data: [0, 100],
          backgroundColor: ["#4CAF50", "#FF5722"],
        },
      ],
    },
    options: {
      responsive: true,
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: "Porcentaje de Notas Correctas",
      },
      tooltips: {
        enabled: false,
      },
    },
    plugins: [centerTextPlugin],
  });
}

window.onload = function () {
  crearGrafica();
  crearGraficoCircular(); // Nueva línea
  actualizarDatos();
  actualizarEstadisticasPorNota();
  actualizarEstadisticas();
  setInterval(() => {
    actualizarDatos();
    actualizarEstadisticasPorNota();
    actualizarEstadisticas();
  }, 1000);
};
