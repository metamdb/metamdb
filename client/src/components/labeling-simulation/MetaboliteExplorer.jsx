import React, { useEffect, useMemo, useState } from "react";
import Select from "react-select";

const atomLabel = (atoms) => `[${atoms.join(", ")}]`;

const formatFlux = (flux) => {
  if (flux === null || flux === undefined) {
    return "missing";
  }
  if (flux === 0) {
    return "0";
  }
  return Number(flux).toPrecision(6);
};

const filterRowsByAtoms = (rows, selectedAtoms, produced) => {
  if (selectedAtoms.length === 0) {
    return rows;
  }

  return rows
    .map((row) => {
      const currentAtoms = produced ? row.target_atoms : row.source_atoms;
      const matchingIndexes = currentAtoms
        .map((atom, index) => (selectedAtoms.includes(atom) ? index : -1))
        .filter((index) => index !== -1);

      if (matchingIndexes.length === 0) {
        return null;
      }

      return {
        ...row,
        source_atoms: matchingIndexes.map((index) => row.source_atoms[index]),
        target_atoms: matchingIndexes.map((index) => row.target_atoms[index]),
      };
    })
    .filter(Boolean);
};

const ReactionConnections = ({ title, rows, produced, onNavigate }) => (
  <div className="mt-3">
    <h3>{title}</h3>
    {rows.length === 0 ? (
      <p className="text-muted">No mapped reactions for this carbon selection.</p>
    ) : (
      <div className="table-responsive">
        <table className="table table-sm table-striped">
          <thead>
            <tr>
              <th>Reaction</th>
              <th>Direction</th>
              <th>Flux</th>
              <th>Carbon transfer</th>
              <th>Follow</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row, index) => {
              const connectedMetabolite = produced
                ? row.source_metabolite
                : row.target_metabolite;
              const connectedAtoms = produced
                ? row.source_atoms
                : row.target_atoms;

              return (
                <tr
                  key={`${row.reaction}-${row.direction}-${connectedMetabolite}-${connectedAtoms.join(
                    "-"
                  )}-${index}`}
                >
                  <td>{row.reaction}</td>
                  <td>{row.direction}</td>
                  <td className={row.flux == null ? "text-danger" : ""}>
                    {formatFlux(row.flux)}
                  </td>
                  <td>
                    {row.source_metabolite} {atomLabel(row.source_atoms)} →{" "}
                    {row.target_metabolite} {atomLabel(row.target_atoms)}
                  </td>
                  <td>
                    <button
                      type="button"
                      className="btn btn-sm btn-outline-primary"
                      onClick={() => onNavigate(row, produced)}
                    >
                      {connectedMetabolite} {atomLabel(connectedAtoms)}
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    )}
  </div>
);

const MetaboliteExplorer = ({ network }) => {
  const options = useMemo(
    () =>
      Object.keys(network || {})
        .sort()
        .map((name) => ({ value: name, label: name })),
    [network]
  );
  const preferredName = network?.["5,10-methylenetetrahydrofolate"]
    ? "5,10-methylenetetrahydrofolate"
    : options[0]?.value || "";
  const [selectedName, setSelectedName] = useState(preferredName);
  const [selectedAtoms, setSelectedAtoms] = useState([]);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (!network?.[selectedName]) {
      setSelectedName(preferredName);
      setSelectedAtoms([]);
      setHistory([]);
    }
  }, [network, preferredName, selectedName]);

  if (options.length === 0) {
    return (
      <div className="alert alert-info mt-4">
        Run the labeling simulation again to create the metabolite network.
      </div>
    );
  }

  const selected = network[selectedName];
  if (!selected) {
    return null;
  }

  const producedRows = filterRowsByAtoms(
    selected.produced_by,
    selectedAtoms,
    true
  );
  const consumedRows = filterRowsByAtoms(
    selected.consumed_by,
    selectedAtoms,
    false
  );

  const selectMetabolite = (option) => {
    setSelectedName(option.value);
    setSelectedAtoms([]);
    setHistory([]);
  };

  const toggleAtom = (atom) => {
    setSelectedAtoms((current) => {
      if (current.length === 0) {
        return [atom];
      }
      const next = current.includes(atom)
        ? current.filter((entry) => entry !== atom)
        : [...current, atom].sort((a, b) => a - b);
      return next;
    });
  };

  const navigate = (row, produced) => {
    const nextName = produced ? row.source_metabolite : row.target_metabolite;
    const nextAtoms = produced ? row.source_atoms : row.target_atoms;
    const currentAtoms = produced ? row.target_atoms : row.source_atoms;
    setHistory((current) => [
      ...current,
      {
        fromName: selectedName,
        fromAtoms: currentAtoms,
        reaction: row.reaction,
        direction: row.direction,
        toName: nextName,
        toAtoms: nextAtoms,
      },
    ]);
    setSelectedName(nextName);
    setSelectedAtoms([...nextAtoms]);
  };

  const goBack = () => {
    const last = history[history.length - 1];
    if (!last) {
      return;
    }
    setSelectedName(last.fromName);
    setSelectedAtoms([...last.fromAtoms]);
    setHistory((current) => current.slice(0, -1));
  };

  return (
    <div className="metabolite-explorer mt-4 mb-5">
      <hr />
      <div className="d-flex justify-content-between align-items-center">
        <div>
          <h2>Metabolite and Carbon Explorer</h2>
          <p className="text-muted">
            Inspect all mapped reactions or select carbon positions and follow
            their atom-resolved path through the flux model.
          </p>
        </div>
        <button
          type="button"
          className="btn btn-outline-secondary"
          disabled={history.length === 0}
          onClick={goBack}
        >
          Back one step
        </button>
      </div>

      <Select
        value={{ value: selectedName, label: selectedName }}
        options={options}
        onChange={selectMetabolite}
        placeholder="Select a metabolite..."
      />

      <div className="mt-3">
        <strong>Carbon positions:</strong>{" "}
        <button
          type="button"
          className={`btn btn-sm mr-1 mb-1 ${
            selectedAtoms.length === 0
              ? "btn-primary"
              : "btn-outline-primary"
          }`}
          onClick={() => setSelectedAtoms([])}
        >
          All
        </button>
        {Array.from({ length: selected.atom_count }, (_, index) => index + 1).map(
          (atom) => (
            <button
              type="button"
              key={atom}
              className={`btn btn-sm mr-1 mb-1 ${
                selectedAtoms.includes(atom)
                  ? "btn-primary"
                  : "btn-outline-primary"
              }`}
              onClick={() => toggleAtom(atom)}
            >
              {atom}
            </button>
          )
        )}
      </div>

      {history.length > 0 && (
        <div className="alert alert-light border mt-3 mb-2">
          <strong>Current trace</strong>
          <ol className="mb-0 mt-2">
            {history.map((step, index) => (
              <li key={`${step.reaction}-${index}`}>
                {step.fromName} {atomLabel(step.fromAtoms)} — {step.reaction} ({" "}
                {step.direction}) → {step.toName} {atomLabel(step.toAtoms)}
              </li>
            ))}
          </ol>
        </div>
      )}

      <ReactionConnections
        title="Produced by"
        rows={producedRows}
        produced
        onNavigate={navigate}
      />
      <ReactionConnections
        title="Consumed by"
        rows={consumedRows}
        produced={false}
        onNavigate={navigate}
      />
    </div>
  );
};

export default MetaboliteExplorer;
