import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip);

const data = {
  datasets: [
    {
      data: [
        {
          y: "BRENDA",
          x: 111469,
        },
        {
          y: "KEGG",
          x: 8974,
        },
        {
          y: "MetaCyc",
          x: 14621,
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

const options = {
  indexAxis: "y",
  responsive: true,
  plugins: {
    legend: {
      display: false,
    },
  },
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

const MetaboliteStatistics = () => {
  return (
    <div className="metabolite-statistics">
      <div className="row">
        <div className="col-12 mb-3">
          <div className="card shadow-sm">
            <div className="card-content">
              <div className="card-body">
                <h3>Metabolites</h3>
                <Bar options={options} data={data} width={"500%"} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MetaboliteStatistics;
