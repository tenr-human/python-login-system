# Python Login & Authentication System

A graphical login and authentication system built using **Python, Tkinter, and MySQL**.  
The project provides a secure interface for user login, registration, password management, and administrator control.

---

## Project Overview

This system demonstrates a complete **GUI-based authentication system** with database integration.  
Users can create accounts, log in securely, and manage their credentials, while administrators can monitor and control the database.

The application focuses on:

- User-friendly graphical interface
- Secure credential storage
- Administrator account management
- Simple database integration

---

## Features

### User Features
- User Login
- User Registration
- Password Reset
- Contact Admin option

### Admin Features
- Secure admin authentication
- Delete user accounts
- View all users in the database
- Display total number of registered users

---

## Technology Stack

| Technology | Purpose |
|------------|--------|
| Python | Backend logic |
| Tkinter | GUI interface |
| MySQL | Database storage |
| mysql-connector-python | Python MySQL connection |

---

## System Requirements

### Hardware
- RAM: 2GB – 4GB
- Storage: Minimum 128GB
- Operating System: Windows

### Software
- Python 3.x
- MySQL 8.0
- Python IDE (VS Code / IDLE)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/USERNAME/python-login-system.git
cd python-login-system
```

### 2. Install dependencies

```bash
pip install mysql-connector-python
```

### 3. Setup MySQL database

Run the SQL file:

```sql
source database.sql
```

or manually create:

```sql
CREATE DATABASE login_data;

USE login_data;

CREATE TABLE data (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50)
);
```

### 4. Update database credentials

In `login_system.py` modify:

```python
db_connection = con.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="login_data"
)
```

### 5. Run the application

```bash
python login_system.py
```

---

## Admin Login

Default Admin Credentials:

```
Username: admin
Password: A4DM1N
```

---

## Project Structure

```
python-login-system
│
├── login_system.py
├── README.md
├── requirements.txt
└── database.sql
```

---

## Future Improvements

- Password hashing for better security
- Email verification for registration
- User session management
- Improved UI design

---

## Conclusion

This project demonstrates how **Python, Tkinter, and MySQL** can be integrated to build a complete login and authentication system with administrative controls.

---

## License

This project is open-source and available for educational purposes.
