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
      data: [
        {
          y: "BRENDA",
          x: 40362,
          aam: [11785, 10134, 11665, 2782, 976, 1011, 532],
        },
        {
          y: "KEGG",
          x: 9831,
          aam: [3414, 2417, 1187, 916, 395, 263, 24],
        },
        {
          y: "MetaCyc",
          x: 14602,
          aam: [3939, 3384, 1817, 1184, 447, 407, 106],
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
      data: [14501, 12100, 12636, 3259, 1158, 1269, 569],
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
        display: false,
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
                <h3>Atom Mappings</h3>
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
                  the "Atom Mappings" bars will change category.
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
