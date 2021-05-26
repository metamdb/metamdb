import { useState, useEffect } from "react";

const useFileForm = (initialState, validate, activation) => {
  const [values, setValues] = useState(initialState);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (isSubmitting) {
      const noErrors = Object.keys(errors).length === 0;
      if (noErrors) {
        activation();
        setSubmitting(false);
      } else {
        setSubmitting(false);
      }
    }
  }, [errors, isSubmitting, activation]);

  const handleChange = event => {
    setValues({
      ...values,
      [event.target.name]: event.target.value
    });
  };

  const handleSubmit = event => {
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
    handleSubmit
  };
};

export default useFileForm;
