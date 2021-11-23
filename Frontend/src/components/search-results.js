import React from "react";
import { Card, Rating, Image } from "semantic-ui-react";
import SearchResultsLoader from "./search-results-loader";

// TODO: Fill
const politicalPartiesToColorMap = new Map([
  ["Sri Lanka Freedom Party", "blue"],
  ["Sri Lanka Freedom Party(People's Alliance)","blue"],
  ["Sri Lanka Freedom Party(United People's Freedom Alliance)","blue"],
  ["United National Party(United National Front for Good Governance)","purple"],
  ["United National Party(United National Front)", "green"],
  ["United National Party","green"],
  ["United National Party |","green"],
  ["Sri Lanka Podujana Peramuna","red"],
  ["Sri Lanka Podujana Peramuna(United People's Freedom Alliance)","red"],
  ["Sri Lanka Podujana Peramuna(Sri Lanka People's Freedom Alliance)","red"],
  ["Samagi Jana Balawegaya","green"],
  ["Lanka Sama Samaja Party","green"],
  ["Tamil United Liberation Front","green"],
  ["Sinhala Language Front","blue"],
  ["Sinhala Language Front(Mahajana Eksath Peramuna)","blue"],
  ["Sri Lanka Freedom Party(Mahajana Eksath Peramuna)","blue"]
]);

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
          {result.length ? <h4>Showing results for "{query}"</h4> : null}
          {result.map((res) => {
            return (
              <Card fluid>
                <Card.Content>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                    }}
                  >
                    <Image
                      src={`${
                        res.Gender_en === "Male" ? "male" : "female"
                      }.jpeg`}
                      size="tiny"
                    />
                    <div
                      style={{
                        marginLeft: "1rem",
                        width: "100%",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                        }}
                      >
                        <div style={{ fontWeight: "900", fontSize: "14pt" }}>
                          {res.Name_si}
                        </div>
                        <Rating
                          icon="star"
                          defaultRating={res.Rate*0.5}
                          maxRating={5}
                          disabled
                        />
                      </div>
                      <div
                        style={{
                          color: politicalPartiesToColorMap.get(
                            res.Political_Party_en
                          ),
                        }}
                      >
                        {res.Political_Party_si}
                      </div>
                      <div>{res.Position_si + " (" + res.Period_si + ") "}</div>
                    </div>
                  </div>
                  <div style={{ marginTop: "1rem" }} />
                  {res.Early_Life ? (
                    <Card.Description style={{ textAlign: "justify" }}>
                      <h4 style={{ color: "black" }}>Early Life</h4>
                      {res.Early_Life}
                    </Card.Description>
                  ) : null}
                  <div style={{ marginTop: "1rem" }} />
                  {res.Education ? (
                    <Card.Description style={{ textAlign: "justify" }}>
                      <h4 style={{ color: "black" }}>Education</h4>
                      {res.Education}
                    </Card.Description>
                  ) : null}
                  <div style={{ marginTop: "1rem" }} />
                  {res.Political_Career ? (
                    <Card.Description style={{ textAlign: "justify" }}>
                      <h4 style={{ color: "black" }}>Political Career</h4>
                      {res.Political_Career}
                    </Card.Description>
                  ) : null}
                  <div style={{ marginTop: "1rem" }} />
                  {res.Family ? (
                    <Card.Description style={{ textAlign: "justify" }}>
                      <h4 style={{ color: "black" }}>Family</h4>
                      {res.Family}
                    </Card.Description>
                  ) : null}
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
      <div style={{ height: "4rem" }} />
    </div>
  );
};

export default SearchResults;
