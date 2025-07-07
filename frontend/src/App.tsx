import React, { useState } from 'react';
import './App.css';

interface AddressEntry {
  id: string;
  address: string;
  startTime: string;
  endTime: string;
  durationMinutes: number;
}

interface RoutePlanRequest {
  start_address: string;
  destination_address: string;
  houses: Array<{
    address: string;
    start_time: string;
    end_time: string;
    duration_minutes: number;
  }>;
}

function App() {
  const [startAddress, setStartAddress] = useState('');
  const [destinationAddress, setDestinationAddress] = useState('');
  const [addressEntries, setAddressEntries] = useState<AddressEntry[]>([]);
  const [generatedCurl, setGeneratedCurl] = useState<string>('');

  const addAddressEntry = () => {
    const newEntry: AddressEntry = {
      id: Date.now().toString(),
      address: '',
      startTime: '',
      endTime: '',
      durationMinutes: 20
    };
    setAddressEntries([...addressEntries, newEntry]);
  };

  const removeAddressEntry = (id: string) => {
    setAddressEntries(addressEntries.filter(entry => entry.id !== id));
  };

  const updateAddressEntry = (id: string, field: keyof AddressEntry, value: string | number) => {
    setAddressEntries(addressEntries.map(entry => 
      entry.id === id ? { ...entry, [field]: value } : entry
    ));
  };

  const generateRequest = () => {
    const request: RoutePlanRequest = {
      start_address: startAddress,
      destination_address: destinationAddress,
      houses: addressEntries.map(entry => ({
        address: entry.address,
        start_time: entry.startTime,
        end_time: entry.endTime,
        duration_minutes: entry.durationMinutes
      }))
    };

    const jsonBody = JSON.stringify(request, null, 2);
    const curlCommand = `curl -X POST "http://localhost:8000/api/v1/plan-route" \\
  -H "Content-Type: application/json" \\
  -d '${jsonBody}'`;

    setGeneratedCurl(curlCommand);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Route Planner</h1>
      </header>
      
      <main className="App-main">
        <div className="form-section">
          <h2>Route Configuration</h2>
          
          <div className="address-inputs">
            <div className="input-group">
              <label htmlFor="start-address">Start Address:</label>
              <input
                id="start-address"
                type="text"
                value={startAddress}
                onChange={(e) => setStartAddress(e.target.value)}
                placeholder="Enter start address"
              />
            </div>
            
            <div className="input-group">
              <label htmlFor="destination-address">Destination Address:</label>
              <input
                id="destination-address"
                type="text"
                value={destinationAddress}
                onChange={(e) => setDestinationAddress(e.target.value)}
                placeholder="Enter destination address (optional)"
              />
            </div>
          </div>

          <div className="houses-section">
            <div className="section-header">
              <h3>House Visits</h3>
              <button 
                className="add-button"
                onClick={addAddressEntry}
                type="button"
              >
                +
              </button>
            </div>

            {addressEntries.length === 0 && (
              <p className="no-entries">No house visits added yet. Click the + button to add one.</p>
            )}

            {addressEntries.map((entry) => (
              <div key={entry.id} className="address-entry">
                <input
                  type="text"
                  value={entry.address}
                  onChange={(e) => updateAddressEntry(entry.id, 'address', e.target.value)}
                  placeholder="Enter address"
                  className="address-input"
                />
                <input
                  type="datetime-local"
                  value={entry.startTime}
                  onChange={(e) => updateAddressEntry(entry.id, 'startTime', e.target.value)}
                  className="time-input"
                />
                <input
                  type="datetime-local"
                  value={entry.endTime}
                  onChange={(e) => updateAddressEntry(entry.id, 'endTime', e.target.value)}
                  className="time-input"
                />
                <input
                  type="number"
                  value={entry.durationMinutes}
                  onChange={(e) => updateAddressEntry(entry.id, 'durationMinutes', parseInt(e.target.value) || 0)}
                  placeholder="Duration (min)"
                  className="duration-input"
                  min="1"
                  max="480"
                />
                <button
                  className="remove-button"
                  onClick={() => removeAddressEntry(entry.id)}
                  type="button"
                >
                  ×
                </button>
              </div>
            ))}
          </div>

          <button 
            className="generate-button"
            onClick={generateRequest}
            disabled={addressEntries.length === 0}
          >
            Generate cURL Command
          </button>
        </div>

        {generatedCurl && (
          <div className="request-section">
            <h2>Generated cURL Command</h2>
            <pre className="request-display">{generatedCurl}</pre>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
