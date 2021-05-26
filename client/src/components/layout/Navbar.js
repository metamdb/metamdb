import React, { useContext } from "react";
import { Link } from "react-router-dom";

import { AuthContext } from "../../contexts/AuthContext";

const Navbar = (props) => {
  const { authState, authDispatch } = useContext(AuthContext);
  const { isUser } = authState;

  const handleLogout = () => {
    authDispatch({
      type: "LOGOUT",
    });
  };

  const authLinks = (
    <li className="nav-item">
      <button onClick={handleLogout} className="btn btn-link nav-link">
        Logout
      </button>
    </li>
  );

  const guestLinks = (
    <li className="nav-item">
      <Link className="nav-link" to="/login">
        Login
      </Link>
    </li>
  );

  return (
    <>
      <nav className="navbar navbar-expand-sm navbar-dark bg-dark">
        <div className="container">
          <Link className="navbar-brand" to="/">
            MetAMDB
          </Link>
          <button
            className="navbar-toggler"
            type="button"
            data-toggle="collapse"
            data-target="#mobile-nav"
          >
            <span className="navbar-toggler-icon" />
          </button>
          <div className="collapse navbar-collapse" id="mobile-nav">
            <ul className="navbar-nav mr-auto">
              <li className="nav-item">
                <Link className="nav-link" to="/atom-mapping">
                  Atom Mapping
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/database-query">
                  Database Query
                </Link>
              </li>
            </ul>
          </div>

          <div className="collapse navbar-collapse" id="mobile-nav">
            <ul className="navbar-nav ml-auto">
              <li className="nav-item">
                <a
                  target="_blank"
                  href="https://collinstark.github.io/metamdb-docs/"
                  className="nav-link"
                  rel="noreferrer"
                >
                  Help
                </a>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/contact">
                  Contact
                </Link>
              </li>
              {isUser ? authLinks : guestLinks}
            </ul>
          </div>
        </div>
      </nav>
    </>
  );
};

export default Navbar;
