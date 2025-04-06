import React from 'react';
import { Table, Card } from 'antd';

const columns = [
  {
    title: 'Animal',
    dataIndex: 'animal',
    key: 'animal',
  },
  {
    title: 'Confidence',
    dataIndex: 'confidence',
    key: 'confidence',
    render: (val) => (val * 100).toFixed(2) + '%',
  },
];

const ResultDisplay = ({ data }) => {
  return (
    <Card title="Recognition Result">
      <Table
        dataSource={data.map((item, index) => ({ ...item, key: index }))}
        columns={columns}
        pagination={false}
      />
    </Card>
  );
};

export default ResultDisplay;
