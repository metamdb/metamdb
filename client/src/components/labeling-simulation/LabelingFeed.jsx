import React from "react";
import GoBackHeader from "../headers/GoBackHeader";
import LabelingData from "./LabelingData";
import LabelingVisualization from "./LabelingVisualization";
import { Tabs, Tab } from "react-bootstrap";

const LabelingFeed = (props) => {
  return (
    <div className="feed">
      <GoBackHeader
        title="Labeling Simulation - Results"
        type="DELETE_SIMULATION"
      />
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
