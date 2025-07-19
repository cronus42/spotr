import time
import argparse
from typing import Any, Dict

from .client import build as build_client
from .config import Config
from .instance import find_latest as find_latest_instance
from .instance import tag
from .spin_cursor import spin


def snapshot(args: argparse.Namespace) -> 'Snapshot':
    client = build_client(args)
    conf = Config(client, args)
    instance = find_latest_instance(client, conf)

    with spin(f">> Creating snapshot for instance: {instance.ip_address}"):
        snap = create_and_wait(client, instance, conf)

    return snap


def create_and_wait(client: Any, instance: Any, conf: Config) -> 'Snapshot':
    image = create(client, instance)
    tag(client, image.id, conf)
    wait_for_completion(client, image)
    return image


def create(client: Any, instance: Any) -> 'Snapshot':
    now = time.strftime("%Y-%m-%d %H-%M")
    response = client.create_image(
        Name=f"Spotr image {now}",
        Description="Spotr image",
        InstanceId=instance.id)
    return Snapshot(response)


def wait_for_completion(client: Any, image: 'Snapshot') -> None:
    waiter = client.get_waiter('image_available')
    waiter.wait(
        Filters=[
            {
                'Name': 'image-id',
                'Values': [image.id]
            },
        ]
    )


class Snapshot:
    def __init__(self, response: Dict[str, Any]) -> None:
        self.id = response['ImageId']
