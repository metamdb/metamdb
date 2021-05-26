import React, { useContext } from "react";
import { MainContext } from "../../contexts/MainContext";
import GoBackHeader from "../headers/GoBackHeader";

const MidFeed = (props) => {
  const { contextState } = useContext(MainContext);

  return (
    <div className="feed">
      <GoBackHeader
        title="MID Calculation - Results"
        type="DELETE_LABELING_DATA"
      />

      <p className="lead text-muted">
        Mass isotopomer distributions for all chosen products.
      </p>
      <div
        id="accordion"
        className="midfeed"
        role="tablist"
        aria-multiselectable="true"
      >
        {contextState.labelingData.map((entry, index) => (
          <div className="card" key={index}>
            <h5 className="card-header" role="tab" id={`heading${index}`}>
              <a
                data-toggle="collapse"
                data-parent="#accordion"
                href={`#collapse${index}`}
                aria-expanded="false"
                aria-controls={`collapse${index}`}
                className="d-block collapsed"
              >
                {entry.name}
                <i className="fa fa-chevron-down float-right" />
              </a>
            </h5>

            <div
              id={`collapse${index}`}
              className="collapse"
              role="tabpanel"
              aria-labelledby={`heading${index}`}
            >
              <div className="card-body table-responsive">
                <table className="table table-striped">
                  <thead>
                    <tr>
                      <th scope="col">Mass Isotopomers</th>
                      <th scope="col">{entry.name}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {entry.data.map((isotopomer, key) => (
                      <tr key={key}>
                        <td>{`M+${key}`}</td>
                        <td>{isotopomer.toFixed(4)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MidFeed;
