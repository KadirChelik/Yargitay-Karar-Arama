import React, { useState } from 'react';

const Input = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleSearch = () => {
    if (query.trim()) {
      onSearch(query);
    }
  };

  const handleDelete = () => {
    setQuery('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault(); // Enter ile yeni satır eklenmesini engelle
      if (query.trim()) {
        onSearch(query);
      }
    }
  };

  return (
    <div className="search-form">
      <textarea
        className="search-input"
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyPress} // Enter tuşuna basıldığında tetiklenecek
        placeholder="Aramak istediğiniz konu veya kararı yazın..."
      />
      <div className="buttons">
        <button
          className="info-btn"
          onClick={handleDelete}
        >
          <dfn
            data-info="Bu uygulama, yapay zeka destekli arama teknolojisi ile Yargıtay kararlarını detaylı bir şekilde tarayarak en doğru ve ilgili sonuçlara hızlıca ulaşılmasını sağlar. Hukuki araştırmalarınızı kolaylaştırır ve verimliliğinizi artırır."
          >
            <i className="fa-solid fa-circle-info"></i>
          </dfn>
        </button>

        <button
          className={`search-btn ${query.trim() ? 'active' : ''}`} // Yazı varsa 'active' sınıfı eklenir
          onClick={handleSearch}
        >
          <i className="fa-solid fa-location-arrow rotate-icon"></i>
        </button>
      </div>
    </div>
  );
};

export default Input;
