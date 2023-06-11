from typing import List, Generator

import openai
import tiktoken

from .dynaconf_utils import settings

openai.api_key = settings.CHATGPT_API_KEY


def prompt_chatgpt_stream(prompt: List[dict], model="gpt-3.5-turbo") -> dict:
    """
    Generates a chat-based response from the OpenAI GPT-3.5 Turbo model.

    Args:
        prompt (List[dict]): A list of message dictionaries representing the conversation.
        model (str, optional): The model name to use. Defaults to "gpt-3.5-turbo".

    Returns:
        dict: A dictionary containing the role and content of the generated response.
    """
    responses = list(
        openai.ChatCompletion.create(model=model, messages=prompt, stream=True)
    )

    return {
        "role": responses[0]["choices"][0]["delta"].get("role", "assistant"),
        "content": "".join(
            chunk["choices"][0]["delta"].get("content", "") for chunk in responses
        ),
    }


def num_tokens_from_messages(messages, model="gpt-3.5-turbo") -> int:
    """
    Returns the number of tokens used by a list of messages.

    Args:
        messages: The list of messages in the conversation.
        model (str, optional): The model name. Defaults to "gpt-3.5-turbo".

    Returns:
        int: The number of tokens used by the messages.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += (
                4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            )
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not presently implemented for model {model}.
    See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
