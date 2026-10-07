import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const ACCENT = '#2a78d6';
const GRID = '#e1e0d9';
const AXIS = '#898781';

export default function Chart({ chart, columns, rows }) {
  if (!chart?.should_chart) return null;
  if (!columns.includes(chart.x_column) || !columns.includes(chart.y_column)) return null;

  const ChartComponent = chart.chart_type === 'line' ? LineChart : BarChart;
  const SeriesComponent = chart.chart_type === 'line' ? Line : Bar;

  return (
    <div className="mb-6 p-4 rounded-lg border border-gray-200">
      <ResponsiveContainer width="100%" height={280}>
        <ChartComponent data={rows} margin={{ top: 8, right: 16, left: 0, bottom: 8 }}>
          <CartesianGrid stroke={GRID} vertical={false} />
          <XAxis dataKey={chart.x_column} stroke={AXIS} tick={{ fontSize: 12 }} />
          <YAxis stroke={AXIS} tick={{ fontSize: 12 }} />
          <Tooltip contentStyle={{ fontSize: 13, borderRadius: 8, border: `1px solid ${GRID}` }} />
          <SeriesComponent
            dataKey={chart.y_column}
            fill={ACCENT}
            stroke={ACCENT}
            radius={chart.chart_type === 'bar' ? [4, 4, 0, 0] : undefined}
            strokeWidth={chart.chart_type === 'line' ? 2 : undefined}
            dot={chart.chart_type === 'line' ? { r: 3, fill: ACCENT } : undefined}
          />
        </ChartComponent>
      </ResponsiveContainer>
    </div>
  );
}