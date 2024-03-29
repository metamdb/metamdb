import React, { useState } from "react";
import Select from "react-select";

function MetaboliteForm({ metabolites, values, setValues }) {
  const [formData, setFormData] = useState({
    name: "",
    labeling: "",
    purity: "",
    enrichment: "",
  });

  const options = metabolites.map((metabolite) => {
    return { value: metabolite, label: metabolite };
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  const onTargetChange = (inputValue, { action, prevInputValue }) => {
    setFormData({ ...formData, name: inputValue.value });
  };

  const handleFormSubmit = (event) => {
    event.preventDefault();
    setValues({ ...values, tracer: [...values.tracer, formData] });
    setFormData({
      ...formData,
      labeling: "",
      purity: "",
      enrichment: "",
    });
  };

  const handleRemove = (index) => {
    setValues({
      ...values,
      tracer: values.tracer.filter((_, i) => i !== index),
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
              minWidth: "450px",
            }),
          }}
        />

        <label className="sr-only" htmlFor="inlineFormInputLabeling">
          Labeling
        </label>
        <input
          type="text"
          name="labeling"
          className="form-control mb-2 mr-sm-2"
          id="inlineFormInputLabeling"
          placeholder="Labeling"
          value={formData.labeling}
          onChange={handleInputChange}
        />

        <label className="sr-only" htmlFor="inlineFormInputPurity">
          Purity
        </label>
        <input
          type="number"
          name="purity"
          min="0"
          max="1"
          step="0.01"
          value={formData.purity}
          onChange={handleInputChange}
          className="form-control mb-2 mr-sm-2"
          id="inlineFormInputPurity"
          placeholder="Purity"
        />
        <label className="sr-only" htmlFor="inlineFormInputEnrichment">
          Enrichment
        </label>
        <input
          type="number"
          name="enrichment"
          min="0"
          max="1"
          step="0.01"
          value={formData.enrichment}
          onChange={handleInputChange}
          className="form-control mb-2 mr-sm-2"
          id="inlineFormInputEnrichment"
          placeholder="Enrichment"
        />

        <button
          onClick={handleFormSubmit}
          className="btn btn-outline-success float-right mb-2 mr-sm-2"
          type="button"
        >
          Add Tracer
        </button>
      </div>
      <ul className="list-group list-group-flush">
        {values.tracer.map((metabolite, index) => (
          <li key={index} className="list-group-item">
            <strong>Tracer: </strong>
            {metabolite.name} - <strong>Labeling: </strong>
            {metabolite.labeling} - <strong>Purity: </strong>
            {Number(metabolite.purity).toFixed(2)} -{" "}
            <strong>Enrichment: </strong>
            {Number(metabolite.enrichment).toFixed(2)}
            <button
              onClick={() => handleRemove(index)}
              className="btn btn-outline-danger float-right"
              type="button"
            >
              Remove Tracer
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
export default MetaboliteForm;
