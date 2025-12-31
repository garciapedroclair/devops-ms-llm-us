import { useEffect, useState } from "react";
import dynamic from "next/dynamic";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

export default function BoxPlot() {
  const [dataLoaded, setDataLoaded] = useState(false);
  const [timesLLMTrue, setTimesLLMTrue] = useState([]);
  const [timesLLMFalse, setTimesLLMFalse] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/tasks/stats_time_llm`)
      .then(res => res.json())
      .then(data => {
        setTimesLLMTrue(data.time_llm_true);
        setTimesLLMFalse(data.time_llm_false);
        setDataLoaded(true); // marca que os dados chegaram
      });
  }, []);

  if (!dataLoaded) {
    // mostra apenas loading no SSR
    return <p>Loading chart...</p>;
  }

  return (
    <Plot
      data={[
        { y: timesLLMTrue, type: "box", name: "LLM True", marker: { color: "red" } },
        { y: timesLLMFalse, type: "box", name: "LLM False", marker: { color: "blue" } },
      ]}
      layout={{
        yaxis: { title: "Time (minutes)" },
        boxmode: "group",
        width: 800,
        height: 400,
      }}
      style={{ width: "100%", height: "400px" }}
    />
  );
}
