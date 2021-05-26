import React, { useContext, useState } from "react";
import AtomTransitionData from "./AtomTransitionData";
import Alerts from "../common/Alerts";
import axios from "axios";

import { ReactionContext } from "../../contexts/ReactionContext";
import { AuthContext } from "../../contexts/AuthContext";

const AtomTransitions = () => {
  const { authState } = useContext(AuthContext);
  const { isUser } = authState;

  const { reaction } = useContext(ReactionContext);
  const { id, atomTransitions } = reaction;

  const [loading, setLoading] = useState(false);
  const [alerts, setAlerts] = useState(null);

  const generateAtomTransition = () => {
    setLoading(true);

    axios
      .post(`/api/query/reaction/${id}/generate`)
      .then((res) => {
        atomTransitions[0] = res.data;
        setLoading(false);
      })
      .catch((err) => {
        console.log(err.response.data);
        setAlerts([{ message: err.response.data, level: "ERROR" }]);
        setLoading(false);
      });
  };

  return (
    <>
      {atomTransitions.file ? (
        <AtomTransitionData
          key={atomTransitions.id.toString()}
          {...atomTransitions}
          reactionId={id}
          isUser={isUser}
        />
      ) : (
        <div className="mt-3">
          <p className="lead text-muted">
            There are no atom transitions for this reaction :(
          </p>
          {isUser && (
            <>
              {alerts && <Alerts alerts={alerts} />}
              <button
                type="button"
                className="btn btn-primary mr-2"
                onClick={generateAtomTransition}
              >
                <i className="fas fa-cog" /> Generate Atom Transition
              </button>
              {loading && <i className="fas fa-spinner fa-pulse" />}
            </>
          )}
        </div>
      )}
    </>
  );
};

export default AtomTransitions;
