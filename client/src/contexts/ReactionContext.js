import React, { createContext, useState } from "react";

export const ReactionContext = createContext();

const ReactionContextProvider = props => {
  const initialState = {
    id: null,
    formula: "",
    atomTransitions: [],
    compounds: [],
    identifiers: []
  };

  const [reaction, setReaction] = useState(initialState);

  return (
    <ReactionContext.Provider value={{ reaction, setReaction }}>
      {props.children}
    </ReactionContext.Provider>
  );
};

export default ReactionContextProvider;
