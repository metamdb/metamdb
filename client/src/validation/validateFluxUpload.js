const validateFluxUpload = (values) => {
  let errors = {};
  if (!values.file) {
    errors.file = "File required";
  } else if (!values.file.name.match(/.(csv)$/i)) {
    errors.file = "File format must be .csv";
  }
  return errors;
};

export default validateFluxUpload;
