# Miyoo Mini Pushover Notifier

This is a python script that has been containerized into a Docker container to check for Miyoo Mini stock every 5 seconds. It will then send a push notification to Pushover to alert you of any new items.

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

# ****Docker Run Command****

Run your docker command like this:

`docker run -it --rm --env "APIKEY=PUSHOVER-API-KEY-HERE" --env "USERKEY=PUSHOVER-USER-KEY-HERE" yenba/miyoo-mini-checker`
