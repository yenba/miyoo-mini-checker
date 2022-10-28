# Miyoo Mini Stock Notifier

This is a python script that has been containerized into a Docker container to check for Miyoo Mini stock every 30 seconds. You can configure it to send alerts to anything that Apprise supports.

## Prerequisites

- **Docker**

## Docker Hub Repo

[https://hub.docker.com/repository/docker/yenba/miyoo-mini-checker](https://hub.docker.com/repository/docker/yenba/miyoo-mini-checker)

## **Docker Compose Command**

Add this to your docker-compose.yml file:

```
version: "3.3"
services:
  miyoo-mini-checker:
    image: yenba/miyoo-mini-checker
    container_name: miyoo-mini-checker
    environment:
      - PYTHONUNBUFFERED=1
```

## Instructions

This docker container sends notifications via the wonderful Apprise. [Check the Apprise documentation here.](https://github.com/caronc/apprise#supported-notifications) 

You’ll need to format the config file found at `config/config.yml` in the same format as the their [YAML documentation](https://github.com/caronc/apprise/wiki/Config_yaml).