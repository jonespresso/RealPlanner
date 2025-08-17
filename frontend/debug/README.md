# Route Planner Frontend

A React-based frontend application for the RealPlanner route optimization system. This interface allows users to input addresses and time windows for house visits, then generates optimized routes.

## Features

- **Address Input**: Add start and destination addresses
- **Dynamic House Visits**: Add/remove house visit entries with address and time window inputs
- **Request Generation**: Generate JSON request payload for the backend API
- **Modern UI**: Clean, responsive design with smooth animations
- **Real-time Validation**: Form validation and user feedback

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## Usage

1. **Enter Start Address**: Provide your starting location
2. **Enter Destination Address** (optional): Provide your final destination
3. **Add House Visits**: Click the "+" button to add house visit entries
4. **Fill in Details**: For each house visit, enter:
   - Address
   - Start time window
   - End time window
5. **Generate Request**: Click "Generate Request" to create the JSON payload
6. **View Request**: The generated request will be displayed in JSON format

## API Integration

The frontend is designed to work with the RealPlanner backend API. The generated request follows this structure:

```json
{
  "start_address": "string",
  "destination_address": "string",
  "houses": [
    {
      "address": "string",
      "start_time": "datetime",
      "end_time": "datetime",
      "duration_minutes": 20
    }
  ]
}
```

## Development

### Project Structure

```
src/
├── App.tsx          # Main application component
├── App.css          # Application styles
├── index.tsx        # Application entry point
└── ...
```

### Available Scripts

- `npm start`: Runs the app in development mode
- `npm test`: Launches the test runner
- `npm run build`: Builds the app for production
- `npm run eject`: Ejects from Create React App (one-way operation)

## Technologies Used

- **React 19**: Modern React with hooks
- **TypeScript**: Type-safe JavaScript
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **Axios**: HTTP client for API requests

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Make your changes in a feature branch
2. Ensure all tests pass
3. Submit a pull request

## License

This project is part of the RealPlanner system.
