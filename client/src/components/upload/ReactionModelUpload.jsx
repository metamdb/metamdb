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
        Reaction Models are user-uploaded models of multiple reactions.
        Reactions and metabolites can be identified by specific database
        identifiers to get accurate atom mapping data, while manual atom
        mappings can be used for your custom or simplified reactions.{" "}
        <a
          href="https://collinstark.github.io/metamdb-docs/reaction-model"
          target="_blank"
          rel="noopener noreferrer"
        >
          You can read about the specifications and more here!
        </a>
      </p>
      <p>
        <a href="https://collinstark.github.io/metamdb-docs/assets/files/example_model-89c060de55622eeeb376a7111a2802ef.csv">
          Download the example model here!
        </a>
      </p>

      <small className="text-muted">
        e.g. v1 [10021], Glucose [1] (abcdef), -->, Glucose 6-phosphate [2]
        (abcdef)
      </small>
      <FileUploadContainer {...initialState} />
    </div>
  );
};

export default ReactionModelUpload;
