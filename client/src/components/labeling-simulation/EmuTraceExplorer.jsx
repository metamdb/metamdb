import React, { useEffect, useMemo, useState } from "react";
import Select from "react-select";

const EMPTY_TARGETS = [];
const EMPTY_NODES = {};

const atomLabel = (atoms) => `[${(atoms || []).join(", ")}]`;

const emuLabel = (emu) =>
  `${emu?.metabolite || "Unknown metabolite"} ${atomLabel(emu?.atoms)}`;

const formatFlux = (flux) => {
  if (flux === null || flux === undefined) {
    return "missing";
  }
  if (flux === 0) {
    return "0";
  }
  return Number(flux).toPrecision(6);
};

const formatPercent = (value) => `${(Number(value || 0) * 100).toFixed(2)}%`;

const MidVector = ({ values, percentages = false }) => (
  <div className="d-flex flex-wrap">
    {(values || []).map((value, index) => (
      <span
        className="badge bg-light text-dark border mr-1 mb-1"
        key={`m-${index}`}
      >
        M+{index}:{" "}
        {percentages ? formatPercent(value) : Number(value).toFixed(6)}
      </span>
    ))}
  </div>
);

const modeLabel = (mode) => {
  if (mode === "convolution") {
    return "combined fragments";
  }
  if (mode === "average") {
    return "equivalent mappings";
  }
  return "direct transfer";
};

const EmuTraceExplorer = ({ trace }) => {
  const targets = trace?.targets || EMPTY_TARGETS;
  const nodes = trace?.nodes || EMPTY_NODES;
  const targetOptions = useMemo(
    () =>
      targets.map((target) => ({
        value: target.id,
        label: emuLabel(target),
      })),
    [targets]
  );
  const preferredTarget =
    targets.find((target) => target.metabolite === "pyruvate")?.id ||
    targets[0]?.id ||
    "";
  const [selectedId, setSelectedId] = useState(preferredTarget);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (!nodes[selectedId]) {
      setSelectedId(preferredTarget);
      setHistory([]);
    }
  }, [nodes, preferredTarget, selectedId]);

  if (targets.length === 0 || Object.keys(nodes).length === 0) {
    return (
      <div className="alert alert-info mt-4">
        Run the labeling simulation again to create the target-specific EMU
        trace.
      </div>
    );
  }

  const selected = nodes[selectedId];
  if (!selected) {
    return null;
  }

  const selectTarget = (option) => {
    setSelectedId(option.value);
    setHistory([]);
  };

  const navigateToSource = (sourceId) => {
    setHistory((current) => [...current, selectedId]);
    setSelectedId(sourceId);
  };

  const navigateToBreadcrumb = (nodeId, index) => {
    setSelectedId(nodeId);
    setHistory((current) => current.slice(0, index));
  };

  const returnToTarget = () => {
    const targetId = history[0] || selectedId;
    setSelectedId(targetId);
    setHistory([]);
  };

  const breadcrumbIds = [...history, selectedId];

  return (
    <div className="emu-trace-explorer mt-4 mb-5">
      <h2>Target EMU Labeling Trace</h2>
      <p className="text-muted">
        Follow the calculated EMUs upstream. Production share describes flux;
        MID contribution describes the labeling supplied through that reaction.
      </p>

      <Select
        value={targetOptions.find(
          (option) => option.value === breadcrumbIds[0]
        )}
        options={targetOptions}
        onChange={selectTarget}
        placeholder="Select a target EMU..."
      />

      <div className="d-flex flex-wrap align-items-center mt-3">
        <strong className="mr-2">Trace:</strong>
        {breadcrumbIds.map((nodeId, index) => {
          const breadcrumb = nodes[nodeId];
          return (
            <React.Fragment key={`${nodeId}-${index}`}>
              {index > 0 && <span className="mr-2">→</span>}
              <button
                type="button"
                className={`btn btn-sm mr-2 mb-1 ${
                  index === breadcrumbIds.length - 1
                    ? "btn-primary"
                    : "btn-outline-secondary"
                }`}
                onClick={() => navigateToBreadcrumb(nodeId, index)}
              >
                {emuLabel(breadcrumb)}
              </button>
            </React.Fragment>
          );
        })}
        <button
          type="button"
          className="btn btn-sm btn-outline-secondary ml-auto"
          disabled={history.length === 0}
          onClick={returnToTarget}
        >
          Return to target
        </button>
      </div>

      <div className="card mt-3">
        <div className="card-body">
          <div className="d-flex justify-content-between align-items-center">
            <h3 className="card-title mb-2">{emuLabel(selected)}</h3>
            {selected.boundary && (
              <span className="badge bg-secondary text-white">
                Boundary EMU
              </span>
            )}
          </div>
          <strong>Calculated MID</strong>
          <MidVector values={selected.mid} />
        </div>
      </div>

      {selected.sources.length === 0 ? (
        <div className="alert alert-secondary mt-3">
          This trace ends here because the EMU is a tracer, boundary, ignored
          input, or has no active producing reaction.
        </div>
      ) : (
        <div className="table-responsive mt-3">
          <table className="table table-sm table-striped table-bordered">
            <thead>
              <tr>
                <th>Producing reaction</th>
                <th>Flux</th>
                <th>Production share</th>
                <th>Source EMU labeling</th>
                <th>Effective source MID</th>
                <th>Contribution to this MID</th>
              </tr>
            </thead>
            <tbody>
              {selected.sources.map((source, sourceIndex) => (
                <tr
                  key={`${source.reaction}-${source.direction}-${sourceIndex}`}
                >
                  <td>
                    <strong>{source.reaction}</strong>
                    <div>{source.direction}</div>
                    <small className="text-muted">
                      {modeLabel(source.source_mode)}
                    </small>
                  </td>
                  <td>{formatFlux(source.flux)}</td>
                  <td>{formatPercent(source.flux_share)}</td>
                  <td>
                    {source.source_emus.map((sourceEmu) => {
                      const alreadyVisited = breadcrumbIds.includes(
                        sourceEmu.id
                      );
                      return (
                        <div className="mb-2" key={sourceEmu.id}>
                          <button
                            type="button"
                            className="btn btn-sm btn-outline-primary mb-1"
                            onClick={() => navigateToSource(sourceEmu.id)}
                          >
                            {emuLabel(sourceEmu)}
                          </button>
                          {alreadyVisited && (
                            <span className="badge bg-warning text-dark ml-1">
                              cycle
                            </span>
                          )}
                          <MidVector values={sourceEmu.mid} />
                        </div>
                      );
                    })}
                  </td>
                  <td>
                    <MidVector values={source.source_mid} />
                  </td>
                  <td>
                    <MidVector values={source.mid_contribution} />
                    <details className="mt-2">
                      <summary>Share of each MID peak</summary>
                      <MidVector
                        values={source.mass_isotopomer_share}
                        percentages
                      />
                    </details>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default EmuTraceExplorer;
