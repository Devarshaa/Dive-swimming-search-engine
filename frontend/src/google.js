//import React, { useState, useEffect } from 'react';
//import { google } from 'googleapis';

//const SearchResults = ({ query }) => {
//  const [results, setResults] = useState([]);

//  useEffect(() => {
//    const search = async () => {
//      const cx = 'YOUR_CSE_ID'; // Replace with your CSE ID
//      const apiKey = 'YOUR_API_KEY'; // Replace with your API key
//      const searchClient = google.customsearch('v1');

//      const res = await searchClient.cse.list({
//        cx: cx,
//        q: query,
//        auth: apiKey,
//        num: 10, // Number of results to fetch
//      });

//      if (res.status === 200 && res.data.items) {
//        setResults(res.data.items);
//      }
//    };

//    search();
//  }, [query]);

//  return (
//    <>
//      <input type="text" defaultValue={query} />
//      <ul>
//        {results.map((result) => (
//          <li key={result.cacheId}>
//            <a href={result.link}>{result.title}</a>
//          </li>
//        ))}
//      </ul>
//    </>
//  );
//};

//export default SearchResults;