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
    return <NoSearch />;
  }

  if (!data.length) {
    return <NoResults />;
  }

  // Türkçe büyük/küçük harf duyarsız kelime vurgulayıcı
  const highlightText = (text, highlight) => {
    if (!highlight || !text) return text;

    const normalizedText = text.toLocaleLowerCase('tr');
    const normalizedHighlight = highlight.toLocaleLowerCase('tr');

    const startIndices = [];
    let startIndex = 0;

    while ((startIndex = normalizedText.indexOf(normalizedHighlight, startIndex)) !== -1) {
      startIndices.push(startIndex);
      startIndex += normalizedHighlight.length;
    }

    if (startIndices.length === 0) return text;

    let result = '';
    let lastIndex = 0;

    startIndices.forEach((index) => {
      result += text.substring(lastIndex, index);
      result += `<span style="color: #C7754F;  font-weight: 500;">${text.substring(index, index + highlight.length)}</span>`;
      lastIndex = index + highlight.length;
    });

    result += text.substring(lastIndex);
    return result;
  };

  return (
    <div className="results">
      {data.map((item, index) => {
        const highlightedText = highlightText(item._source.metin, query);

        return (
          <div className="result" key={index}>
            <div className={expandedIndices.includes(index) ? 'index active' : 'index'}>
              {index + 1}
            </div>
            <div className="result-content">
              <div className="result-header">
                {item._source.baslik}
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
                  height: expandedIndices.includes(index) ? contentHeight[index] || 'auto' : '88px',
                  transition: 'all 0.8s ease-in-out',
                  overflow: expandedIndices.includes(index) ? 'scroll' : 'hidden',
                  marginBottom: expandedIndices.includes(index) ? '0px' : '10px',
                }}
                dangerouslySetInnerHTML={{ __html: highlightedText }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ResultsList;
