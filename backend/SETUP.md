# RealPlanner Backend Setup Guide

## Quick Start (Routes API Only)

For immediate use with basic route optimization:

1. **Get Google Maps API Key**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the **Routes API**
   - Create an API key
   - Add the API key to your `.env` file:
     ```
     GOOGLE_MAPS_API_KEY=your_api_key_here
     GOOGLE_CLOUD_PROJECT_ID=your_project_id_here
     ```

2. **Test the Setup**:
   ```bash
   cd backend
   python3 tests/test_optimization.py
   ```

This will use Google Routes API with waypoint optimization, which provides good route optimization with minimal setup.

## Full Setup (Route Optimization API + Routes API)

For advanced optimization features:

1. **Enable Route Optimization API**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the **Route Optimization API**
   - Create a service account
   - Download the service account key JSON file

2. **Configure OAuth Credentials**:
   - Add the service account key to your `.env` file:
     ```
     GOOGLE_SERVICE_ACCOUNT_KEY={"type": "service_account", ...}
     ```
   - Or set it as an environment variable

3. **Install Dependencies**:
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2
   ```

4. **Test Both APIs**:
   ```bash
   python3 tests/test_optimization.py
   ```

## Environment Variables

Create a `.env` file in the backend directory:

```env
# Required for Routes API (minimum setup)
GOOGLE_MAPS_API_KEY=your_api_key_here
GOOGLE_CLOUD_PROJECT_ID=your_project_id_here

# Optional for Route Optimization API (advanced setup)
GOOGLE_SERVICE_ACCOUNT_KEY={"type": "service_account", ...}

# Database (if using)
DATABASE_URL=postgresql://user:pass@localhost/db
```

## API Comparison

| Feature | Routes API | Route Optimization API |
|---------|------------|------------------------|
| Setup Complexity | Simple (API key) | Complex (OAuth) |
| Optimization Quality | Good | Excellent |
| Time Windows | Basic | Advanced |
| Multi-vehicle | No | Yes |
| Cost | Lower | Higher |
| Reliability | High | High (with fallback) |

## Troubleshooting

### 401 Unauthorized Error
- **Routes API**: Check your API key is valid and Routes API is enabled
- **Route Optimization API**: Check OAuth credentials and API enablement

### 400 Bad Request Error
- Check that addresses are valid and geocodable
- Ensure timestamps are in the future
- Verify project ID is correct

### Fallback Behavior
The app automatically falls back to Routes API if Route Optimization API fails. Check logs to see which API is being used.

## Testing

Run the test suite:
```bash
cd backend
python3 tests/run_tests.py
```

Or test individual components:
```bash
python3 tests/test_optimization.py
``` 