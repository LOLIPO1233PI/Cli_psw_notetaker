
# CLI Password Manager

A simple, open‑source, terminal‑based password manager written in Python.  
Entries are stored in a hidden directory as a Base85‑encoded JSON blob.

---

## Table of Contents

- [Features](#features)  
- [Requirements](#requirements)  
- [Installation](#installation) 

---

## Features

- **Add** new password entries (name, password, email/username).  
- **Retrieve** and display saved entries with colored output.  
- Stores everything in a hidden folder (`_`) using Base85 encoding so data isn’t immediately readable.  

---

## Requirements

- Python 3.6+ (uses `f-strings`)  
- Standard library only (no external dependencies)

---

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/LOLIPO1233PI/Cli_psw_notetaker.git
   cd cli-password-manager
