import React, { useState } from "react";
import { Popover, OverlayTrigger, Button } from "react-bootstrap";
import axios from "axios";
import classnames from "classnames";
import styled from "styled-components";
import { Link } from "react-router-dom";
import { Tabs, Tab } from "react-bootstrap";
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";

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
  rxnFile,
  updated,
  updated_by,
  updatedOn,
  reactionId,
  isUser,
}) => {
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState(null);
  const [description, setDescription] = useState("");
  const [alert, setAlert] = useState(null);

  const { values, errors, isSubmitting, handleChange, handleSubmit } =
    useFileFormValidation({ file: null }, validateUpload, uploadFile);

  const imageSource = `${process.env.PUBLIC_URL}/img/aam/${reactionId}.svg`;

  const downloadRxn = (e) => {
    e.preventDefault();

    const element = document.createElement("a");
    document.body.appendChild(element);
    const fileData = new Blob([rxnFile], {
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

  const downloadSvg = (e) => {
    e.preventDefault();

    const element = document.createElement("a");
    document.body.appendChild(element);
    element.href = imageSource;
    element.download = `AAM${reactionId}.svg`;
    element.click();
    setTimeout(() => {
      document.body.removeChild(element);
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
        setAlert(res.data.message);
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
        <pre>{rxnFile}</pre>
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
      {alert && (
        <div
          className="alert alert-dismissible fade show alert-success"
          role="alert"
        >
          <button
            type="button"
            className="close"
            data-dismiss="alert"
            aria-label="Close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
          {alert}
        </div>
      )}
      <h2>Atom Mapping</h2>
      <p className="lead text-muted">
        <strong>Curated: </strong>
        {updated ? (
          <i className="fas fa-check" />
        ) : (
          <i className="fas fa-times" />
        )}{" "}
        {updated_by && (
          <>
            <strong>By: </strong>
            <Link
              className="text-primary"
              to={`/user/${updated_by.id}`}
              target="_blank"
            >
              {updated_by.name}
            </Link>
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
        {/* <strong>Image:</strong>
        <OverlayTrigger
          placement="right"
          trigger="focus"
          overlay={popoverImage}
        >
          <Button variant="link">Click</Button>
        </OverlayTrigger> */}
      </p>
      <p>
        <TransformWrapper>
          <TransformComponent>
            <img
              src={imageSource}
              onError={(e) => {
                e.target.onError = null;
                e.target.src = no_aam;
              }}
              alt={`Structure Atom Mapping ${id}`}
              style={{ width: "100%" }}
            />
          </TransformComponent>
        </TransformWrapper>
      </p>
      <div className="download mb-3">
        <button
          type="button"
          className="btn btn-success mr-2"
          onClick={downloadRxn}
        >
          <i className="fa fa-download" /> Download RXN
        </button>
        <button type="button" className="btn btn-primary" onClick={downloadSvg}>
          <i className="fa fa-download" /> Download SVG
        </button>
      </div>
    </div>
  );
};

export default AtomTransitionData;
