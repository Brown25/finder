// src/components/Marker.js
import React from 'react';
import { Marker as LeafletMarker, Popup } from 'react-leaflet';

export default function Marker({ place }) {
    return (
        <LeafletMarker position={[place.lat, place.lng]}>
            <Popup>{place.name}</Popup>
        </LeafletMarker>
    );
}
