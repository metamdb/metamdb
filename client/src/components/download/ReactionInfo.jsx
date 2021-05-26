import React, { useContext } from "react";

import { ReactionContext } from "../../contexts/ReactionContext";

const ReactionInfo = () => {
  const { reaction } = useContext(ReactionContext);
  const { formula, compounds } = reaction;

  const unique = [...new Set(compounds.map((item) => item.source))]; // [ 'A', 'B']

  const newCompounds = compounds.filter(function(obj) {
    return obj.source === unique[0];
  });

  const unorderedCompounds = newCompounds.reduce((r, a) => {
    r[a.reactant] = r[a.reactant] || [];
    r[a.reactant].push(a);
    return r;
  }, Object.create(null));

  const orderedCompounds = {};
  Object.keys(unorderedCompounds)
    .reverse()
    .forEach(function(key) {
      orderedCompounds[key] = unorderedCompounds[key];
    });

  return (
    <div className="mt-3">
      <p className="text-muted">
        <strong>formula:</strong>
      </p>
      <p className="text-muted">{formula} </p>
    </div>
  );
};

export default ReactionInfo;
