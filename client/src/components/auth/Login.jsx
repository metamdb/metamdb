import React from "react";
import axios from "axios";

import ORCIDiD_iconvector from "../../shared/ORCIDiD_iconvector.svg";

const Login = (props) => {
  return (
    <div className="login">
      <div className="login-content">
        <div className="header mb-15">
          <h1 className="text-center">Sign In</h1>
        </div>
        <div className="body">
          {" "}
          <div className="form-group">
            <a
              className="btn btn-block btn-lg btn-light"
              href={`${axios.defaults.baseURL}/api/auth/orcid`}
            >
              <img
                src={ORCIDiD_iconvector}
                style={{ width: "8%" }}
                alt="ORCID Icon"
              />{" "}
              Continue with ORCID
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
