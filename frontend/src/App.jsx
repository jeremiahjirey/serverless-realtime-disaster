import { useEffect, useState } from "react";
import { API_BASE_URL } from "./config";

export default function App() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/events`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch data");
        return res.json();
      })
      .then((data) => {
        setEvents(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p style={{ textAlign: "center" }}>Loading data...</p>;
  if (error) return <p style={{ color: "red", textAlign: "center" }}>Error: {error}</p>;

  return (
    <div style={{ fontFamily: "Arial, sans-serif", padding: "2rem" }}>
      <h1 style={{ textAlign: "center" }}>🌍 Real-Time Disaster Tracker</h1>
      <p style={{ textAlign: "center" }}>Latest earthquake data from BMKG</p>

      {events.length === 0 ? (
        <p style={{ textAlign: "center" }}>No data available</p>
      ) : (
        <div style={{ maxWidth: "800px", margin: "0 auto" }}>
          {events.map((item) => (
            <div
              key={item.id}
              style={{
                background: "#f8f9fa",
                margin: "10px 0",
                padding: "15px",
                borderRadius: "10px",
                boxShadow: "0 0 5px rgba(0,0,0,0.1)",
              }}
            >
              <h3 style={{ margin: "0 0 5px 0" }}>{item.Wilayah}</h3>
              <p style={{ margin: 0 }}>
                <b>Magnitude:</b> {item.Magnitude}<br />
                <b>Kedalaman:</b> {item.Kedalaman}<br />
                <b>Lintang:</b> {item.Lintang}<br />
                <b>Bujur:</b> {item.Bujur}<br />
                <small>{item.Tanggal} — {item.Jam}</small>
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
