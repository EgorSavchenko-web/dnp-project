# Phonebook Lookups with RPC

A modifiable phonebook service where users can add, edit, delete, and look up contacts.  
Built as a remote phonebook using XML-RPC, where multiple clients can query and manage contact information concurrently.  
The backend is memory-based with optional JSON snapshots for durability.

## Features

- Add, edit, delete, and lookup contacts
- Name-to-number resolution
- Concurrent client request handling (threaded server + RLock)
- Crash-safe persistence with atomic JSON writes
- In-memory storage for fast read access
## How To Run
### Start server
```bash
python phonebook_server.py
````
### Start client
```bash
python phonebook_client.py http://localhost:8000
```
### Commands
```bash
add NAME NUMBER
edit NAME NUMBER
delete NAME
lookup NAME
list
exit
```

### Run stress test
```bash
python stress_test.py
```

### Run latency benchmark
```bash
python look_up.py
```
## Demonstration
[Watch demo](./demo.mp4)

## Connection to the repository

### Option 1: Fresh Clone (recommended)

```bash
git clone https://github.com/EgorSavchenko-web/dnp-project.git
cd dnp-project
```

### Option 2: Connect Existing Local Repo

```
cd existing_repo
git remote add origin https://github.com/EgorSavchenko-web/dnp-project.git
git branch -M main
git push -uf origin main
```
***
## Git Workflow
Used a **main** branch and separate branches for each team member (`aksiniia`, `andrey`, `egor`, `ekaterina`, `matvey`). Everyone worked in their own branch. Changes were merged into `main` via pull requests after code review. All branches were regularly synced with `main` to avoid conflicts.
## Authors and acknowledgment
**Ekaterina Kuznetsova** (...)<br>
**Aksiniia Miasoedova** (README and report writer)<br>
**Andrei Ilin** (...)<br>
**Egor Savchenko** (...)<br>
**Matvey Shulaev** (...)<br>
