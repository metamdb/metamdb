import React, { createContext, useReducer, useEffect } from "react";
import { authReducer } from "./reducers";

export const AuthContext = createContext();

const AuthContextProvider = props => {
  const initialState = {
    id: null,
    name: null,
    isUser: false
  };

  const [authState, authDispatch] = useReducer(
    authReducer,
    initialState,
    () => {
      const localData = localStorage.getItem("authState");
      return localData ? JSON.parse(localData) : initialState;
    }
  );

  useEffect(() => {
    localStorage.setItem("authState", JSON.stringify(authState));
  }, [authState]);

  return (
    <AuthContext.Provider value={{ authState, authDispatch }}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthContextProvider;
