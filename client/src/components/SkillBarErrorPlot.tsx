'use client';

import React, { useEffect, useState } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

interface SkillLevel {
  mean: number;
  std: number;
}

interface SkillData {
  low?: SkillLevel;
  medium?: SkillLevel;
  high?: SkillLevel;
}

interface Props {
  skill: string;
  type: "time" | "grad_mean";
}

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const SkillBarErrorPlot: React.FC<Props> = ({ skill, type }) => {
  const [data, setData] = useState<SkillData | null>(null);

  useEffect(() => {
    if (!skill) return;

    fetch(`/api/skill/aggregate?skill=${skill}&metric=${type}`)
      .then((res) => res.json())
      .then((json) => {
        setData({
          low: json.low ?? { mean: 0, std: 0 },
          medium: json.medium ?? { mean: 0, std: 0 },
          high: json.high ?? { mean: 0, std: 0 },
        });
      })
      .catch((err) => {
        console.error("Error fetching skill data:", err);
        setData(null);
      });
  }, [skill, type]);

  if (!data) return <p>Loading data...</p>;

  const chartData = {
    labels: ["Low", "Medium", "High"],
    datasets: [
      {
        label: type === "time" ? "Execution Time" : "Grades",
        data: [data.low!.mean, data.medium!.mean, data.high!.mean],
        backgroundColor: "rgba(220, 38, 38, 0.7)", // vermelho
        borderColor: "rgba(220, 38, 38, 1)",
        borderWidth: 1,
        // Simulando error bars com borderWidth em cima/baixo
      },
    ],
  };

  const options: any = {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: {
        display: true,
        text: `${type === "time" ? "Execution Time" : "Grades"} by Knowledge Level (${skill})`,
        color: "#991B1B",
        font: { size: 16, weight: "bold" },
      },
      tooltip: {
        callbacks: {
          label: function (context: any) {
            const level = context.dataIndex;
            const stdArr = [data.low!.std, data.medium!.std, data.high!.std];
            return `Mean: ${context.raw.toFixed(2)}, Std: ${stdArr[level].toFixed(2)}`;
          },
        },
      },
    },
    scales: {
      y: { beginAtZero: true },
    },
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default SkillBarErrorPlot;
