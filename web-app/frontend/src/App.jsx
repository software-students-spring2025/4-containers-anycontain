import React, { useState } from 'react';
import { Layout, Typography, Spin, Divider } from 'antd';
import ImageUpload from './components/ImageUpload';
import ResultDisplay from './components/ResultDisplay';

const { Header, Content, Footer } = Layout;
const { Title } = Typography;

const App = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header>
        <Title level={3} style={{ color: 'white', margin: 0 }}>Animal Detection</Title>
      </Header>
      <Content style={{ padding: '2rem' }}>
        <ImageUpload
          setLoading={setLoading}
          setResult={setResult}
          setImageUrl={setImageUrl}
        />
        <Divider />
        {loading ? (
          <Spin size="large" />
        ) : (
          result && <ResultDisplay data={result} imageUrl={imageUrl} /> 
        )}
      </Content>
      <Footer style={{ textAlign: 'center' }}>
        &copy; 2025 AnyContain
      </Footer>
    </Layout>
  );
};

export default App;