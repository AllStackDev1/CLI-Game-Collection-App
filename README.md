# 🎮 GameHub CLI App

A terminal-based game collection application with user management, profile controls, and game menu navigation. Built for simplicity and extensibility — designed to support future game implementations with a clean, user-friendly CLI experience.

---

## 🚀 Features

- 🧑 **User Management**
  - Sign up / Login
  - View & edit profile
  - Password updates and validations
  - Soft delete (account deactivation with restoration support)

- 🎯 **Game Menu**
  - "Play Games" section with placeholder titles
  - Future-ready structure using OOP-based game definitions
  - Clean game selection flow with Rich CLI UI

- 🧱 **Architecture**
  - Flat, functional menu routing
  - Modular services, repositories, and services
  - `Session` state management
  - Clean separation between UI, logic, and data layers

---

## 🧑‍💻 Tech Stack

- **Language:** Python 3.10+
- **UI:** [Rich](https://github.com/Textualize/rich) for enhanced terminal visuals
- **Storage:** SQLite (via basic custom Database abstraction)
- **Dependency Management:** Poetry
- **Architecture:** Modular CLI with optional OOP layer for games

---

## 🧩 Folder Structure (Planned or Current)

```
project/
│
├── app/                   # Application UI and menu flow logic
│  └── menu.py             # Handles main and sub-menu display and routing
│
├── db/                   # Database-related components
│  ├── data/              # SQLite database files and backups
│  ├── migrations/        # SQL or Python migration scripts
│  ├── connection.py      # Centralized database connection logic
│  └── migration.py       # Migration runner and setup coordinator
│
├── games/                # Game module (OOP-based architecture)
│  └── base.py            # BaseGame class defining shared game interface
│
├── models/               # Data model representations
│  ├── user.py            # User model schema and helpers
│  └── game_session.py    # Game session model for tracking play history
│
├── repositories/         # Data access layer
│  ├── user.py            # User repository (CRUD + lookup)
│  └── game_session.py    # Game session repository (insert, update, fetch)
│
├── services/             # Business logic layer
│  ├── user.py            # Auth, profile update, and user flow handling
│  └── game_session.py    # Game tracking and session service functions
│
├── utils/                # Utility modules for cross-cutting concerns
│  ├── password.py        # Password hashing and verification
│  ├── session.py         # Logged-in session state management
│  └── validation.py      # Input validation and sanitization utilities
│
├── main.py                # Application entry point
└── README.md              # Project documentation and setup guide

```

---

## 🕹 Sample Menu Flow

```
Main Menu:
1. Play Games
2. View My Profile
3. Edit My Profile
4. Delete My Account
5. Logout
6. Exit Application

> Games Menu:
1. Game 1 - Hangman
2. Game 2 - Number Guessing
3. Game 3 - Tic Tac Toe
4. Return to Main Menu
```

---

## 🔒 Security & UX Highlights

- Password masking and confirmation
- Soft deletion using `deleted_at` flag
- Session clearing on logout and deletion
- Multiple confirmation prompts for sensitive actions
- Prevent login for deleted users

---

## 🔧 Setup Instructions

```bash
git clone https://github.com/yourusername/gamehub-cli.git
cd gamehub-cli

# Install dependencies using Poetry
poetry install

# Run the app in a Poetry shell
poetry shell
python main.py
```

---

## 🛠️ Roadmap / TODO

- [ ] Implement actual games (e.g., Hangman, Tic Tac Toe)
- [ ] Save game stats (scores, play counts)
- [ ] Leaderboard system
- [ ] Game difficulty settings via user preferences
- [ ] KYC verification flow (for multi-player support)
- [ ] Migrate to text-based GUI (e.g., Textual framework)

---

## 📄 License

MIT License — see `LICENSE` for details.

---

## 🙌 Acknowledgements

- [Rich by Textualize](https://github.com/Textualize/rich) for terminal formatting
- Inspired by classic CLI games and educational Python projects

---

