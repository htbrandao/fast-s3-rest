from fastapi.testclient import TestClient

from fast_s3_rest import app

test_cli = TestClient(app)
