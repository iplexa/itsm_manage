
import json
from typing import List
from datetime import date, timedelta, datetime
from models import Task, Services
from api_client import RanepaHelpdeskAPI
from tasks import BaseTasks
from task_list import tasks_all, tasks_dev, tasks_emp, tasks_st

def get_date(date_str: str) -> date:
    return datetime.strptime(date_str, '%d.%m.%Y').date()

LOG_fILE = f'log ({datetime.now().date()}).txt'

def main():
    log = open(LOG_fILE, 'w', encoding='utf-8')
    log.write(f"Начало выполнения скрипта: {datetime.now()}\n\n")
    log.flush()

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
    log.write("Инициализация API клиента...\n")
    log.flush()
    

    api_client = RanepaHelpdeskAPI(BASE_URL, BEARER_TOKEN, COOKIES)
    bt = BaseTasks()

    log.write("Начало обработки задач...\n")
    log.flush()

    for tasks in tasks_all:
        log.write('*'*50 + "\n")
        for task in tasks:
            log.write(f"Обработка задачи: {task}\n")
            log.flush()
            try:
                service = None
                if tasks == tasks_st:
                    service = Services.EDU_SERVICE.value
                elif tasks == tasks_emp:
                    if 'принтер' in task.name.lower() or 'мфу' in task.name.lower():
                        service = Services.EMPLOYE_PRINT_REPL.value
                    elif 'моноблок' in task.name.lower() or 'модернизац' in task.name.lower():
                        service = Services.EMPLOYE_MAINTENANCE_PC_REPAIR.value
                    else:
                        service = Services.EMPLOYE_MAINTENANCE_PC.value
                elif tasks == tasks_dev:
                    service = Services.EDU_MAINTENANCE.value
                
                response = api_client.create_itsm_request(
                    subject=task.name,
                    description=task.desc,
                    service=service,  
                    auto_assign=True 
                )
                
                request_id = None
                if isinstance(response, dict) and 'data' in response:
                    request_id = response['data'].get('record_id')
                
                if request_id:
                    print(f"Запрос успешно создан и взят в работу для {task.name} (ID: {request_id})")
                    log.write(f"Запрос успешно создан и взят в работу для {task.name} (ID: {request_id})\n")
                    
                    if task.time_spent_minutes > 0:
                        try:
                            time_info = f"{task.time_spent_minutes} минут ({task.time_spent_minutes/60:.2f} часов)"
                            if task.closure_date:
                                time_info += f" за {task.closure_date.strftime('%Y-%m-%d')} 13:00"
                            
                            time_response = api_client.log_time_spent(
                                request_id=request_id,
                                time_spent_minutes=task.time_spent_minutes,
                                closure_text=task.closure_text,
                                work_date=task.closure_date  
                            )
                            print(f"  ✓ Трудозатраты списаны: {time_info}")
                            log.write(f"  ✓ Трудозатраты списаны: {time_info}\n")
                        except Exception as e:
                            print(f"  ⚠ Ошибка при списании трудозатрат: {e}")
                            log.write(f"  ⚠ Ошибка при списании трудозатрат: {e}\n")
                    
                    if task.closure_text:
                        try:
                            close_response = api_client.close_itsm_request(
                                request_id=request_id,
                                closure_text=task.closure_text
                            )
                            print(f"  ✓ Заявка закрыта: {task.closure_text}")
                            log.write(f"  ✓ Заявка закрыта: {task.closure_text}\n")
                        except Exception as e:
                            print(f"  ⚠ Ошибка при закрытии заявки: {e}")
                            log.write(f"  ⚠ Ошибка при закрытии заявки: {e}\n")
                
                else:
                    print(f"Запрос успешно создан для {task.name}, но не удалось получить ID")
                    log.write(f"Запрос успешно создан для {task.name}, но не удалось получить ID\n")
                    # print(json.dumps(response, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"Ошибка при создании запроса: {e}")
                log.write(f"Ошибка при создании запроса: {e}\n")
                import traceback
                traceback.print_exc()
            
            log.write("\n")
            log.flush()


if __name__ == "__main__":
    main()

