import React from "react";
import classnames from "classnames";

const TextFieldGroup = ({
  name,
  placeholder,
  value,
  info,
  error,
  apiError,
  type,
  onChange,
  onBlur,
  disabled,
}) => {
  return (
    <div className="form-group">
      <input
        type={type}
        className={classnames("form-control", {
          "is-invalid": error || apiError,
        })}
        placeholder={placeholder}
        name={name}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
        disabled={disabled}
      />
      {info && <small className="form-text text-muted">{info}</small>}
      {error && <div className="invalid-feedback">{error}</div>}
      {apiError && <div className="invalid-feedback">{apiError}</div>}
    </div>
  );
};

export default TextFieldGroup;
