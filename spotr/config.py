from .ami import get_by_tag
import os.path
from pathlib import Path
from typing import Any, Dict, Optional
from botocore.configloader import raw_config_parse
import argparse


class Config:
    def __init__(self, client: Any, args: argparse.Namespace, config_file_path: str = "~/.spotr/config") -> None:
        self.client = client
        config_path = Path(config_file_path).expanduser()
        if config_path.is_file():
            self._config: Dict[str, Any] = raw_config_parse(str(config_path))['config']
        else:
            self._config = {}
        self._config.update({k: v for k, v in vars(args).items() if v})

    def map_subnet_id(self, az: str) -> str:
        subnet_var = f"{az}_subnet_id"
        subnet_id = self._config[subnet_var]
        return subnet_id

    def set_subnet_id(self, subnet_id: str) -> None:
        self._config['subnet_id'] = subnet_id

    def set_az(self, az: str) -> None:
        self._config['az'] = az

    @property
    def ami_tag(self) -> str:
        return self._config.get('ami_tag', 'spotr')

    @property
    def instance_tag(self) -> str:
        return self._config.get('instance_tag', 'spotr')

    @property
    def type(self) -> str:
        return self._get_required('type')

    @property
    def max_bid(self) -> str:
        return self._get_required('max_bid')

    @property
    def ami(self) -> str:
        if 'ami' not in self._config:
            self._config['ami'] = get_by_tag(self.client, self.ami_tag)
        return self._config['ami']

    @property
    def key_name(self) -> str:
        return self._config.get('key_name', 'spotr')

    @property
    def az(self) -> str:
        if 'az' not in self._config:
            self._config['az'] = ''
        return self._config['az']

    @property
    def security_group_id(self) -> Optional[str]:
        return self._config.get('security_group_id')

    @property
    def subnet_id(self) -> Optional[str]:
        if 'subnet_id' not in self._config:
            self._config['subnet_id'] = ''
        return self._config.get('subnet_id')

    @property
    def ebs_optimized(self) -> bool:
        return bool(self._config['ebs_optimized'])

    @property
    def iam_instance_profile_arn(self) -> Optional[str]:
        return self._config.get('iam_instance_profile_arn')

    @property
    def user_data(self) -> Optional[str]:
        return self._config.get('user_data')

    @property
    def hosted_zone_id(self) -> Optional[str]:
        return self._config.get('hosted_zone_id')

    @property
    def record_name(self) -> Optional[str]:
        return self._config.get('record_name')

    def _get_required(self, key: str) -> str:
        if not self._config.get(key):
            raise RuntimeError(f"Missing required parameter: {key}")
        return self._config.get(key)
