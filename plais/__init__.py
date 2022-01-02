import os
from pathlib import Path

# package directories
package_path = Path(os.path.dirname(__file__)).parent
package_data_path = package_path / 'data'

# package imports
from .main import Plais
