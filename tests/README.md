# Test Suite Structure - Updated 2025-05-18

## Organization
- `unit/`: Unit tests
  - `core/`: Core functionality tests
  - `ai/`: AI module tests
  - `analysis/`: Analysis module tests
    - `technical/`: Technical analysis tests
    - `sentiment/`: Sentiment analysis tests
  - `exchanges/`: Exchange-related tests
- `integration/`: Integration tests
  - `arbitrage/`: Arbitrage integration tests
  - `exchanges/`: Exchange integration tests
  - `sentiment/`: Sentiment integration tests
- `performance/`: Performance tests
- `system/`: System-level tests

## Running Tests
```bash
./run_tests_v2.sh
```

## Version History
See VERSION_HISTORY.md for complete evolution history.

## Note
All test versions are preserved in Git history.
Use `git log --follow <file>` to see complete file history.
