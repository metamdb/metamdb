import React, { useContext, useState } from "react";
import { Row, Col, Alert } from "react-bootstrap";
import classnames from "classnames";
import axios from "axios";
import { Link } from "react-router-dom";

import { MainContext } from "../../contexts/MainContext";

import GoBackHeader from "../headers/GoBackHeader";

const MidParameter = (props) => {
  const { contextState, dispatch } = useContext(MainContext);

  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [element, setElement] = useState("");
  const [products, setProducts] = useState([]);
  const [tracer, setTracer] = useState({
    metabolite: "",
    labeling: "",
    purity: "",
  });

  const handleChange = (event) => {
    setTracer({
      ...tracer,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);

    const parameterData = new FormData();
    parameterData.append("element", element);
    parameterData.append("tracer", JSON.stringify(tracer));
    parameterData.append("products", JSON.stringify(products));
    parameterData.append("model", JSON.stringify(contextState.reactions));

    setLabelingParameters(parameterData);
  };

  const setLabelingParameters = (paramData) => {
    axios
      .post(`/api/calculation`, paramData)
      .then((res) => {
        dispatch({
          type: "SET_LABELING",
          payload: res.data,
        });
      })
      .catch((err) => {
        setLoading(false);
        console.log(err.response.data);
        setErrors(err.response.data);
      });
  };

  const addProduct = (e) => {
    if (e.target.value !== "" && !products.includes(e.target.value)) {
      setProducts([...products, e.target.value]);
    }
  };

  const deleteProduct = (e) => {
    setProducts(products.filter((product) => product !== e.target.value));
  };

  return (
    <div className="parameter">
      <GoBackHeader
        title="MID Calculation - Parameters"
        type="DELETE_FLUX_MODEL"
      />

      {errors.message && (
        <Alert variant="danger" dismissible>
          {errors.message}
        </Alert>
      )}

      <p className="lead text-muted">
        MID parameter selection. Multiple tracer can be selected for MID
        simulation. Choose element to label, metabolite to be used as a tracer,
        labeling state in additional mass (0 or 1), and purity percentage.
        Additionally multiple products can be chosen.
      </p>
      <p className="lead text-muted">
        Want to inspect your Reaction Model?{" "}
        <Link className="text-primary" to="/reaction-model" target="_blank">
          Click here!
        </Link>
      </p>
      <form onSubmit={handleSubmit} id="midForm" name="midForm">
        <div className="form-group">
          <select
            name="element"
            id="element"
            className={classnames("form-control", {
              "is-invalid": errors.element,
            })}
            style={{ width: "300px" }}
            onChange={(e) => setElement(e.target.value)}
          >
            <option value="">Select Element...</option>
            {Object.keys(contextState.elements).map((key) => (
              <option
                key={contextState.elements[key].id}
                value={contextState.elements[key].symbol}
              >
                {contextState.elements[key].name}
              </option>
            ))}
          </select>
          {errors.element && (
            <div className="invalid-feedback">{errors.element}</div>
          )}
        </div>
        <div className="form-group">
          <Row>
            <Col>
              <select
                name="metabolite"
                id="metabolite"
                className={classnames("form-control float-left", {
                  "is-invalid": errors.metabolite,
                })}
                style={{ width: "300px" }}
                onChange={handleChange}
                value={tracer.metabolite}
              >
                <option value="">Select Tracer...</option>
                {element
                  ? contextState.elements[element].metabolites.map(
                      (metabolite) => (
                        <option
                          key={metabolite.identifier}
                          value={metabolite.identifier}
                        >
                          {metabolite.name}
                        </option>
                      )
                    )
                  : null}
              </select>
              {errors.metabolite && (
                <div className="invalid-feedback">{errors.metabolite}</div>
              )}
            </Col>
            <Col>
              {" "}
              <input
                name="labeling"
                id="labeling"
                type="number"
                placeholder="Labeling State..."
                className={classnames("form-control", {
                  "is-invalid": errors.labeling,
                })}
                onChange={handleChange}
                value={tracer.labeling}
              />
              {errors.labeling && (
                <div className="invalid-feedback">{errors.labeling}</div>
              )}
            </Col>
            <Col>
              <input
                name="purity"
                id="purity"
                type="number"
                step="0.01"
                placeholder="Purity..."
                className={classnames("form-control", {
                  "is-invalid": errors.purity,
                })}
                onChange={handleChange}
                value={tracer.purity}
              />
              {errors.purity && (
                <div className="invalid-feedback">{errors.purity}</div>
              )}
            </Col>
          </Row>
        </div>

        <div className="form-group">
          <select
            id="products"
            className={classnames("form-control", {
              "is-invalid": errors.products,
            })}
            style={{ width: "300px" }}
            onChange={addProduct}
          >
            <option value="">Select Products...</option>
            {element
              ? contextState.elements[element].metabolites.map((metabolite) => (
                  <option
                    key={metabolite.identifier}
                    value={metabolite.identifier}
                  >
                    {metabolite.name}
                  </option>
                ))
              : null}
          </select>
          {errors.products && (
            <div className="invalid-feedback">{errors.products}</div>
          )}
        </div>
        <div className="form-row">
          <div className="form-group col-md-6">
            {products.length !== 0
              ? products.map((product) => (
                  <button
                    key={product}
                    type="button"
                    value={product}
                    onClick={deleteProduct}
                    className="btn btn-link"
                  >
                    {product}
                  </button>
                ))
              : null}
          </div>
        </div>

        <div className="mt-3">
          <button className="btn btn-outline-primary mr-2" type="submit">
            <i className="fas fa-file-upload" /> Submit
          </button>
          {loading && <i className="fas fa-spinner fa-pulse" />}
        </div>
      </form>
    </div>
  );
};

export default MidParameter;
