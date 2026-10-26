from django.test import TestCase, Client

# Create your tests here.

class HealthTest(TestCase):
    def test_health_returns_ok(self):
        response = Client().get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

