import { useRef } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, TooltipItem } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import { SentimentData } from '../types';
import './SentimentChart.css';

ChartJS.register(ArcElement, Tooltip, Legend);

interface SentimentChartProps {
  sentiment: SentimentData;
}

const SentimentChart: React.FC<SentimentChartProps> = ({ sentiment }) => {
  const chartRef = useRef<ChartJS<'pie'>>(null);

  const total = sentiment.positive + sentiment.neutral + sentiment.negative;
  
  const data = {
    labels: ['ポジティブ', 'ニュートラル', 'ネガティブ'],
    datasets: [
      {
        data: [sentiment.positive, sentiment.neutral, sentiment.negative],
        backgroundColor: [
          '#28a745', // グリーン（ポジティブ）
          '#ffc107', // イエロー（ニュートラル）
          '#dc3545', // レッド（ネガティブ）
        ],
        borderColor: [
          '#1e7e34',
          '#e0a800',
          '#c82333',
        ],
        borderWidth: 2,
        hoverBackgroundColor: [
          '#34ce57',
          '#ffcd39',
          '#e24567',
        ],
        hoverBorderWidth: 3,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          padding: 20,
          font: {
            size: 14,
          },
        },
      },
      tooltip: {
        callbacks: {
          label: function(context: TooltipItem<'pie'>) {
            const count = context.raw as number;
            const percentage = ((count / total) * 100).toFixed(1);
            return `${context.label}: ${count}件 (${percentage}%)`;
          },
        },
      },
    },
    elements: {
      arc: {
        borderWidth: 2,
      },
    },
  };

  const calculatePercentage = (value: number) => {
    if (total === 0) return '0.0';
    return ((value / total) * 100).toFixed(1);
  };

  return (
    <div className="sentiment-chart-container">
      <div className="chart-wrapper">
        <Pie ref={chartRef} data={data} options={options} />
      </div>
      
      <div className="sentiment-stats">
        <div className="stat-item positive">
          <div className="stat-color"></div>
          <div className="stat-info">
            <span className="stat-label">ポジティブ</span>
            <span className="stat-value">{sentiment.positive}件</span>
            <span className="stat-percentage">({calculatePercentage(sentiment.positive)}%)</span>
          </div>
        </div>
        
        <div className="stat-item neutral">
          <div className="stat-color"></div>
          <div className="stat-info">
            <span className="stat-label">ニュートラル</span>
            <span className="stat-value">{sentiment.neutral}件</span>
            <span className="stat-percentage">({calculatePercentage(sentiment.neutral)}%)</span>
          </div>
        </div>
        
        <div className="stat-item negative">
          <div className="stat-color"></div>
          <div className="stat-info">
            <span className="stat-label">ネガティブ</span>
            <span className="stat-value">{sentiment.negative}件</span>
            <span className="stat-percentage">({calculatePercentage(sentiment.negative)}%)</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SentimentChart;