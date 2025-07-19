import os
from pathlib import Path
from typing import Any


def find_or_create(client: Any, conf_key_name: str) -> str:
    path = Path(f"~/.ssh/{conf_key_name}.pem").expanduser()
    if not path.exists():
        response = client.create_key_pair(KeyName=conf_key_name)

        with os.fdopen(os.open(str(path), os.O_WRONLY | os.O_CREAT, 0o400), "w") as handle:
            handle.write(response["KeyMaterial"])

    return str(path)
