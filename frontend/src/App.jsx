import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Input from './components/Input';
import ResultsList from './components/ResultsList';
import Loading from './components/Loading';
import logo from '../public/gavel-logo.png';

const App = () => {
  const [data, setData] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [shrink, setShrink] = useState(false);

  const fetchData = async (searchQuery) => {
    setLoading(true);
    try {
      const response = await axios.post(
        'https://search-yargitay-karar-arama-search-l7mql3maj2ujdb6sbrqkizyr5y.eu-central-1.es.amazonaws.com/yargitay-kararlari/_search',
        {
          query: {
            match: {
              metin: searchQuery
            }
          }
        },
        {
          headers: {
            'Content-Type': 'application/json'
          },
          auth: {
            username: 'admin',
            password: '201675K.c'
          }
        }
      );
          console.log('API cevabı:', response.data.hits.hits);
      // Elasticsearch / OpenSearch sonuçlarının asıl verileri hits.hits dizisinde
      setData(response.data.hits.hits);
    } catch (error) {
      console.error('OpenSearch API hatası:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (query) {
      setShrink(true);
      fetchData(query);
    }
  }, [query]);

  return (
    <div className="App">
      <div className="container">
        <div className={`upper-container ${shrink ? 'shrink' : ''}`}>
          <img className="logo" src={logo} alt="Yargıtay Karar Rehberi" />
          <h1>Yargıtay Karar Rehberi</h1>
          <Input onSearch={setQuery} />
        </div>
        {loading ? <Loading /> : <ResultsList data={data} query={query} />}
      </div>
    </div>
  );
};

export default App;
