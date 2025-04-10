import React from 'react';
import { Upload, message } from 'antd';
import { InboxOutlined } from '@ant-design/icons';

const { Dragger } = Upload;

const ImageUpload = ({ setLoading, setResult, setImageUrl }) => {
  const props = {
    name: 'file',
    multiple: false,
    accept: 'image/*',
    showUploadList: false,
    customRequest({ file, onSuccess }) {
      setLoading(true);

      const previewUrl = URL.createObjectURL(file);
      setImageUrl(previewUrl);

      const formData = new FormData();
      formData.append('file', file);

      fetch('http://localhost:5114/upload', {
        method: 'POST',
        body: formData,
      })
        .then(res => res.json())
        .then(data => {
          setTimeout(() => {
            setResult(data);
            setLoading(false);
            onSuccess();
          }, 1000);
        })
        .catch(err => {
          message.error('Upload failed');
          console.error(err);
          setLoading(false);
        });
    },
  };

  return (
    <Dragger {...props}>
      <p className="ant-upload-drag-icon">
        <InboxOutlined />
      </p>
      <p className="ant-upload-text">Click or drag image to upload</p>
      <p className="ant-upload-hint">Supports single image upload (.jpg, .png)</p>
    </Dragger>
  );
};

export default ImageUpload;