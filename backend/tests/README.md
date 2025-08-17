# Backend Tests

This directory contains tests for the RealPlanner backend.

## Test Files

- `test_optimization.py` - Tests the route optimization functionality using Google Routes API
- `run_tests.py` - Test runner script to execute all tests

## Running Tests

### Run all tests:
```bash
cd backend
python3 tests/run_tests.py
```

### Run individual test (script):
```bash
cd backend
python3 tests/test_optimization.py
```

### Run with pytest (optional):
```bash
cd backend
pytest tests/test_optimization.py -s -q
```

## Test Requirements

- Google Maps API key must be set in environment variables
- Internet connection required for API calls
- Python 3.7+ required

## Test Structure

Tests are organized to:
- Import from the parent `app` directory
- Use realistic test data (San Francisco addresses)
- Handle API errors gracefully
- Provide clear output for debugging

## Adding New Tests

1. Create new test file in this directory
2. Import from parent directory: `sys.path.append(os.path.join(os.path.dirname(__file__), '..'))`
3. Add test to `run_tests.py` if needed
4. Follow naming convention: `test_*.py` 