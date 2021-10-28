import React, { useState, useContext } from "react";
import { Tabs, Tab } from "react-bootstrap";
import axios from "axios";
import classnames from "classnames";

import useFileFormValidation from "../forms/useFileForm";
import validateUpload from "../../validation/validateRxn";

import { ReactionContext } from "../../contexts/ReactionContext";

const ReviewPanel = () => {
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState(null);
  const [description, setDescription] = useState("");
  const [alert, setAlert] = useState(null);

  const { reaction } = useContext(ReactionContext);

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
    uploadData.append("rxnFile", file, file.name);
    uploadData.append("description", description);

    const token = localStorage.getItem("token");
    const config = {
      headers: { Authorization: "Bearer " + token },
    };

    axios
      .post(
        `/api/query/reaction/${reaction.id}/upload/${reaction.id}`,
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

  return (
    <div className="mt-3">
      <Tabs defaultActiveKey="file" variant="pills" className="mb-3">
        <Tab eventKey="file" title="Upload RXN-File">
          <div className="upload mb-3">
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
        </Tab>
        <Tab eventKey="abc" title="Upload ABC-Atom Mapping"></Tab>
        <Tab eventKey="feedback" title="Send Feedback"></Tab>
      </Tabs>
    </div>
  );
};

export default ReviewPanel;
