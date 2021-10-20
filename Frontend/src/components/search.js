import React from "react";
import { Input } from "semantic-ui-react";

const Search = ({ loading, onSearch }) => {
  const onKeyPress = (e) => {
    if (e.charCode === 13) onSearch(e.target.value);
  };

  return (
    <div style={{ margin: "1rem", width: "300px" }}>
      <Input
        icon="search"
        placeholder="Search"
        fluid
        loading={loading}
        onKeyPress={onKeyPress}
      />
    </div>
  );
};

export default Search;
