# Contributing to Gemini Cowork OS

Thank you for your interest in building the future of autonomous work!

## Development Philosophy
1. **Evidence over Architecture**: We merge PRs that solve empirical failures identified in `FAILURE_REPORT.csv` or `HOW_USERS_THINK.md`.
2. **Observability First**: Any new feature must emit telemetry to the `ObservabilityLayer`.
3. **No Unsafe Tools**: Any tool that modifies state must declare `requires_approval=True`.

## Getting Started
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Install dev dependencies: `pip install -r requirements-dev.txt` (to be added)
4. Ensure code formatting using `black` and `isort`.

## Pull Request Process
1. Ensure all tests pass (`pytest`).
2. Update documentation if introducing architectural changes.
3. Describe *why* the change is needed, referencing a specific Chaos Benchmark if applicable.

## Roadmap Alignment
Before starting a massive refactor, please open an Issue to discuss it with the maintainers. We are currently prioritizing the transition from "Alpha Prototype" to "Production Runtime."
