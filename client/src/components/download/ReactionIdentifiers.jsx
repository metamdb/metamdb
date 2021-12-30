import React, { useContext } from "react";

import { ReactionContext } from "../../contexts/ReactionContext";

const ReactionIdentifiers = () => {
  const { reaction } = useContext(ReactionContext);
  const { identifiers } = reaction;
  const orderedIdentifiers = identifiers.reduce((r, a) => {
    if (a.source.name === "KEGG") {
      a.link = `https://www.genome.jp/dbget-bin/www_bget?rn:${a.databaseIdentifier}`;
    } else if (a.source.name === "MetaCyc") {
      a.link = `https://biocyc.org/META/NEW-IMAGE?object=${a.databaseIdentifier}`;
    } else if (a.source.name === "BRENDA") {
      if (a.databaseIdentifier.includes("BR")) {
        a.link = `https://www.brenda-enzymes.org/structure.php?show=reaction&id=${a.databaseIdentifier.replace(
          "BR",
          ""
        )}&type=I&displayType=marvin`;
      } else if (a.databaseIdentifier.includes("BS")) {
        a.link = `https://www.brenda-enzymes.org/structure.php?show=reaction&id=${a.databaseIdentifier.replace(
          "BS",
          ""
        )}&type=S&displayType=marvin`;
      } else {
        a.link = null;
      }
    }
    r[a.source.name] = r[a.source.name] || [];
    r[a.source.name].push(a);
    return r;
  }, Object.create(null));

  return (
    <div className="mt-3">
      <h2>Identifiers</h2>
      {Object.entries(orderedIdentifiers).map(([key, values], idx) => {
        return (
          <div className={`source-${key}`} key={idx}>
            <p className="text-muted">
              <strong>{key}: </strong>{" "}
              {values.map((value, id) => {
                return (
                  <a
                    className="mr-2"
                    key={value.databaseIdentifier}
                    href={value.link}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <i className="fas fa-external-link-alt"></i>{" "}
                    {value.databaseIdentifier}
                  </a>
                );
              })}
            </p>
          </div>
        );
      })}
    </div>
  );
};

export default ReactionIdentifiers;
