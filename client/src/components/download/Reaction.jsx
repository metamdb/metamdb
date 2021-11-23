import React, { useEffect, useState, useContext } from "react";
import { Tabs, Tab } from "react-bootstrap";
import axios from "axios";

import { ReactionContext } from "../../contexts/ReactionContext";
import { AuthContext } from "../../contexts/AuthContext";
import ReactionInfo from "./ReactionInfo";
import ReactionIdentifiers from "./ReactionIdentifiers";
import Compounds from "./Compounds";
import AtomTransitions from "./AtomTransitions";
import ReviewPanel from "./ReviewPanel";

const ReactionContainer = (props) => {
  const { id } = props.match.params;
  const { setReaction } = useContext(ReactionContext);
  const { authState } = useContext(AuthContext);
  const { isUser } = authState;

  useEffect(() => {
    axios
      .get(`/api/query/reaction/${id}`)
      .then((res) => {
        setReaction(res.data);
        setIsReaction(true);
      })
      .catch((err) => {
        console.log(err.response.data);
        setNotFound(true);
      });
  }, [id, setReaction]);

  const [notFound, setNotFound] = useState(false);
  const [isReaction, setIsReaction] = useState(false);

  return (
    <Reaction
      id={id}
      notFound={notFound}
      isReaction={isReaction}
      isUser={isUser}
    />
  );
};

export default ReactionContainer;

const Reaction = ({ id, notFound, isReaction, isUser }) => {
  return (
    <div className="reaction">
      <div className="content">
        <div className="container">
          <h1>Reaction {id}</h1>
          {isReaction && (
            <>
              <Tabs defaultActiveKey="reaction">
                <Tab eventKey="reaction" title="Reaction">
                  <ReactionInfo />
                  <ReactionIdentifiers />
                </Tab>
                <Tab eventKey="compounds" title="Compounds">
                  <Compounds />
                </Tab>
                <Tab eventKey="transitions" title="Atom Mappings">
                  <AtomTransitions />
                </Tab>
                {isUser && (
                  <Tab eventKey="review" title="Review Panel">
                    <ReviewPanel />
                  </Tab>
                )}
              </Tabs>
            </>
          )}
          {notFound && (
            <>
              <h3 className="text-muted">No reaction match for the id: {id}</h3>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
