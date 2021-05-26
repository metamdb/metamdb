const validateUpload = values => {
  let errors = {};
  if (!values.file) {
    errors.file = "File required";
  } else if (!values.file.name.match(/.(rxn)$/i)) {
    errors.file = "File format must be .rxn";
  }
  return errors;
};

export default validateUpload;
