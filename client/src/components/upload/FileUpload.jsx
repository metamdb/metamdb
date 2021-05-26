import React, { useState, useContext } from "react";
import axios from "axios";
import classnames from "classnames";

import { MainContext } from "../../contexts/MainContext";

import useFileFormValidation from "../forms/useFileForm";
import validateUpload from "../../validation/validateUpload";

const FileUpload = (props) => {
  const {
    values,
    errors,
    apiError,
    loading,
    isSubmitting,
    handleSubmit,
    handleChange,
  } = props;

  return (
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
              {values.file ? values.file.name : "Upload File..."}
            </label>
            {errors.file && (
              <div className="invalid-feedback">{errors.file}</div>
            )}
            {apiError && <div className="invalid-feedback">{apiError}</div>}
          </div>
        </div>
        <div className="mt-3">
          <button
            className="btn btn-outline-primary mr-2"
            type="submit"
            disabled={isSubmitting}
          >
            <i className="fas fa-file-upload" /> Submit
          </button>
          {loading && <i className="fas fa-spinner fa-pulse" />}
        </div>
      </form>
    </div>
  );
};

const initialState = {
  file: null,
};

const FileUploadContainer = (props) => {
  const { contextState, dispatch } = useContext(MainContext);

  const {
    values,
    errors,
    isSubmitting,
    handleChange,
    handleSubmit,
  } = useFileFormValidation(initialState, validateUpload, uploadFile);

  const [apiError, setApiError] = useState(null);
  const [loading, setLoading] = useState(false);

  function uploadFile() {
    setLoading(true);

    const { file } = values;
    const { name, uploadPath, type } = props;
    const uploadData = new FormData();
    uploadData.append(name, file, file.name);
    if (name === "flux_file") {
      const model = {
        reactions: contextState.reactions,
      };
      uploadData.append("model", JSON.stringify(model));
    }

    axios
      .post(uploadPath, uploadData)
      .then((res) => {
        dispatch({
          type: type,
          payload: res.data,
        });
      })
      .catch((err) => {
        setApiError(err.response.data.file);
        setLoading(false);
      });
  }

  const state = {
    values,
    errors,
    apiError,
    loading,
    isSubmitting,
    handleChange,
    handleSubmit,
  };

  return <FileUpload {...state} />;
};

export default FileUploadContainer;
