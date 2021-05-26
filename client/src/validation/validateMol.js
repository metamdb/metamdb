const validateUpload = (values) => {
  let errors = {};
  if (!values.file) {
    errors.file = "File required";
  } else if (!values.file.name.match(/.(mol)$/i)) {
    errors.file = "File format must be .mol";
  }
  return errors;
};

export default validateUpload;
