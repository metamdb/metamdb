import React, { createContext, useReducer, useEffect } from "react";
import { mainReducer } from "./reducers";

export const MainContext = createContext();

const MainContextProvider = props => {
  const initialState = {
    isReactionModel: false,
    isFluxModel: false,
    elements: null,
    metabolites: null,
    reactions: null,
    labelingData: null,
    atomMappingModel: null,
    alerts: []
  };

  const [contextState, dispatch] = useReducer(mainReducer, initialState, () => {
    const localData = localStorage.getItem("contextState");
    return localData ? JSON.parse(localData) : initialState;
  });

  useEffect(() => {
    localStorage.setItem("contextState", JSON.stringify(contextState));
  }, [contextState]);

  return (
    <MainContext.Provider value={{ contextState, dispatch }}>
      {props.children}
    </MainContext.Provider>
  );
};

export default MainContextProvider;
