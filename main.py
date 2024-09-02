import os
import sys
import time

import dotenv
import schedule
import soco


def set_nightmode(speaker: soco.SoCo, enabled: bool):
    print(f"nightmode before: {speaker.night_mode}")
    speaker.night_mode = enabled
    print(f"nightmode after: {speaker.night_mode}")


def main():
    dotenv.load_dotenv()
    name = os.getenv("SONOS_NAME")
    if name is None:
        print(f"could not find env var: SONOS_NAME")
        sys.exit(1)

    # name = "Living Room"
    speaker = soco.discovery.by_name(name)
    if speaker is None:
        print(f"could not find speaker: {name}")
        sys.exit(1)

    on = os.getenv("NIGHTMODE_ON")
    if name is None:
        print(f"could not find env var: NIGHTMODE_ON")
        sys.exit(1)

    off = os.getenv("NIGHTMODE_OFF")
    if name is None:
        print(f"could not find env var: NIGHTMODE_OFF")
        sys.exit(1)

    # on = "09:00"
    # off = "20:00"

    print(f"successfully found speaker: {name}")
    print(f"currently nightmode is: {speaker.night_mode}")
    print(f"scheduling system {name} nightmode on at {on} and off at {off}")

    schedule.every().day.at(on).do(set_nightmode, speaker=speaker, enabled=True)
    schedule.every().day.at(off).do(set_nightmode, speaker=speaker, enabled=False)

    while True:
        schedule.run_pending()
        time.sleep(15)


if __name__ == "__main__":
    main()
