"use client";

import React, { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";

export default function PositiveSankey() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch(`/api/participant/sankey/positive`)
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch((err) => console.error("Positive Sankey error:", err));
  }, ['/api']);

  if (!data) {
    return <p className="text-center text-blue-400 animate-pulse">Loading positive Sankey...</p>;
  }

  const option = {
    tooltip: {
      trigger: 'item',
      triggerOn: 'mousemove'
    },
    series: [
      {
        type: 'sankey',
        data: [
          { name: 'Time', itemStyle: { color: '#1e3a8a' } },
          { name: 'Quality', itemStyle: { color: '#065f46' } },
          { name: 'Speed', itemStyle: { color: '#bfdbfe' } },
          { name: 'Agility', itemStyle: { color: '#bfdbfe' } },
          { name: 'Precision', itemStyle: { color: '#bfdbfe' } },
          { name: 'Ease of Use', itemStyle: { color: '#a7f3d0' } },
          { name: 'Creativity & Ideas', itemStyle: { color: '#a7f3d0' } },
          { name: 'Clarity', itemStyle: { color: '#a7f3d0' } },
          { name: 'Standardization', itemStyle: { color: '#a7f3d0' } },
          { name: 'Context', itemStyle: { color: '#a7f3d0' } }
        ],
        links: data.links,
        emphasis: { focus: 'adjacency' },
        lineStyle: {
          color: 'source',
          opacity: 0.45,
          curveness: 0.5
        },
        label: {
          position: 'right',
          color: '#064e3b',
          fontSize: 12
        }
      }
    ]
  };

  return (
    <div className="bg-white p-6 rounded-xl border border-emerald-100 shadow-md">
      <h2 className="text-xl font-bold text-emerald-800 mb-6 text-center border-b border-emerald-50 pb-2">
        Positive Perceptions of LLM Usage
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