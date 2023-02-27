import React, { useState, useContext, useRef, useEffect } from "react";
import axios from "axios";
import classnames from "classnames";
import { Row, Col, Alert } from "react-bootstrap";
import { Link } from "react-router-dom";
import GoBackHeader from "../headers/GoBackHeader";
import Select from "react-select";
import makeAnimated from "react-select/animated";

import { MainContext } from "../../contexts/MainContext";

import validateUpload from "../../validation/validateUpload";
import MetaboliteForm from "./MetaboliteForm";
import SymmetryForm from "./SymmetryForm";

const animatedComponents = makeAnimated();

const LabelingOptions = (props) => {
  const [jsonFile, setJsonFile] = useState("");
  const [fileContent, setFileContent] = useState("");
  let fileRef = useRef();

  const readFile = (event) => {
    setJsonFile(event.target.files[0]);
    const fileReader = new FileReader();
    const { files } = event.target;

    fileReader.readAsText(files[0], "UTF-8");
    fileReader.onload = (e) => {
      const content = e.target.result;
      setFileContent(JSON.parse(content));
    };
  };

  const useJson = () => {
    if (fileContent.tracer) {
      fileContent.tracer.forEach((tracer) => {
        setTimeout(() => {
          setValues((values) => ({
            ...values,
            tracer: [...values.tracer, tracer],
          }));
        }, "500");
      });
    }
    if (fileContent.targets) {
      fileContent.targets.forEach((target) => {
        setTimeout(() => {
          setValues((values) => ({
            ...values,
            targets: [...values.targets, { label: target, value: target }],
          }));
        }, "500");
      });
    }
    if (fileContent.symmetry) {
      fileContent.symmetry.forEach((sym) => {
        setTimeout(() => {
          setValues((values) => ({
            ...values,
            symmetry: [...values.symmetry, sym],
          }));
        }, "500");
      });
    }
    if (fileContent.ignore) {
      fileContent.ignore.forEach((ignore) => {
        console.log(ignore);
        setTimeout(() => {
          setValues((values) => ({
            ...values,
            ignore: [...values.ignore, { label: ignore, value: ignore }],
          }));
        }, "500");
      });
    }
  };

  const { contextState, dispatch } = useContext(MainContext);
  const { metabolites } = contextState;

  const options = metabolites.map((metabolite) => {
    return { value: metabolite, label: metabolite };
  });

  const initialValues = {
    tracer: [],
    targets: [],
    symmetry: [],
    ignore: [],
  };
  const [values, setValues] = useState(initialValues);
  const [targets, setTargets] = useState([]);
  const [file, setFile] = useState(null);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setSubmitting] = useState(false);

  const onTargetChange = (inputValue, { action, prevInputValue }) => {
    setValues({ ...values, targets: inputValue });
  };
  const onIgnoreChange = (inputValue, { action, prevInputValue }) => {
    setValues({ ...values, ignore: inputValue });
  };

  const upload = () => {
    setLoading(true);

    const uploadData = new FormData();
    uploadData.append("flux_file", file, file.name);

    const model = {
      reactions: contextState.reactions,
    };
    uploadData.append("model", JSON.stringify(model));
    uploadData.append("options", JSON.stringify(values));

    axios
      .post(`/api/upload/flux`, uploadData)
      .then((res) => {
        console.log(res.data);
        dispatch({
          type: "UPLOAD_FLUX_MODEL",
          payload: res,
        });
        setLoading(false);
      })
      .catch((err) => {
        setApiError(err.response.data.file);
        setLoading(false);
      });
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleChange = (event) => {
    setValues({
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // const validationErrors = validateUpload(values);
    // setErrors(validationErrors);

    setSubmitting(true);
    const noErrors = Object.keys(errors).length === 0;
    if (noErrors) {
      upload();
      setSubmitting(false);
    } else {
      setSubmitting(false);
    }
  };

  const [apiError, setApiError] = useState(null);
  const [loading, setLoading] = useState(false);
  console.log(values);
  return (
    <div className="labeling-options">
      <div className="content">
        <div className="container">
          <GoBackHeader
            title="Labeling Simulation - Options"
            type="DELETE_REACTION_MODEL"
          />

          <form onSubmit={handleSubmit}>
            <div className="flux-upload">
              <h1>Flux Model</h1>
              <p className="lead text-muted">
                Flux model upload for the calculation of mass isotopomer
                distributions (MID). The flux model has to be seperated into
                three columns, 1. reaction name, 2. first flux, 3. second flux.
                A header has to include the flux type, indicating
                FORWARD/REVERSE or NET/EXCHANGE fluxes. Supported file formats
                include: csv.
              </p>
              <p className="lead text-muted">
                Want to inspect your Reaction Model?{" "}
                <Link
                  className="text-primary"
                  to="/atom-mapping"
                  target="_blank"
                >
                  Click here!
                </Link>
              </p>
              <small className="text-muted">e.g. v1 | 4 | 4</small>
              <div className="form-group">
                <div className="custom-file">
                  <input
                    type="file"
                    name="file"
                    className={classnames("custom-file-input", {
                      "is-invalid": errors.file || apiError,
                    })}
                    id="customUpload"
                    onChange={handleFileChange}
                  />
                  <label
                    id="customUploadLabel"
                    htmlFor="customUpload"
                    className="custom-file-label"
                  >
                    {file ? file.name : "Upload File..."}
                  </label>
                  {errors.file && (
                    <div className="invalid-feedback">{errors.file}</div>
                  )}
                </div>
              </div>
            </div>
            <div className="json-upload">
              <h1>Options</h1>
              <div className="form-group">
                <div className="row">
                  <div className="col-10">
                    <div className="custom-file">
                      <input
                        ref={fileRef}
                        type="file"
                        onChange={readFile}
                        name="file"
                        className={classnames("custom-file-input", {
                          "is-invalid": errors.jsonfile,
                        })}
                        id="customUpload"
                      />
                      <label
                        id="customUploadLabel"
                        htmlFor="customUpload"
                        className="custom-file-label"
                      >
                        {jsonFile ? jsonFile.name : "Upload JSON Config..."}
                      </label>
                    </div>
                  </div>
                  <div className="col-2">
                    <button
                      className="btn btn-outline-primary mr-2"
                      type="button"
                      onClick={useJson}
                    >
                      <i className="fas fa-file-upload" /> Activate Config
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div className="tracers">
              <h2>Tracers</h2>
              <p className="lead text-muted">
                Add your desired tracer combinations! To add a tracer choose the
                metabolite from the drowdown and add it's labeling state in
                string format with 0 for unlabeled atoms and 1 for labeled atoms
                (e.g. "101" for a 1,3 labeled tracer). Then add the purity from
                0.0-1.0 and the enrichment from 0.0-1.0. You can use the
                enrichment to simulate tracer combinations (e.g. "111111"
                enrichment 0.5 + "000000" enrichment 0.5 for a 50% fully labeled
                tracer).
              </p>
              {errors.tracer && (
                <div className="invalid-feedback">{errors.tracer}</div>
              )}
              <MetaboliteForm
                metabolites={metabolites}
                values={values}
                setValues={setValues}
              />
            </div>
            <div className="targets mt-3">
              <h2>Targets</h2>
              <p className="lead text-muted">
                Target metabolites for labeling simulation. Choose metabolites
                from your model in the below dropdown menu. The menu is
                searchable and you can remove single metabolites from the list
                or all of them together.
              </p>
              {errors.target && (
                <div className="invalid-feedback">{errors.target}</div>
              )}
              <Select
                value={values.targets}
                placeholder="Select Target Metabolites..."
                closeMenuOnSelect={false}
                components={animatedComponents}
                isMulti
                options={options}
                onChange={onTargetChange}
                styles={{
                  control: (baseStyles, state) => ({
                    ...baseStyles,
                    width: "max-content",
                    minWidth: "100%",
                  }),
                }}
              />
            </div>
            <div className="symmetries mt-3">
              <h2>Symmetries</h2>
              <p className="lead text-muted">
                Add symmetric metabolites for the simulation! Choose the
                symmetric metabolite from the dropdown and reorder the indeces
                of its atom mapping in string format (e.g. given the atom
                mapping "abcd" with a/d and b/c symmetric atoms reorder its
                indices to "4321").
              </p>
              <SymmetryForm
                metabolites={metabolites}
                values={values}
                setValues={setValues}
              />
              {errors.symmetry && (
                <div className="invalid-feedback">{errors.symmetry}</div>
              )}
            </div>
            <div className="ignore mt-3">
              <h2>Metabolites To Ignore</h2>
              <p className="lead text-muted">
                Metabolites to ignore for the labeling simulation.
              </p>
              {errors.ignore && (
                <div className="invalid-feedback">{errors.ignore}</div>
              )}
              <Select
                placeholder="Select Metabolites To Ignore..."
                value={values.ignore}
                closeMenuOnSelect={false}
                components={animatedComponents}
                isMulti
                options={options}
                onChange={onIgnoreChange}
              />
            </div>
            <div className="mt-3">
              {apiError && <div className="invalid-feedback">{apiError}</div>}
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
      </div>
    </div>
  );
};

export default LabelingOptions;
