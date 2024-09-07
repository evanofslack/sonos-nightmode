import os
import sys
import time
from dataclasses import dataclass
from typing import Optional

import dotenv
import schedule
import soco
from loguru import logger


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
        logger.error(f"could not find env var: SONOS_NAME")
        sys.exit(1)

    nightmode_on_var = "NIGHTMODE_ON"
    nightmode_on = os.getenv(nightmode_on_var)

    nightmode_off_var = "NIGHTMODE_OFF"
    nightmode_off = os.getenv(nightmode_off_var)

    speech_on_var = "SPEECH_ENHANCE_ON"
    speech_enhance_on = os.getenv(speech_on_var)

    speech_off_var = "SPEECH_ENHANCE_OFF"
    speech_enhance_off = os.getenv(speech_off_var)

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
        logger.error(f"could not find speaker: {speaker_name}")
        sys.exit(1)
    logger.info(f"successfully found speaker: {speaker_name}")
    logger.info(f"currently nightmode is: {speaker.night_mode}")
    logger.info(f"currently speech enhancement is: {speaker.dialog_mode}")
    return speaker


def set_nightmode(speaker: soco.SoCo, enabled: bool):
    speaker.night_mode = enabled
    if enabled:
        logger.info(f"nightmode enabled")
    else:
        logger.info(f"nightmode disabled")


def set_speech_enhance(speaker: soco.SoCo, enabled: bool):
    speaker.night_mode = enabled
    if enabled:
        logger.info(f"speech enhancement enabled")
    else:
        logger.info(f"speech enhancement disabled")


def set_schedule(config: Config, speaker: soco.SoCo):
    if config.nightmode_on is not None:
        logger.info(f"scheduling nightmode on at {config.nightmode_on}")
        schedule.every().day.at(config.nightmode_on).do(
            set_nightmode, speaker=speaker, enabled=True
        )

    if config.nightmode_off is not None:
        logger.info(f"scheduling nightmode off at {config.nightmode_off}")
        schedule.every().day.at(config.nightmode_off).do(
            set_nightmode, speaker=speaker, enabled=False
        )

    if config.speech_enhance_on is not None:
        logger.info(f"scheduling speech enhancement on at {config.speech_enhance_on}")
        schedule.every().day.at(config.speech_enhance_on).do(
            set_speech_enhance, speaker=speaker, enabled=True
        )

    if config.speech_enhance_off is not None:
        logger.info(f"scheduling speech enhancement off at {config.speech_enhance_off}")
        schedule.every().day.at(config.speech_enhance_off).do(
            set_speech_enhance, speaker=speaker, enabled=False
        )
    logger.info("scheduling complete, waiting for next invocation...")


def main():
    logger.remove()
    logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
    dotenv.load_dotenv()
    config = config_from_env()
    speaker = find_speaker(config.speaker_name)
    set_schedule(config, speaker)

    while True:
        schedule.run_pending()
        time.sleep(15)


if __name__ == "__main__":
    main()
