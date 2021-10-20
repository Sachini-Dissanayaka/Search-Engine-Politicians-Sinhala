import React from "react";
import ContentLoader from "react-content-loader";

const SearchResultsLoader = () => (
  <ContentLoader
    speed={1.2}
    width={1000}
    height={160}
    viewBox="0 0 1000 160"
    backgroundColor="#d3d3d3"
    foregroundColor="#ecebeb"
  >
    <rect x="15" y="18" rx="0" ry="0" width="180" height="14" />
    <rect x="15" y="38" rx="0" ry="0" width="800" height="8" />
    <rect x="15" y="53" rx="0" ry="0" width="800" height="8" />
    <rect x="15" y="67" rx="0" ry="0" width="800" height="8" />
    <rect x="15" y="82" rx="0" ry="0" width="800" height="8" />
    <rect x="15" y="110" rx="0" ry="0" width="80" height="8" />
  </ContentLoader>
);

export default SearchResultsLoader;
