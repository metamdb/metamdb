import React, { useContext, useState, useEffect } from "react";
import { Tabs, Tab } from "react-bootstrap";
import axios from "axios";

import { MetaboliteContext } from "../../contexts/MetaboliteContext";

import MetaboliteInfo from "./MetaboliteInfo";
import MetaboliteIdentifiers from "./MetaboliteIdentifiers";
import Reactions from "./Reactions";

const MetaboliteContainer = (props) => {
  const { id } = props.match.params;
  const { setMetabolite } = useContext(MetaboliteContext);

  useEffect(() => {
    axios
      .get(`/api/query/metabolite/${id}`)
      .then((res) => {
        setMetabolite(res.data);
        setIsMetabolite(true);
      })
      .catch((err) => {
        console.log(err.response.data);
        setNotFound(true);
      });
  }, [id, setMetabolite]);

  const [notFound, setNotFound] = useState(false);
  const [isMetabolite, setIsMetabolite] = useState(false);

  return <Metabolite id={id} notFound={notFound} isMetabolite={isMetabolite} />;
};

export default MetaboliteContainer;

const Metabolite = ({ id, notFound, isMetabolite }) => {
  return (
    <div className="metabolite">
      <div className="content">
        <div className="container">
          <h1>Metabolite {id}</h1>
          {isMetabolite && (
            <>
              <Tabs defaultActiveKey="metabolite">
                <Tab eventKey="metabolite" title="Metabolite">
                  <MetaboliteInfo id={id} />
                </Tab>
                <Tab eventKey="identifiers" title="Identifiers">
                  <MetaboliteIdentifiers />
                </Tab>
              </Tabs>
            </>
          )}
          {notFound && (
            <>
              <h3 className="text-muted">
                No metabolite match for the id: {id}
              </h3>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
