import React, { useContext } from "react";
import { MainContext } from "../../contexts/MainContext";
import { Link } from "react-router-dom";
import LabelingData from "./LabelingData";
import LabelingVisualization from "./LabelingVisualization";
import { Tabs, Tab } from "react-bootstrap";

const LabelingFeed = (props) => {
  const { dispatch } = useContext(MainContext);

  const goBack = () => {
    dispatch({
      type: "DELETE_SIMULATION",
    });
  };

  return (
    <div className="feed">
      <div className="row">
        <div className="col-6">
          <h1>Labeling Simulation - Results</h1>
        </div>
        <div className="col-4 ml-auto">
          <Link
            className="btn btn-primary"
            to="/flux-model"
            target="_blank"
            style={{ float: "left" }}
          >
            <i className="fas fa-external-link-alt" /> Check Flux Model
          </Link>
        </div>
        <div className="col-2 ml-auto">
          <button
            type="button"
            className="btn btn-danger"
            onClick={goBack}
            style={{ float: "right" }}
          >
            <i className="fas fa-arrow-left" /> Go Back
          </button>
        </div>
      </div>
      <Tabs defaultActiveKey="vis">
        <Tab eventKey="vis" title="Visualization">
          <LabelingVisualization />
        </Tab>
        <Tab eventKey="data" title="Data">
          <LabelingData />
        </Tab>
      </Tabs>
    </div>
  );
};

export default LabelingFeed;
