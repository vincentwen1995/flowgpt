from pathlib import Path
from dynaconf import Dynaconf
from dynaconf.vendor.dotenv import load_dotenv

for filename in (Path(__file__).parent.parent.parent / "secrets").glob("*.env"):
    load_dotenv(str(filename.absolute()))

settings = Dynaconf(
    settings_files=["config.yaml"],
    root_path=Path(__file__).parent.parent,
    envvar_prefix=False,
)
