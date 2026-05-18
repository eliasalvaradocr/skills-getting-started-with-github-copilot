import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

import app as app_module  # noqa: E402


@pytest.fixture
def client():
    original_activities = copy.deepcopy(app_module.activities)

    with TestClient(app_module.app) as client:
        yield client

    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original_activities))
