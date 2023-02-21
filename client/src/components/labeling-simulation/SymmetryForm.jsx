import React, { useState } from "react";

function SymmetryForm({ metabolites, values, setValues }) {
  const [formData, setFormData] = useState({
    name: "",
    symmetry: "",
  });

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
        <select
          className="form-control mb-2 mr-sm-2"
          name="name"
          value={formData.name}
          onChange={handleInputChange}
        >
          <option value="">Metabolite...</option>
          {metabolites.map((metabolite, index) => (
            <option key={index} value={metabolite}>
              {metabolite}
            </option>
          ))}
        </select>

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
