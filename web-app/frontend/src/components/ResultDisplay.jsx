import React from 'react';
import { Descriptions, Card, Tag, Image } from 'antd';

const ResultDisplay = ({ data, imageUrl }) => {
  if (!data) return null;

  const detected = data.animal_or_not === 1;

  return (
    <Card title="Recognition Result" style={{ marginTop: 24 }}>
      {imageUrl && (
        <div style={{ textAlign: 'center', marginBottom: 16 }}>
          <Image
            src={imageUrl}
            alt="Uploaded"
            width={200}
            height={200}
            style={{ objectFit: 'cover', borderRadius: 8 }}
            preview={false}
          />
        </div>
      )}

      <Descriptions bordered column={1} size="middle">
        <Descriptions.Item label="Animal Detected">
          {detected ? <Tag color="green">Yes</Tag> : <Tag color="red">No</Tag>}
        </Descriptions.Item>
        <Descriptions.Item label="Type">
          {data.type || "Unknown"}
        </Descriptions.Item>
        <Descriptions.Item label="Description">
          {data.text_description || "No description available."}
        </Descriptions.Item>
      </Descriptions>
    </Card>
  );
};

export default ResultDisplay;