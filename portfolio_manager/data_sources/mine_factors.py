import json
import math
import re
from pathlib import Path

import orjson
from data_sources.research.extract_pdf import process_files
from utils.chatgpt import (
    chunk_string,
    num_tokens_from_messages,
    num_tokens_from_string,
    prompt_chatgpt_stream,
)
from utils.dynaconf_utils import settings


def extract_json_from_string(string):
    pattern = r"{\s*\"[^{}]+\":\s*(?:\{(?:[^{}]+|(?R))*\}|\[(?:[^[\]]+|(?R))*\]|\"[^\"]*\"|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*}"
    matches = re.findall(pattern, string)
    json_objects = []

    for match in matches:
        try:
            json_objects.append(orjson.loads(match))
        except Exception as e:
            print(e)
            continue

    return json_objects


def prepare_messages_python_computation(text: str) -> dict:
    return [
        {
            "role": "system",
            "content": "You are a financial analysis assistant answering in English.",
        },
        {
            "role": "user",
            "content": f"""Extract {settings.MINING_FACTOR_LIMIT_FOR_DEMO if settings.MINING_FACTOR_LIMIT_FOR_DEMO else 'all the'} financial factors from the research paper and implement the computation in Python. The research paper content is the following:```\n{text}\n```""",
        },
    ]


def prepare_messages_json_format(text: str) -> dict:
    return [
        {
            "role": "system",
            "content": "You are a financial analysis asistant answering in English with NO elaboration or detailed explanation but ONLY JSON.",
        },
        {
            "role": "user",
            "content": f"""For the Python implementation of each factor provided in the following text, include the imports and rewrite factor as function `signal(df: pd.DataFrame, window: int, factor_name: str, **kwargs) -> float`, and serialize them into a strict JSON format like {{"<factor-name-1>": "<python-code-1>","<factor-name-2>": "<python-code-2>"...}}.\nThe text is:\n```\n{text}\n```""",
        },
    ]


def mine_factors_from_files():
    chatgpt_model = settings.CHATGPT_MODEL
    token_limit = settings.CHATGPT_TOKEN_LIMIT

    files_dir = Path(settings.ROOT_PATH_FOR_DYNACONF) / settings.RESEARCH_PAPERS_DIR
    file_contents = process_files(files_dir.glob("*.pdf"))

    factors = {}
    for text in file_contents:
        messages = prepare_messages_python_computation(text)
        num_token = num_tokens_from_messages(messages)
        message_overhead = num_token - num_tokens_from_string(text)
        print(f"{message_overhead=}")
        print(f"Input has {num_token} tokens.")
        if num_token > token_limit:
            batch = math.ceil(num_token / (token_limit - message_overhead))
            print(f"Chunking into {batch} batches.")
            num_factors = 0
            for sub_text in chunk_string(text, batch):
                try:
                    messages = prepare_messages_python_computation(sub_text)
                    print(
                        f"Chunked message tokens: {num_tokens_from_messages(messages)}"
                    )
                    result = prompt_chatgpt_stream(
                        messages,
                        model=chatgpt_model,
                        # temperature=0.75,
                    )
                    print(f"Returned message:\n{result['content']}")
                    result = prompt_chatgpt_stream(
                        prepare_messages_json_format(result["content"]),
                        model=chatgpt_model,
                        # temperature=0.75,
                    )
                    print(f"Returned message:\n{result['content']}")
                    # TODO: Refine the parsing of the returned results, as JSON format is not always guaranteed.
                    try:
                        decoded = orjson.loads(result["content"])
                        # decoded = extract_json_from_string(result["content"])
                    except ValueError:
                        decoded = eval(result["content"])
                    factors.update(decoded)
                    num_factors += 1
                except Exception as e:
                    print(e)
                    continue

                if (
                    settings.MINING_FACTOR_LIMIT_FOR_DEMO
                    and num_factors > settings.MINING_FACTOR_LIMIT_FOR_DEMO
                ):
                    break
            continue

        try:
            result = prompt_chatgpt_stream(
                messages,
                model=chatgpt_model,
                temperature=0.75,
            )
            print(f"Returned message:\n{result['content']}")
            result = prompt_chatgpt_stream(
                prepare_messages_json_format(result["content"]),
                model=chatgpt_model,
                # temperature=0.75,
            )
            print(f"Returned message:\n{result['content']}")
            # TODO: Refine the parsing of the returned results, as JSON format is not always guaranteed.
            try:
                decoded = orjson.loads(result["content"])
            except ValueError:
                decoded = eval(result["content"])
            factors.update(decoded)
            num_factors += 1
        except Exception as e:
            print(e)

    for factor_name, factor_python in factors.items():
        with open(
            Path(settings.ROOT_PATH_FOR_DYNACONF)
            / settings.FACTORS_DIR
            / f"{factor_name}.py",
            "w",
        ) as py_file:
            print(f"Writing to {f'{factor_name}.py'}")
            print(factor_python, file=py_file)
