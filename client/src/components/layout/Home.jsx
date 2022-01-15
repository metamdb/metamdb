import React from "react";
import DataStatistics from "../data/DataStatistics";

const Home = (props) => {
  return (
    <div className="home">
      <div className="content">
        <div className="container">
          <h1>MetAMDB - Metabolic Atom Mapping Database</h1>
          <p className="lead text-muted">Welcome to MetAMDB</p>
          <DataStatistics />
        </div>
      </div>
    </div>
  );
};

export default Home;
