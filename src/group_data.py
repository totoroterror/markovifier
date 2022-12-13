import markovify
from loguru import logger

from config import config


class GroupData:
    def __init__(self, chat_id: int, existing_data: list[str] | None = None) -> None:
        self.chat_id = chat_id
        self.model = None
        if type(existing_data) is list and len(existing_data) > 0:
            self.model = markovify.combine(
                [markovify.Text(x, well_formed=False) for x in existing_data]
            )

    def generate(self) -> str | None:
        if self.model is None:
            return None

        message: str = self.model.make_sentence( # type: ignore
            tries=25000,
            max_overlap_total=config.MAX_OVERLAP_TOTAL, max_overlap_ratio=config.MAX_OVERLAP_RATIO
        )

        logger.debug('Generated message: {message}', message=message)

        return message

    def add_message(self, message: str) -> None:
        new_model = markovify.Text(message, well_formed=False)

        if self.model is None:
            self.model = new_model
        else:
            self.model = markovify.combine([self.model, new_model])
