import unittest

from ai_weather_forecasting_agent.agent import WeatherAgent


class TestWeatherAgent(unittest.TestCase):
    def test_forecast_returns_dict(self):
        agent = WeatherAgent()
        out = agent.forecast("Testville")
        self.assertIsInstance(out, dict)
        self.assertEqual(out.get("location"), "Testville")
        self.assertIn("forecast", out)


if __name__ == "__main__":
    unittest.main()
