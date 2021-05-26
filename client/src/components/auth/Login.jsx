import React, { useState, useContext } from "react";
import { useHistory } from "react-router-dom";

import { AuthContext } from "../../contexts/AuthContext";

import useTextForm from "../forms/useTextForm";
import { validateLogin } from "../../validation/validateAuth";

import axios from "axios";
import classnames from "classnames";

const initialState = {
  name: "",
  password: "",
};

const Login = (props) => {
  const { authDispatch } = useContext(AuthContext);
  const history = useHistory();

  function loginUser() {
    axios
      .post("/api/auth/login", values)
      .then((res) => {
        authDispatch({
          type: "LOGIN",
          payload: res.data,
        });

        history.goBack();
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
  } = useTextForm(initialState, validateLogin, loginUser);

  return (
    <div className="login">
      <div className="login-content">
        <div className="header mb-15">
          <h1 className="text-center">Sign In</h1>
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
              <button
                disabled={isSubmitting}
                type="submit"
                className="btn btn-primary btn-block btn-lg"
              >
                Sign In
              </button>
            </div>
            {/* <p className="hint-text">
              Don't have an account?{" "}
              <Link className="text-primary" to="/register">
                Create one
              </Link>
            </p> */}
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
