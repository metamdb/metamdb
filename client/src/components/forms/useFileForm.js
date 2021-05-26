import { useState, useEffect } from "react";

const useFileForm = (initialState, validate, upload, change = false) => {
  const [values, setValues] = useState(initialState);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (isSubmitting) {
      const noErrors = Object.keys(errors).length === 0;
      if (noErrors) {
        upload();
        setSubmitting(false);
      } else {
        setSubmitting(false);
      }
    }
  }, [errors, isSubmitting, upload]);

  const handleChange = (event) => {
    setValues({
      [event.target.name]: event.target.files[0],
    });
    if (change) {
      change(event.target.files[0]);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const validationErrors = validate(values);
    setErrors(validationErrors);

    setSubmitting(true);
  };

  return {
    values,
    errors,
    isSubmitting,
    handleChange,
    handleSubmit,
  };
};

export default useFileForm;
