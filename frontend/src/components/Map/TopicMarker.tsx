import { Marker, Popup } from 'react-leaflet';
import { Card } from 'antd';

interface TopicMarkerProps {
  topic: string;
  position: [number, number];
  articleCount: number;
  articles: {
    title: string;
    url: string;
    summary?: string; 
  }[];
}

export default function TopicMarker({ topic, position, articleCount, articles }: TopicMarkerProps) {
  return (
    <Marker position={position}>
      <Popup minWidth={350}>
        {}
        <Card 
          title={topic} 
          style={{ width: 350, maxHeight: '400px', overflowY: 'auto' }}
          bodyStyle={{ padding: '12px' }}
        >
          <p style={{ marginBottom: '16px' }}><strong>Article Count:</strong> {articleCount}</p>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {}
            {articles.map(({ title, url, summary }) => (
              <div key={url}>
                <a 
                  href={url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  style={{ fontWeight: '600', fontSize: '14px', display: 'block', lineHeight: '1.2' }}
                >
                  {title}
                </a>
                
                {}
                {summary && (
                  <p style={{ fontSize: '12px', color: '#555', marginTop: '6px', marginBottom: '0', lineHeight: '1.4' }}>
                    {summary}
                  </p>
                )}
              </div>
            ))}
          </div>
        </Card>
      </Popup>
    </Marker>
  );
}