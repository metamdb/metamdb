import React, { useContext } from "react";

import { ReactionContext } from "../../contexts/ReactionContext";

const ReactionInfo = () => {
  const { reaction } = useContext(ReactionContext);
  const { formula } = reaction;

  return (
    <div className="mt-3">
      {/* <p className="text-muted">
        <strong>formula:</strong>
      </p> */}
      <p className="text-muted">{formula} </p>
    </div>
  );
};

export default ReactionInfo;
