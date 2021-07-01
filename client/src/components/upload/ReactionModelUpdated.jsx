import React, { useContext, useState } from "react";
import { CSVLink } from "react-csv";
import { Link } from "react-router-dom";
import {
  useTable,
  usePagination,
  useSortBy,
  useFilters,
  useExpanded,
  useResizeColumns,
  useFlexLayout,
} from "react-table";
import styled from "styled-components";
import { Popover, OverlayTrigger, Button } from "react-bootstrap";
import Pagination from "react-bootstrap/Pagination";
import no_aam from "../../shared/no_aam.png";

import { MainContext } from "../../contexts/MainContext";

const Styles = styled.div`
  padding: 1rem;
  ${"" /* These styles are suggested for the table fill all available space in its containing element */}
  display: block;
  ${"" /* These styles are required for a horizontaly scrollable table overflow */}
  overflow: auto;

  table {
    border-spacing: 0;
    border: 1px solid black;

    .thead {
      ${"" /* These styles are required for a scrollable body to align with the header properly */}
      overflow-y: auto;
      overflow-x: hidden;
    }

    .tbody {
      ${"" /* These styles are required for a scrollable table body */}
      overflow-y: scroll;
      overflow-x: hidden;
      height: 250px;
    }

    tr {
      :last-child {
        td {
          border-bottom: 0;
        }
      }
    }

    th,
    td {
      margin: 0;
      padding: 0.5rem;
      border-bottom: 1px solid black;
      border-right: 1px solid black;

      ${"" /* In this example we use an absolutely position resizer,
        so this is required. */}
      position: relative;

      :last-child {
        border-right: 0;
      }
      .resizer {
        right: 0;
        background: blue;
        width: 10px;
        height: 100%;
        position: absolute;
        top: 0;
        z-index: 1;
        ${"" /* prevents from scrolling while dragging on touch devices */}
        touch-action :none;

        &.isResizing {
          background: red;
        }
      }
    }

    td {
      input {
        font-size: 1rem;
        padding: 0;
        margin: 0;
        border: 0;
      }
    }
  }

  .pagination {
    padding: 0.5rem;
  }
`;

function SelectColumnFilter({
  column: { filterValue, setFilter, preFilteredRows, id },
}) {
  const options = React.useMemo(() => {
    const options = new Set();
    preFilteredRows.forEach((row) => {
      options.add(row.values[id]);
    });
    return [...options.values()];
  }, [id, preFilteredRows]);

  return (
    <select
      value={filterValue}
      onChange={(e) => {
        setFilter(e.target.value || undefined);
      }}
    >
      <option value="">All</option>
      {options.map((option, i) => {
        let content;
        if (option === "True") {
          content = "Yes";
        } else if (option === "user") {
          content = "User";
        } else {
          content = "No";
        }

        return (
          <option key={i} value={option}>
            {content}
          </option>
        );
      })}
    </select>
  );
}

const ReactionModel = () => {
  const { contextState, dispatch } = useContext(MainContext);
  const { reactions } = contextState;

  const goBack = () => {
    dispatch({
      type: "DELETE_REACTION_MODEL",
    });
  };

  const columns = React.useMemo(
    () => [
      {
        // Make an expander cell
        Header: ({ getToggleAllRowsExpandedProps, isAllRowsExpanded }) => (
          <span {...getToggleAllRowsExpandedProps()}>
            {isAllRowsExpanded ? "👇" : "👉"}
          </span>
        ),
        id: "expander", // It needs an ID
        width: 60,
        minWidth: 60,
        maxWidth: 60,
        Cell: ({ row }) => (
          // Use Cell to render an expander for each row.
          // We can use the getToggleRowExpandedProps prop-getter
          // to build the expander.
          <span {...row.getToggleRowExpandedProps()}>
            {row.isExpanded ? "👇" : "👉"}
          </span>
        ),
      },
      {
        Header: "ID",
        accessor: "identifier",
        Cell: reactionLink,
        width: 60,
        maxwidth: 80,
        minWidth: 50,
      },
      {
        Header: "Name",
        accessor: "name",
        width: 250,
        // Cell: EditableCell,
      },
      {
        Header: "Substrates",
        accessor: "metabolites.substrate",
        disableSortBy: true,
        Cell: metaboliteCell,
        width: 300,
        minWidth: 200,
      },
      {
        Header: "Products",
        accessor: "metabolites.product",
        disableSortBy: true,
        Cell: metaboliteCell,
        width: 300,
        minWidth: 200,
      },
      {
        Header: "Curated",
        accessor: "curated",
        Cell: curatedIcon,
        Filter: SelectColumnFilter,
        filter: "includes",
        width: 100,
      },
      {
        Header: "Image",
        ID: "imgId",
        accessor: (row) => row.identifier,
        Cell: mappingImage,
        width: 100,
      },
      {
        Header: "Conversion",
        accessor: "conversion",
        Cell: mappingConversion,
        width: 100,
      },
    ],
    []
  );

  const csvData = React.useMemo(() => makeCsvData(reactions), [reactions]);
  const [data, setData] = React.useState(() => reactions);

  const updateMyData = (rowIndex, columnId, value) => {
    setData((old) =>
      old.map((row, index) => {
        if (index === rowIndex) {
          return {
            ...old[rowIndex],
            [columnId]: value,
          };
        }
        return row;
      })
    );
  };

  const [currentPage, setPage] = useState({});
  const setPagination = (index, number) => {
    let currentPageObj = {};
    currentPageObj[index] = number - 1;
    setPage({ ...currentPage, ...currentPageObj });
  };

  const renderRowSubComponent = React.useCallback(
    ({ row }) => {
      let pagination;
      let aams;
      console.log(reactions);
      console.log(row);
      if (reactions[row.index].mappings.length > 1) {
        let items = [];
        for (
          let number = 1;
          number <= reactions[row.index].mappings.length;
          number++
        ) {
          items.push(
            <Pagination.Item
              key={number}
              active={number === currentPage[row.index] + 1}
              onClick={() => setPagination(row.index, number)}
            >
              {number}
            </Pagination.Item>
          );
          pagination = <Pagination>{items}</Pagination>;
        }
        aams = reactions[row.index].mappings[currentPage[row.index]].map(
          (metabolite, index) => (
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
                        rowIndex: row.index,
                        index: index,
                        currentMapping: currentPage[row.index],
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
                        rowIndex: row.index,
                        index: index,
                        currentMapping: currentPage[row.index],
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
                        rowIndex: row.index,
                        index: index,
                        currentMapping: currentPage[row.index],
                      },
                    })
                  }
                />
              </div>
              <div className="col-2">{metabolite.reactant}</div>
            </div>
          )
        );
      } else if (reactions[row.index].mappings.length === 0) {
        aams = (
          <div className="">
            <h3>Sorry, sadly there is no atom mapping!</h3>
          </div>
        );
      } else {
        aams = reactions[row.index].mappings[0].map((metabolite, index) => (
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
                      rowIndex: row.index,
                      index: index,
                      currentMapping: currentPage[row.index],
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
                      rowIndex: row.index,
                      index: index,
                      currentMapping: currentPage[row.index],
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
                      rowIndex: row.index,
                      index: index,
                      currentMapping: currentPage[row.index],
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

    []
  );

  return (
    <>
      <div className="row">
        <div className="col-5">
          <h1>Atom Mapping Model</h1>
        </div>

        <div className="col-7">
          <CSVLink
            className="btn btn-primary"
            data={csvData}
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
        <Styles>
          <Table
            columns={columns}
            data={data}
            updateMyData={updateMyData}
            renderRowSubComponent={renderRowSubComponent}
          />
        </Styles>
      </div>
    </>
  );
};

export default ReactionModel;

const Table = ({ columns, data, updateMyData, renderRowSubComponent }) => {
  const defaultColumn = React.useMemo(
    () => ({
      // Let's set up our default Filter UI
      Filter: "",
      minWidth: 50,
      width: 200,
      maxWidth: 350,
    }),
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    prepareRow,
    page, // Instead of using 'rows', we'll use page,
    // which has only the rows for the active page

    // The rest of these things are super handy, too ;)
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setPageSize,
    visibleColumns,
    state: { pageIndex, pageSize },
  } = useTable(
    {
      columns,
      data,
      defaultColumn,
      initialState: { pageIndex: 0 },
      updateMyData,
      renderRowSubComponent,
    },
    useFilters,
    useSortBy,
    useResizeColumns,
    useFlexLayout,

    useExpanded,
    usePagination
  );

  return (
    <>
      <table {...getTableProps()}>
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                // Add the sorting props to control sorting. For this example
                // we can add them into the header props
                <th {...column.getHeaderProps()}>
                  <div>
                    <span {...column.getSortByToggleProps()}>
                      {column.render("Header")}
                      {/* Add a sort direction indicator */}
                      {column.isSorted
                        ? column.isSortedDesc
                          ? " 🔽"
                          : " 🔼"
                        : ""}
                      {column.canResize && (
                        <div
                          {...column.getResizerProps()}
                          className={`resizer ${
                            column.isResizing ? "isResizing" : ""
                          }`}
                        />
                      )}
                    </span>
                  </div>
                  <div>{column.canFilter ? column.render("Filter") : null}</div>
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {page.map((row, i) => {
            prepareRow(row);
            return (
              <>
                <tr {...row.getRowProps()}>
                  {row.cells.map((cell) => {
                    return (
                      <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
                    );
                  })}
                </tr>
                {/*
                    If the row is in an expanded state, render a row with a
                    column that fills the entire length of the table.
                  */}
                {row.isExpanded ? (
                  <tr>
                    <td colSpan={visibleColumns.length}>
                      {/*
                          Inside it, call our renderRowSubComponent function. In reality,
                          you could pass whatever you want as props to
                          a component like this, including the entire
                          table instance. But for this example, we'll just
                          pass the row
                        */}
                      {renderRowSubComponent({ row })}
                    </td>
                  </tr>
                ) : null}
              </>
            );
          })}
        </tbody>
      </table>
      {/* 
        Pagination can be built however you'd like. 
        This is just a very basic UI implementation:
      */}
      <div className="pagination">
        <button onClick={() => gotoPage(0)} disabled={!canPreviousPage}>
          {"<<"}
        </button>{" "}
        <button onClick={() => previousPage()} disabled={!canPreviousPage}>
          {"<"}
        </button>{" "}
        <button onClick={() => nextPage()} disabled={!canNextPage}>
          {">"}
        </button>{" "}
        <button onClick={() => gotoPage(pageCount - 1)} disabled={!canNextPage}>
          {">>"}
        </button>{" "}
        <span>
          Page{" "}
          <strong>
            {pageIndex + 1} of {pageOptions.length}
          </strong>{" "}
        </span>
        <span>
          | Go to page:{" "}
          <input
            type="number"
            defaultValue={pageIndex + 1}
            onChange={(e) => {
              const page = e.target.value ? Number(e.target.value) - 1 : 0;
              gotoPage(page);
            }}
            style={{ width: "100px" }}
          />
        </span>{" "}
        <select
          value={pageSize}
          onChange={(e) => {
            setPageSize(Number(e.target.value));
          }}
        >
          {[10, 20, 30, 40, 50].map((pageSize) => (
            <option key={pageSize} value={pageSize}>
              Show {pageSize}
            </option>
          ))}
        </select>
      </div>
    </>
  );
};

const makeCsvData = (reactions) => {
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
  return data;
};

function reactionLink({ value }) {
  return (
    <Link className="text-primary" to={`/reaction/${value}`} target="_blank">
      {value}
    </Link>
  );
}

function curatedIcon({ value }) {
  let content;
  if (value === "True") {
    content = <i className="fas fa-check" />;
  } else if (value === "user") {
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
        textAlign: "center",
      }}
    >
      {content}
    </span>
  );
}

function metaboliteCell({ value }) {
  return (
    <>
      {value.map((metabolite, index) => (
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
}

function mappingImage({ value }) {
  const StyledPopoverImage = styled(Popover)`
    min-width: 1000px;
  `;

  const imageSource = `${process.env.PUBLIC_URL}/img/aam/${value}.svg`;

  const popoverImage = (
    <StyledPopoverImage id="popover" className="shadow">
      <StyledPopoverImage.Title as="h3">
        Atom Transition Image {value}
      </StyledPopoverImage.Title>
      <StyledPopoverImage.Content>
        <img
          src={imageSource}
          onError={(e) => {
            e.target.onError = null;
            e.target.src = no_aam;
          }}
          alt={`Structure Atom Mapping ${value}`}
          style={{ width: "100%" }}
        />
      </StyledPopoverImage.Content>
    </StyledPopoverImage>
  );

  return (
    <>
      <OverlayTrigger
        placement="left"
        trigger={["click"]}
        overlay={popoverImage}
      >
        <Button variant="link">Click</Button>
      </OverlayTrigger>
    </>
  );
}

function mappingConversion({ value }) {
  let abcString;
  abcString = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

  let valueCopy = Object.assign({}, value);

  Object.keys(value).forEach((key) => {
    valueCopy[key] = abcString.charAt(value[key]);
  });

  const StyledPopover = styled(Popover)`
    min-width: 100px;
  `;

  const popover = (
    <StyledPopover id="popover" className="shadow">
      <StyledPopover.Content>
        {Object.keys(value).length ? (
          <ul className="list-group">
            {Object.keys(valueCopy).map((key, index) => (
              <li key={index} className="list-group-item">
                {key} = {valueCopy[key]}
              </li>
            ))}
          </ul>
        ) : (
          <h3>No Conversion</h3>
        )}
      </StyledPopover.Content>
    </StyledPopover>
  );

  return (
    <>
      <OverlayTrigger
        placement="right"
        trigger={["focus", "hover"]}
        overlay={popover}
      >
        <Button variant="link">Click</Button>
      </OverlayTrigger>
    </>
  );
}
