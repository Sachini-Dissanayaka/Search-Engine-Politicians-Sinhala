import { useEffect, useState } from "react";
import "./App.css";
import Search from "./components/search";
import SearchResults from "./components/search-results";
import axios from "axios";

const App = () => {
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState("");
  const [result, setResult] = useState([]);
  const [gender,setGender] = useState();
  const [position,setPosition] = useState();
  const [party,setParty] = useState();

  const handlegenderchange = (e,val) => {
    setGender(val.value);
  }
  const handlepartychange = (e,val) => {
    setParty(val.value);
  }
  const handlepositionchange = (e,val) => {
    setPosition(val.value);
  }
  const onSearch = (q) => {
    console.log(q);
    setQuery(q);
    setLoading(true);

    if (gender || position || party){
      const filters = [];

      if (party) {
        filters.push({"Political_Party_si": party})
      } 
      if (position) {
        filters.push({"Position_si": position})
      } 
      if (gender) {
        filters.push({"Gender_si": gender})
      } 
      axios
      .post(`http://127.0.0.1:5000/facetedSearch`,{ "term": q, "filter" :filters})
      .then((res) => {
        console.log(res);
        setResult(res.data.results)
        setLoading(false);
      })
      .catch((err) => {
        console.log(err);
        setLoading(false);
      });
    } else{
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
    }
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
        <Search loading={loading} onSearch={onSearch}  handlegenderchange = {handlegenderchange} handlepartychange = {handlepartychange} handlepositionchange = {handlepositionchange} />
        <SearchResults loading={loading} query={query} result={result} />
      </div>
    </>
  );
};

export default App;
