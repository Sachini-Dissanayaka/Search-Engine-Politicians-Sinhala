import { useEffect, useState } from "react";
import "./App.css";
import Search from "./components/search";
import SearchResults from "./components/search-results";
import axios from "axios";

const App = () => {
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState("");
  const [result, setResult] = useState([]);

  const onSearch = (q) => {
    console.log(q);
    setQuery(q);

    setLoading(true);
    axios
      .get(`http://127.0.0.1:5000/searchBy?term=${q}`)
      .then((res) => {
        console.log(res);
        setResult(res.data.results)
        setLoading(false);
      })
      .catch((err) => {
        console.log(err);
        setLoading(false);
      });
  };

  return (
    <>
      <div
        style={{
          marginTop: "6rem",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <h2>Welcome to Sri Lankan Politicians Search</h2>
        <Search loading={loading} onSearch={onSearch} />
        <SearchResults loading={loading} query={query} result={result} />
      </div>
    </>
  );
};

export default App;
