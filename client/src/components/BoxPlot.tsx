import {
  ResponsiveContainer,
  ComposedChart,
  XAxis,
  YAxis,
  Line,
} from 'recharts'

export default function BoxPlot({ data }: { data: any[] }) {
  return (
    <ResponsiveContainer width="100%" height={320}>
      <ComposedChart data={data}>
        <XAxis
          dataKey="name"
          tick={{ fontSize: 12 }}
        />
        <YAxis
          tick={{ fontSize: 12 }}
          label={{
            value: 'Time (s)',
            angle: -90,
            position: 'insideLeft',
            style: { fontSize: 12 },
          }}
        />

        {/* Min */}
        <Line dataKey="min" stroke="#000" dot={false} />

        {/* Q1 */}
        <Line dataKey="q1" stroke="#000" dot={false} />

        {/* Median */}
        <Line
          dataKey="median"
          stroke="#000"
          strokeWidth={2}
          dot={false}
        />

        {/* Q3 */}
        <Line dataKey="q3" stroke="#000" dot={false} />

        {/* Max */}
        <Line dataKey="max" stroke="#000" dot={false} />
      </ComposedChart>
    </ResponsiveContainer>
  )
}
