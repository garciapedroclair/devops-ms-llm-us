"use client";

import React, { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";

export default function NegativeSankey() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch(`/api/participant/sankey/negative`)
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch((err) => console.error("Negative Sankey error:", err));
  }, ["/api"]);

  if (!data) {
    return <p className="text-center text-red-400 animate-pulse">Loading negative Sankey...</p>;
  }

  const option = {
    tooltip: {
      trigger: 'item',
      triggerOn: 'mousemove'
    },
    series: [
      {
        type: 'sankey',
        data: data.nodes,
        links: data.links,
        emphasis: {
          focus: 'adjacency'
        },
        levels: [
          {
            depth: 0,
            itemStyle: { color: '#7f1d1d' }, // Dark Red for source nodes
            lineStyle: { color: 'source', opacity: 0.4 }
          },
          {
            depth: 1,
            itemStyle: { color: '#fecaca' }, // Light Red for target nodes
            lineStyle: { color: 'source', opacity: 0.2 }
          }
        ],
        lineStyle: {
          curveness: 0.5
        },
        label: {
          position: 'right',
          color: '#450a0a', // Darker red/brown for text
          fontSize: 12
        }
      }
    ]
  };

  return (
    <div className="bg-white p-6 rounded-xl border border-red-100 shadow-md">
      <h2 className="text-xl font-bold text-red-800 mb-6 text-center border-b border-red-50 pb-2">
        Negative Perceptions of LLM Usage
      </h2>
      <div style={{ width: "100%", height: "400px" }}>
        <ReactECharts 
          option={option} 
          style={{ height: "100%", width: "100%" }} 
        />
      </div>
    </div>
  );
}