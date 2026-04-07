# sonos-nightmode

Schedule night mode and speech enhancement on your Sonos system.

## Overview

Sonos does not currently allow scheduling night mode or speech enhancement
through the app. This container uses the Sonos API to apply those settings on a
daily schedule.

The service now also:
- skips unnecessary writes when the speaker is already in the target state
- retries transient failures and re-discovers the speaker when needed

## Running

This app can be run from a [pre-built docker container](https://hub.docker.com/r/evanofslack/sonos-nightmode/tags).

```yaml
services:
  sonos-nightmode:
    container_name: sonos-nightmode
    image: evanofslack/sonos-nightmode # or use `build: { context: . }` for local patched version
    restart: unless-stopped
    network_mode: host # must run with host networking to discover sonos system
    env_file:
      - .env
    environment:
      - SONOS_NAME=${SONOS_NAME}
      - NIGHTMODE_ON=${NIGHTMODE_ON}
      - NIGHTMODE_OFF=${NIGHTMODE_OFF}
      - SPEECH_ENHANCE_ON=${SPEECH_ENHANCE_ON}
      - SPEECH_ENHANCE_OFF=${SPEECH_ENHANCE_OFF}
      - TZ=${TZ}
```

## Run Local Patched Version

```bash
cp .env.example .env
# edit .env (at least SONOS_NAME)
docker compose up -d --build
```

## Compatibility

Currently images are built for amd64, arm64, arm/v6, and arm/v7. The image has
been tested on Ubuntu and Raspberry Pi instances. The image currently does not
run on macOS.
