import React from "react";
import { Link } from "react-router-dom";

import FileUploadContainer from "./FileUpload";
import GoBackHeader from "../headers/GoBackHeader";

const FluxModelUpload = (props) => {
  const initialState = {
    name: "flux_file",
    uploadPath: `/api/upload/flux`,
    type: "UPLOAD_FLUX_MODEL",
  };

  return (
    <div className="flux-file-upload">
      <div className="content">
        <div className="container">
          <GoBackHeader
            title="Upload - Flux Model"
            type="DELETE_REACTION_MODEL"
          />
          <p className="lead text-muted">
            Flux model upload for the calculation of mass isotopomer
            distributions (MID). The flux model has to be seperated into three
            columns, 1. reaction name, 2. first flux, 3. second flux. A header
            has to include the flux type, indicating FORWARD/REVERSE or
            NET/EXCHANGE fluxes. Supported file formats include: csv.
          </p>
          <p className="lead text-muted">
            Want to inspect your Reaction Model?{" "}
            <Link className="text-primary" to="/atom-mapping" target="_blank">
              Click here!
            </Link>
          </p>
          <small className="text-muted">e.g. v1 | 4 | 4</small>
          <FileUploadContainer {...initialState} />
        </div>
      </div>
    </div>
  );
};

export default FluxModelUpload;
