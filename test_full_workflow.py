import json
import traceback
from datetime import datetime
from models import Task, Services
from api_client import RanepaHelpdeskAPI


def log_step(step_name: str, message: str = ""):
    """Логирование шага с временной меткой"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{timestamp}] {'='*80}")
    print(f"[{timestamp}] {step_name}")
    if message:
        print(f"[{timestamp}] {message}")
    print(f"[{timestamp}] {'='*80}")


def log_success(message: str):
    """Логирование успешного выполнения"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] ✓ {message}")


def log_error(message: str, exception: Exception = None):
    """Логирование ошибки"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] ✗ ОШИБКА: {message}")
    if exception:
        print(f"[{timestamp}] Тип ошибки: {type(exception).__name__}")
        print(f"[{timestamp}] Сообщение: {str(exception)}")
        print(f"[{timestamp}] Трассировка:")
        traceback.print_exc()


def log_data(data_name: str, data: any):
    """Логирование данных"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{timestamp}] {data_name}:")
    if isinstance(data, dict):
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(data)


def main():
    log_step("НАЧАЛО ТЕСТОВОГО СКРИПТА", "Полная обработка одной заявки")
    
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
    
    # Создание тестовой задачи
    from datetime import date, timedelta
    
    # Пример: закрыть заявку завтра в 13:00
    tomorrow = date.today() + timedelta(days=1)
    
    test_task = Task(
        name="Восстановление работоспособности REQ0254012",
        desc="Восстановить подключение к интернету на одном из ноубуков по REQ0254012. Переустановить WiFi драйвера.",
        time_spent_minutes=30,  # 30 минут = 0.5 часа
        closure_text="Работоспособность восстановлена.",
        closure_date=tomorrow  # Опционально: дата закрытия (время будет 13:00)
    )
    
    log_step("НАСТРОЙКА", f"Создана тестовая задача: {test_task.name}")
    task_params = {
        "name": test_task.name,
        "desc": test_task.desc,
        "time_spent_minutes": test_task.time_spent_minutes,
        "time_spent_hours": f"{test_task.time_spent_minutes/60:.2f}",
        "closure_text": test_task.closure_text
    }
    if test_task.closure_date:
        task_params["closure_date"] = test_task.closure_date.strftime("%Y-%m-%d")
        task_params["closure_time"] = "13:00"
    log_data("Параметры задачи", task_params)
    
    # Создание экземпляра клиента
    try:
        api_client = RanepaHelpdeskAPI(BASE_URL, BEARER_TOKEN, COOKIES)
        log_success("API клиент успешно создан")
    except Exception as e:
        log_error("Не удалось создать API клиент", e)
        return
    
    request_id = None
    
    # ШАГ 1: Создание заявки
    log_step("ШАГ 1: СОЗДАНИЕ ЗАЯВКИ")
    try:
        log_data("Параметры создания", {
            "subject": test_task.name,
            "description": test_task.desc,
            "service": "EDU_MAINTENANCE",
            "auto_assign": True
        })
        
        response = api_client.create_itsm_request(
            subject=test_task.name,
            description=test_task.desc,
            service=Services.EDU_MAINTENANCE.value,
            auto_assign=True  # Автоматически берем в работу
        )
        
        log_data("Ответ API при создании", response)
        
        # Извлекаем ID заявки
        if isinstance(response, dict):
            if 'data' in response and isinstance(response['data'], dict):
                request_id = response['data'].get('record_id')
                if request_id:
                    log_success(f"Заявка успешно создана. ID: {request_id}")
                    if 'display_value' in response['data']:
                        log_success(f"Номер заявки: {response['data']['display_value']}")
                else:
                    log_error("ID заявки не найден в ответе")
                    log_data("Полный ответ", response)
                    return
            else:
                log_error("Неожиданная структура ответа")
                log_data("Полный ответ", response)
                return
        else:
            log_error(f"Неожиданный тип ответа: {type(response)}")
            return
            
    except Exception as e:
        log_error("Ошибка при создании заявки", e)
        return
    
    if not request_id:
        log_error("Не удалось получить ID заявки. Прерываем выполнение.")
        return
    
    # ШАГ 2: Проверка взятия в работу (уже выполнено автоматически)
    log_step("ШАГ 2: ВЗЯТИЕ В РАБОТУ", "Выполнено автоматически при создании")
    log_success("Заявка уже взята в работу")
    
    # ШАГ 3: Списание трудозатрат
    log_step("ШАГ 3: СПИСАНИЕ ТРУДОЗАТРАТ")
    try:
        time_params = {
            "request_id": request_id,
            "time_spent_minutes": test_task.time_spent_minutes,
            "time_spent_hours": f"{test_task.time_spent_minutes/60:.2f}",
            "closure_text": test_task.closure_text
        }
        if test_task.closure_date:
            time_params["work_date"] = test_task.closure_date.strftime("%Y-%m-%d")
            time_params["work_time"] = "13:00"
        log_data("Параметры списания", time_params)
        
        time_response = api_client.log_time_spent(
            request_id=request_id,
            time_spent_minutes=test_task.time_spent_minutes,
            closure_text=test_task.closure_text,
            work_date=test_task.closure_date  # Передаем дату выполнения работы
        )
        
        log_data("Ответ API при списании трудозатрат", time_response)
        time_info = f"{test_task.time_spent_minutes} минут ({test_task.time_spent_minutes/60:.2f} часов)"
        if test_task.closure_date:
            time_info += f" за {test_task.closure_date.strftime('%Y-%m-%d')} 13:00"
        log_success(f"Трудозатраты успешно списаны: {time_info}")
        
    except Exception as e:
        log_error("Ошибка при списании трудозатрат", e)
        log_error("Продолжаем выполнение, но заявка может быть не закрыта корректно")
    
    # ШАГ 4: Закрытие заявки
    log_step("ШАГ 4: ЗАКРЫТИЕ ЗАЯВКИ")
    try:
        log_data("Параметры закрытия", {
            "request_id": request_id,
            "closure_text": test_task.closure_text,
            "closure_code": "2",
            "state": "7"
        })
        
        close_response = api_client.close_itsm_request(
            request_id=request_id,
            closure_text=test_task.closure_text
        )
        
        log_data("Ответ API при закрытии", close_response)
        log_success(f"Заявка успешно закрыта: {test_task.closure_text}")
        
    except Exception as e:
        log_error("Ошибка при закрытии заявки", e)
    
    # Итоги
    log_step("ИТОГИ", f"Обработка заявки {request_id} завершена")
    log_data("Результаты", {
        "request_id": request_id,
        "task_name": test_task.name,
        "time_spent": f"{test_task.time_spent_minutes} минут",
        "closure_text": test_task.closure_text,
        "status": "Успешно обработана" if request_id else "Ошибка"
    })
    
    log_step("КОНЕЦ ТЕСТОВОГО СКРИПТА")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[ПРЕРВАНО ПОЛЬЗОВАТЕЛЕМ]")
    except Exception as e:
        print(f"\n\n[КРИТИЧЕСКАЯ ОШИБКА] {type(e).__name__}: {e}")
        traceback.print_exc()

