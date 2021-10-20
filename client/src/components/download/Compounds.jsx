import React, { useContext } from "react";
import { Link } from "react-router-dom";

import { ReactionContext } from "../../contexts/ReactionContext";

const Compounds = () => {
  const { reaction } = useContext(ReactionContext);
  const { compounds } = reaction;
  const unorderedCompounds = compounds.reduce((r, a) => {
    r[a.reactant] = r[a.reactant] || [];
    r[a.reactant].push(a);
    return r;
  }, Object.create(null));
  const orderedCompounds = {};
  Object.keys(unorderedCompounds)
    .reverse()
    .forEach(function(key) {
      orderedCompounds[key] = unorderedCompounds[key];
    });

  return (
    <div className="mt-3">
      <table className="table table-striped">
        <thead>
          <tr>
            <th scope="col">Substrates</th>
            <th scope="col">Products</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              {orderedCompounds.substrate
                ? orderedCompounds.substrate.map((metabolite, id) => (
                    <Link
                      key={id}
                      className="btn-link mr-1 ml-1"
                      to={{ pathname: `/metabolite/${metabolite.compound.id}` }}
                      target="_blank"
                    >
                      {metabolite.compound.name}
                    </Link>
                  ))
                : "No substrates"}
            </td>
            <td>
              {orderedCompounds.product
                ? orderedCompounds.product.map((metabolite, id) => (
                    <Link
                      key={id}
                      className="btn-link mr-1 ml-1"
                      to={{ pathname: `/metabolite/${metabolite.compound.id}` }}
                      target="_blank"
                    >
                      {metabolite.compound.name}
                    </Link>
                  ))
                : "No products"}
            </td>
          </tr>
          {/* {entry.data.map((isotopomer, key) => (
                      <tr key={key}>
                        <td>{`M+${key}`}</td>
                        <td>{isotopomer.toFixed(3)}</td>
                      </tr>
                    ))} */}
        </tbody>
      </table>
    </div>
  );
};

export default Compounds;
