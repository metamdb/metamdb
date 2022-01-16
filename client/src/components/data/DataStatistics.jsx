import React, { useState } from "react";
import classnames from "classnames";

import MetaboliteStatistics from "./MetaboliteStatistics";
import PathwayStatistics from "./PathwayStatistics";
import ReactionStatistics from "./ReactionStatistics";

const DataStatistics = () => {
  const [statistic, setStatistic] = useState("reaction");

  return (
    <div className="data-statistics">
      <h2>Statistics</h2>
      <div className="statistics-nav">
        <ul className="nav nav-tabs">
          <li className="nav-item">
            <button
              className={classnames("btn btn-link nav-link", {
                active: statistic === "reaction",
              })}
              onClick={() => setStatistic("reaction")}
            >
              Reactions
            </button>
          </li>
          <li className="nav-item">
            <button
              className={classnames("btn btn-link nav-link", {
                active: statistic === "metabolite",
              })}
              onClick={() => setStatistic("metabolite")}
            >
              Metabolites
            </button>
          </li>
          <li className="nav-item">
            <button
              className={classnames("btn btn-link nav-link", {
                active: statistic === "pathway",
              })}
              onClick={() => setStatistic("pathway")}
            >
              Pathways
            </button>
          </li>
        </ul>
      </div>

      {statistic === "reaction" ? (
        <ReactionStatistics />
      ) : statistic === "metabolite" ? (
        <MetaboliteStatistics />
      ) : (
        <PathwayStatistics />
      )}
    </div>
  );
};

export default DataStatistics;
