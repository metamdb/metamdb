import React, { useState } from "react";
import { useHistory } from "react-router-dom";

import useTextForm from "../forms/useTextForm";
import { validateRegister } from "../../validation/validateAuth";

import axios from "axios";
import classnames from "classnames";

const initialState = {
  name: "",
  email: "",
  password: "",
  password2: "",
};

const Register = (props) => {
  let history = useHistory();

  function registerUser() {
    axios
      .post("/api/auth/register", values)
      .then((res) => {
        history.push("/");
      })
      .catch((err) => setApiErrors(err.response.data));
  }

  const [apiErrors, setApiErrors] = useState({});

  const {
    values,
    errors,
    isSubmitting,
    handleChange,
    handleSubmit,
  } = useTextForm(initialState, validateRegister, registerUser);

  return (
    <div className="login">
      <div className="login-content">
        <div className="header mb-15">
          <h1 className="text-center">Sign Up</h1>
        </div>
        <div className="body">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <div className="input-group">
                <span className="input-group-addon">
                  <i className="fa fa-user"></i>
                </span>
                <div className="name-group">
                  <input
                    type="name"
                    className={classnames("form-control", {
                      "is-invalid": errors.name || apiErrors.name,
                    })}
                    name="name"
                    placeholder="Name"
                    value={values.name}
                    onChange={handleChange}
                  />
                  {errors.name && (
                    <div className="invalid-feedback">{errors.name}</div>
                  )}
                  {apiErrors.name && (
                    <div className="invalid-feedback">{apiErrors.name}</div>
                  )}
                </div>
              </div>
            </div>
            <div className="form-group">
              <div className="input-group">
                <span className="input-group-addon">
                  <i className="fa fa-envelope"></i>
                </span>
                <div className="email-group">
                  <input
                    type="email"
                    className={classnames("form-control", {
                      "is-invalid": errors.email || apiErrors.email,
                    })}
                    name="email"
                    placeholder="Email"
                    value={values.email}
                    onChange={handleChange}
                  />
                  {errors.email && (
                    <div className="invalid-feedback">{errors.email}</div>
                  )}
                  {apiErrors.email && (
                    <div className="invalid-feedback">{apiErrors.email}</div>
                  )}
                </div>
              </div>
            </div>
            <div className="form-group">
              <div className="input-group">
                <span className="input-group-addon">
                  <i className="fa fa-lock"></i>
                </span>
                <div className="password-group">
                  <input
                    type="password"
                    className={classnames("form-control", {
                      "is-invalid": errors.password || apiErrors.password,
                    })}
                    name="password"
                    placeholder="Password"
                    value={values.password}
                    onChange={handleChange}
                  />
                  {errors.password && (
                    <div className="invalid-feedback">{errors.password}</div>
                  )}
                  {apiErrors.password && (
                    <div className="invalid-feedback">{apiErrors.password}</div>
                  )}
                </div>
              </div>
            </div>
            <div className="form-group">
              <div className="input-group">
                <span className="input-group-addon">
                  <i className="fa fa-lock"></i>
                </span>
                <div className="password2-group">
                  <input
                    type="password"
                    className={classnames("form-control", {
                      "is-invalid": errors.password2 || apiErrors.password2,
                    })}
                    name="password2"
                    placeholder="Confirm Password"
                    value={values.password2}
                    onChange={handleChange}
                  />
                  {errors.password2 && (
                    <div className="invalid-feedback">{errors.password2}</div>
                  )}
                  {apiErrors.password2 && (
                    <div className="invalid-feedback">
                      {apiErrors.password2}
                    </div>
                  )}
                </div>
              </div>
            </div>
            <div className="form-group">
              <button
                disabled={isSubmitting}
                type="submit"
                className="btn btn-primary btn-block btn-lg"
              >
                Sign Up
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Register;
