import React, { useContext } from "react";

import { MainContext } from "../../contexts/MainContext";

import FluxModelUpload from "../upload/FluxModelUpload";
import ReactionModelUpload from "../upload/ReactionModelUpload";
import MidParameter from "./MidParameter";
import MidFeed from "./MidFeed";

const MidCalculation = props => {
  const { contextState } = useContext(MainContext);

  let midContent;
  if (!contextState.isReactionModel) {
    midContent = <ReactionModelUpload />;
  } else {
    if (!contextState.isFluxModel) {
      midContent = <FluxModelUpload />;
    } else {
      if (!contextState.labelingData) {
        midContent = <MidParameter />;
      } else {
        midContent = <MidFeed />;
      }
    }
  }

  return <div className="mid-calcultion">{midContent}</div>;
};

export default MidCalculation;
