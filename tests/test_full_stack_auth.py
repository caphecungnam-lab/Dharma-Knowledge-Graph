from __future__ import annotations

import os
import unittest
from pathlib import Path

from dkg_api.app.auth.auth_service import AuthError, AuthService


ROOT = Path(__file__).resolve().parents[1]


class FullStackAuthTest(unittest.TestCase):
    def setUp(self):
        self.previous_user = os.environ.get("DKG_ADMIN_USER")
        self.previous_password = os.environ.get("DKG_ADMIN_PASSWORD")
        self.previous_secret = os.environ.get("DKG_JWT_SECRET")
        os.environ["DKG_ADMIN_USER"] = "tester"
        os.environ["DKG_ADMIN_PASSWORD"] = "secret"
        os.environ["DKG_JWT_SECRET"] = "test-secret"

    def tearDown(self):
        self._restore("DKG_ADMIN_USER", self.previous_user)
        self._restore("DKG_ADMIN_PASSWORD", self.previous_password)
        self._restore("DKG_JWT_SECRET", self.previous_secret)

    def test_login_generates_valid_jwt(self):
        auth = AuthService()

        response = auth.login("tester", "secret")
        payload = auth.validate_token(response["access_token"])

        self.assertEqual(response["user"]["role"], "admin")
        self.assertEqual(payload["sub"], "tester")
        self.assertEqual(payload["role"], "admin")

    def test_login_rejects_invalid_credentials(self):
        with self.assertRaises(AuthError):
            AuthService().login("tester", "bad-password")

    def test_backend_registers_auth_and_node_routes(self):
        main_source = (ROOT / "dkg_api/app/main.py").read_text()
        auth_source = (ROOT / "dkg_api/app/api/auth.py").read_text()
        node_source = (ROOT / "dkg_api/app/api/node.py").read_text()

        self.assertIn("JWTAuthMiddleware", main_source)
        self.assertIn("auth_router", main_source)
        self.assertIn("node_router", main_source)
        self.assertIn('@router.post("/login")', auth_source)
        self.assertIn('@router.get("/{node_id}")', node_source)

    def test_ai_orchestrator_returns_graph_contract(self):
        source = (ROOT / "dkg_api/app/services/orchestrator.py").read_text()

        self.assertIn('"nodes"', source)
        self.assertIn('"edges"', source)
        self.assertIn('"center_node"', source)
        self.assertIn('"epistemic_layers"', source)
        self.assertIn('"confidence_map"', source)

    def test_frontend_uses_jwt_and_no_mock_graph(self):
        frontend_root = ROOT / "dkg-mvp-frontend"
        api_source = (frontend_root / "lib/dkgApi.ts").read_text()
        query_source = (frontend_root / "components/QueryBar.tsx").read_text()

        self.assertIn("/auth/login", api_source)
        self.assertIn("Authorization", api_source)
        self.assertIn("/ai/ask", api_source)
        self.assertIn("/node/", api_source)
        self.assertNotIn("mockGraph", api_source + query_source)
        self.assertFalse((frontend_root / "data/mockGraph.json").exists())
        self.assertFalse((frontend_root / "lib/mockApi.ts").exists())

    def _restore(self, name: str, value: str | None) -> None:
        if value is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = value


if __name__ == "__main__":
    unittest.main()
