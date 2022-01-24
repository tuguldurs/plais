from __future__ import annotations

import json

from . import package_config_path


def parse_config(config_name) -> dict:
	"""Parse logging or patch config."""

	config_file = f'{package_config_path}/{config_name}.json'

	with open(config_file) as handler:
		configuration = json.load(handler)

	return configuration
