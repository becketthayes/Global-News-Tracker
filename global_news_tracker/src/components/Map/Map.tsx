import { MapContainer, TileLayer } from 'react-leaflet';
import TopicMarker from './TopicMarker';

export default function Map() {
  return (
    <>
      <MapContainer
        center={[0, 0]}
        zoom={2}
        scrollWheelZoom={false}
        style={{ height: '100vh', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <TopicMarker position={[51.505, -0.09]} />
        <TopicMarker position={[40.7128, -74.006]} />
      </MapContainer>
    </>
  );
}
