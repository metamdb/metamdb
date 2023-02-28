import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import MainContextProvider from "./contexts/MainContext";
import AuthContextProvider from "./contexts/AuthContext";
import ReactionContextProvider from "./contexts/ReactionContext";
import MetaboliteContextProvider from "./contexts/MetaboliteContext";

import Navbar from "./components/layout/Navbar";
import Home from "./components/layout/Home";
import Footer from "./components/layout/Footer";

import AtomMapping from "./components/atom-mapping/AtomMapping";
import LabelingSimulation from "./components/labeling-simulation/LabelingSimulation";
import DatabaseQuery from "./components/database-query/DatabaseQuery";

import ReactionModel from "./components/upload/ReactionModel";

import Contact from "./components/info/Contact";
import Datenschutz from "./components/info/Datenschutz";
import Impressum from "./components/info/Impressum";

import ReactionContainer from "./components/download/Reaction";
import MetaboliteContainer from "./components/download/Metabolite";
import PathwayContainer from "./components/download/Pathway";

import Login from "./components/auth/Login";
import Profile from "./components/user/Profile";
import PostLogin from "./components/auth/PostLogin";

import "./App.css";
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";
import "bootstrap/dist/css/bootstrap.min.css";

import User from "./components/user/User";

const App = (props) => {
  return (
    <MainContextProvider>
      <AuthContextProvider>
        <Router>
          <div className="App">
            <Navbar />
            <Routes>
              <Route exact path="/" element={<Home />} />
              <Route exact path="/atom-mapping" element={<AtomMapping />} />
              <Route
                exact
                path="/simulation"
                element={<LabelingSimulation />}
              />
              <Route exact path="/database-query" element={<DatabaseQuery />} />

              <Route exact path="/reaction-model" element={<ReactionModel />} />

              <Route exact path="/contact" element={<Contact />} />
              <Route exact path="/datenschutz" element={<Datenschutz />} />
              <Route exact path="/impressum" element={<Impressum />} />

              <Route
                exact
                path="/reaction/:id"
                element={
                  <ReactionContextProvider>
                    <ReactionContainer />
                  </ReactionContextProvider>
                }
              />

              <Route
                exact
                path="/metabolite/:id"
                element={
                  <MetaboliteContextProvider>
                    <MetaboliteContainer />
                  </MetaboliteContextProvider>
                }
              />

              <Route exact path="/pathway/:id" element={<PathwayContainer />} />

              <Route exact path="/login" element={<Login />} />
              <Route exact path="/me" element={<Profile />} />
              <Route exact path="/postLogin" element={<PostLogin />} />
              <Route exact path="/user/:id" element={<User />} />
              {/* <Route exact path="/register" component={Register} /> */}
            </Routes>
            <Footer />
          </div>
        </Router>
      </AuthContextProvider>
    </MainContextProvider>
  );
};

export default App;
