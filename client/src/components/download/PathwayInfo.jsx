import React from "react";

const PathwayInfo = ({ name, source_id, source }) => {
  return (
    <div className="mt-3">
      <p className="text-muted">
        <strong>Name:</strong>
      </p>
      <p className="text-muted">{name} </p>
      <p className="text-muted">
        <strong>Identifier:</strong>
      </p>
      <p className="text-muted">{source_id} </p>
      <p className="text-muted">
        <strong>Database:</strong>
      </p>
      <p className="text-muted">{source} </p>
    </div>
  );
};

export default PathwayInfo;
