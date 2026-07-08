![](https://github.com/scanapi/design/raw/main/images/github-hero-dark.png)

# Community Dashboard

A modern dashboard for tracking community health, contributor activity, and project momentum for ScanAPI. It helps maintainers and contributors quickly understand engagement trends, onboarding opportunities, and repository performance through a clean Streamlit interface.

## About the Project

This project turns GitHub community data into actionable insights. It highlights open issues, pull request activity, response and merge times, and contributor trends so teams can better support onboarding and ecosystem growth.

### Tech Stack

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-ff4b4b)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458)
![Plotly](https://img.shields.io/badge/Plotly-Visualizations-3F4F75)
![PyGithub](https://img.shields.io/badge/PyGithub-GitHub%20API-181717)

## Getting Started

### Prerequisites

- Python 3.9 or newer
- A virtual environment tool such as `venv`
- Git

### Installation

```bash
git clone <your-fork-url>
cd community-dashboard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run src/app.py
```

Then open the local URL shown in the terminal in your browser.

## Contributing

Contributions are welcome. If you find a bug, have an idea for an improvement, or want to help shape the dashboard, please open an issue or submit a pull request.

Important: before committing any changes, developers must run `black src/` to ensure the codebase stays consistently formatted.
