# Miyoo Mini Stock Notifier

This is a python script that has been containerized into a Docker container to check for Miyoo Mini stock every 30 seconds. It will then send a push notification to Pushover to alert you of any new items as well as how much of each Miyoo is in stock.

## Prerequisites

- **Pushover Account**
    - Notifications are achieved by utilizing [Pushover](https://pushover.net/). You will need to create a Pushover account to properly run this script.
- **Pushover API User Key (`USERKEY`)**
    - Documentation is here - [https://pushover.net/api](https://pushover.net/api)
- **Pushover API Token (`APIKEY`)**
    - Documentation is here - [https://pushover.net/api](https://pushover.net/api)
- **Docker**

## Docker Hub Repo

[https://hub.docker.com/repository/docker/yenba/miyoo-mini-checker](https://hub.docker.com/repository/docker/yenba/miyoo-mini-checker)

# **Docker Run Command**

Run your docker command like this:

```docker 
docker run -d --name=miyoo-mini-checker --env "PYTHONUNBUFFERED=1" --env "APIKEY=PUSHOVER-API-KEY-HERE" --env "USERKEY=PUSHOVER-USER-KEY-HERE" yenba/miyoo-mini-checker
```

# **Docker Compose Command**

Add this to your docker-compose.yml file:

```docker
version: "3.3"
services:
  miyoo-mini-checker:
    image: yenba/miyoo-mini-checker
    container_name: miyoo-mini-checker
    environment:
      - APIKEY=PUSHOVER_API_KEY_HERE
      - USERKEY=PUSHOVER_USER_KEY_HERE
      - PYTHONUNBUFFERED=1
```
