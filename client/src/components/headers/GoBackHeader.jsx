import React, { useContext } from "react";

import { MainContext } from "../../contexts/MainContext";

const GoBackHeader = props => {
  const { dispatch } = useContext(MainContext);

  const { title, type } = props;

  const goBack = () => {
    dispatch({
      type: type
    });
  };

  return (
    <div className="row">
      <div className="col-10">
        <h1>{title}</h1>
      </div>
      <div className="col-2 ml-auto">
        <button
          type="button"
          className="btn btn-outline-primary"
          onClick={goBack}
          style={{ float: "right" }}
        >
          <i className="fas fa-arrow-left" /> Go Back
        </button>
      </div>
    </div>
  );
};

export default GoBackHeader;
