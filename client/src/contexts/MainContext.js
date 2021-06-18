import React, { createContext, useReducer } from "react";
import { mainReducer } from "./reducers";

export const MainContext = createContext();

const MainContextProvider = (props) => {
  const initialState = {
    isReactionModel: false,
    reactions: null,
    alerts: [],
  };

  const [contextState, dispatch] = useReducer(mainReducer, initialState);

  return (
    <MainContext.Provider value={{ contextState, dispatch }}>
      {props.children}
    </MainContext.Provider>
  );
};

export default MainContextProvider;
