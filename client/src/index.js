import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import * as serviceWorker from "./serviceWorker";
import axios from "axios";
import "./fonts/OpenSans-Regular.ttf";

let development = process.env.NODE_ENV !== "production";
axios.defaults.baseURL = development
  ? "http://localhost:5000"
  : process.env.REACT_APP_LOCAL_IP + ":" + window.location.port;
ReactDOM.render(<App />, document.getElementById("root"));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();
