import React, { useContext, useState } from "react";
import { Popover, OverlayTrigger, Button } from "react-bootstrap";
import styled from "styled-components";
import axios from "axios";
import classnames from "classnames";

import { MetaboliteContext } from "../../contexts/MetaboliteContext";
import { AuthContext } from "../../contexts/AuthContext";
import useFileFormValidation from "../forms/useFileForm";
import validateUpload from "../../validation/validateMol";

// import no_met from "../../shared/no_met.png";

const StyledPopover = styled(Popover)`
  min-width: 600px;
`;

// const StyledPopoverImage = styled(Popover)`
//   min-width: 1000px;
// `;

const MetaboliteInfo = ({ id }) => {
  const { authState } = useContext(AuthContext);
  const { isUser } = authState;

  const { metabolite } = useContext(MetaboliteContext);
  const [loading, setLoading] = useState(false);
  const [apiError] = useState(null);

  // const imageSource = `${process.env.PUBLIC_URL}/img/met/${id}.svg`;

  const popover = (
    <StyledPopover id="popover">
      <StyledPopover.Title as="h3">Mol File</StyledPopover.Title>
      <StyledPopover.Content>
        <pre>{metabolite.file}</pre>
      </StyledPopover.Content>
    </StyledPopover>
  );

  // const popoverImage = (
  //   <StyledPopoverImage id="popover">
  //     <StyledPopoverImage.Title as="h3">
  //       Metabolite Image
  //     </StyledPopoverImage.Title>
  //     <StyledPopoverImage.Content>
  //       <img
  //         src={imageSource}
  //         onError={(e) => {
  //           e.target.onError = null;
  //           e.target.src = no_met;
  //         }}
  //         alt={`Structure Metabolite ${id}`}
  //         style={{ width: "100%" }}
  //       />
  //     </StyledPopoverImage.Content>
  //   </StyledPopoverImage>
  // );

  const downloadMol = (e) => {
    e.preventDefault();

    const element = document.createElement("a");
    document.body.appendChild(element);
    const file = new Blob([metabolite.file], {
      type: "text/plain",
    });
    const url = URL.createObjectURL(file);
    element.href = url;
    element.download = `MET${metabolite.id}.mol`;
    element.click();
    setTimeout(() => {
      document.body.removeChild(element);
      window.URL.revokeObjectURL(url);
    }, 0);
  };

  const {
    values,
    errors,
    isSubmitting,
    handleChange,
    handleSubmit,
  } = useFileFormValidation({ file: null }, validateUpload, uploadFile);

  function uploadFile() {
    setLoading(true);

    const { file } = values;
    const uploadData = new FormData();
    uploadData.append("molfile", file, file.name);

    axios
      .post(`/api/query/metabolite/${id}/upload`, uploadData)
      .then((res) => {
        setLoading(false);
      })
      .catch((err) => {
        setLoading(false);
      });
  }

  return (
    <div className="mt-3">
      <p className="text-muted">
        <strong>name: </strong>
        {metabolite.name}
      </p>
      <p className="text-muted">
        <strong>formula: </strong>
        {metabolite.formula}
      </p>
      <p className="text-muted">
        <strong>inchi: </strong>
        {metabolite.inchi}
      </p>
      <p className="text-muted">
        <strong>inchiShort: </strong>
        {metabolite.inchiShort}
      </p>
      <p className="text-muted">
        <strong>inchiKey: </strong>
        {metabolite.inchiKey}
      </p>
      <p className="text-muted">
        <strong>Mol File:</strong>
        <OverlayTrigger placement="right" trigger="click" overlay={popover}>
          <Button variant="link">Click</Button>
        </OverlayTrigger>
        {/* <strong>Image:</strong>
        <OverlayTrigger
          placement="right"
          trigger="click"
          overlay={popoverImage}
        >
          <Button variant="link">Click</Button>
        </OverlayTrigger> */}
      </p>
      <div className="download mb-3">
        <button type="button" className="btn btn-success" onClick={downloadMol}>
          <i className="fa fa-download" /> Download Mol File
        </button>
      </div>
      {isUser && (
        <div className="upload mb-3">
          <div className="file-upload">
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <div className="custom-file">
                  <input
                    type="file"
                    name="file"
                    className={classnames("custom-file-input", {
                      "is-invalid": errors.file || apiError,
                    })}
                    id="customUpload"
                    onChange={handleChange}
                  />
                  <label
                    id="customUploadLabel"
                    htmlFor="customUpload"
                    className="custom-file-label"
                  >
                    {values.file ? values.file.name : "Browse File..."}
                  </label>
                  {errors.file && (
                    <div className="invalid-feedback">{errors.file}</div>
                  )}
                  {apiError && (
                    <div className="invalid-feedback">{apiError}</div>
                  )}
                </div>
              </div>
              <div className="mt-3">
                <button
                  className="btn btn-warning mr-2"
                  type="submit"
                  disabled={isSubmitting}
                >
                  <i className="fas fa-upload" /> Upload Mol
                </button>
                {loading && <i className="fas fa-spinner fa-pulse" />}
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default MetaboliteInfo;
