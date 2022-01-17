import React from "react";
import DataStatistics from "../data/DataStatistics";

const Home = (props) => {
  return (
    <div className="home">
      <div className="content">
        <div className="container">
          <h1>MetAMDB - Metabolic Atom Mapping Database</h1>
          <p className="lead text-muted">Welcome to MetAMDB!</p>
          {/* <br /> */}
          <p className="lead text-muted">
            MetAMDB is an easy to use tool for atom mappings. MetAMDB provides
            atom mapping models for user-specific uploaded metabolic models, as
            well as atom mappings for individual reactions. Additionally, the
            MetAMDB{" "}
            <a
              href="https://metamdb.github.io/docs/api"
              target="_blank"
              rel="noreferrer"
            >
              API
            </a>{" "}
            can be utilized to query the database.
          </p>
          <DataStatistics />
        </div>
      </div>
    </div>
  );
};

export default Home;
