import React from "react";
import classnames from "classnames";
import classNames from "classnames/bind";

const Alerts = ({ alerts }) => {
  const alertStyles = {
    INFO: "alert-info",
    WARNING: "alert-warning",
    ERROR: "alert-danger",
  };

  const alertClasses = classNames.bind(alertStyles);

  if (typeof alerts !== Array) {
    alerts = [alerts];
  }
  return (
    <div>
      {alerts.map((alert) => (
        <div
          key={alert.message}
          className={classnames(
            "alert alert-dismissible fade show",
            alertClasses(alert.level)
          )}
          role="alert"
        >
          <button
            type="button"
            className="close"
            data-dismiss="alert"
            aria-label="Close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
          {alert.message}
        </div>
      ))}
    </div>
  );
};

export default Alerts;
