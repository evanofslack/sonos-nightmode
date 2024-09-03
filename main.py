import os
import sys
import time
from dataclasses import dataclass
from typing import Optional

import dotenv
import schedule
import soco


@dataclass
class Config:
    speaker_name: str
    nightmode_on: Optional[str]
    nightmode_off: Optional[str]
    speech_enhance_on: Optional[str]
    speech_enhance_off: Optional[str]


def config_from_env() -> Config:
    speaker_name = os.getenv("SONOS_NAME")
    if speaker_name is None:
        print(f"could not find env var: SONOS_NAME")
        sys.exit(1)

    nightmode_on_var = "NIGHTMODE_ON"
    nightmode_on = os.getenv(nightmode_on_var)
    if nightmode_on is None:
        print(f"could not find env var: {nightmode_on_var}")

    nightmode_off_var = "NIGHTMODE_OFF"
    nightmode_off = os.getenv(nightmode_off_var)
    if nightmode_off is None:
        print(f"could not find env var: {nightmode_off_var}")

    speech_on_var = "SPEECH_ENHANCE_ON"
    speech_enhance_on = os.getenv(speech_on_var)
    if speech_enhance_on is None:
        print(f"could not find env var: {speech_on_var}")

    speech_off_var = "SPEECH_ENHANCE_OFF"
    speech_enhance_off = os.getenv(speech_off_var)
    if speech_enhance_off is None:
        print(f"could not find env var: {speech_off_var}")

    config = Config(
        speaker_name=speaker_name,
        nightmode_on=nightmode_on,
        nightmode_off=nightmode_off,
        speech_enhance_on=speech_enhance_on,
        speech_enhance_off=speech_enhance_off,
    )
    return config


def find_speaker(speaker_name: str) -> soco.SoCo:
    speaker = soco.discovery.by_name(speaker_name)
    if speaker is None:
        print(f"could not find speaker: {speaker_name}")
        sys.exit(1)
    print(f"successfully found speaker: {speaker_name}")
    print(f"currently nightmode is: {speaker.night_mode}")
    print(f"currently speech enhancement is: {speaker.dialog_mode}")
    return speaker


def set_nightmode(speaker: soco.SoCo, enabled: bool):
    print(f"nightmode before: {speaker.night_mode}")
    speaker.night_mode = enabled
    print(f"nightmode after: {speaker.night_mode}")


def set_speech_enhance(speaker: soco.SoCo, enabled: bool):
    print(f"speech enhanced before: {speaker.dialog_mode}")
    speaker.night_mode = enabled
    print(f"speech enhanced after: {speaker.dialog_mode}")


def set_schedule(config: Config, speaker: soco.SoCo):
    if config.nightmode_on is not None:
        print(
            f"scheduling system {config.speaker_name} nightmode on at {config.nightmode_on}"
        )
        schedule.every().day.at(config.nightmode_on).do(
            set_nightmode, speaker=speaker, enabled=True
        )

    if config.nightmode_off is not None:
        print(
            f"scheduling system {config.speaker_name} nightmode off at {config.nightmode_off}"
        )
        schedule.every().day.at(config.nightmode_off).do(
            set_nightmode, speaker=speaker, enabled=False
        )

    if config.speech_enhance_on is not None:
        print(
            f"scheduling system {config.speaker_name} speech enhance on at {config.speech_enhance_on}"
        )
        schedule.every().day.at(config.speech_enhance_on).do(
            set_speech_enhance, speaker=speaker, enabled=True
        )

    if config.speech_enhance_off is not None:
        print(
            f"scheduling system {config.speaker_name} speech enhance off at {config.speech_enhance_off}"
        )
        schedule.every().day.at(config.nightmode_on).do(
            set_speech_enhance, speaker=speaker, enabled=False
        )
    print("scheduling set, waiting for next invocation...")


def main():
    dotenv.load_dotenv()
    config = config_from_env()
    speaker = find_speaker(config.speaker_name)
    set_schedule(config, speaker)

    while True:
        schedule.run_pending()
        time.sleep(15)


if __name__ == "__main__":
    main()
