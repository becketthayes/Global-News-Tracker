import { MapContainer, TileLayer } from 'react-leaflet';
import TopicMarker from './TopicMarker';

export default function Map() {
  return (
    <>
      <MapContainer center={[0, 0]} zoom={2} scrollWheelZoom={false} style={{ height: '100vh', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {/* Example topic marker usage */}
        <TopicMarker
          topic="Topic 1"
          position={[51.505, -0.09]}
          articleCount={0}
          articles={[{ title: 'Article Title', url: 'https://www.bbc.com/sport' }]}
        />
      </MapContainer>
    </>
  );
}
