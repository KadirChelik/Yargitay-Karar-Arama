import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Input from './components/Input';
import ResultsList from './components/ResultsList';
import Loading from './components/Loading';
import logo from '../public/gavel-logo.png';

const App = () => {
  const [data, setData] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false); // Loading durumu
  const [shrink, setShrink] = useState(false); // Upper-container yüksekliğini kontrol eden state

  const fetchData = async (searchQuery) => {
    setLoading(true);
    try {
      const response = await axios.get('http://yargitaykarararamabackend.eu-north-1.elasticbeanstalk.com/api/search', {
        params: { query: searchQuery },
      });
      setData(response.data);
    } catch (error) {
      console.error('API hatası:', error);
    } finally {
      setLoading(false);
    }
  };
  

  useEffect(() => {
    if (query) {
      setShrink(true); // Arama yapıldığında shrink state'i true
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
