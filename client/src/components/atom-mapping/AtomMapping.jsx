import React, { useContext } from "react";

import { MainContext } from "../../contexts/MainContext";

import ReactionModelUpload from "../upload/ReactionModelUpload";
import ReactionModel from "../upload/ReactionModelUpdated";

const AtomMapping = (props) => {
  const { contextState } = useContext(MainContext);
  let atomContent;

  if (!contextState.isReactionModel) {
    atomContent = <ReactionModelUpload />;
  } else {
    atomContent = <ReactionModel />;
  }

  return (
    <div className="mapping">
      <div className="content">
        <div className="container">{atomContent}</div>
      </div>
    </div>
  );
};

export default AtomMapping;
