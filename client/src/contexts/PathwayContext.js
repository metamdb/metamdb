import React, { createContext, useState } from "react";

export const MetaboliteContext = createContext();

const MetaboliteContextProvider = props => {
  const initialState = {
    id: null,
    name: "",
    inchi: "",
    inchiShort: "",
    inchiKey: "",
    formula: "",
    file: null,
    elements: [],
    identifiers: [],
    reactions: []
  };

  const [metabolite, setMetabolite] = useState(initialState);

  return (
    <MetaboliteContext.Provider value={{ metabolite, setMetabolite }}>
      {props.children}
    </MetaboliteContext.Provider>
  );
};

export default MetaboliteContextProvider;