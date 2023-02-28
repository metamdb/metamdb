import React, { useState, useContext, useEffect } from "react";
import { MainContext } from "../../contexts/MainContext";
import Select from "react-select";
import {
  VictoryBar,
  VictoryChart,
  VictoryAxis,
  VictoryLabel,
  VictoryTheme,
} from "victory";

const BarChart = ({ data }) => {
  const xValues = data[0].data.map((d, i) => `M+${i}`);
  const bars = data.map((d) => (
    <VictoryBar
      barRatio={0.8}
      animate={{
        duration: 2000,
        onLoad: { duration: 1000 },
      }}
      style={{
        data: { fill: "#336fa3", stroke: "#000000", strokeWidth: 1 },
      }}
      key={d.name}
      data={d.data.map((y, i) => ({ x: i + 1, y }))}
    />
  ));
  return (
    <VictoryChart
      padding={{ top: 10, bottom: 30, left: 50, right: 20 }}
      height={220}
      domainPadding={25}
      theme={VictoryTheme.material}
      style={{
        parent: {
          labels: { fontSize: 1, padding: 30 },
        },
      }}
    >
      <VictoryAxis tickValues={xValues} />
      <VictoryAxis
        dependentAxis
        domain={[0, 1]}
        axisLabelComponent={<VictoryLabel dy={-25} />}
        label="relative abundance"
      />
      {bars}
    </VictoryChart>
  );
};

const LabelingVisualization = () => {
  const { contextState } = useContext(MainContext);
  const { mids } = contextState;
  const [selectedName, setSelectedName] = useState(mids[0].name);
  const selectedData = mids.find((d) => d.name === selectedName);

  const handleDataChange = (inputValue) => {
    console.log(inputValue);
    const selectedValue = inputValue.value;
    setSelectedName(selectedValue);
  };

  const options = mids.map((mid) => {
    return { value: mid.name, label: mid.name };
  });

  return (
    <div className="visualization mt-3 row">
      <div className="col-2">
        <Select
          defaultValue={options[0]}
          closeMenuOnSelect={true}
          options={options}
          onChange={handleDataChange}
          styles={{
            control: (baseStyles, state) => ({
              ...baseStyles,
              width: "max-content",
              minWidth: "100%",
            }),
          }}
        />
      </div>
      <div className="col-10">
        <BarChart data={[selectedData]} />
      </div>
    </div>
  );
};

export default LabelingVisualization;
