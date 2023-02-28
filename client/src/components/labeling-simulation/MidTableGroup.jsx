import React, { useState, useContext } from "react";
import classnames from "classnames";

import { MainContext } from "../../contexts/MainContext";

const MidTableGroup = props => {
  const { contextState } = useContext(MainContext);

  const { errors, element, tracer } = props;

  let midTableFeed;
  if (tracer.length === 0) {
    midTableFeed = null;
  } else {
    midTableFeed = (
      <table className="table table-borderless">
        <thead>
          <tr>
            <th>Metabolite</th>
            <th>Labeling State</th>
            <th>Purity</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {tracer.map((item, index) => (
            <tr key={index}>
              <td>
                {item.metaboliteName}
                {errors[`metabolite_${index}`] && (
                  <div className="invalid-feedback">
                    {errors[`metabolite_${index}`]}
                  </div>
                )}
              </td>
              <td>
                {item.labeling}
                {errors[`labeling_${index}`] ? (
                  <div className="invalid-feedback">
                    {errors[`labeling_${index}`]}
                  </div>
                ) : null}
              </td>
              <td>
                {item.purity}
                {errors[`purity_${index}`] && (
                  <div className="invalid-feedback">
                    {errors[`purity_${index}`]}
                  </div>
                )}
              </td>
              <td>
                <button
                  className="btn btn-outline-danger float-right"
                  type="button"
                  onClick={props.removeTracer.bind(this, item.id)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }

  return (
    <div className="midtablegroup">
      <div className="form-group">
        <table className="table table-borderless">
          <tbody>
            <tr>
              <td className="pr-0">
                <select
                  name="metabolite"
                  id="metabolite"
                  className={classnames("form-control float-left", {
                    "is-invalid": errors.metabolite
                  })}
                  style={{ width: "auto" }}
                  onChange={props.handler}
                  value={props.metabolite}
                >
                  <option value="">Select Tracer...</option>
                  {element
                    ? contextState.metabolites[element].map(metabolite => (
                        <option key={metabolite.name} value={metabolite.id}>
                          {metabolite.name}
                        </option>
                      ))
                    : null}
                </select>
                {errors.metabolite && (
                  <div className="invalid-feedback">{errors.metabolite}</div>
                )}
              </td>
              <td>
                <input
                  name="labeling"
                  id="labeling"
                  type="number"
                  placeholder="Labeling State..."
                  className={classnames("form-control", {
                    "is-invalid": errors.labeling
                  })}
                  onChange={props.handler}
                  value={props.labeling}
                />
                {errors.labeling && (
                  <div className="invalid-feedback">{errors.labeling}</div>
                )}
              </td>
              <td>
                <input
                  name="purity"
                  id="purity"
                  type="number"
                  step="0.01"
                  placeholder="Purity..."
                  className={classnames("form-control", {
                    "is-invalid": errors.purity
                  })}
                  onChange={props.handler}
                  value={props.purity}
                />
                {errors.purity && (
                  <div className="invalid-feedback">{errors.purity}</div>
                )}
              </td>
              <td>
                <button
                  className="btn btn-outline-success float-right"
                  type="button"
                  onClick={props.addTracer.bind(this)}
                >
                  Add
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        {midTableFeed}
      </div>
    </div>
  );
};

export default MidTableGroup;
