from __future__ import annotations

import json

from plais import package_config_path


def logger_config() -> dict:
	"""Parse logging config."""

	config_file = f'{package_config_path}/logger.json'
	with open(config_file) as handler:
		log_config = json.load(handler)

	return log_config


def patch_config() -> list:
	"""Parse patch config."""
	...