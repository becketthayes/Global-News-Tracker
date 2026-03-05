import { useEffect, useState } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import TopicMarker from '../components/Map/TopicMarker';
import { supabase } from '../supabaseClient';

// --- LEAFLET CSS & VITE 404 FIX ---
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconRetina from 'leaflet/dist/images/marker-icon-2x.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

// Override the default icon paths so Vite doesn't lose them in deployment
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: iconRetina,
  iconUrl: icon,
  shadowUrl: iconShadow,
});
// ----------------------------------

interface Article {
  title: string;
  url: string;
  summary: string;
}

interface ClusterData {
  id: number;
  lat: number;
  lng: number;
  label: string;
  article_count: number;
  articles: Article[];
}

export default function Map() {
  const [clusterData, setClusterData] = useState<ClusterData[]>([]);

  useEffect(() => {
    const fetchMapData = async () => {
      const { data, error } = await supabase
        .from('clusters')
        .select(`
          id,
          lat,
          lng,
          label,
          article_count,
          articles (
            title,
            url,
            summary
          )
        `);

      if (error) {
        console.error('Error fetching from Supabase:', error);
      } else {
        console.log('Fetched cluster data:', data);
        setClusterData(data as ClusterData[] || []);
      }
    };

    fetchMapData();
  }, []);

  return (
    <MapContainer 
      center={[20, 0]} 
      zoom={2} 
      scrollWheelZoom={true} 
      style={{ height: '100vh', width: '100%' }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      {clusterData.map((cluster) => (
        <TopicMarker
          key={cluster.id}
          topic={cluster.label || 'Trending Topic'}
          position={[cluster.lat, cluster.lng]}
          articleCount={cluster.article_count}
          articles={cluster.articles || []}
        />
      ))}
    </MapContainer>
  );
}