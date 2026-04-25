import json
from models import Services
from api_client import RanepaHelpdeskAPI


def main():
    # Настройки API
    BASE_URL = "https://help.ranepa.ru/v1"
    BEARER_TOKEN = "3Z8p64BDikJUF40ESmxEtynSJKmRC1VG"
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
    
    # Создание экземпляра клиента
    api_client = RanepaHelpdeskAPI(BASE_URL, BEARER_TOKEN, COOKIES)
    
    # Создаем одну тестовую заявку БЕЗ автоматического взятия в работу
    print("Создаю тестовую заявку...")
    print("-" * 80)
    
    try:
        response = api_client.create_itsm_request(
            subject="Сопровождение учебного процесса",
            description="Оказать сопровождение учебного процесса REQ0257474 П/2 305 02.12 19:00-22:00",
            service=Services.EDU_MAINTENANCE.value,
            auto_assign=False  # Отключаем автоматическое взятие в работу
        )
        
        print("\n✅ Заявка успешно создана!")
        print("\n" + "=" * 80)
        print("СТРУКТУРА ОТВЕТА:")
        print("=" * 80)
        print(json.dumps(response, indent=2, ensure_ascii=False))
        print("=" * 80)
        
        print("\n" + "-" * 80)
        print("АНАЛИЗ СТРУКТУРЫ:")
        print("-" * 80)
        
        # Пытаемся найти ID в разных местах
        print(f"\nТип ответа: {type(response)}")
        
        if isinstance(response, dict):
            print(f"\nКлючи верхнего уровня: {list(response.keys())}")
            
            # Проверяем различные варианты
            if 'id' in response:
                print(f"✓ Найден ID в корне: {response['id']}")
            
            if 'record' in response:
                record = response['record']
                print(f"\nТип 'record': {type(record)}")
                
                if isinstance(record, dict):
                    print(f"Ключи в 'record': {list(record.keys())}")
                    if 'id' in record:
                        print(f"✓ Найден ID в record: {record['id']}")
                
                elif isinstance(record, list):
                    print(f"record - это список из {len(record)} элементов")
                    if len(record) > 0:
                        print(f"Первый элемент: {type(record[0])}")
                        if isinstance(record[0], dict):
                            print(f"Ключи в первом элементе: {list(record[0].keys())}")
                            if 'id' in record[0]:
                                print(f"✓ Найден ID в record[0]: {record[0]['id']}")
            
            # Ищем ID рекурсивно
            def find_id(obj, path=""):
                """Рекурсивный поиск ID"""
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        current_path = f"{path}.{key}" if path else key
                        if key == 'id' or key == 'ID' or key == 'request_id':
                            print(f"✓ Найден ID по пути '{current_path}': {value}")
                        elif isinstance(value, (dict, list)):
                            find_id(value, current_path)
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        find_id(item, f"{path}[{i}]")
            
            print("\nРекурсивный поиск ID:")
            find_id(response)
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n❌ Ошибка при создании заявки: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

