# Phonebook Lookups with RPC

A write-once phonebook service that supports querying and returns data signed by the server for verification.  
Built as a remote phonebook using RPC, where clients can query and manage contact information.  
The backend can be memory-based or use a database for persistence.

## Features

- Name-to-number resolution
- Find the number of a person based on a name
- Server-signed responses for verification
- Concurrent client request handling

## Demonstration
![ADD demo video](./demo.gif)

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

## Git Workflow Process description

We decided to separate the development into ???? branches: **main**, ??????? странно писать ветки с именами

**main** is a branch to which other branches are merged. Apart from merge commits it includes the commits of **README.md** file


Each branch merge is accompanied by a Pull Request. If both branches are compatible each other and every team member
came to consensus, then branches are merged completely. Each Pull Request ideally is solved within 1 day


## Authors and acknowledgment
**Ekaterina Kuznetsova** (...)<br>
**Aksiniia Miasoedova** (README and report writer)<br>
**Andrei Ilin** (...)<br>
**Egor Savchenko** (...)<br>
**Matvey Shulaev** (...)<br>

## Project status
On active process...
