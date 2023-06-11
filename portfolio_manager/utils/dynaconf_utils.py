from pathlib import Path
from dynaconf import Dynaconf

settings = Dynaconf(settings_files=["config.yaml"], root_path=Path(__file__).parent.parent, envvar_prefix=False)