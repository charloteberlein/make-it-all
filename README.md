# Team 2 (Team Projects - Part 1): PySide6 Productivity and Knowledge Management System Desktop Application

## Key Features
*   **Account Management & Security**
    *   **Sign in, registration & password recovery:** Simple, secure login flow with custom input checks for every field requirement.
    *   **Sign out & accessibility:** Quick sign out feature with a built-in light/dark theme toggle, designed to meet contrast standards for easier reading.

*   **Interactive Dashboard**
    *   **Metrics & insights:** Visual widgets and progress bars showing team performance and individual employee task progress at a glance.
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
│   ├── pages/
│   │   ├── account/
│   │   ├── dashboard/         # Dashboard files
│   │   ├── posts/             # make_post, make_content_page, post_content, posts_page
│   │   ├── todos/             # Todo list files
│   │   ├── topics/            # topics_content_page, topic_content, topic_page
│   │   ├── base_page.py
│   │   ├── header.py
│   │   ├── page_index.py
│   │   └── sidebar.py
│   ├── helpers.py             # Reads and writes to .JSON files
│   └── app.py                 # Main entry point
└── README.md
```

## Getting Started
### Prerequisites
* **Python 3.10+** installed on your system.
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
4. **Install dependencies:**
   ```bash
   pip install PySide6
   ```

## Running the Application
Once the virtual environment is active and the dependencies are installed, launch the application from the root directory using:
``` bash
python src/app.py
```

## Authors & Acknowledgements
### Team members
| Team member | Responsibility |
|---|---|
Charlot Eberlein | Initial Repo Set-Up, File structure and refactoring, Header module, Posts and Topics section, populating .JSON files. |
Yasmin Ahrabi | Posts & Topics section, Sign In credential validation, helper.py and refactoring, populating .JSON files. |
Eleanor Cooke | Dashboard pages for each user type, incl. data widgets and progress trackers. |
Juliette Crossman | Dashboard pages for each user type, incl. data widgets and progress trackers. |
Kei Mann | Sign up page layout, forgot password & register pages layout & validation, sidebar & setting dropdown, light/dark config, README guide. |s
Elizabeth Watson | Personal to-do list section, incl. status & type. |

### Tech Stack
Language: [Python](https://www.python.org/)
GUI Framework: [PySide6 (QtWidget & Qt modules)](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/index.html)