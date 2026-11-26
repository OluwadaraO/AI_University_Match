import logging
import time

from app.ai.client import client, MODEL


logger = logging.getLogger(__name__)

MAX_ATTEMPTS = 3
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def generate_text(prompt: str) -> str:

    for attempt in range(MAX_ATTEMPTS):
        try:
            response = client.interactions.create(
                model=MODEL,
                input=prompt,
            )

            if not response.output_text:
                raise ValueError(
                    "Gemini returned an empty response."
                )

            return response.output_text

        except Exception as error:
            status_code = getattr(error, "code", None)

            if status_code is None:
                status_code = getattr(
                    error, "status_code", None
                )

            retryable = (
                str(status_code)
                in {
                    str(code)
                    for code in RETRYABLE_STATUS_CODES
                }
            )

            if not retryable or attempt == MAX_ATTEMPTS - 1:
                raise

            delay = 2 ** (attempt + 1)

            logger.warning(
                "Gemini request failed. "
                "Retrying in %s seconds (%s/%s).",
                delay,
                attempt + 1,
                MAX_ATTEMPTS - 1,
            )

            time.sleep(delay)

    raise RuntimeError("Gemini generation failed.")