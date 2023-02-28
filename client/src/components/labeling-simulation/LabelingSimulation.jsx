import React, { useContext } from "react";

import { MainContext } from "../../contexts/MainContext";

import ReactionModelUpload from "../upload/ReactionModelUpload";
import LabelingOptions from "./LabelingOptions";
import LabelingFeed from "./LabelingFeed";

const LabelingSimulation = (props) => {
  const { contextState } = useContext(MainContext);

  let simulationContent;
  if (!contextState.isReactionModel) {
    simulationContent = <ReactionModelUpload />;
  } else {
    if (!contextState.isCalculated) {
      simulationContent = <LabelingOptions />;
    } else {
      simulationContent = <LabelingFeed />;
    }
  }

  return (
    <div className="simulation">
      <div className="content">
        <div className="container">{simulationContent}</div>
      </div>
    </div>
  );
};

export default LabelingSimulation;
