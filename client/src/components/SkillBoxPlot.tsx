'use client';

import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';

interface SkillBoxPlotProps {
  skill: string;           // habilidade selecionada
  type: 'time' | 'grade';  // define se é tempo ou nota
  xLabels: string[];       // ["Low", "Medium", "High"]
  title: string;           // Título do gráfico
}

interface BoxPlotData {
  low: number[];
  medium: number[];
  high: number[];
}

const SkillBoxPlot: React.FC<SkillBoxPlotProps> = ({ skill, type, xLabels, title }) => {
  const [data, setData] = useState<BoxPlotData>({ low: [], medium: [], high: [] });
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(`${API_URL}/tasks_${type}_by_skill?skill=${skill}`);
        const json = await res.json();
        setData({
          low: json.low || [],
          medium: json.medium || [],
          high: json.high || []
        });
      } catch (err) {
        console.error("Error fetching boxplot data:", err);
      }
    };

    fetchData();
  }, [skill, type, API_URL]);

  const option = {
    title: {
      text: title,
      left: 'center',
      textStyle: { color: '#b91c1c', fontSize: 16, fontWeight: 'bold' } // vermelho estilo dashboard
    },
    tooltip: {
      trigger: 'item',
      axisPointer: { type: 'shadow' }
    },
    xAxis: {
      type: 'category',
      data: xLabels
    },
    yAxis: {
      type: 'value',
      name: type === 'time' ? 'Minutes' : 'Grade'
    },
    series: [
      {
        name: title,
        type: 'boxplot',
        data: [data.low, data.medium, data.high].map(arr => arr.map(Number)),
        itemStyle: { color: '#f87171' } // vermelho claro do seu tema
      }
    ]
  };

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <ReactECharts option={option} style={{ height: 350 }} />
    </div>
  );
};

export default SkillBoxPlot;
