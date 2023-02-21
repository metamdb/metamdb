import React, { useContext } from "react";

import { MainContext } from "../../contexts/MainContext";

import ReactionModelUpload from "../upload/ReactionModelUpload";
import LabelingOptions from "./LabelingOptions";

const LabelingSimulation = (props) => {
  const { contextState } = useContext(MainContext);

  let simulationContent;
  if (!contextState.isReactionModel) {
    simulationContent = <ReactionModelUpload />;
  } else {
    if (!contextState.isFluxModel) {
      simulationContent = <LabelingOptions />;
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
