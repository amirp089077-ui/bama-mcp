"""
Bama API Client
Direct REST integration for Bama (باما) car, motorcycle, and commercial vehicle marketplace.
"""

import json
import logging
import os
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

logger = logging.getLogger("bama_mcp.client")

BAMA_BASE = "https://bama.ir"
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
TOKEN_STORAGE_PATH = os.path.expanduser("~/.bama_mcp_token.json")


class BamaClient:
    """Production client for Bama (باما) Marketplace."""

    def __init__(self, timeout: float = 12.0):
        self.timeout = timeout
        self.token = self._load_persisted_token()

    def _load_persisted_token(self) -> Optional[str]:
        try:
            if os.path.exists(TOKEN_STORAGE_PATH):
                with open(TOKEN_STORAGE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("access_token")
        except Exception:
            pass
        return None

    def set_token(self, token: str) -> None:
        self.token = token.strip()
        try:
            with open(TOKEN_STORAGE_PATH, "w", encoding="utf-8") as f:
                json.dump({"access_token": self.token}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning("Could not persist Bama token: %s", e)

    def _get_headers(self, auth_required: bool = False) -> Dict[str, str]:
        headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "fa,en;q=0.9",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _fetch_json(self, url: str, auth_required: bool = False) -> Dict[str, Any]:
        req = urllib.request.Request(url, headers=self._get_headers(auth_required=auth_required))
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data_text = resp.read().decode("utf-8", errors="replace")
                return json.loads(data_text)
        except urllib.error.HTTPError as he:
            err_body = he.read().decode("utf-8", errors="replace") if hasattr(he, "read") else ""
            logger.error("HTTP error %d for %s: %s", he.code, url, err_body)
            try:
                return json.loads(err_body)
            except Exception:
                return {"error": f"HTTP {he.code}", "details": err_body}
        except Exception as ex:
            logger.exception("Failed to fetch %s", url)
            return {"error": str(ex)}

    def search_cars(
        self,
        brand: Optional[str] = None,
        model: Optional[str] = None,
        province: Optional[str] = None,
        price_min: Optional[int] = None,
        price_max: Optional[int] = None,
        page: int = 0,
        limit: int = 24,
    ) -> Dict[str, Any]:
        """Search car listings on Bama."""
        params = {"pageIndex": str(page)}
        if brand:
            params["brand"] = brand.strip().lower()
        if model:
            params["model"] = model.strip().lower()
        if province:
            params["province"] = province.strip()
        if price_min is not None or price_max is not None:
            p_min = price_min or 0
            p_max = price_max or 0
            params["price"] = f"{p_min},{p_max}"

        query_str = urllib.parse.urlencode(params)
        url = f"{BAMA_BASE}/cad/api/search?{query_str}"
        res = self._fetch_json(url)

        ads_raw = res.get("data", {}).get("ads", []) if isinstance(res.get("data"), dict) else []
        items = []
        for a in ads_raw:
            d = a.get("detail")
            if not d:
                continue
            p = a.get("price") or {}
            specs = a.get("specs") or {}
            dealer = a.get("dealer") or {}

            items.append({
                "code": d.get("code"),
                "title": d.get("title"),
                "subtitle": d.get("subtitle"),
                "year": d.get("year"),
                "mileage": d.get("mileage"),
                "location": d.get("location"),
                "price_string": p.get("price") or "توافقی",
                "price_type": p.get("type", "lumpsum"),
                "transmission": d.get("transmission"),
                "fuel": d.get("fuel"),
                "color": d.get("color"),
                "body_status": d.get("body_status"),
                "body_type": d.get("body_type_fa"),
                "image": d.get("image"),
                "time": d.get("time"),
                "url": f"{BAMA_BASE}{d.get('url', '')}",
                "brand": d.get("brand"),
                "engine": specs.get("engine"),
                "fuel_consumption": specs.get("fuel"),
                "dealer_name": dealer.get("name") if dealer else None,
            })
            if len(items) >= limit:
                break

        metadata = res.get("metadata") or {}
        return {
            "total_count": metadata.get("total_count", len(items)),
            "page": page,
            "items_count": len(items),
            "ads": items,
        }

    def get_car_details(self, ad_code: str) -> Dict[str, Any]:
        """Get full details of a specific car advertisement."""
        clean_code = ad_code.strip()
        url = f"{BAMA_BASE}/cad/api/detail/{clean_code}"
        res = self._fetch_json(url)
        data = res.get("data")
        if not data:
            return {"error": "Ad not found or removed", "code": clean_code}

        d = data.get("detail", {})
        p = data.get("price", {})
        specs = data.get("specs") or {}
        dealer = data.get("dealer") or {}
        images = [img.get("url") for img in (data.get("images") or []) if isinstance(img, dict) and img.get("url")]

        return {
            "code": clean_code,
            "title": d.get("title"),
            "subtitle": d.get("subtitle"),
            "trim": d.get("trim"),
            "year": d.get("year"),
            "location": d.get("location"),
            "province": d.get("province"),
            "mileage": d.get("mileage"),
            "transmission": d.get("transmission"),
            "fuel": d.get("fuel"),
            "color": d.get("color"),
            "body_status": d.get("body_status"),
            "description": d.get("description"),
            "price_irr_formatted": p.get("price"),
            "price_type": p.get("type"),
            "specs": {
                "volume": specs.get("volume"),
                "engine": specs.get("engine"),
                "acceleration": specs.get("acceleration"),
                "fuel_consumption": specs.get("fuel"),
            },
            "seller_masked_phone": d.get("phone"),
            "dealer": {
                "name": dealer.get("name"),
                "address": dealer.get("address"),
                "score": dealer.get("score"),
                "ad_count": dealer.get("ad_count"),
            } if dealer else None,
            "images": images,
            "time": d.get("time"),
            "bama_url": f"{BAMA_BASE}{d.get('url', '')}",
        }

    def search_motorcycles(self, page: int = 0, limit: int = 24) -> Dict[str, Any]:
        """Search motorcycle listings on Bama."""
        url = f"{BAMA_BASE}/mad/api/search?pageIndex={page}"
        res = self._fetch_json(url)
        ads_raw = res.get("data", {}).get("ads", []) if isinstance(res.get("data"), dict) else []
        items = []
        for a in ads_raw:
            d = a.get("detail")
            if not d:
                continue
            p = a.get("price") or {}
            items.append({
                "code": d.get("code"),
                "title": d.get("title"),
                "subtitle": d.get("subtitle"),
                "year": d.get("year"),
                "mileage": d.get("mileage"),
                "location": d.get("location"),
                "price": p.get("price") or "توافقی",
                "image": d.get("image"),
                "time": d.get("time"),
                "url": f"{BAMA_BASE}{d.get('url', '')}",
            })
            if len(items) >= limit:
                break
        return {"items_count": len(items), "ads": items}

    def search_trucks(self, page: int = 0, limit: int = 24) -> Dict[str, Any]:
        """Search trucks and commercial vehicle listings on Bama."""
        url = f"{BAMA_BASE}/tad/api/search?pageIndex={page}"
        res = self._fetch_json(url)
        ads_raw = res.get("data", {}).get("ads", []) if isinstance(res.get("data"), dict) else []
        items = []
        for a in ads_raw:
            d = a.get("detail")
            if not d:
                continue
            p = a.get("price") or {}
            items.append({
                "code": d.get("code"),
                "title": d.get("title"),
                "subtitle": d.get("subtitle"),
                "year": d.get("year"),
                "mileage": d.get("mileage"),
                "location": d.get("location"),
                "price": p.get("price") or "توافقی",
                "image": d.get("image"),
                "time": d.get("time"),
                "url": f"{BAMA_BASE}{d.get('url', '')}",
            })
            if len(items) >= limit:
                break
        return {"items_count": len(items), "ads": items}

    def list_brands(self) -> List[Dict[str, Any]]:
        """List all car brands and their models catalog."""
        url = f"{BAMA_BASE}/cad/api/filter/vehicle"
        res = self._fetch_json(url)
        raw_items = res.get("data", [])
        brands = []
        for b in raw_items:
            slug = b.get("value")
            name = b.get("title")
            models = []
            for m in b.get("items") or []:
                models.append({
                    "name": m.get("title"),
                    "slug": m.get("value"),
                })
            if slug and name:
                brands.append({
                    "brand_slug": slug,
                    "brand_name": name,
                    "models_count": len(models),
                    "models": models,
                })
        return brands

    def get_trending_searches(self) -> Dict[str, Any]:
        """Get trending searches on Bama for cars and motorcycles."""
        url = f"{BAMA_BASE}/srh/api/general/search/top"
        res = self._fetch_json(url)
        return {
            "trending_cars": [c.get("title") or c.get("name") for c in res.get("cars", [])],
            "trending_motors": [m.get("title") or m.get("name") for m in res.get("motors", [])],
        }

    def get_contact(self, ad_code: str) -> Dict[str, Any]:
        """Retrieve contact info and seller card."""
        details = self.get_car_details(ad_code)
        if "error" in details:
            return details

        dealer = details.get("dealer")
        return {
            "code": ad_code,
            "title": details.get("title"),
            "seller_type": "Dealer / نمایشگاه" if dealer else "Individual / شخصی",
            "phone": details.get("seller_masked_phone"),
            "location": details.get("location"),
            "dealer": dealer,
            "bama_url": details.get("bama_url"),
        }

    def get_user_profile(self) -> Dict[str, Any]:
        """Get authenticated user info."""
        if not self.token:
            return {"authenticated": False, "message": "No Bearer token configured. Use bama_auth_set_token."}
        url = f"{BAMA_BASE}/prf/api/user/userinfo"
        res = self._fetch_json(url, auth_required=True)
        if "error" in res:
            return {"authenticated": False, "error": res.get("error")}
        return {"authenticated": True, "user": res}

    def get_my_ads(self) -> Dict[str, Any]:
        """Get user's published advertisements."""
        if not self.token:
            return {"authenticated": False, "message": "No Bearer token configured."}
        url = f"{BAMA_BASE}/prf/api/User/advertisements/search"
        res = self._fetch_json(url, auth_required=True)
        return res

    def get_saved_cars(self) -> Dict[str, Any]:
        """Get user's bookmarked cars from Bama Parking."""
        if not self.token:
            return {"authenticated": False, "message": "No Bearer token configured."}
        url = f"{BAMA_BASE}/prf/api/parking/minimal"
        res = self._fetch_json(url, auth_required=True)
        return res
