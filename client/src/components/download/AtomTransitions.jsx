import React, { useContext } from "react";
import AtomTransitionData from "./AtomTransitionData";

import { ReactionContext } from "../../contexts/ReactionContext";
import { AuthContext } from "../../contexts/AuthContext";

const AtomTransitions = () => {
  const { authState } = useContext(AuthContext);
  const { isUser } = authState;

  const { reaction } = useContext(ReactionContext);

  return (
    <>
      {reaction.rxnFile ? (
        <AtomTransitionData
          key={reaction.id.toString()}
          {...reaction}
          reactionId={reaction.id}
          isUser={isUser}
        />
      ) : (
        <div className="mt-3">
          <p className="lead text-muted">
            There are no atom transitions for this reaction :(
          </p>
        </div>
      )}
    </>
  );
};

export default AtomTransitions;
