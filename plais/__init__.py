import os
from pathlib import Path

package_path = Path(os.path.dirname(__file__)).parent
package_config_path = package_path / 'config'
package_output_path = 'PLAIS_RESULTS'