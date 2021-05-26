export const validateContact = (values) => {
  let errors = {};
  // Name errors
  if (!values.name) {
    errors.name = "Required Name";
  }

  if (!values.email) {
    errors.email = "Required Email";
  } else if (!/\S+@\S+\.\S+/.test(values.email)) {
    errors.email = "Not a valid email";
  }

  if (!values.message) {
    errors.message = "Required Message";
  }

  return errors;
};

export const validateRegister = (values) => {
  let errors = {};
  // Name errors
  if (!values.name) {
    errors.name = "Required Name";
  } else if (values.name.length !== 3) {
    errors.name = "Name must be 3 characters long";
  }

  // Email errors
  if (!values.email) {
    errors.email = "Required Email";
  } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)) {
    errors.email = "Invalid email address";
  }

  //Password Errors
  if (!values.password) {
    errors.password = "Required Password";
  } else if (values.password.length < 6) {
    errors.password = "Password must be at least 6 characters";
  } else if (values.password.length > 15) {
    errors.password = "Password can be upto 15 characters";
  }

  //Password Errors
  if (values.password !== values.password2) {
    errors.password2 = "Passwords must be the same";
  }

  return errors;
};
