const validateUpload = values => {
  let errors = {};
  if (!values.file) {
    errors.file = "File required";
  } else if (!values.file.name.match(/.(csv|txt)$/i)) {
    errors.file = "File format must be .csv or .txt";
  }
  return errors;
};

export default validateUpload;
