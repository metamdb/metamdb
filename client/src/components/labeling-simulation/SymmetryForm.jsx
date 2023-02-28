import React, { useState } from "react";
import Select from "react-select";

function SymmetryForm({ metabolites, values, setValues }) {
  const [formData, setFormData] = useState({
    name: "",
    symmetry: "",
  });

  const options = metabolites.map((metabolite) => {
    return { value: metabolite, label: metabolite };
  });
  const onTargetChange = (inputValue, { action, prevInputValue }) => {
    setFormData({ ...formData, name: inputValue.value });
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleFormSubmit = (event) => {
    event.preventDefault();
    setValues({ ...values, symmetry: [...values.symmetry, formData] });
    setFormData({
      name: "",
      symmetry: "",
    });
  };

  const handleRemove = (index) => {
    setValues({
      ...values,
      symmetry: values.symmetry.filter((_, i) => i !== index),
    });
  };

  return (
    <div>
      <div className="form-inline">
        <Select
          placeholder="Select Tracer Metabolite..."
          className="mb-2 mr-sm-2"
          closeMenuOnSelect={true}
          options={options}
          onChange={onTargetChange}
          styles={{
            control: (baseStyles, state) => ({
              ...baseStyles,
              width: "100%",
              minWidth: "450px",
            }),
          }}
        />

        <label className="sr-only" htmlFor="inlineFormInputsymmetry">
          Symmetry
        </label>
        <input
          type="text"
          name="symmetry"
          className="form-control mb-2 mr-sm-2"
          id="inlineFormInputSymmetry"
          placeholder="Symmetry"
          value={formData.symmetry}
          onChange={handleInputChange}
        />

        <button
          onClick={handleFormSubmit}
          className="btn btn-outline-success float-right mb-2 mr-sm-2"
          type="button"
        >
          Add Symmetry
        </button>
      </div>
      <ul className="list-group list-group-flush">
        {values.symmetry.map((metabolite, index) => (
          <li key={index} className="list-group-item">
            <strong>Metabolite: </strong>
            {metabolite.name} - <strong>Symmetry: </strong>
            {metabolite.symmetry}
            <button
              onClick={() => handleRemove(index)}
              className="btn btn-outline-danger float-right"
              type="button"
            >
              Remove Symmetry
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
export default SymmetryForm;
