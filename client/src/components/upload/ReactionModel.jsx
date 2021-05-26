import React, { useContext, useState } from "react";
import { Link } from "react-router-dom";
import BootstrapTable from "react-bootstrap-table-next";
import cellEditFactory from "react-bootstrap-table2-editor";
import paginationFactory from "react-bootstrap-table2-paginator";
import { CSVLink } from "react-csv";
import Pagination from "react-bootstrap/Pagination";

import { MainContext } from "../../contexts/MainContext";

function reactionLink(cell, row) {
  return (
    <span
      style={{
        width: 50,
      }}
    >
      <Link
        className="text-primary"
        to={`/reaction/${row.identifier}`}
        target="_blank"
      >
        {cell}
      </Link>
    </span>
  );
}

const columns = [
  {
    dataField: "identifier",
    text: "ID",
    editable: false,
    sort: true,
    formatter: reactionLink,
    headerStyle: (colum, colIndex) => {
      return { width: "6%" };
    },
  },
  {
    dataField: "name",
    text: "Name",
    sort: true,
    headerStyle: (colum, colIndex) => {
      return { width: "10%" };
    },
    formatter: (col, row) => {
      return (
        <span
          style={{
            display: "block",
            overflow: "hidden",
            whiteSpace: "nowrap",
            textOverflow: "ellipsis",
          }}
        >
          {col}
        </span>
      );
    },
  },
  {
    dataField: "metabolites.substrate",
    text: "Substrates",
    editable: false,
    formatter: (cell) => {
      return (
        <>
          {cell.map((metabolite, index) => (
            <div key={index}>
              {metabolite.identifier ? (
                <Link
                  key={index}
                  className="btn-link mr-1 ml-1"
                  to={{ pathname: `/metabolite/${metabolite.identifier}` }}
                  target="_blank"
                >
                  {`${metabolite.qty} ${metabolite.name}`}
                </Link>
              ) : (
                <div key={index} className="mr-1 ml-1">
                  {`${metabolite.qty} ${metabolite.name}`}
                </div>
              )}
            </div>
          ))}
        </>
      );
    },
  },
  {
    dataField: "metabolites.product",
    text: "Products",
    editable: false,
    formatter: (cell) => {
      return (
        <>
          {cell.map((metabolite, index) => (
            <div key={index}>
              {metabolite.identifier ? (
                <Link
                  key={index}
                  className="btn-link mr-1 ml-1"
                  to={{ pathname: `/metabolite/${metabolite.identifier}` }}
                  target="_blank"
                >
                  {`${metabolite.qty} ${metabolite.name}`}
                </Link>
              ) : (
                <div key={index} className="mr-1 ml-1">
                  {`${metabolite.qty} ${metabolite.name}`}
                </div>
              )}
            </div>
          ))}
        </>
      );
    },
  },
  {
    dataField: "curated",
    text: "Curated",
    sort: true,
    align: "center",
    headerStyle: (colum, colIndex) => {
      return { width: "9%" };
    },
    formatter: (col, row) => {
      let content;
      if (col === "True") {
        content = <i className="fas fa-check" />;
      } else if (col === "user") {
        content = <i className="fas fa-user" />;
      } else {
        content = <i className="fas fa-times" />;
      }

      return (
        <span
          style={{
            display: "block",
            overflow: "hidden",
            whiteSpace: "nowrap",
            textOverflow: "ellipsis",
          }}
        >
          {content}
        </span>
      );
    },
  },
  {
    dataField: "forward",
    text: "Forward",
    headerStyle: (colum, colIndex) => {
      return { width: "10%" };
    },
    formatter: (col, row) => {
      return (
        <span
          style={{
            display: "block",
            overflow: "hidden",
            whiteSpace: "nowrap",
            textOverflow: "ellipsis",
          }}
        >
          {col}
        </span>
      );
    },
  },
  {
    dataField: "reverse",
    text: "Reverse",
    headerStyle: (colum, colIndex) => {
      return { width: "10%" };
    },
    formatter: (col, row) => {
      return (
        <span
          style={{
            display: "block",
            overflow: "hidden",
            whiteSpace: "nowrap",
            textOverflow: "ellipsis",
          }}
        >
          {col}
        </span>
      );
    },
  },
];

const ReactionModel = () => {
  const { contextState, dispatch } = useContext(MainContext);
  const { reactions } = contextState;

  const goBack = () => {
    dispatch({
      type: "DELETE_REACTION_MODEL",
    });
  };

  let data = reactions.map((reaction) => {
    let substrates = [];
    let products = [];
    reaction.mappings.forEach((aam) => {
      aam.forEach((met) => {
        if (met.reactant === "substrate" && met.mapping !== "") {
          substrates.push(`${met.name} (${met.mapping})`);
        } else if (met.reactant === "product" && met.mapping !== "") {
          products.push(`${met.name} (${met.mapping})`);
        }
      });
    });
    return {
      name: reaction.name,
      substrates: substrates.join(" + "),
      arrow: reaction.arrow,
      products: products.join(" + "),
    };
  });

  const afterSaveCell = () => {
    localStorage.setItem("contextState", JSON.stringify(contextState));
  };
  const [currentPage, setPage] = useState({});
  const setPagination = (index, number) => {
    let currentPageObj = {};
    currentPageObj[index] = number - 1;
    setPage({ ...currentPage, ...currentPageObj });
  };

  const expandRow = {
    onExpand: (row, isExpand, rowIndex, e) => {
      currentPage[row.index - 1] = 0;
    },
    onExpandAll: (isExpandAll, results, e) => {
      results.forEach((row) => {
        currentPage[row.index - 1] = 0;
      });
    },
    renderer: (row, rowIndex) => {
      let pagination;
      let aams;

      if (reactions[row.index - 1].mappings.length > 1) {
        let items = [];
        for (
          let number = 1;
          number <= reactions[row.index - 1].mappings.length;
          number++
        ) {
          items.push(
            <Pagination.Item
              key={number}
              active={number === currentPage[row.index - 1] + 1}
              onClick={() => setPagination(row.index - 1, number)}
            >
              {number}
            </Pagination.Item>
          );
          pagination = <Pagination>{items}</Pagination>;
        }
        aams = reactions[row.index - 1].mappings[
          currentPage[row.index - 1]
        ].map((metabolite, index) => (
          <div key={index} className="row mb-1 mt-1">
            <div className="col-2">
              <input
                type="text"
                className="form-control"
                placeholder="Name"
                value={metabolite.metabolite}
                onChange={(e) =>
                  dispatch({
                    type: "UPDATE_ATOM_MAPPING",
                    payload: {
                      key: "metabolite",
                      value: e.target.value,
                      rowIndex: row.index - 1,
                      index: index,
                    },
                  })
                }
              />
            </div>
            <div className="col">
              <input
                type="text"
                className="form-control"
                placeholder="Name"
                value={metabolite.name}
                onChange={(e) =>
                  dispatch({
                    type: "UPDATE_ATOM_MAPPING",
                    payload: {
                      key: "name",
                      value: e.target.value,
                      rowIndex: row.index - 1,
                      index: index,
                    },
                  })
                }
              />
            </div>
            <div className="col">
              <input
                type="text"
                className="form-control"
                placeholder="Atom mapping"
                value={metabolite.mapping}
                onChange={(e) =>
                  dispatch({
                    type: "UPDATE_ATOM_MAPPING",
                    payload: {
                      value: e.target.value,
                      key: "mapping",
                      rowIndex: row.index - 1,
                      index: index,
                    },
                  })
                }
              />
            </div>
            <div className="col-2">{metabolite.reactant}</div>
          </div>
        ));
      } else {
        aams = reactions[row.index - 1].mappings[0].map((metabolite, index) => (
          <div key={index} className="row mb-1 mt-1">
            <div className="col-2">
              <input
                type="text"
                className="form-control"
                placeholder="Name"
                value={metabolite.metabolite}
                onChange={(e) =>
                  dispatch({
                    type: "UPDATE_ATOM_MAPPING",
                    payload: {
                      key: "metabolite",
                      value: e.target.value,
                      rowIndex: row.index - 1,
                      index: index,
                    },
                  })
                }
              />
            </div>
            <div className="col">
              <input
                type="text"
                className="form-control"
                placeholder="Name"
                value={metabolite.name}
                onChange={(e) =>
                  dispatch({
                    type: "UPDATE_ATOM_MAPPING",
                    payload: {
                      key: "name",
                      value: e.target.value,
                      rowIndex: row.index - 1,
                      index: index,
                    },
                  })
                }
              />
            </div>
            <div className="col">
              <input
                type="text"
                className="form-control"
                placeholder="Atom mapping"
                value={metabolite.mapping}
                onChange={(e) =>
                  dispatch({
                    type: "UPDATE_ATOM_MAPPING",
                    payload: {
                      value: e.target.value,
                      key: "mapping",
                      rowIndex: row.index - 1,
                      index: index,
                    },
                  })
                }
              />
            </div>
            <div className="col-2">{metabolite.reactant}</div>
          </div>
        ));
      }

      return (
        <div>
          <div>{pagination}</div>
          {aams}
        </div>
      );
    },
    showExpandColumn: true,
    expandByColumnOnly: true,
    expandColumnPosition: "left",
    headerStyle: (colum, colIndex) => {
      return { width: "6%" };
    },
    expandHeaderColumnRenderer: ({ isAnyExpands }) => {
      if (isAnyExpands) {
        return <b>-</b>;
      }
      return <b>+</b>;
    },
    expandColumnRenderer: ({ expanded }) => {
      if (expanded) {
        return <b>-</b>;
      }
      return <b>+</b>;
    },
  };

  return (
    <>
      <div className="row">
        <div className="col-5">
          <h1>Reaction Model</h1>
        </div>

        <div className="col-7">
          <CSVLink
            className="btn btn-primary"
            data={data}
            filename={"aam_model.csv"}
            target="_blank"
          >
            Download Model
          </CSVLink>
          <button
            type="button"
            className="btn btn-danger float-right"
            onClick={goBack}
          >
            <i className="fas fa-arrow-left" /> Go Back
          </button>
        </div>
      </div>
      <div className="model">
        <BootstrapTable
          keyField="index"
          data={reactions}
          columns={columns}
          cellEdit={cellEditFactory({
            mode: "dbclick",
            afterSaveCell: afterSaveCell,
          })}
          pagination={paginationFactory({
            sizePerPageList: [
              {
                text: "10",
                value: 10,
              },
              {
                text: "25",
                value: 25,
              },
              {
                text: "50",
                value: 50,
              },
              {
                text: "100",
                value: 100,
              },
              {
                text: "All",
                value: reactions.length,
              },
            ],
            sizePerPage: 50,
          })}
          expandRow={expandRow}
          bootstrap4
        />
      </div>
    </>
  );
};

export default ReactionModel;
