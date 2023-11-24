# Pre-release 0.1

- Install and configure ErsatzTV
  - delete sample channel
  - configure Default encoding profile
  - configure default watermark
  - configure general settings
    - check default profile

- Connect your plex media server
- Sync the Movies Library
- Wait for sync to finish

locate your local ersatztv.sqlite3 data file to map as the DB
```
 docker run -it --rm -v ./ersatztv-config-folder:/db pknw1/ersatztv-bulkadd-channels:latest
```