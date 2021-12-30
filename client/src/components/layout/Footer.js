import React from "react";
import { Link } from "react-router-dom";

const Footer = (props) => {
  return (
    // <footer className="fixed-bottom bg-dark mt-5 p-3">
    //   <div className="container text-center">
    //     <span className="text-white ">
    //       Copyright &copy; {new Date().getFullYear()} MetAMDB
    //     </span>
    //   </div>
    // </footer>
    <footer className="fixed-bottom mt-5 p-3">
      <div className="container">
        <div className="row text-center">
          <div className="col-md-4 box">
            <span className="copyright quick-links text-white">
              Copyright &copy; {new Date().getFullYear()} MetAMDB
            </span>
          </div>
          <div className="col-md-4 box">
            <ul className="list-inline social-buttons">
              <li className="list-inline-item">
                <a
                  href="https://github.com/metamdb/metamdb"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <i className="fab fa-github"></i>
                </a>
              </li>
            </ul>
          </div>
          <div className="col-md-4 box">
            <ul className="list-inline quick-links">
              <li className="list-inline-item">
                <Link to="/impressum">Impressum</Link>
              </li>
              <li className="list-inline-item">
                <Link to="/datenschutz">Datenschutz</Link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
