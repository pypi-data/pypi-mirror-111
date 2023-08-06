"""
Runs tests via pytest. Invoke using `python -m potluck.tests`.

tests/__main__.py
"""

import pytest

pytest.main(["--pyargs", "potluck.tests"])
