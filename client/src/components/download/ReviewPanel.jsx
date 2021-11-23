import React, { useState, useContext } from "react";
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

  const { values, errors, isSubmitting, handleChange, handleSubmit } =
    useFileFormValidation({ file: null }, validateUpload, uploadFile);

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

  function keepFile() {
    setLoading(true);

    const token = localStorage.getItem("token");
    const data = { dummy: true };
    const config = {
      headers: { Authorization: "Bearer " + token },
    };

    axios
      .post(`/api/query/reaction/${reaction.id}/upload/correct`, data, config)
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
      <h2>Review Panel</h2>
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
      <div className="row">
        <div className="col-3">
          <div
            className="nav flex-column nav-pills"
            id="v-pills-tab"
            role="tablist"
            aria-orientation="vertical"
          >
            <a
              className="nav-link active"
              id="v-pills-no-changes-tab"
              data-toggle="pill"
              href="#v-pills-no-changes"
              role="tab"
              aria-controls="v-pills-no-changes"
              aria-selected="true"
            >
              No Changes
            </a>
            <a
              className="nav-link"
              id="v-pills-rxn-tab"
              data-toggle="pill"
              href="#v-pills-rxn"
              role="tab"
              aria-controls="v-pills-rxn"
              aria-selected="false"
            >
              Upload RXN-File
            </a>
            {/* <a
              className="nav-link"
              id="v-pills-abc-tab"
              data-toggle="pill"
              href="#v-pills-abc"
              role="tab"
              aria-controls="v-pills-abc"
              aria-selected="false"
            >
              Upload ABC-Mapping
            </a>
            <a
              className="nav-link"
              id="v-pills-feedback-tab"
              data-toggle="pill"
              href="#v-pills-feedback"
              role="tab"
              aria-controls="v-pills-feedback"
              aria-selected="false"
            >
              Send Feedback
            </a> */}
          </div>
        </div>
        <div className="col-9">
          <div className="tab-content" id="v-pills-tabContent">
            <div
              className="tab-pane fade show active"
              id="v-pills-no-changes"
              role="tabpanel"
              aria-labelledby="v-pills-no-changes-tab"
            >
              <h3>Is the current Atom Mapping correct?</h3>
              <button
                type="button"
                className="btn btn-success mt-2"
                onClick={() => keepFile()}
              >
                The Atom Mapping is Correct!
              </button>
            </div>
            <div
              className="tab-pane fade"
              id="v-pills-rxn"
              role="tabpanel"
              aria-labelledby="v-pills-rxn-tab"
            >
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
            </div>
            {/* <div
              className="tab-pane fade"
              id="v-pills-abc"
              role="tabpanel"
              aria-labelledby="v-pills-abc-tab"
            >
              ...
            </div>
            <div
              className="tab-pane fade"
              id="v-pills-feedback"
              role="tabpanel"
              aria-labelledby="v-pills-feedback-tab"
            >
              ...
            </div> */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReviewPanel;
