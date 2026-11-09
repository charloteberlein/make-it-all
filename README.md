# Team 2 (Team Projects - Part 1): PySide6 Productivity and Knowledge Management System Desktop Application

## Key Features
*   **Account Management & Security**
    *   **Sign in, registration & password recovery:** Simple, secure login flow with custom input checks for every field requirement.
    *   **Sign out & accessibility:** Quick sign out feature with a built-in light/dark theme toggle, designed to meet contrast standards for easier reading.

*   **Interactive Dashboard**
    *   **Metrics & insights:** Visual widgets, progress bars and graphs showing team performance and individual employee task progress at a glance.
    *   **Tailored user views:** Automatically changes its layout and features depending on the logged-in user's role/rank type.

*   **Task & Project Management (To-Do Lists)**
    *   **Dedicated task views:** Separate to-do list pages for managing personal and shared project tasks.
    *   **Status management:** Clear visual indicators to monitor the status/progress on all active tasks.

*   **Knowledge Base (Topics & Posts)**
    *   **Categorised discussions:** Dedicated boards/filters to organise technical and non-technical topics.
    *   **Rich formatting:** Posts support formatted text and custom styling to keep communications informative, clean, and easy to read.

*   **Data & System Design**
    *   **JSON data storage:** Simple local .JSON files act as the database to hold and update posts, topics, tasks, and user data.

## Repository structure
```
├── assets/
│   ├── mock_data/
│   │    ├── posts.json
│   │    ├── tasks.json
│   │    ├── topics.json
│   │    └── users.json
│   └── styles/
│        ├── dark.qss          # Dark theme stylesheet
│        └── light.qss         # Light theme stylesheet
├── src/
│   └── make_it_all/           # Importable application package
│       ├── pages/
│       ├── app.py
│       ├── helpers.py
│       └── notifications.py
├── tests/                     # Pytest
├── pyproject.toml             # Package metadata and dev tools
├── requirements.txt
└── README.md
```

## Getting Started
### Prerequisites
* **Python 3.14+** (recommended) installed on your system.
* **pip** Python package manager, usually included with Python.

### Installation Guide
1. **Clone the Repository:**

2. **Create & activate the virtual environment:**

   Windows -
   ```powershell
   python -m venv C:\dev\env
   C:\dev\env\Scripts\Activate.ps1
   ```

   MacOS/Linux -
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

## Running the Application
Once the virtual environment is active and the package is installed, launch it from the repository root using:
``` bash
python -m make_it_all
```
The `make-it-all` command is also available after installation. Development helpers are installed
with the `dev` extra; launch from the repository root so the current root-level assets and JSON
files can be found. Once tests are added, run them with `pytest` and check style with `ruff check .`.

## Authors & Acknowledgements
### Team Members
Charlot Eberlein
Yasmin Ahrabi
Kei Mann
Eleanor Cooke
Juliette Crossman
Elizabeth Watson

### Tech Stack
Language: [Python](https://www.python.org/)

GUI Framework: [PySide6 (QtWidget & Qt modules)](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/index.html)