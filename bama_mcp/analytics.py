"""
Bama Automotive Analytics and Valuation Engine
Calculates vehicle deal quality, body condition index, and comparative analysis.
"""

from typing import Any, Dict


def appraise_car(details: Dict[str, Any]) -> Dict[str, Any]:
    """Appraise vehicle condition, mileage, and market deal quality."""
    if "error" in details:
        return details

    title = details.get("title", "")
    body_status = details.get("body_status", "")
    mileage_str = details.get("mileage", "")
    year_str = str(details.get("year", ""))
    price_str = details.get("price_irr_formatted") or details.get("price_string") or ""

    # 1. Body condition score (0-40)
    body_score = 40.0
    if "بدون رنگ" in body_status:
        body_score = 40.0
        body_tier = "بدون رنگ (فابریک)"
    elif "یک لکه رنگ" in body_status:
        body_score = 32.0
        body_tier = "یک لکه رنگ جزئی"
    elif "چند لکه رنگ" in body_status or "دور رنگ" in body_status:
        body_score = 22.0
        body_tier = "دور رنگ / چند لکه رنگ"
    elif "تصادفی" in body_status or "تعویض" in body_status:
        body_score = 12.0
        body_tier = "تصادفی یا دارای تعویض"
    else:
        body_tier = body_status or "نامشخص"

    # 2. Mileage score (0-30)
    mileage_score = 30.0
    if "صفر" in mileage_str:
        mileage_score = 30.0
        mileage_tier = "صفر کیلومتر"
    else:
        # Extract digits
        digits = "".join([c for c in mileage_str if c.isdigit()])
        if digits:
            km = int(digits)
            if km < 30000:
                mileage_score = 27.0
                mileage_tier = f"کم‌کارکرد ({km:,} کیلومتر)"
            elif km < 80000:
                mileage_score = 22.0
                mileage_tier = f"کارکرد استاندارد ({km:,} کیلومتر)"
            elif km < 150000:
                mileage_score = 16.0
                mileage_tier = f"کارکرد بالا ({km:,} کیلومتر)"
            else:
                mileage_score = 10.0
                mileage_tier = f"کارکرد بسیار بالا ({km:,} کیلومتر)"
        else:
            mileage_tier = mileage_str or "نامشخص"

    # 3. Model Year & Seller Factor (0-30)
    year_score = 20.0
    dealer = details.get("dealer")
    seller_bonus = 5.0 if dealer else 0.0

    total_score = round(min(100.0, body_score + mileage_score + year_score + seller_bonus), 1)

    if total_score >= 85:
        deal_rating = "Excellent Deal (معامله بسیار عالی و تمیز)"
    elif total_score >= 70:
        deal_rating = "Good Deal (معامله منصفانه)"
    elif total_score >= 55:
        deal_rating = "Average (معمولی)"
    else:
        deal_rating = "High Risk / Needs Inspection (نیازمند کارشناسی دقیق فنی)"

    return {
        "code": details.get("code"),
        "title": title,
        "price": price_str,
        "total_score": total_score,
        "body_score": body_score,
        "mileage_score": mileage_score,
        "body_status": body_tier,
        "mileage_status": mileage_tier,
        "deal_rating": deal_rating,
        "verdict": f"خودروی {title} با امتیاز سلامت {total_score}/100 در رده '{deal_rating}' برآورد گردید.",
    }


def compare_cars(car_a: Dict[str, Any], car_b: Dict[str, Any]) -> Dict[str, Any]:
    """Side-by-side comparison between two cars."""
    app_a = appraise_car(car_a)
    app_b = appraise_car(car_b)

    score_a = app_a.get("total_score", 0)
    score_b = app_b.get("total_score", 0)
    winner = car_a.get("title") if score_a >= score_b else car_b.get("title")

    return {
        "car_1": {
            "title": car_a.get("title"),
            "year": car_a.get("year"),
            "price": car_a.get("price_irr_formatted") or car_a.get("price_string"),
            "mileage": car_a.get("mileage"),
            "score": score_a,
        },
        "car_2": {
            "title": car_b.get("title"),
            "year": car_b.get("year"),
            "price": car_b.get("price_irr_formatted") or car_b.get("price_string"),
            "mileage": car_b.get("mileage"),
            "score": score_b,
        },
        "recommended_choice": winner,
        "comparison_summary": f"با توجه به سلامت بدنه، کارکرد و ارزش خرید، '{winner}' پیشنهاد برتر شناخته می‌شود.",
    }
