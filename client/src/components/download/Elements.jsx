import React, { useContext } from "react";

import { MetaboliteContext } from "../../contexts/MetaboliteContext";

const Elements = () => {
  const { metabolite } = useContext(MetaboliteContext);
  const { elements } = metabolite;

  const orderedElements = elements.reduce((r, a) => {
    r[a.symbol] = r[a.symbol] || [];
    r[a.symbol].push(a);
    return r;
  }, Object.create(null));

  return (
    <div className="mt-3">
      {Object.entries(orderedElements).map(([key, values], idx) => {
        return (
          <div className={`symbol-${key}`} key={idx}>
            {values.map((value, id) => {
              return (
                <p className="text-muted" key={id}>
                  <strong>name: </strong>
                  {value.name} <strong>symbol: </strong>
                  {value.symbol} <strong>qty: </strong>
                  {value.qty}
                </p>
              );
            })}
          </div>
        );
      })}
    </div>
  );
};

export default Elements;
