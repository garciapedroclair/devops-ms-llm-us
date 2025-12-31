'use client';

import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function KnowledgeHeatmap() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(`${API_URL}/llm_us/knowledge/heatmap`);
        const json = await res.json();
        setData(json);
      } catch (err) {
        console.error('Error loading heatmap data:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <p>Loading knowledge heatmap...</p>;
  if (!data || data.length === 0) return <p>No data available for heatmap.</p>;

  const knowledgeLabels = data.map((item: any) => item.knowledge);
  const levelLabels = ['1', '2', '3', '4', '5'];

  // Apenas UMA declaração tipada
  const heatmapValues: any[] = [];

  data.forEach((item: any, yIndex: number) => {
    levelLabels.forEach((level: string, xIndex: number) => {
      heatmapValues.push([
        xIndex,
        yIndex,
        item.levels[level] || 0
      ]);
    });
  });

  const option = {
    tooltip: {
      position: 'top',
      formatter: (params: any) =>
        `${knowledgeLabels[params.value[1]]}<br/>
        Level ${levelLabels[params.value[0]]}: 
        <b>${params.value[2]}%</b>`
    },
    grid: { height: '70%', top: '10%' },
    xAxis: {
      type: 'category',
      data: levelLabels,
      name: 'Level',
      splitArea: { show: true }
    },
    yAxis: {
      type: 'category',
      data: knowledgeLabels,
      name: 'Area',
      splitArea: { show: true }
    },
    visualMap: {
      min: 0,
      max: 100,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '2%',
      inRange: {
        color: ['#ffffff', '#969696', '#000000']
      }
    },
    series: [{
      type: 'heatmap',
      data: heatmapValues,
      label: {
        show: true,
        formatter: (params: any) => `${params.value[2]}%`
      }
    }]
  };

  return (
    <div style={{ width: '100%', height: '500px', marginTop: '20px' }}>
      <ReactECharts option={option} style={{ height: '100%', width: '100%' }} />
    </div>
  );
}