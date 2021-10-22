import React, { useState, useEffect } from "react";
import classnames from "classnames";
import axios from "axios";
import qs from "qs";
import { Link, useLocation } from "react-router-dom";
import Alerts from "../common/Alerts";

import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";

function reactionLink(cell, row) {
  return (
    <span
      style={{
        width: 50,
      }}
    >
      <Link className="text-primary" to={`/reaction/${row.id}`} target="_blank">
        {cell}
      </Link>
    </span>
  );
}

function pathwayLink(cell, row) {
  return (
    <span
      style={{
        width: 50,
      }}
    >
      <Link className="text-primary" to={`/pathway/${cell}`} target="_blank">
        {cell}
      </Link>
    </span>
  );
}

function identifierFormatter(cell, row) {
  return cell ? (
    <span
      style={{
        width: 50,
      }}
    >
      {cell
        .map((entry) => {
          return entry.databaseIdentifier;
        })
        .join(" , ")}
    </span>
  ) : null;
}

function iconFormatter(cell, row) {
  return (
    <span
      style={{
        width: 50,
      }}
    >
      {cell ? <i className="fas fa-check" /> : <i className="fas fa-times" />}
    </span>
  );
}

const columnsPathway = [
  {
    dataField: "name",
    text: "Name",
    headerStyle: (colum, colIndex) => {
      return { width: "30%" };
    },
  },
  {
    dataField: "pw_id",
    text: "Pathway ID",
    sort: true,
    headerStyle: (colum, colIndex) => {
      return { width: "10%" };
    },
    formatter: pathwayLink,
  },
  {
    dataField: "source_id",
    text: "Identifier",
    sort: true,
    headerStyle: (colum, colIndex) => {
      return { width: "10%" };
    },
  },
  {
    dataField: "source",
    text: "Source",
    sort: true,
    headerStyle: (colum, colIndex) => {
      return { width: "10%" };
    },
  },
];

const columnsReaction = [
  {
    dataField: "identifiers",
    text: "Name",
    headerStyle: (colum, colIndex) => {
      return { width: "20%" };
    },
    formatter: identifierFormatter,
  },
  {
    dataField: "id",
    text: "Reaction ID",
    sort: true,
    headerStyle: (colum, colIndex) => {
      return { width: "10%" };
    },
    formatter: reactionLink,
  },

  {
    dataField: "formula",
    text: "Formula",
    headerStyle: (colum, colIndex) => {
      return { width: "30%" };
    },
  },
  {
    dataField: "updated",
    text: "Curated",
    sort: true,
    headerStyle: (colum, colIndex) => {
      return { width: "12%" };
    },
    formatter: iconFormatter,
  },
];

const DatabaseQuery = (props) => {
  const [reaction, setReaction] = useState("");
  const [type, setType] = useState("name");
  const [feed, setFeed] = useState(null);
  const [loading, setLoading] = useState(false);
  const [alerts, setAlerts] = useState(null);

  const searchPlaceholder = {
    name: "Search Reaction...",
    metabolite: "Search Metabolite...",
    pathway: "Search Pathway...",
  };

  const location = useLocation();
  useEffect(() => {
    if (location.search) {
      let query = qs.parse(location.search, { ignoreQueryPrefix: true });
      let keys = Object.keys(query);

      const reactionData = new FormData();
      reactionData.append("query", query[keys[0]]);
      reactionData.append("type", keys[0]);

      setLoading(true);

      axios
        .post("/api/query", reactionData)
        .then((res) => {
          setFeed(res.data);
          setLoading(false);
          setAlerts(null);
        })
        .catch((err) => {
          console.log(err.response.data);
          setFeed(null);
          setLoading(false);
          setAlerts(err.response.data);
        });
    }
  }, [location]);

  const columns = {
    name: columnsReaction,
    metabolite: columnsReaction,
    pathway: columnsPathway,
  };
  useEffect(() => {
    setFeed(null);
  }, [type]);

  const handleSubmit = (event) => {
    event.preventDefault();

    const reactionData = new FormData();
    reactionData.append("query", reaction);
    reactionData.append("type", type);
    if (reaction) {
      setLoading(true);
    }
    axios
      .post("/api/query", reactionData)
      .then((res) => {
        setFeed(res.data);
        setLoading(false);
        setAlerts(null);
      })
      .catch((err) => {
        setFeed(null);
        setLoading(false);
        setAlerts(err.response.data);
      });
  };

  return (
    <div className="feed">
      <div className="content">
        <div className="container">
          <h1>Database Query</h1>
          <p className="lead text-muted">
            The database can be queried for reaction names as well as metabolite
            names. The type of query can be changed by clicking on the dropdown
            menu. The search is performed with a fuzzy match algorithm, meaning
            that patterns are matched. For example Glucose not only matches
            D-Glucose but also Glucose-6-phosphate (Glucose{" "}
            <i className="fas fa-long-arrow-alt-right"></i>{" "}
            D-Glucose/Glucose-6-phosphate). <br />
            Further information{" "}
            <a
              href="https://collinstark.github.io/metamdb-docs/database-search"
              target="_blank"
              rel="noopener noreferrer"
            >
              can be found in the documentation.
            </a>
          </p>
          <div className="reaction-form">
            <div className="form-row">
              <form onSubmit={handleSubmit} className="form-group">
                <div className="input-group">
                  <div className="input-group-append">
                    <select
                      className="form-select"
                      onChange={(e) => setType(e.target.value)}
                    >
                      <option default value="name">
                        Reaction
                      </option>
                      <option value="metabolite">Metabolite</option>
                      <option value="pathway">Pathway</option>
                    </select>
                  </div>
                  <input
                    type="text"
                    name="text"
                    value={reaction}
                    onChange={(e) => setReaction(e.target.value)}
                    className={classnames("form-control")}
                    placeholder={searchPlaceholder[type]}
                    aria-label="reaction"
                    aria-describedby="button-reaction"
                  />
                  <div className="input-group-append">
                    <button type="submit" className="btn btn-dark">
                      <i className="fas fa-search" />
                    </button>
                  </div>
                </div>
              </form>
            </div>
            {alerts && <Alerts alerts={alerts} />}
            <div className="form-feed">
              {loading && <i className="fas fa-spinner fa-pulse" />}
              {feed && (
                <BootstrapTable
                  keyField="index"
                  data={feed}
                  columns={columns[type]}
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
                        value: feed.length,
                      },
                    ],
                    sizePerPage: 50,
                  })}
                  bootstrap4
                  striped
                  bordered={false}
                />
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DatabaseQuery;
