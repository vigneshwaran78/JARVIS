import unittest
from app import app


class AppApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JARVIS", response.data)

    def test_status_endpoint(self):
        response = self.client.get("/api/status")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "online")
        self.assertIn("model", data)
        self.assertIn("memory_count", data)

    def test_memory_endpoint_and_clear(self):
        # Fetch memory
        response = self.client.get("/api/memory")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("history", data)
        self.assertIn("count", data)

        # Clear memory
        clear_resp = self.client.post("/api/memory/clear")
        self.assertEqual(clear_resp.status_code, 200)
        clear_data = clear_resp.get_json()
        self.assertTrue(clear_data["success"])

        # Fetch memory again, should be empty
        response = self.client.get("/api/memory")
        data = response.get_json()
        self.assertEqual(data["count"], 0)


if __name__ == "__main__":
    unittest.main()
