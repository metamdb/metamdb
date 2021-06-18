import React, { useContext } from "react";

import { MetaboliteContext } from "../../contexts/MetaboliteContext";

const MetaboliteIdentifiers = () => {
  const { metabolite } = useContext(MetaboliteContext);
  const { identifiers } = metabolite;
  const orderedIdentifiers = identifiers.reduce((r, a) => {
    if (a.source === "KEGG") {
      a.link = `https://www.genome.jp/dbget-bin/www_bget?${a.identifier}`;
    } else if (a.source === "MetaCyc") {
      a.link = `https://biocyc.org/compound?orgid=META&id=${a.identifier}`;
    } else {
      a.link = `https://www.brenda-enzymes.org/ligand.php?brenda_ligand_id=${a.identifier}`;
    }
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
      })}
    </div>
  );
};

export default MetaboliteIdentifiers;
