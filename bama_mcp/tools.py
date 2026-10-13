"""
Bama MCP Tool Definitions and Handlers
Exposes 15 specialized automotive tools for Bama (باما).
"""

import json
import logging
from typing import Any, Dict, List

from .analytics import appraise_car, compare_cars
from .client import BamaClient

logger = logging.getLogger("bama_mcp.tools")

client = BamaClient()

TOOLS: List[Dict[str, Any]] = [
    {
        "name": "bama_search_cars",
        "description": "جستجوی آگهی‌های خودرو در باما با فیلتر برند، مدل، استان، قیمت و کارکرد",
        "inputSchema": {
            "type": "object",
            "properties": {
                "brand": {"type": "string", "description": "برند خودرو (مثلاً 'peugeot', 'toyota', 'pride', 'tara')"},
                "model": {"type": "string", "description": "مدل خودرو (مثلاً '207', 'corolla', '206')"},
                "province": {"type": "string", "description": "استان مورد نظر (مثلاً 'تهران', 'اصفهان')"},
                "price_min": {"type": "integer", "description": "حداقل قیمت به تومان"},
                "price_max": {"type": "integer", "description": "حداکثر قیمت به تومان"},
                "page": {"type": "integer", "description": "شماره صفحه (پیش‌فرض: 0)", "default": 0},
                "limit": {"type": "integer", "description": "حداکثر تعداد نتایج (پیش‌فرض: 20)", "default": 20},
            },
        },
    },
    {
        "name": "bama_get_car_details",
        "description": "دریافت جزئیات کامل و مشخصات فنی یک آگهی خودرو در باما با کد آگهی",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ad_code": {"type": "string", "description": "کد یکتای آگهی باما (مثلاً 'pdli97lw', 'xfgntw97')"},
            },
            "required": ["ad_code"],
        },
    },
    {
        "name": "bama_search_motorcycles",
        "description": "جستجوی آگهی‌های موتورسیکلت در باما (هوندا، بنلی، وسپا، یاماها و...)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "page": {"type": "integer", "description": "شماره صفحه (پیش‌فرض: 0)", "default": 0},
                "limit": {"type": "integer", "description": "حداکثر نتایج (پیش‌فرض: 20)", "default": 20},
            },
        },
    },
    {
        "name": "bama_search_trucks",
        "description": "جستجوی آگهی‌های خودروهای سنگین، کامیون و تجاری در باما",
        "inputSchema": {
            "type": "object",
            "properties": {
                "page": {"type": "integer", "description": "شماره صفحه (پیش‌فرض: 0)", "default": 0},
                "limit": {"type": "integer", "description": "حداکثر نتایج (پیش‌فرض: 20)", "default": 20},
            },
        },
    },
    {
        "name": "bama_list_brands",
        "description": "فهرست کامل برندها و مدل‌های خودرو موجود در بازار باما (پژو، تویوتا، کیا، هیوندای و...)",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "bama_trending_searches",
        "description": "مشاهده پرطرفدارترین و داغ‌ترین جستجوهای روز خودرو و موتور در باما",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "bama_appraise_car",
        "description": "ارزیابی و تحلیل هوشمند سلامت بدنه، کارکرد، قیمت و ارزش معامله خودرو در باما",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ad_code": {"type": "string", "description": "کد آگهی مورد نظر جهت ارزیابی"},
            },
            "required": ["ad_code"],
        },
    },
    {
        "name": "bama_compare_cars",
        "description": "مقایسه رودرروی دو خودرو در باما از نظر قیمت، کارکرد، مشخصات فنی و سلامت",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ad_code_1": {"type": "string", "description": "کد آگهی اول"},
                "ad_code_2": {"type": "string", "description": "کد آگهی دوم"},
            },
            "required": ["ad_code_1", "ad_code_2"],
        },
    },
    {
        "name": "bama_get_contact",
        "description": "دریافت اطلاعات تماس، مشخصات فروشنده (شخصی یا نمایشگاه) و آدرس در باما",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ad_code": {"type": "string", "description": "کد آگهی"},
            },
            "required": ["ad_code"],
        },
    },
    {
        "name": "bama_auth_status",
        "description": "بررسی وضعیت ورود و اعتبار توکن حساب کاربری باما",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "bama_auth_set_token",
        "description": "تنظیم و ذخیره توکن Bearer کاربر باما برای دسترسی به آگهی‌های من و پارکینگ",
        "inputSchema": {
            "type": "object",
            "properties": {
                "token": {"type": "string", "description": "توکن احراز هویت (Bearer Token)"},
            },
            "required": ["token"],
        },
    },
    {
        "name": "bama_get_my_ads",
        "description": "مشاهده آگهی‌های فعال و پیش‌نویس‌های کاربر لاگین‌شده در باما",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "bama_get_saved_cars",
        "description": "مشاهده خودروهای نشان‌شده و ذخیره‌شده در پارکینگ کاربر در باما",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "bama_status",
        "description": "بررسی وضعیت اتصال و سلامت سرور MCP باما",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "bama_help",
        "description": "راهنمای جامع ابزارها و کاتالوگ قابلیت‌های سرور باما",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
]


def execute_tool(name: str, arguments: Dict[str, Any]) -> Any:
    """Dispatch tool execution."""
    try:
        if name == "bama_search_cars":
            return client.search_cars(
                brand=arguments.get("brand"),
                model=arguments.get("model"),
                province=arguments.get("province"),
                price_min=arguments.get("price_min"),
                price_max=arguments.get("price_max"),
                page=int(arguments.get("page", 0)),
                limit=int(arguments.get("limit", 20)),
            )

        elif name == "bama_get_car_details":
            code = arguments.get("ad_code", "")
            return client.get_car_details(ad_code=code)

        elif name == "bama_search_motorcycles":
            return client.search_motorcycles(
                page=int(arguments.get("page", 0)),
                limit=int(arguments.get("limit", 20)),
            )

        elif name == "bama_search_trucks":
            return client.search_trucks(
                page=int(arguments.get("page", 0)),
                limit=int(arguments.get("limit", 20)),
            )

        elif name == "bama_list_brands":
            return client.list_brands()

        elif name == "bama_trending_searches":
            return client.get_trending_searches()

        elif name == "bama_appraise_car":
            code = arguments.get("ad_code", "")
            details = client.get_car_details(code)
            return appraise_car(details)

        elif name == "bama_compare_cars":
            code1 = arguments.get("ad_code_1", "")
            code2 = arguments.get("ad_code_2", "")
            d1 = client.get_car_details(code1)
            d2 = client.get_car_details(code2)
            return compare_cars(d1, d2)

        elif name == "bama_get_contact":
            code = arguments.get("ad_code", "")
            return client.get_contact(ad_code=code)

        elif name == "bama_auth_status":
            return client.get_user_profile()

        elif name == "bama_auth_set_token":
            tok = arguments.get("token", "")
            client.set_token(tok)
            return {"status": "success", "message": "Bama Bearer token saved successfully."}

        elif name == "bama_get_my_ads":
            return client.get_my_ads()

        elif name == "bama_get_saved_cars":
            return client.get_saved_cars()

        elif name == "bama_status":
            test_search = client.search_cars(limit=1)
            is_ok = test_search.get("items_count", 0) > 0
            return {
                "server": "bama-mcp",
                "version": "1.0.0",
                "status": "online" if is_ok else "degraded",
                "marketplace": "Bama (باما)",
                "endpoints_supported": [
                    "car_search",
                    "motorcycle_search",
                    "truck_search",
                    "ad_details",
                    "brands_catalog",
                    "trending_searches",
                    "deal_appraisal",
                    "contact_card",
                    "parking_bookmarks",
                    "user_ads",
                ],
            }

        elif name == "bama_help":
            return {
                "description": "Bama MCP Server provides comprehensive API access to Iran's vehicle marketplace.",
                "tools_count": len(TOOLS),
                "tools": [{"name": t["name"], "description": t["description"]} for t in TOOLS],
            }

        else:
            return {"error": f"Tool '{name}' not found."}

    except Exception as ex:
        logger.exception("Error executing tool %s: %s", name, ex)
        return {"error": str(ex), "tool": name}
