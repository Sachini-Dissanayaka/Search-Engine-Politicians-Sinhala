import React from "react";
import { Card, Icon } from "semantic-ui-react";
import SearchResultsLoader from "./search-results-loader";

const SearchResults = ({ loading, query, result }) => {
  return (
    <div
      style={{
        marginTop: "1rem",
        width: "800px",
      }}
    >
      {!loading ? (
        <>
          {result.length ?<h4>Showing results for "{query}"</h4>:null}
          {result.map((res) => {
            return (
              <Card fluid>
                <Card.Content>
                  <Card.Header>{res.Name_si}</Card.Header>
                  <Card.Meta>
                    <span>{res.Political_Party_si}</span>
                  </Card.Meta>
                  <Card.Meta>
                    <span>{res.Position_si+" - "+ res.Period_si}</span>
                  </Card.Meta>
                  <div style={{marginTop:"1rem"}}/>
                  {res.Early_Life?<Card.Description>
                    <h4>Early Life</h4>
                    {res.Early_Life}
                  </Card.Description>:null}
                  <div style={{marginTop:"1rem"}}/>
                  {res.Education?<Card.Description>
                    <h4>Education</h4>
                    {res.Education}
                  </Card.Description>:null}
                  <div style={{marginTop:"1rem"}}/>
                  {res.Political_Career?<Card.Description>
                    <h4>Political Career</h4>
                    {res.Political_Career}
                  </Card.Description>:null}
                  <div style={{marginTop:"1rem"}}/>
                  {res.Family?<Card.Description>
                    <h4>Family</h4>
                    {res.Family}
                  </Card.Description>:null}
                </Card.Content>
              </Card>
            );
          })}
        </>
      ) : (
        <>
          <SearchResultsLoader />
          <SearchResultsLoader />
          <SearchResultsLoader />
        </>
      )}
    </div>
  );
};

export default SearchResults;
