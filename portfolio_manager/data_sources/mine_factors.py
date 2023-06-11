import orjson
import math
from pathlib import Path

from data_sources.research.extract_pdf import process_files
from utils.chatgpt import num_tokens_from_messages, prompt_chatgpt_stream, chunk_string
from utils.dynaconf_utils import settings


def prepare_messages(text: str) -> dict:
    return [
        {"role": "system", "content": "You are a financial analysis assistant."},
        {
            "role": "user",
            "content": f'Extract {settings.MINING_FACTOR_LIMIT_FOR_DEMO} financial factors from the research paper and provide pure Python implementation including imports STRICTLY in JSON format {{"<factor_name>": "<code-block>"}}) for each factors with the function signature `factor_name(df: pd.DataFrame) -> float` where the new factor is computed based on the input dataframe. Translate the code to English characters. The research paper content is the following:```\n{text}```',
        },
    ]


def mine_factors_from_files():
    chatgpt_model = settings.CHATGPT_MODEL
    token_limit = settings.CHATGPT_TOKEN_LIMIT

    files_dir = Path(settings.ROOT_PATH_FOR_DYNACONF) / settings.RESEARCH_PAPERS_DIR
    file_contents = process_files(files_dir.glob("*.pdf"))

    factors = {}
    for text in file_contents:
        messages = prepare_messages(text)
        num_token = num_tokens_from_messages(messages)
        print(f"Paper has {num_token} tokens.")
        if num_token > token_limit:
            batch = num_token // token_limit
            print(f"Chunking into {batch} batches.")
            num_factors = 0
            for sub_text in chunk_string(text, batch):
                try:
                    result = prompt_chatgpt_stream(
                        prepare_messages(sub_text),
                        model=chatgpt_model,
                        temperature=0.75,
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
                    continue

                if (
                    settings.MINING_FACTOR_LIMIT_FOR_DEMO
                    and num_factors > settings.MINING_FACTOR_LIMIT_FOR_DEMO
                ):
                    break

    for factor_name, factor_python in factors.items():
        with open(
            Path(settings.ROOT_PATH_FOR_DYNACONF)
            / settings.FACTORS_DIR
            / f"{factor_name}.py",
            "w",
        ) as py_file:
            print(f"Writing to {f'{factor_name}.py'}")
            print(factor_python, file=py_file)
