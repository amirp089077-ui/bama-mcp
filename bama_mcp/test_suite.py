"""
Automated Unit and Integration Test Suite for Bama MCP Server
"""

import sys
import unittest

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from bama_mcp.client import BamaClient
from bama_mcp.tools import TOOLS, execute_tool


class TestBamaMCP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = BamaClient()
        # Find a real live car ad code
        res = cls.client.search_cars(limit=3)
        ads = res.get("ads", [])
        cls.test_code = ads[0]["code"] if ads else "pdli97lw"
        cls.test_code_2 = ads[1]["code"] if len(ads) > 1 else "xfgntw97"

    def test_01_tool_registration(self):
        self.assertGreaterEqual(len(TOOLS), 14)
        tool_names = [t["name"] for t in TOOLS]
        self.assertIn("bama_search_cars", tool_names)
        self.assertIn("bama_get_car_details", tool_names)
        self.assertIn("bama_search_motorcycles", tool_names)
        self.assertIn("bama_search_trucks", tool_names)
        self.assertIn("bama_list_brands", tool_names)
        self.assertIn("bama_trending_searches", tool_names)
        self.assertIn("bama_appraise_car", tool_names)
        self.assertIn("bama_compare_cars", tool_names)
        self.assertIn("bama_get_contact", tool_names)
        self.assertIn("bama_status", tool_names)

    def test_02_search_cars(self):
        res = execute_tool("bama_search_cars", {"brand": "peugeot", "limit": 5})
        self.assertIsInstance(res, dict)
        ads = res.get("ads", [])
        self.assertGreater(len(ads), 0)
        first = ads[0]
        self.assertTrue(first.get("code"))
        self.assertTrue(first.get("title"))

    def test_03_get_car_details(self):
        res = execute_tool("bama_get_car_details", {"ad_code": self.test_code})
        self.assertIsInstance(res, dict)
        self.assertEqual(res.get("code"), self.test_code)
        self.assertTrue(res.get("title"))
        self.assertIn("price_irr_formatted", res)

    def test_04_search_motorcycles(self):
        res = execute_tool("bama_search_motorcycles", {"limit": 5})
        self.assertIsInstance(res, dict)
        ads = res.get("ads", [])
        self.assertGreater(len(ads), 0)

    def test_05_search_trucks(self):
        res = execute_tool("bama_search_trucks", {"limit": 5})
        self.assertIsInstance(res, dict)
        ads = res.get("ads", [])
        self.assertGreater(len(ads), 0)

    def test_06_list_brands(self):
        res = execute_tool("bama_list_brands", {})
        self.assertIsInstance(res, list)
        self.assertGreater(len(res), 10)
        self.assertTrue(any(b["brand_slug"] == "peugeot" for b in res))

    def test_07_trending_searches(self):
        res = execute_tool("bama_trending_searches", {})
        self.assertIsInstance(res, dict)
        self.assertIn("trending_cars", res)
        self.assertGreater(len(res["trending_cars"]), 0)

    def test_08_appraise_car(self):
        res = execute_tool("bama_appraise_car", {"ad_code": self.test_code})
        self.assertIsInstance(res, dict)
        self.assertIn("total_score", res)
        self.assertGreater(res["total_score"], 0)
        self.assertIn("deal_rating", res)

    def test_09_compare_cars(self):
        res = execute_tool("bama_compare_cars", {
            "ad_code_1": self.test_code,
            "ad_code_2": self.test_code_2,
        })
        self.assertIsInstance(res, dict)
        self.assertIn("recommended_choice", res)

    def test_10_get_contact(self):
        res = execute_tool("bama_get_contact", {"ad_code": self.test_code})
        self.assertIsInstance(res, dict)
        self.assertEqual(res.get("code"), self.test_code)
        self.assertIn("phone", res)

    def test_11_auth_status(self):
        res = execute_tool("bama_auth_status", {})
        self.assertIsInstance(res, dict)
        self.assertIn("authenticated", res)

    def test_12_status_and_help(self):
        st = execute_tool("bama_status", {})
        self.assertEqual(st.get("status"), "online")
        hp = execute_tool("bama_help", {})
        self.assertGreaterEqual(hp.get("tools_count", 0), 14)


if __name__ == "__main__":
    unittest.main()
