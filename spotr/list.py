import argparse

from .client import build as build_client
from .config import Config
from .instance import find_instances
from .spin_cursor import spin


def list_instances(args: argparse.Namespace) -> None:
    client = build_client(args)
    conf = Config(client, args)
    with spin("Searching for instances..."):
        instances = find_instances(client, conf)
    print(f'\nFound {len(instances)} instances')
    if instances:
        for instance in instances:
            print(f'Instance ID: {instance.id}')
            print(f'IP Address: {instance.ip_address}')
            print(f'Launch Time: {instance.launch_time}')
            print(f'Security Groups: {instance.security_groups}')
    if not instances:
        print('No instances found')
