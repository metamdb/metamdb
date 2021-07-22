import React, { useState } from "react";
import { Popover, OverlayTrigger, Button } from "react-bootstrap";
import axios from "axios";
import classnames from "classnames";
import styled from "styled-components";

import useFileFormValidation from "../forms/useFileForm";
import validateUpload from "../../validation/validateRxn";

import no_aam from "../../shared/no_aam.png";

const StyledPopover = styled(Popover)`
  min-width: 600px;
`;

const StyledPopoverImage = styled(Popover)`
  min-width: 1000px;
`;

const AtomTransitionData = ({
  id,
  file,
  updated,
  updatedBy,
  updatedOn,
  reactionId,
  isUser,
}) => {
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState(null);
  const [description, setDescription] = useState("");

  const {
    values,
    errors,
    isSubmitting,
    handleChange,
    handleSubmit,
  } = useFileFormValidation({ file: null }, validateUpload, uploadFile);

  const imageSource = `${process.env.PUBLIC_URL}/img/aam/${reactionId}.svg`;

  const downloadRxn = (e) => {
    e.preventDefault();

    const element = document.createElement("a");
    document.body.appendChild(element);
    const fileData = new Blob([file], {
      type: "text/plain",
    });
    const url = URL.createObjectURL(fileData);
    element.href = url;
    element.download = `AAM${reactionId}.rxn`;
    element.click();
    setTimeout(() => {
      document.body.removeChild(element);
      window.URL.revokeObjectURL(url);
    }, 0);
  };

  function uploadFile() {
    setLoading(true);

    const { file } = values;
    const uploadData = new FormData();
    uploadData.append("rxnFile", file, file.name);
    uploadData.append("description", description);

    const token = localStorage.getItem("token");
    const config = {
      headers: { Authorization: "Bearer " + token },
    };

    axios
      .post(
        `/api/query/reaction/${reactionId}/upload/${id}`,
        uploadData,
        config
      )
      .then((res) => {
        // setAtomTransition({ ...atomTransition, ...res.data });
        setLoading(false);
      })
      .catch((err) => {
        setApiError(err.response.data.file);
        setLoading(false);
      });
  }

  const popover = (
    <StyledPopover id="popover" className="shadow">
      <StyledPopover.Title as="h3">Atom Transition</StyledPopover.Title>
      <StyledPopover.Content>
        <pre>{file}</pre>
      </StyledPopover.Content>
    </StyledPopover>
  );

  const popoverImage = (
    <StyledPopoverImage id="popover" className="shadow">
      <StyledPopoverImage.Title as="h3">
        Atom Transition Image
      </StyledPopoverImage.Title>
      <StyledPopoverImage.Content>
        <img
          src={imageSource}
          onError={(e) => {
            e.target.onError = null;
            e.target.src = no_aam;
          }}
          alt={`Structure Atom Mapping ${id}`}
          style={{ width: "100%" }}
        />
      </StyledPopoverImage.Content>
    </StyledPopoverImage>
  );

  return (
    <div className="mt-3">
      <h2>Atom Transition {id}</h2>
      <p className="lead text-muted">
        <strong>Updated: </strong>
        {updated ? (
          <i className="fas fa-check" />
        ) : (
          <i className="fas fa-times" />
        )}{" "}
        {updatedBy && (
          <>
            <strong>By: </strong>
            {updatedBy}
          </>
        )}{" "}
        {updatedOn && (
          <>
            <strong>On: </strong>
            {updatedOn}
          </>
        )}
      </p>
      <p className="text-muted">
        <strong>Atom Transition:</strong>
        <OverlayTrigger placement="right" trigger="focus" overlay={popover}>
          <Button variant="link">Click</Button>
        </OverlayTrigger>
        <strong>Image:</strong>
        <OverlayTrigger
          placement="right"
          trigger="focus"
          overlay={popoverImage}
        >
          <Button variant="link">Click</Button>
        </OverlayTrigger>
      </p>
      <div className="download mb-3">
        <button type="button" className="btn btn-success" onClick={downloadRxn}>
          <i className="fa fa-download" /> Download RXN
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
                <div className="mt-3">
                  <textarea
                    className="form-control"
                    id="description"
                    rows="3"
                    placeholder="Changes..."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                  ></textarea>
                </div>
              </div>
              <div className="mt-3">
                <button
                  className="btn btn-warning mr-2"
                  type="submit"
                  disabled={isSubmitting}
                >
                  <i className="fas fa-upload" /> Upload RXN
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

export default AtomTransitionData;
