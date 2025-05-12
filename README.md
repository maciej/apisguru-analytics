# API Guru Analytics

Analytics tools for OpenAPI specifications from APIs.guru.

## Setup

This project uses `uv` as the package manager. To set up the development environment:

1. Create a virtual environment:
```bash
uv venv .venv
```

2. Activate the virtual environment:
```bash
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
uv pip install -e ".[dev]"
```

## Development

The project uses:
- `black` for code formatting
- `isort` for import sorting
- `ruff` for linting
- `mypy` for type checking
- `pytest` for testing

## License

MIT 