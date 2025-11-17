import { Marker, Popup } from 'react-leaflet';

interface TopicMarkerProps {
  position: [number, number];
}

export default function TopicMarker({ position }: TopicMarkerProps) {
  return (
    <>
      <Marker position={position}>
        <Popup>
          A pretty CSS3 popup. <br /> Easily customizable.
        </Popup>
      </Marker>
    </>
  );
}
