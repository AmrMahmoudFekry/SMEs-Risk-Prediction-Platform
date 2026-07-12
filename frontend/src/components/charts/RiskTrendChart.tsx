'use client';

import ReactECharts from 'echarts-for-react';
import { useEffect, useState } from 'react';

export default function RiskTrendChart() {
  const [mounted, setMounted] = useState(false);
  // محاكاة لبيانات الـ Trend
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
  const highRisk = [12, 15, 10, 8, 14, 9];
  const lowRisk = [45, 50, 55, 60, 58, 65];

  useEffect(() => {
    setMounted(true);
  }, []);

  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#334155',
      textStyle: { color: '#F8FAFC' }
    },
    legend: {
      data: ['High Risk', 'Low Risk'],
      textStyle: { color: '#64748b' },
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      top: '5%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: months,
      axisLine: { lineStyle: { color: '#334155' } },
      axisLabel: { color: '#64748b' }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#1E293B', type: 'dashed' } },
      axisLabel: { color: '#64748b' }
    },
    series: [
      {
        name: 'High Risk',
        type: 'line',
        smooth: true,
        itemStyle: { color: '#EF4444' },
        areaStyle: {
          color: {
            type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(239, 68, 68, 0.3)' },
              { offset: 1, color: 'rgba(239, 68, 68, 0)' }
            ]
          }
        },
        data: highRisk
      },
      {
        name: 'Low Risk',
        type: 'line',
        smooth: true,
        itemStyle: { color: '#10B981' },
        areaStyle: {
          color: {
            type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(16, 185, 129, 0.3)' },
              { offset: 1, color: 'rgba(16, 185, 129, 0)' }
            ]
          }
        },
        data: lowRisk
      }
    ]
  };

  if (!mounted) return null;

  return <ReactECharts option={option} style={{ height: '100%', width: '100%' }} />;
}