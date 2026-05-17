import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from facade import ConverterFacade

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")


@pytest.fixture(scope="session")
def facade():
    return ConverterFacade()


@pytest.fixture(scope="session", autouse=True)
def require_test_files():
    from tests._test_vectors import TEST_VECTORS

    missing = [
        v.filename
        for v in TEST_VECTORS
        if not os.path.exists(os.path.join(TEST_FILES_DIR, v.filename))
    ]
    if missing:
        pytest.skip(
            f"Test files missing: {missing}. Run `python tests/create_test_files.py` first."
        )
