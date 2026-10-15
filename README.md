# Team 2 (Team Projects - Part 1): PySide6 Productivity and Knowledge Management System Desktop Application

## Key Features

## Repository structure
```
├── app.py              # Main application entry point & QStackedWidget navigation controller
├── styles/
│   ├── light.qss       # Light theme Qt Style Sheet
│   └── dark.qss        # Dark theme Qt Style Sheet
├── pages/
│   ├── sign_in.py      # SignInPage widget
│   ├── register.py     # RegisterPage widget
│   └── main_window.py  # MainWindow controller, sidebar navigation, and theme toggling
└── README.md
```

## Getting Started
### Prerequisites
* **Python 3.10+** installed on your system.
* **pip** Python package manager, usually included with Python.

### Installation Guide
1. **Clone the Repository:**
2. **Create & activate the virtual environment**
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
   pip install PySide6
   ```

## Running the Application
Once the virtual environment is active and the dependencies are installed, launch the application from the root directory using:
``` bash
python app.py
```

## Authors & Acknowledgements
### Team members
| Team member | Responsibility |
|---|---|
Charlot Eberlein | Initial Repo Set-Up, Readme Authors & Mock-data .JSON files |
Yasmin Ahrabi | TBD |
Eleanor Cooke | TBD |
Juliette Crossman | TBD |
Kei Mann | Login, Register, Light & Dark Theme, Readme Instructions & File Structure |
Elizabeth Watson | TBD |

