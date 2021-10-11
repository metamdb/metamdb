import React, { useEffect, useState } from "react";
import { Tabs, Tab } from "react-bootstrap";
import axios from "axios";

import PathwayInfo from "./PathwayInfo";
import PathwayReactions from "./PathwayReactions";

const PathwayContainer = (props) => {
  const { id } = props.match.params;
  const [pathway, setPathway] = useState(null);

  useEffect(() => {
    axios
      .get(`/api/pathways/${id}/reactions`)
      .then((res) => {
        setPathway(res.data);
        setIsPathway(true);
      })
      .catch((err) => {
        console.log(err.response.data);
        setNotFound(true);
      });
  }, [id]);

  const [notFound, setNotFound] = useState(false);
  const [isPathway, setIsPathway] = useState(false);

  return (
    <div className="reaction">
      <div className="content">
        <div className="container">
          <h1>Pathway {id}</h1>
          {isPathway && (
            <>
              <Tabs defaultActiveKey="pathway">
                <Tab eventKey="pathway" title="Pathway">
                  <PathwayInfo {...pathway} />
                </Tab>
                <Tab eventKey="reactions" title="Reactions">
                  <PathwayReactions {...pathway} />
                </Tab>
              </Tabs>
            </>
          )}
          {notFound && (
            <>
              <h3 className="text-muted">No pathway match for the id: {id}</h3>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default PathwayContainer;
