"""Slack reader."""
import logging
import os
import re
import time
from datetime import datetime, timedelta
from ssl import SSLContext
from typing import Any, List, Optional

from llama_index.core.bridge.pydantic import PrivateAttr
from llama_index.core.readers.base import BasePydanticReader
from llama_index.core.schema import Document
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)


class SlackReader(BasePydanticReader):
    """Slack reader.

    Reads conversations from channels. If an earliest_date is provided, an
    optional latest_date can also be provided. If no latest_date is provided,
    we assume the latest date is the current timestamp.

    Args:
        slack_token (Optional[str]): Slack token. If not provided, we
            assume the environment variable `SLACK_BOT_TOKEN` is set.
        ssl (Optional[str]): Custom SSL context. If not provided, it is assumed
            there is already an SSL context available.
        earliest_date (Optional[datetime]): Earliest date from which
            to read conversations. If not provided, we read all messages.
        latest_date (Optional[datetime]): Latest date from which to
            read conversations. If not provided, defaults to current timestamp
            in combination with earliest_date.
    """

    is_remote: bool = True
    slack_token: str
    earliest_date_timestamp: Optional[float]
    latest_date_timestamp: float
    

    _client: Any = PrivateAttr()

    def __init__(
        self,
        slack_token: Optional[str] = None,
        ssl: Optional[SSLContext] = None,
        earliest_date: Optional[datetime] = None,
        latest_date: Optional[datetime] = None,
        earliest_date_timestamp: Optional[float] = None,
        latest_date_timestamp: Optional[float] = None,
    ) -> None:
        """Initialize with parameters."""

        three_days_ago = datetime.now() - timedelta(days=30)

        # Convert to UNIX timestamp
        earliest_date_timestamp = int(three_days_ago.timestamp())

        if slack_token is None:
            slack_token = os.environ["SLACK_BOT_TOKEN"]
        if slack_token is None:
            raise ValueError(
                "Must specify `slack_token` or set environment "
                "variable `SLACK_BOT_TOKEN`."
            )
        if ssl is None:
            self._client = WebClient(token=slack_token)
        else:
            self._client = WebClient(token=slack_token, ssl=ssl)
        if latest_date is not None and earliest_date is None:
            raise ValueError(
                "Must specify `earliest_date` if `latest_date` is specified."
            )
        if earliest_date is not None:
            earliest_date_timestamp = earliest_date.timestamp()
        else:
            earliest_date_timestamp = None or earliest_date_timestamp
        if latest_date is not None:
            latest_date_timestamp = latest_date.timestamp()
        else:
            latest_date_timestamp = datetime.now().timestamp() or latest_date_timestamp
        res = self._client.api_test()
        if not res["ok"]:
            raise ValueError(f"Error initializing Slack API: {res['error']}")

        super().__init__(
            slack_token=slack_token,
            earliest_date_timestamp=earliest_date_timestamp,
            latest_date_timestamp=latest_date_timestamp,
        )

    @classmethod
    def class_name(cls) -> str:
        return "SlackReader"

    def _read_message(self, channel_id: str,_user_id_name_mapping:dict, message_ts: str) -> str:

        """Read a message."""

        messages_text: List[str] = []
        next_cursor = None
        while True:
            try:
                # https://slack.com/api/conversations.replies
                # List all replies to a message, including the message itself.
                if self.earliest_date_timestamp is None:
                    result = self._client.conversations_replies(
                        channel=channel_id, ts=message_ts, cursor=next_cursor
                    )
                else:
                    conversations_replies_kwargs = {
                        "channel": channel_id,
                        "ts": message_ts,
                        "cursor": next_cursor,
                        "latest": str(self.latest_date_timestamp),
                    }
                    if self.earliest_date_timestamp is not None:
                        conversations_replies_kwargs["oldest"] = str(
                            self.earliest_date_timestamp
                        )
                    result = self._client.conversations_replies(
                        **conversations_replies_kwargs  # type: ignore
                    )

                
                messages = result["messages"]
                
                for message in messages:
                    curr_user_id = message["user"]
                    curr_user_name = str()
                    try:
                        if curr_user_id not in _user_id_name_mapping:
                        # Call the users.info method using the WebClient
                            result = self._client.users_info(
                            user = curr_user_id
                            )
                            logger.info(result)
                            # print(result["user"])
                            curr_user_name = result["user"].get("real_name","name")

                            _user_id_name_mapping[curr_user_id] = curr_user_name
                        
                        else:
                            curr_user_name = _user_id_name_mapping.get(curr_user_id)

                        final_message = curr_user_name + " : " + re.sub(r"<@[A-Z0-9]+>", ' ',message["text"])
                        # print(final_message)
                        messages_text.append(final_message)

                    except SlackApiError as e:
                        logger.error("Error fetching conversations: {}".format(e))
                
                # messages_text.extend(message["text"] for message in messages)
                # messages_text.extend(message["text"] for message in messages)
                if not result["has_more"]:
                    break

                next_cursor = result["response_metadata"]["next_cursor"]
            except SlackApiError as e:
                if e.response["error"] == "ratelimited":
                    logger.error(
                        "Rate limit error reached, sleeping for: {} seconds".format(
                            e.response.headers["retry-after"]
                        )
                    )
                    time.sleep(int(e.response.headers["retry-after"]))
                elif e.response["error"] == "thread_not_found":
                    logger.error(f"thread not found: {e}")
                    break;
                else:
                    logger.error(f"Error parsing conversation replies: {e}")
        # print(f"from read_message",messages_text)
        return "\n\n".join(messages_text)

    def _read_channel(self, channel_id: str,_user_id_name_mapping:dict, reverse_chronological: bool) -> str:
        from slack_sdk.errors import SlackApiError

        """Read a channel."""

        result_messages: List[str] = []
        next_cursor = None
        while True:
            try:
                # Call the conversations.history method using the WebClient
                # conversations.history returns the first 100 messages by default
                # These results are paginated,
                # see: https://api.slack.com/methods/conversations.history$pagination
                conversations_history_kwargs = {
                    "channel": channel_id,
                    "cursor": next_cursor,
                    "latest": str(self.latest_date_timestamp),
                }
                if self.earliest_date_timestamp is not None:
                    conversations_history_kwargs["oldest"] = str(
                        self.earliest_date_timestamp
                    )
                result = self._client.conversations_history(
                    **conversations_history_kwargs  # type: ignore
                )
                conversation_history = result["messages"]
                # print(f"{conversation_history=}")
                # Print results
                logger.info(
                    f"{len(conversation_history)} messages found in {channel_id}"
                )
                result_messages.extend(
                    self._read_message(channel_id,_user_id_name_mapping, message["ts"])
                    for message in conversation_history
                )
                if not result["has_more"]:
                    break
                next_cursor = result["response_metadata"]["next_cursor"]

            except SlackApiError as e:
                if e.response["error"] == "ratelimited":
                    logger.error(
                        "Rate limit error reached, sleeping for: {} seconds".format(
                            e.response.headers["retry-after"]
                        )
                    )
                    time.sleep(int(e.response.headers["retry-after"]))
                elif e.response["error"] == "not_in_channel":
                    logger.error(f"Your bot is not added in this channel: {e}")
                    break;
                else:
                    logger.error(f"Error parsing conversation replies: {e}")
        # print("from read channel ",(
        #     "\n\n".join(result_messages)
        #     if reverse_chronological
        #     else "\n\n".join(result_messages[::-1])
        # ))
        return (
            "\n\n".join(result_messages)
            if reverse_chronological
            else "\n\n".join(result_messages[::-1])
        )

    def load_data(
        self, channel_ids: List[str] = [], reverse_chronological: bool = True
    ) -> List[Document]:
        """Load data from the input directory.

        Args:
            channel_ids (List[str]): List of channel ids to read.

        Returns:
            List[Document]: List of documents.
        """
        results = []
        channel_ids = []
        channel_names = []

        channels_list_response = self._client.conversations_list()

        for res in channels_list_response['channels']:
            channel_ids.append(res['id'])
            channel_names.append(res['name'])

        # print(f"{channel_ids=}", f"{channel_names=}")
        _user_id_name_mapping = {}
        final_channel_content = {}
        for channel_id,channel_name in zip(channel_ids, channel_names):
            channel_content = self._read_channel(
                channel_id,_user_id_name_mapping, reverse_chronological=reverse_chronological
            )

            if channel_content:
                # print(f"{channel_content=}")
                final_channel_content = { "slack channels name" : channel_name, "channel conversation": channel_content }
                print(f"{channel_name=}")
                
                results.append(
                Document(
                id_= "slack",
                text=str(final_channel_content),
                        metadata={"slack channel name": channel_name,"source": "Slack"},
                    )
                )


        
        # print(f"{results=}")
        return results


if __name__ == "__main__":
    reader = SlackReader()
    logger.info(reader.load_data(channel_ids=["C04DC2VUY3F"]))
