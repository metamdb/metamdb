import React, { useState } from "react";
import classnames from "classnames";
import axios from "axios";

import useTextForm from "../forms/useTextForm";
import { validateContact } from "../../validation/validateContact";

const initialState = {
  name: "",
  email: "",
  message: "",
};

const Contact = (props) => {
  const [apiSuccess, setApiSuccess] = useState({});
  const [apiErrors, setApiErrors] = useState({});

  function sendContact() {
    axios
      .post("/api/contact", values)
      .then((res) => {
        setValues(initialState);
        setApiSuccess(res.data);
      })
      .catch((err) => setApiErrors(err.response.data));
  }

  const {
    values,
    errors,
    isSubmitting,
    handleChange,
    handleSubmit,
    setValues,
  } = useTextForm(initialState, validateContact, sendContact);

  return (
    <div className="contact">
      <div className="d-flex h-100">
        <div className="col mt-5">
          <div className="container">
            <div className="card border-0 shadow">
              <div
                className="card-header contact-header text-center text-white"
                style={{ paddingTop: "4rem", paddingBottom: "4rem" }}
              >
                <h2>Contact Us</h2>
                <span className="lead">
                  Leave your details below and get in touch!
                </span>
              </div>
              <div className="card-body">
                {apiSuccess.contact && (
                  <div
                    className="alert alert-success alert-dismissible fade show"
                    role="alert"
                  >
                    <strong>Success!</strong> Your message has been sent.
                    <button
                      type="button"
                      className="close"
                      data-dismiss="alert"
                      aria-label="Close"
                    >
                      <span aria-hidden="true">&times;</span>
                    </button>
                  </div>
                )}
                {apiErrors.contact && (
                  <div
                    className="alert alert-danger alert-dismissible fade show"
                    role="alert"
                  >
                    <strong>Sorry!</strong> We encountered an error.
                    <button
                      type="button"
                      className="close"
                      data-dismiss="alert"
                      aria-label="Close"
                    >
                      <span aria-hidden="true">&times;</span>
                    </button>
                  </div>
                )}
                <form id="contact-form" onSubmit={handleSubmit}>
                  <div className="form-group row">
                    <label
                      htmlFor="name"
                      className="col-sm-2 col-form-label text-right lead text-muted"
                    >
                      Full Name:
                    </label>
                    <div className="col-sm-10">
                      <input
                        name="name"
                        type="text"
                        className={classnames("contact-body form-control", {
                          "has-value": values.name && !errors.name,
                          "is-invalid": errors.name,
                        })}
                        placeholder="Enter full name"
                        value={values.name}
                        onChange={handleChange}
                      />
                      {errors.name && (
                        <div className="invalid-feedback">{errors.name}</div>
                      )}
                    </div>
                  </div>
                  <div className="form-group row">
                    <label
                      htmlFor="exampleInputEmail1"
                      className="col-sm-2 col-form-label text-right lead text-muted"
                    >
                      Email:
                    </label>
                    <div className="col-sm-10">
                      <input
                        name="email"
                        type="email"
                        className={classnames("contact-body form-control", {
                          "has-value": values.email && !errors.email,
                          "is-invalid": errors.email,
                        })}
                        aria-describedby="emailHelp"
                        placeholder="Enter email address"
                        value={values.email}
                        onChange={handleChange}
                      />
                      {errors.email && (
                        <div className="invalid-feedback">{errors.email}</div>
                      )}
                    </div>
                  </div>
                  <div className="form-group row">
                    <label
                      htmlFor="message"
                      className="col-sm-2 col-form-label text-right lead text-muted"
                    >
                      Message:
                    </label>
                    <div className="col-sm-10">
                      <textarea
                        name="message"
                        value={values.message}
                        onChange={handleChange}
                        className={classnames("contact-body form-control", {
                          "has-value": values.message && !errors.message,
                          "is-invalid": errors.message,
                        })}
                        rows="5"
                        placeholder="Your comment..."
                      ></textarea>
                      {errors.message && (
                        <div className="invalid-feedback">{errors.message}</div>
                      )}
                      <button
                        type="submit"
                        className="btn btn-success mt-3"
                        disabled={isSubmitting}
                      >
                        Submit
                      </button>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;
