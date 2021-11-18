import React, { useContext } from "react";
import { Popover, OverlayTrigger, Button } from "react-bootstrap";
import styled from "styled-components";
import { Link } from "react-router-dom";

import { MetaboliteContext } from "../../contexts/MetaboliteContext";

const StyledPopover = styled(Popover)`
  min-width: 600px;
`;

const MetaboliteInfo = ({ id }) => {
  const { metabolite } = useContext(MetaboliteContext);

  const popover = (
    <StyledPopover id="popover" className="shadow">
      <StyledPopover.Title as="h3">Mol File</StyledPopover.Title>
      <StyledPopover.Content>
        <pre>{metabolite.file}</pre>
      </StyledPopover.Content>
    </StyledPopover>
  );

  const downloadMol = (e) => {
    e.preventDefault();

    const element = document.createElement("a");
    document.body.appendChild(element);
    const file = new Blob([metabolite.file], {
      type: "text/plain",
    });
    const url = URL.createObjectURL(file);
    element.href = url;
    element.download = `MET${metabolite.id}.mol`;
    element.click();
    setTimeout(() => {
      document.body.removeChild(element);
      window.URL.revokeObjectURL(url);
    }, 0);
  };

  return (
    <div className="mt-3">
      <p className="text-muted">
        <strong>name: </strong>
        {metabolite.name}
      </p>
      <p className="text-muted">
        <strong>formula: </strong>
        {metabolite.formula}
      </p>
      <p className="text-muted">
        <strong>inchi: </strong>
        {metabolite.inchi}
      </p>
      <p className="text-muted">
        <strong>inchiKey: </strong>
        {metabolite.inchiKey}
      </p>
      <p className="text-muted">
        <strong>reactions: </strong>
        <Link
          target="_blank"
          to={`/database-query?metabolite_id=${metabolite.id}`}
        >
          See the reactions here!
        </Link>
      </p>
      <p className="text-muted">
        <strong>Mol File:</strong>
        <OverlayTrigger placement="right" trigger="focus" overlay={popover}>
          <Button variant="link">Click</Button>
        </OverlayTrigger>
      </p>
      <div className="download mb-3">
        <button type="button" className="btn btn-success" onClick={downloadMol}>
          <i className="fa fa-download" /> Download Mol File
        </button>
      </div>
    </div>
  );
};

export default MetaboliteInfo;
