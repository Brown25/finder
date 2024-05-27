// src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import Map from './components/Map';

const places = [
    { name: "Place 1", lat: 51.505, lng: -0.09 },
    { name: "Place 2", lat: 51.51, lng: -0.1 }
];

ReactDOM.render(
    <React.StrictMode>
        <Map places={places} placeActions={{ append: console.log }} selectedIndex={0} />
    </React.StrictMode>,
    document.getElementById('root')
);
