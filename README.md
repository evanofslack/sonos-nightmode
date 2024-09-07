# sonos-nightmode

Schedule nightmode and speech enhancement on your sonos system.

## Overview

For some reason, sonos currently does not allow you to set a schedule for
nightmode or speech enhancement through their app. Therefore I wrote a simple
container capable of interacting with sonos api and scheduling these settings.

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

## Compatibility

Currently images are build for amd64, arm64, arm/v6 and arm/v7. The image has been
tested and runs on ubuntu and raspberry pi instances. The image currently does
not run on MacOS.
