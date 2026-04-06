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
    image: evanofslack/sonos-nightmode
    restart: unless-stopped
    network_mode: host # must run with host networking to discover sonos system
    environment:
      - SONOS_NAME=Living Room # name of your sonos system
      - NIGHTMODE_ON=20:00 # 24 hour time
      - NIGHTMODE_OFF=09:00 # must include leading 0
      - SPEECH_ENHANCE_ON=20:00
      - SPEECH_ENHANCE_OFF=09:00
      - TZ=America/New_York # important to set timezone so scheduling is accurate
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
