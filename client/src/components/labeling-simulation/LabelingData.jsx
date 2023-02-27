import React, { useContext } from "react";
import { CSVLink } from "react-csv";
import { MainContext } from "../../contexts/MainContext";

const makeCsvData = (mids) => {
  let res = mids.map((mid) => {
    let res2 = mid.data.map((entry, index) => {
      return { name: mid.name, mass: index, data: entry };
    });
    return res2;
  });
  return res.flat(1);
};

const LabelingData = () => {
  const { contextState } = useContext(MainContext);
  const csvData = React.useMemo(
    () => makeCsvData(contextState.mids),
    [contextState.mids]
  );
  return (
    <div className="labeling-data">
      <div class="row">
        <div class="col text-center">
          <CSVLink
            className="btn btn-primary mt-3 text-center"
            data={csvData}
            filename={"sim_mids.csv"}
            target="_blank"
          >
            Download MIDs
          </CSVLink>
        </div>
      </div>

      <div
        id="accordion"
        className="LabelingFeed mt-3"
        role="tablist"
        aria-multiselectable="true"
      >
        {contextState.mids.map((entry, index) => (
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

export default LabelingData;
