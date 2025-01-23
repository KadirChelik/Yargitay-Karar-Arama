import React, { useState } from 'react';
import NoResults from './NoResults.jsx';
import NoSearch from './NoSearch.jsx';

const ResultsList = ({ data, query }) => {
  const [expandedIndices, setExpandedIndices] = useState([]);
  const [contentHeight, setContentHeight] = useState({});

  const toggleExpand = (index) => {
    setExpandedIndices((prev) => {
      const newExpandedIndices = prev.includes(index)
        ? prev.filter((i) => i !== index)
        : [...prev, index];

      if (!newExpandedIndices.includes(index)) {
        setContentHeight((prevHeight) => ({
          ...prevHeight,
          [index]: 0,
        }));
      } else {
        setContentHeight((prevHeight) => ({
          ...prevHeight,
          [index]: document.getElementById(`content-${index}`).scrollHeight,
        }));
      }

      return newExpandedIndices;
    });
  };

  if (!query.trim()) {
    // Henüz arama yapılmadıysa
    return <NoSearch/>;
  }

  if (!data.length) {
    // Arama yapılmış ama sonuç bulunamamışsa
    return <NoResults />;
  }

  // Arama yapılmış ve sonuç bulunmuşsa
  return (
    <div className="results">
      {data.map((item, index) => (
        <div className="result" key={index}>
          <div className={expandedIndices.includes(index) ? 'index active' : 'index'}>
            {index + 1}
          </div>
          <div className="result-content">
            <div className="result-header">
              {item.baslik}
              <button className="expand-icon" onClick={() => toggleExpand(index)}>
                {expandedIndices.includes(index) ? (
                  <i className="fa-solid fa-circle-chevron-up"></i>
                ) : (
                  <i className="fa-solid fa-circle-chevron-down"></i>
                )}
              </button>
            </div>
            <div
              id={`content-${index}`}
              className="result-text"
              style={{
                height: expandedIndices.includes(index)
                  ? contentHeight[index] || 'auto'
                  : '88px',
                transition: 'all 0.8s ease-in-out',
                overflow: expandedIndices.includes(index) ? 'scroll' : 'hidden',
                marginBottom: expandedIndices.includes(index) ? '0px' : '10px',
              }}
            >
              {item.metin}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ResultsList;
