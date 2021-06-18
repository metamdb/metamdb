import React, { useContext } from "react";

import { ReactionContext } from "../../contexts/ReactionContext";

const ReactionIdentifiers = () => {
  const { reaction } = useContext(ReactionContext);
  const { identifiers } = reaction;
  const orderedIdentifiers = identifiers.reduce((r, a) => {
    if (a.source === "KEGG") {
      a.link = `https://www.genome.jp/dbget-bin/www_bget?rn:${a.identifier}`;
    } else if (a.source === "MetaCyc") {
      a.link = `https://biocyc.org/META/NEW-IMAGE?object=${a.identifier}`;
    } else {
      a.link = null;
    }
    r[a.source] = r[a.source] || [];
    r[a.source].push(a);
    return r;
  }, Object.create(null));

  return (
    <div className="mt-3">
      {Object.entries(orderedIdentifiers).map(([key, values], idx) => {
        if (key === "BRENDA") {
          return (
            <div className={`source-${key}`} key={idx}>
              <p className="text-muted">
                <strong>{key}: </strong>
              </p>
              <p className="text-muted">
                {values
                  .map((value, id) => {
                    console.log(value);
                    return value.identifier;
                  })
                  .join(", ")}
              </p>
            </div>
          );
        } else {
          return (
            <div className={`source-${key}`} key={idx}>
              <p className="text-muted">
                <strong>{key}: </strong>
              </p>
              <p className="text-muted">
                {values.map((value, id) => {
                  return (
                    <a
                      className="mr-2"
                      key={value.identifier}
                      href={value.link}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <i className="fas fa-external-link-alt"></i>{" "}
                      {value.identifier}
                    </a>
                  );
                })}
              </p>
            </div>
          );
        }
      })}
    </div>
  );
};

export default ReactionIdentifiers;
