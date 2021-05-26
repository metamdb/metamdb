import React from "react";

import FileUploadContainer from "./FileUpload";

const ReactionModelUpload = (props) => {
  const initialState = {
    name: "reaction_file",
    uploadPath: "/api/upload/reaction",
    type: "UPLOAD_REACTION_MODEL",
  };

  return (
    <div className="reaction-file-upload">
      <h1>Upload - Reaction Model</h1>
      <p className="lead text-muted">
        Reaction model upload for atom mapping network generation or labeling
        simulation. Model must consist of identifiers from{" "}
        <a
          href="https://www.brenda-enzymes.org/"
          target="_blank"
          rel="noopener noreferrer"
        >
          BRENDA
        </a>
        ,{" "}
        <a
          href="https://www.genome.jp/kegg/"
          target="_blank"
          rel="noopener noreferrer"
        >
          KEGG
        </a>
        , or{" "}
        <a
          href="https://metacyc.org/"
          target="_blank"
          rel="noopener noreferrer"
        >
          MetaCyc
        </a>{" "}
        in square brackets. Supported file formats include: csv.
      </p>
      <small className="text-muted">
        e.g. v1 [10021], Glucose [1], -->, Glucose 6-phosphate [2]
      </small>
      <FileUploadContainer {...initialState} />
    </div>
  );
};

export default ReactionModelUpload;
