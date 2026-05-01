import os
import sys
import time
from dataclasses import dataclass
from typing import Optional

import dotenv
import schedule
import soco
from requests import RequestException
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
        logger.error(f"could not find speaker '{speaker_name}'")
        sys.exit(1)
    logger.info(f"successfully found speaker '{speaker_name}'")

    if speaker.night_mode:
        logger.info(f"currently nightmode is enabled")
    else:
        logger.info(f"currently nightmode is disabled")

    if speaker.dialog_mode:
        logger.info(f"currently speech enhancement is enabled")
    else:
        logger.info(f"currently speech enhancement is disabled")
    return speaker


def _set_nightmode(speaker: soco.SoCo, enabled: bool):
    if speaker.night_mode == enabled:
        logger.info(f"nightmode already {'enabled' if enabled else 'disabled'}, skipping")
        return
    speaker.night_mode = enabled
    logger.info(f"nightmode {'enabled' if enabled else 'disabled'}")


def _set_speech_enhance(speaker: soco.SoCo, enabled: bool):
    if speaker.dialog_mode == enabled:
        logger.info(
            f"speech enhancement already {'enabled' if enabled else 'disabled'}, skipping"
        )
        return
    speaker.dialog_mode = enabled
    logger.info(f"speech enhancement {'enabled' if enabled else 'disabled'}")


def run_with_retry(
    speaker_name: str, speaker: soco.SoCo, action: str, enabled: bool, retries: int = 2
) -> soco.SoCo:
    current_speaker = speaker
    for attempt in range(1, retries + 2):
        try:
            if action == "nightmode":
                _set_nightmode(current_speaker, enabled)
            elif action == "speech_enhance":
                _set_speech_enhance(current_speaker, enabled)
            else:
                logger.error(f"unknown action: {action}")
            return current_speaker
        except (RequestException, OSError, soco.exceptions.SoCoException) as err:
            logger.error(
                f"{action} update failed (attempt {attempt}/{retries + 1}): {err}"
            )
            if attempt > retries:
                break
            time.sleep(2)
            current_speaker = find_speaker(speaker_name)
    return current_speaker


def make_job(speaker_name: str, speaker_holder: dict, action: str, enabled: bool):
    def _job():
        speaker_holder["speaker"] = run_with_retry(
            speaker_name=speaker_name,
            speaker=speaker_holder["speaker"],
            action=action,
            enabled=enabled,
        )

    return _job


def set_schedule(config: Config, speaker: soco.SoCo):
    speaker_holder = {"speaker": speaker}

    if config.nightmode_on is not None:
        logger.info(f"scheduling nightmode enabled at {config.nightmode_on}")
        schedule.every().day.at(config.nightmode_on).do(
            make_job(config.speaker_name, speaker_holder, "nightmode", True)
        )

    if config.nightmode_off is not None:
        logger.info(f"scheduling nightmode disabled at {config.nightmode_off}")
        schedule.every().day.at(config.nightmode_off).do(
            make_job(config.speaker_name, speaker_holder, "nightmode", False)
        )

    if config.speech_enhance_on is not None:
        logger.info(f"scheduling speech enhancement enabled at {config.speech_enhance_on}")
        schedule.every().day.at(config.speech_enhance_on).do(
            make_job(config.speaker_name, speaker_holder, "speech_enhance", True)
        )

    if config.speech_enhance_off is not None:
        logger.info(f"scheduling speech enhancement disabled at {config.speech_enhance_off}")
        schedule.every().day.at(config.speech_enhance_off).do(
            make_job(config.speaker_name, speaker_holder, "speech_enhance", False)
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
