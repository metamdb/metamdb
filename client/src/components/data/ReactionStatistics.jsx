import React, { useRef } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const data = {
  datasets: [
    {
      label: "AAM",
      data: [
        {
          y: "BRENDA",
          x: 40362,
          aam: [17084, 12620, 18228, 3477, 1251, 1238, 617],
        },
        {
          y: "KEGG",
          x: 9831,
          aam: [5748, 3900, 2837, 1321, 537, 390, 45],
        },
        {
          y: "MetaCyc",
          x: 14602,
          aam: [6568, 4688, 32211, 1580, 607, 540, 227],
        },
      ],
      backgroundColor: [
        "rgb(46, 49, 146, 1)",
        "rgb(193, 39, 45, 1)",
        "rgb(0, 146, 69, 1)",
      ],
      borderColor: [
        "rgb(46, 49, 146, 1)",
        "rgb(193, 39, 45, 1)",
        "rgb(0, 146, 69, 1)",
      ],
      borderWidth: 1,
    },
    {
      label: "No AAM",
      data: [
        {
          y: "BRENDA",
          x: 20767,
          noAam: [3685, 6630, 7757, 781, 447, 920, 562],
        },
        {
          y: "KEGG",
          x: 1483,
          noAam: [525, 728, 168, 36, 23, 89, 7],
        },
        {
          y: "MetaCyc",
          x: 3062,
          noAam: [767, 996, 426, 96, 59, 127, 28],
        },
      ],
      backgroundColor: [
        "rgb(46, 49, 146, 0.2)",
        "rgb(193, 39, 45, 0.2)",
        "rgb(0, 146, 69, 0.2)",
      ],
      borderColor: [
        "rgb(46, 49, 146, 1)",
        "rgb(193, 39, 45, 1)",
        "rgb(0, 146, 69, 1)",
      ],
      borderWidth: 1,
    },
  ],
};

const options2 = {
  indexAxis: "x",
  scales: {
    x: { ticks: { font: { size: 14 } } },
    y: { ticks: { font: { size: 14 } } },
  },
  plugins: {
    legend: {
      labels: {
        font: {
          size: 14,
        },
      },
      position: "right",
      onHover: (event, chartElement) => {
        event.native.target.style.cursor = "pointer";
      },
      onLeave: (event, chartElement) => {
        event.native.target.style.cursor = "default";
      },
    },
  },
  responsive: true,
};

const data2 = {
  labels: [
    "E.C. 1",
    "E.C. 2",
    "E.C. 3",
    "E.C. 4",
    "E.C. 5",
    "E.C. 6",
    "E.C. 7",
  ],
  datasets: [
    {
      label: "Total",
      data: [34377, 29562, 61627, 7291, 2924, 3304, 1486],
      backgroundColor: ["rgb(0, 0, 0, 0.2)"],
      borderColor: ["rgb(0, 0, 0, 1)"],
      borderWidth: 1,
    },
  ],
};

const ReactionStatistics = () => {
  const chartRef = useRef(null);

  const clickHandler = (event, elements, chart) => {
    if (elements.length === 1) {
      const dataIndex = elements[0].datasetIndex;
      const bgColor = elements[0].element.options.backgroundColor;
      const brColor = elements[0].element.options.borderColor;
      const y = elements[0].element.$context.raw.y;
      const aam = elements[0].element.$context.raw.aam;
      const noAam = elements[0].element.$context.raw.noAam;

      chartRef.current.config.data.datasets[0].borderColor = [brColor];
      chartRef.current.config.data.datasets[0].backgroundColor = [bgColor];
      chartRef.current.config.data.datasets[0].label = y;

      if (dataIndex === 0) {
        chartRef.current.config.data.datasets[0].data = aam;
      }
      if (dataIndex === 1) {
        chartRef.current.config.data.datasets[0].data = noAam;
      }

      chartRef.current.update();
    }
  };

  const options = {
    onClick: clickHandler,
    indexAxis: "y",
    plugins: {
      legend: {
        labels: {
          font: {
            size: 14,
          },
        },
        position: "right",
        onHover: (event, chartElement) => {
          event.native.target.style.cursor = "pointer";
        },
        onLeave: (event, chartElement) => {
          event.native.target.style.cursor = "default";
        },
      },
    },
    responsive: true,
    scales: {
      x: {
        stacked: true,
        ticks: { font: { size: 14 } },
      },
      y: {
        stacked: true,
        ticks: { font: { size: 14 } },
      },
    },
  };
  return (
    <div className="reaction-statistics">
      <div className="row">
        <div className="col-12 mb-3">
          <div class="card shadow-sm">
            <div class="card-content">
              <div class="card-body">
                <h3>Reactions/Atom Mappings</h3>
                <Bar options={options} data={data} width={"500%"} />
              </div>
            </div>
          </div>
        </div>

        <div className="col-12">
          <div class="card shadow-sm">
            <div class="card-content">
              <div class="card-body">
                <h3>Enzymes</h3>
                <p className="lead text-muted">
                  Enzymes per category selected (default: total). Clicking on
                  the "Reactions/Atom Mappings" bars will change category.
                </p>
                <Bar
                  options={options2}
                  data={data2}
                  ref={chartRef}
                  width={"500%"}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReactionStatistics;
