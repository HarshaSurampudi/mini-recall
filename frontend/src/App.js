import React, { useState } from "react";
import SearchBar from "./components/SearchBar";
import "./index.css";

const App = () => {
  const [results, setResults] = useState([]);

  const handleSearch = async (query) => {
    try {
      const response = await fetch("http://localhost:5000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: query }),
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="container">
      <h1>Recall System</h1>
      <SearchBar onSearch={handleSearch} />
      <div className="search-results">
        {results.map((result) => (
          <div key={result.id}>
            <img
              src={`http://localhost:5000/static/${result.image_path}`}
              alt={`Result ${result.id}`}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
