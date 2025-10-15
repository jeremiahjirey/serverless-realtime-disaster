import { useEffect, useState } from "react";
import { API_BASE_URL } from "./config";

export default function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE_URL}/events`)
      .then(res => res.json())
      .then(setData)
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ fontFamily: "Arial", padding: "2rem", textAlign: "center" }}>
      <h2>🌍 Real-Time Disaster Tracker</h2>
      {data.length === 0 ? (
        <p>Loading...</p>
      ) : (
        data.map((item) => (
          <div key={item.id} style={{
            margin: "10px auto",
            background: "#fff",
            padding: "10px",
            borderRadius: "8px",
            boxShadow: "0 0 5px rgba(0,0,0,0.1)",
            width: "60%"
          }}>
            <b>{item.Wilayah}</b><br/>
            Magnitude: {item.Magnitude}<br/>
            {item.Tanggal} {item.Jam}
          </div>
        ))
      )}
    </div>
  );
}
