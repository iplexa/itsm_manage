import re
import json
import time
from typing import Dict

from api_client import RanepaHelpdeskAPI


BASE_URL = "https://help.ranepa.ru/v1"

BEARER_TOKEN = "MLS1CwT_LaafKIrWz8CUrDphvm8QL0Wz"

COOKIES = {
    "SERVERID": "srv-ZX+LjaYo74PPaRAbaBcVCg|aPZkh",
    "BITRIX_CONVERSION_CONTEXT_s1": "%7B%22ID%22%3A6%2C%22EXPIRE%22%3A1756933140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D",
    "tmr_lvid": "a57c27c01481de50209456b0f0f1a9b9",
    "tmr_lvidTS": "1756899510168",
    "BITRIX_SM_GUEST_ID": "33458112",
    "BITRIX_SM_LAST_VISIT": "03.09.2025%2014%3A38%3A27",
    "_ym_d": "1751286514",
    "_ym_uid": "1751286514368500676"
}


links = [
    "https://help.ranepa.ru/record/itsm_request/177141862596882100",
    "https://help.ranepa.ru/record/itsm_request/177151933297043641",
]


# ---------- helpers ----------

def extract_id(url: str) -> str:
    return re.search(r'/itsm_request/(\d+)', url).group(1)


def get_value(field):
    if not isinstance(field, dict):
        return field

    value = field.get("value")

    if isinstance(value, dict):
        return value.get("display_value") or value.get("database_value")

    return value


# ---------- поиск кастомных полей ----------

def extract_custom_fields(item: dict) -> Dict:
    date = None
    audience = None

    for key, field in item.items():
        val = get_value(field)

        if not val:
            continue

        key_lower = key.lower()

        # ---- ДАТА ----
        if not date and (
            "date" in key_lower
            or "дата" in key_lower
            or "start" in key_lower
        ):
            date = val

        # ---- АУДИТОРИЯ ----
        if not audience and any(x in key_lower for x in [
            "aud", "room", "cab", "ауд", "кабин"
        ]):
            audience = val

    return {
        "date": date,
        "audience": audience
    }


# ---------- основной парсер ----------

def extract_request(data: dict) -> dict:
    try:
        items = data["data"]["related_lists"]["active_related_grid_data"]["items"]

        if not items:
            return {}

        item = items[0]

        custom = extract_custom_fields(item)

        return {
            "id": data["data"].get("record_id"),
            "number": get_value(item.get("number")),
            "subject": get_value(item.get("subject")),
            "description": get_value(item.get("description")),
            "caller": get_value(item.get("caller")),
            "state": get_value(item.get("state")),
            "priority": get_value(item.get("priority")),
            "assigned_user": get_value(item.get("assigned_user")),
            "created_at": get_value(item.get("sys_created_at")),

            # 👇 кастом
            "date": custom["date"],
            "audience": custom["audience"],
        }

    except Exception as e:
        print(f"Ошибка парсинга: {e}")
        return {}


# ---------- main ----------

def main():
    api = RanepaHelpdeskAPI(BASE_URL, BEARER_TOKEN, COOKIES)

    results = []

    for i, link in enumerate(links):
        req_id = extract_id(link)

        print(f"[{i+1}/{len(links)}] {req_id}")

        try:
            data = api.get_itsm_request(req_id)
            parsed = extract_request(data)

            print(f"  ✓ {parsed.get('number')} | {parsed.get('subject')}")

            if parsed.get("date") or parsed.get("audience"):
                print(f"    📅 {parsed.get('date')} | 🏫 {parsed.get('audience')}")

            results.append(parsed)

        except Exception as e:
            print(f"  ❌ Ошибка: {e}")

        time.sleep(0.3)

    with open("requests.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\nГотово → requests.json")


if __name__ == "__main__":
    main()