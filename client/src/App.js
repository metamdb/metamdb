import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";

import MainContextProvider from "./contexts/MainContext";
import AuthContextProvider from "./contexts/AuthContext";
import ReactionContextProvider from "./contexts/ReactionContext";
import MetaboliteContextProvider from "./contexts/MetaboliteContext";

import Navbar from "./components/layout/Navbar";
import Home from "./components/layout/Home";
import Footer from "./components/layout/Footer";

import AtomMapping from "./components/atom-mapping/AtomMapping";
import MidCalculation from "./components/mid-calculation/MidCalculation";
import DatabaseQuery from "./components/database-query/DatabaseQuery";

import ReactionModel from "./components/upload/ReactionModel";

import Contact from "./components/info/Contact";
import Datenschutz from "./components/info/Datenschutz";
import Impressum from "./components/info/Impressum";

import ReactionContainer from "./components/download/Reaction";
import MetaboliteContainer from "./components/download/Metabolite";
import PathwayContainer from "./components/download/Pathway";

import Login from "./components/auth/Login";

import "./App.css";
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";

const App = (props) => {
  return (
    <MainContextProvider>
      <AuthContextProvider>
        <Router>
          <div className="App">
            <Navbar />
            <div>
              <Route exact path="/" component={Home} />
              <Route exact path="/atom-mapping" component={AtomMapping} />
              <Route exact path="/mid-calculation" component={MidCalculation} />
              <Route exact path="/database-query" component={DatabaseQuery} />

              <Route exact path="/reaction-model" component={ReactionModel} />

              <Route exact path="/contact" component={Contact} />
              <Route exact path="/datenschutz" component={Datenschutz} />
              <Route exact path="/impressum" component={Impressum} />

              <ReactionContextProvider>
                <Route
                  exact
                  path="/reaction/:id"
                  component={ReactionContainer}
                />
              </ReactionContextProvider>
              <MetaboliteContextProvider>
                <Route
                  exact
                  path="/metabolite/:id"
                  component={MetaboliteContainer}
                />
              </MetaboliteContextProvider>
              <Route exact path="/pathway/:id" component={PathwayContainer} />

              <Route exact path="/login" component={Login} />
              {/* <Route exact path="/register" component={Register} /> */}
            </div>
            <Footer />
          </div>
        </Router>
      </AuthContextProvider>
    </MainContextProvider>
  );
};

export default App;
