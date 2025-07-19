import argparse
from typing import Any

from .client import build as build_client
from .config import Config
from .dns import build_client as dns_build_client
from .dns import set_record
from .instance import get_by_instance_id, open_port
from .instance import tag as tag_instance
from .key import find_or_create as find_or_create_key
from .pricing import get_az
from .spin_cursor import spin
from .spot_instance import request


def launch(args: argparse.Namespace) -> Any:
    client = build_client(args)
    conf = Config(client, args)

    key_path = find_or_create_key(client, conf.key_name)

    # if az is set in config, don't lookup zone
    if conf.az:
        az = conf.az
    else:
        az = get_az(client, conf)
        conf.set_az(az.zone_name)

    # map the subnet_id from the config vars
    conf.set_subnet_id(conf.map_subnet_id(conf.az))

    with spin(f"Launching: {az}"):
        inst = request(client, conf, tag_instance, get_by_instance_id, open_port)

    _log_instance_creation(inst, key_path)

    if conf.hosted_zone_id and conf.record_name:
        set_record(dns_build_client(args), inst, conf)

    return inst


def _log_instance_creation(instance: Any, key_path: str) -> None:
    print(f">> Instance {instance.id} launched, connect with:")
    ip = str(instance.ip_address)
    print(f"ssh -i {key_path} ubuntu@{ip}")
