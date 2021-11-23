import React from "react";

const PathwayInfo = ({ name, sourceId, source }) => {
  let homepage;
  let pathwayLink;
  if (source === "brenda") {
    homepage = "https://www.brenda-enzymes.org/";
    const newSourceId = sourceId.replace("pw_", "");
    pathwayLink = `https://www.brenda-enzymes.org/pathway_index.php?pathway=${newSourceId}`;
  } else if (source === "kegg") {
    homepage = "https://www.genome.jp/kegg/";
    pathwayLink = `https://www.genome.jp/pathway/${sourceId}`;
  } else if (source === "metacyc") {
    homepage = "https://metacyc.org/";
    pathwayLink = `https://metacyc.org/META/NEW-IMAGE?object=${sourceId}`;
  }
  return (
    <div className="mt-3">
      <p className="text-muted">
        <strong>Name: </strong>
        {name}
      </p>
      <p className="text-muted">
        <strong>Identifier: </strong>
        <a
          className="mr-2"
          href={pathwayLink}
          target="_blank"
          rel="noopener noreferrer"
        >
          <i className="fas fa-external-link-alt"></i> {sourceId}
        </a>
      </p>
      <p className="text-muted">
        <strong>Database: </strong>
        <a
          className="mr-2"
          href={homepage}
          target="_blank"
          rel="noopener noreferrer"
        >
          <i className="fas fa-external-link-alt"></i> {source}
        </a>
      </p>
    </div>
  );
};

export default PathwayInfo;
