import argparse
from typing import Any

from .client import build as build_client
from .config import Config
from .instance import destroy as destroy_instance
from .instance import find_latest as find_latest_instance
from .spin_cursor import spin


def destroy(args: argparse.Namespace) -> Any:
    client = build_client(args)
    conf = Config(client, args)
    instance = find_latest_instance(client, conf)

    with spin(">> Destroying instance."):
        destroyed = destroy_instance(client, instance.id)

    _log_instance_destroyed(instance)

    return destroyed


def _log_instance_destroyed(instance: Any) -> None:
    print(f">> Instance {instance.id} destroyed")
