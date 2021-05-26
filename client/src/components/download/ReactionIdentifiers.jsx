import React, { useContext } from "react";

import { ReactionContext } from "../../contexts/ReactionContext";

const ReactionIdentifiers = () => {
  const { reaction } = useContext(ReactionContext);
  const { identifiers } = reaction;
  const orderedIdentifiers = identifiers.reduce((r, a) => {
    r[a.source] = r[a.source] || [];
    r[a.source].push(a);
    return r;
  }, Object.create(null));

  return (
    <div className="mt-3">
      {Object.entries(orderedIdentifiers).map(([key, values], idx) => {
        return (
          <div className={`source-${key}`} key={idx}>
            <p className="text-muted">
              <strong>{key} identifiers: </strong>
            </p>
            <p className="text-muted">
              {values
                .map((value, id) => {
                  return value.identifier;
                })
                .join(", ")}
            </p>
          </div>
        );
      })}
    </div>
  );
};

export default ReactionIdentifiers;
