import React from 'react';
import { Upload, message } from 'antd';
import { InboxOutlined } from '@ant-design/icons';

const { Dragger } = Upload;

const VideoUpload = ({ setLoading, setResult }) => {
  const props = {
    name: 'file',
    multiple: false,
    accept: 'video/*',
    beforeUpload: (file) => {
      message.success(`${file.name} uploaded successfully`);
      setLoading(true);
      setTimeout(() => {
        const mockResult = [
          { animal: 'Cat', confidence: 0.91 },
          { animal: 'Dog', confidence: 0.83 },
          { animal: 'Bird', confidence: 0.65 },
        ];
        setResult(mockResult);
        setLoading(false);
      }, 2000);
      return false;
    },
    onDrop(e) {
      console.log('Dropped files', e.dataTransfer.files);
    },
  };

  return (
    <Dragger {...props}>
      <p className="ant-upload-drag-icon">
        <InboxOutlined />
      </p>
      <p className="ant-upload-text">Click or drag video file to this area to upload</p>
      <p className="ant-upload-hint">Only single video file is supported. (mp4, mov...)</p>
    </Dragger>
  );
};

export default VideoUpload;
