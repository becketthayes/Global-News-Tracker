import { Marker, Popup } from 'react-leaflet';
import { Card } from 'antd';

interface TopicMarkerProps {
  topic: string;
  position: [number, number];
  articleCount: number;
  articles: {
    title: string;
    url: string;
  }[];
}

export default function TopicMarker({ topic, position, articleCount, articles }: TopicMarkerProps) {
  return (
    <>
      <Marker position={position}>
        <Popup>
          <Card title={topic} style={{ width: 300 }}>
            <p>Article Count: {articleCount}</p>
            {articles.map(({ title, url }) => (
              <div key={title}>
                <a href={url}>{title}</a>
              </div>
            ))}
          </Card>
        </Popup>
      </Marker>
    </>
  );
}
