'use client'

import { useEffect, useState } from 'react'
import ReactECharts from 'echarts-for-react'

export default function BoxPlot({
  url,
  yAxisLabel,
}: {
  url: string
  yAxisLabel: string
}) {
  const [labels, setLabels] = useState<string[]>([])
  const [boxplot, setBoxplot] = useState<number[][]>([])

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(data => {
        setLabels(data.labels)
        setBoxplot(data.boxplot)
      })
  }, [url])

  const option = {
    tooltip: {
      trigger: 'item',
    },
    xAxis: {
      type: 'category',
      data: labels,
    },
    yAxis: {
      type: 'value',
      name: yAxisLabel,
    },
    series: [
      {
        type: 'boxplot',
        data: boxplot,
        itemStyle: {
          color: 'rgba(0,0,0,0)',
          borderColor: '#000',
          borderWidth: 2,
        },
        lineStyle: {
          color: '#000',
          width: 2,
        },
      },
    ],
  }

  return <ReactECharts option={option} style={{ height: 400 }} />
}
