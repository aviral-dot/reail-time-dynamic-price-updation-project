import React, { useEffect, useState } from 'react';

function App() {
  const [prices, setPrices] = useState({});

  useEffect(() => {
    const ws = new WebSocket(`ws://${window.location.hostname}:3001`);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setPrices(prev => ({
        ...prev,
        [data.region]: data
      }));
    };
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Real-Time Regional Pricing</h1>
      {["NY", "CA", "TX"].map(region => (
        <div key={region} style={{ margin: "1rem 0", border: "1px solid #ccc", padding: "1rem", borderRadius: "10px" }}>
          <h3>{region}</h3>
          <p><b>Predicted Price:</b> {prices[region]?.predicted_price || "Loading..."}</p>
          <p><b>Timestamp:</b> {prices[region]?.timestamp || "Loading..."}</p>
        </div>
      ))}
    </div>
  );
}

export default App;
