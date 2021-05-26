import React, { useContext } from "react";
import { Link } from "react-router-dom";

import { MetaboliteContext } from "../../contexts/MetaboliteContext";

const Reactions = () => {
  const { metabolite } = useContext(MetaboliteContext);
  const { reactions } = metabolite;

  const orderedReactions = reactions.reduce((r, a) => {
    r[a.reactant] = r[a.reactant] || [];
    r[a.reactant].push(a);
    return r;
  }, Object.create(null));

  return (
    <div className="mt-3">
      {Object.entries(orderedReactions).map(([key, values], idx) => {
        return (
          <div className={`source-${key}`} key={idx}>
            <p className="text-muted">
              <strong>{key}: </strong>
            </p>

            {values.map((value, id) => {
              return (
                <p className="text-muted" key={id}>
                  <Link target="_blank" to={`/reaction/${value.id}`}>
                    {value.formula}
                  </Link>
                </p>
              );
            })}
          </div>
        );
      })}
    </div>
  );
};

export default Reactions;
