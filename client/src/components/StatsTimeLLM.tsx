import { useEffect, useState } from 'react'
import BoxPlot from '@/components/BoxPlot'

export default function StatsTimeLLM() {
  const [data, setData] = useState<any>(null)

  useEffect(() => {
    fetch('http://localhost:8001/tasks/stats_time_llm')
      .then(res => res.json())
      .then(json => setData(json))
  }, [])

  if (!data) return <p>Loading...</p>

  const chartData = [
    { name: 'With LLM', ...data.with_llm },
    { name: 'Without LLM', ...data.without_llm },
  ]

  return (
    <div style={{ width: '100%', maxWidth: 700 }}>
      <BoxPlot data={chartData} />
    </div>
  )
}
