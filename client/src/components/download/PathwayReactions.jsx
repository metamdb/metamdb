import React, { useContext, useState } from "react";
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
import no_aam from "../../shared/no_aam.png";

const Styles = styled.div`
  padding: 1rem;
  ${
    "" /* These styles are suggested for the table fill all available space in its containing element */
  }
  display: block;
  ${
    "" /* These styles are required for a horizontaly scrollable table overflow */
  }
  overflow: auto;

  table {
    .thead {
      ${
        "" /* These styles are required for a scrollable body to align with the header properly */
      }
      overflow-y: auto;
      overflow-x: hidden;
    }

    .tbody {
      ${"" /* These styles are required for a scrollable table body */}
      overflow-y: scroll;
      overflow-x: hidden;
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
      ${
        "" /* In this example we use an absolutely position resizer,
        so this is required. */
      }
      position: relative;

      :last-child {
        border-right: 0;
      }
      .resizer {
        display: inline-block;
        background: #a6a6a600;
        width: 15px;
        height: 100%;
        position: absolute;
        right: 0;
        top: 0;
        transform: translateX(50%);
        z-index: 1;
        touch-action :none;


      }
     
        

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
      className="custom-select"
      value={filterValue}
      onChange={(e) => {
        setFilter(e.target.value || undefined);
      }}
    >
      <option value="">All</option>
      {options.map((option, i) => {
        let content;
        if (option === true) {
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

const PathwayReactions = ({ reactions }) => {
  const columns = React.useMemo(
    () => [
      {
        Header: "ID",
        accessor: "id",
        Cell: reactionLink,
        width: 50,
        maxwidth: 60,
        minWidth: 40,
      },
      {
        Header: "Formula",
        accessor: "formula",
        width: 400,
      },
      {
        Header: "Curated",
        accessor: "updated",
        Cell: curatedIcon,
        Filter: SelectColumnFilter,
        filter: "exactTextCase",
        width: 60,
        maxwidth: 60,
      },
      {
        Header: "Image",
        accessor: (row) => row.id,
        Cell: mappingImage,
        width: 60,
        maxwidth: 60,
        disableSortBy: true,
      },
    ],
    []
  );

  console.log("reactions", reactions);
  const data = React.useMemo(() => reactions, [reactions]);

  console.log(typeof data);

  return (
    <>
      <div className="model">
        <Styles>
          <Table columns={columns} data={data} />
        </Styles>
      </div>
    </>
  );
};

export default PathwayReactions;

const Table = ({ columns, data }) => {
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
    page,
    rows,
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
      <table
        className="table table-striped table-bordered"
        {...getTableProps()}
      >
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th {...column.getHeaderProps()}>
                  <div>
                    <span {...column.getSortByToggleProps()}>
                      {column.render("Header")}
                      {"  "}
                      {column.isSorted ? (
                        column.isSortedDesc ? (
                          <i className="fas fa-sort-down"></i>
                        ) : (
                          <i className="fas fa-sort-up"></i>
                        )
                      ) : column.canSort ? (
                        <i className="fas fa-sort"></i>
                      ) : (
                        ""
                      )}
                    </span>
                    {column.canResize && (
                      <div
                        {...column.getResizerProps()}
                        className={`resizer ${
                          column.isResizing ? "isResizing" : ""
                        }`}
                      />
                    )}
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
              </>
            );
          })}
        </tbody>
      </table>

      <nav aria-label="atom mapping navigation">
        <div className="row">
          <div className="col-md-5">
            <div className="mt-3">
              <span>
                Showing <strong>{pageIndex * pageSize + 1}</strong> to{" "}
                <strong>{(pageIndex + 1) * pageSize}</strong> of{" "}
                <strong>{rows.length}</strong> results
              </span>
            </div>
          </div>
          <div className="col-md-2">
            <select
              className="mt-3 custom-select"
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
          <div className="col-md-5">
            <ul className="pagination float-right">
              <li className="page-item">
                <button
                  className="page-link"
                  onClick={() => gotoPage(0)}
                  disabled={!canPreviousPage}
                >
                  <span aria-hidden="true">&laquo;</span>
                </button>
              </li>
              <li className="page-item">
                <button
                  className="page-link"
                  onClick={() => previousPage()}
                  disabled={!canPreviousPage}
                >
                  &lt;
                </button>
              </li>
              <li className="page-item">
                <button
                  className="page-link"
                  onClick={() => nextPage()}
                  disabled={!canNextPage}
                >
                  &gt;
                </button>
              </li>
              <li className="page-item">
                <button
                  className="page-link"
                  onClick={() => gotoPage(pageCount - 1)}
                  disabled={!canNextPage}
                >
                  &raquo;
                </button>{" "}
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </>
  );
};

function curatedIcon({ value }) {
  let content;
  if (value === true) {
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

function reactionLink({ value }) {
  return (
    <Link className="text-primary" to={`/reaction/${value}`} target="_blank">
      {value}
    </Link>
  );
}
