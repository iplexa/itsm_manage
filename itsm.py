import requests
import json
from typing import Dict, Any, Optional, List

from dataclasses import dataclass
from enum import Enum


@dataclass
class Task:
    name: str
    desc: str

class TaskType(Enum):
    DEV='Разработка'
    EDU='Сопровождение обучения'
    EMP='ПК сотрудника'

@dataclass
class Service:
    level: int
    id: str
    name: str

class Services(Enum):
    EMPLOYE_SERVICE: Service = Service(
        level=1,
        id='174283069691576051',
        name='Сопровождение сервисов сотрудника',
    )
    EMPLOYE_ACCOUNT: Service = Service(
        level=2,
        id='171827434296827078',
        name='Учетная запись (УЗ) сотрудников',
    )
    EMPLOYE_ACCOUNT_RESET: Service = Service(
        level=3,
        id='171834970892408003',
        name='Сброс пароля УЗ',
    )
    EMPLOYE_MAINTENANCE: Service = Service(
        level=2,
        id='171827435390586219',
        name='Обслуживание техники на рабочих местах (ПК)',
    )
    EMPLOYE_MAINTENANCE_PC: Service = Service(
        level=3,
        id='171834970892408136',
        name='Обслуживание ПК',
    )
    EMPLOYE_MAINTENANCE_PC_REPAIR: Service = Service(
        level=4,
        id='171835197993241692',
        name='Восстановление работоспособности ПК',
    )
    EMPLOYE_PRINT: Service = Service(
        level=3,
        id='174283120990205435',
        name='Устройство печати и сканирования',
    )
    EMPLOYE_PRINT_REPL: Service = Service(
        level=4,
        id='174288745591658729',
        name='Замена расходных материалов',
    )
    EMPLOYE_PRINT_INST: Service = Service(
        level=4,
        id='174288745591658729',
        name='Подключение/настройка/отключение оборудования',
    )

    EDU: Service = Service(
        level=1,
        id='174291345197423243',
        name='Сопровождение мероприятий и учебного процесса'
    )
    EDU_SERVICE: Service = Service(
        level=2,
        id='173979049797789044',
        name='Сопровождение учебного процесса'
    )
    EDU_MAINTENANCE: Service = Service(
        level=3,
        id='174288904894201605',
        name='Сопровождение учебного процесса'
    )


    

class HelpServices:
    pass


class RanepaHelpdeskAPI:
    """Класс для работы с API help.ranepa.ru"""
    
    def __init__(self, base_url: str, bearer_token: str, cookies: Dict[str, str] = None):
        """
        Инициализация клиента API
        
        Args:
            base_url: Базовый URL API
            bearer_token: Токен для авторизации
            cookies: Словарь с cookies (опционально)
        """
        self.base_url = base_url.rstrip('/')
        self.bearer_token = bearer_token
        self.cookies = cookies or {}
        self.session = requests.Session()
        
        # Настройка заголовков по умолчанию
        self.session.headers.update({
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json'
        })
        
        # Установка cookies если они предоставлены
        if self.cookies:
            self.session.cookies.update(self.cookies)
    
    def _make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> requests.Response:
        """
        Базовый метод для выполнения HTTP запросов
        
        Args:
            method: HTTP метод (GET, POST, PUT, DELETE)
            endpoint: Конечная точка API
            data: Данные для отправки
            
        Returns:
            Response object
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            raise
    
    def create_itsm_request(
            self, 
            subject: str, 
            description: str,
            assignment_group: str = "173822703391995789",
            assigned_user: str = "172604794594718175", # я
            # assigned_user: str = "171204857597715805", # влад
            
            caller: str = "173148413796748031",
            company: str = "170853763708902887",
            service: str = "174291345197423243",
            service_2nd_level: str = "173979049797789044",
            service_3rd_level: str = "174288904894201605",
            **additional_fields
            ) -> Dict[str, Any]:
        """
        Создание ITSM запроса
        
        Args:
            subject: Тема запроса
            description: Описание запроса
            assignment_group: Группа назначения
            assigned_user: Назначенный пользователь
            caller: Инициатор запроса
            company: Компания
            service: Услуга
            service_2nd_level: Услуга 2-го уровня
            service_3rd_level: Услуга 3-го уровня
            **additional_fields: Дополнительные поля для записи
            
        Returns:
            Ответ от API
        """
        # Базовая структура записи
        record_data = {
            "state": "2",
            "priority": "1",
            "resubmission": "",
            "external_company": "",
            "external_task": "",
            "assignment_group": assignment_group,
            "assigned_user": assigned_user,
            "subject": subject,
            "description": description,
            "related_cis": "",
            "caller": caller,
            "company": company,
            "contact_type": "30",
            "tag": "",
            "service": service,
            "service_2nd_level": service_2nd_level,
            "service_3rd_level": service_3rd_level,
            "service_4th_level": "",
            "link_task": "https://tracker.yandex.ru/",
            "admissions_committee": 0,
            "attention_required": 0,
            "task_confidentiality": 0,
            "first_line_task": 0,
            "processed_ai_cb": 0,
            "faq_article": "",
            "additional_comments": "",
            "work_notes": "",
            "basic_service": "Сопровождение мероприятий и учебного процесса. Сопровождение учебного процесса. Сопровождение учебного процесса.",
            "followers_list": "",
            "admin_closure": None,
            "related_request_model": "",
            "request_template": "",
            "slave_request": "",
            "solved_by_changes": "",
            "related_problems": "",
            "level_of_dependency": None,
            "master_request": "",
            "related_inquiry": "",
            "related_incident": "",
            "glpi_link": "",
            "closure_code": None,
            "closure_notes": "",
            "performer_note": "",
            "manager_note": "",
            "service_manager_satisfaction": None,
            "service_satisfaction": None,
            "resolved_by": "",
            "resolved_at": "",
            "predicted_group": "",
            "predicted_service": "",
            "predicted_group_icl": "",
            "predicted_service_icl": ""
        }
        
        # Обновляем базовые данные дополнительными полями
        record_data.update(additional_fields)
        
        # Полная структура запроса
        request_data = {
            "record": record_data,
            "attachments": [],
            "rem_attributes": []
        }
        
        # Выполняем PUT запрос
        response = self._make_request('PUT', 'record/itsm_request', request_data)
        return response.json()
    
    def update_itsm_request(self, request_id: str, **update_fields) -> Dict[str, Any]:
        """
        Обновление существующего ITSM запроса
        
        Args:
            request_id: ID запроса для обновления
            **update_fields: Поля для обновления
            
        Returns:
            Ответ от API
        """
        endpoint = f"record/itsm_request/{request_id}"
        return self._make_request('PUT', endpoint, update_fields)
    
    def get_itsm_request(self, request_id: str) -> Dict[str, Any]:
        """
        Получение информации о ITSM запросе
        
        Args:
            request_id: ID запроса
            
        Returns:
            Информация о запросе
        """
        endpoint = f"record/itsm_request/{request_id}"
        response = self._make_request('GET', endpoint)
        return response.json()


class BaseTasks:

    vks = Task('ВКС этапы автоматизации сброса паролей сотрудников', 'посещение ВКС')
    vks_sa = Task('ВКС автомаизация сброса паролей сотрудников', 'посещение ВКС')

    rooms2: List[Task] = [
        Task("Регламентные работы", "Совершить обход всех аудиторий П/2 1,2 этаж"),
        Task("Регламентные работы", "Совершить обход всех аудиторий П/2 3 этаж"),
        Task("Регламентные работы", "Совершить обход всех аудиторий П/2 4 этаж"),
    ]
    
    rooms1: List[Task] = [
        Task("Регламентные работы", "Совершить обход всех аудиторий П/1 1,2 этаж"),
        Task("Регламентные работы", "Совершить обход всех аудиторий П/1 3 этаж"),
        Task("Регламентные работы", "Совершить обход всех аудиторий П/1 4 этаж"),
    ]

    @classmethod
    def get_modern_tasks(inv_num: str):
        modern_tasks = [
            Task('Подготовка моноблока к модернизации',f'Подготовить моноблок {inv_num} к модернизации: собрать данные у пользователя, сжать раздел диска C до 500гб. Транспортировать моноблок в кабинет для последющей модернизаци.'),
            Task('Модернизация моноблока, замена диска',f'Провести модернизацию моноблока {inv_num}. Установить M2 SSD накопитель.'),
            Task('Провести клонирование системы моноблока после модернизации',f'Клонировать раздел и все файлы старого накопителя на новый. Настроить и подготовить моноблок {inv_num} к использованию после замены (обновить драйвера, выставить порядок загрузки в BIOS). Демонтировать старый накопитель из моноблока после установки.'),
            Task('Установка моноблока после модернизации',f'Установить моноблок {inv_num} в кабинет. Проинформировать пользователя о проведенных работах и возможных ошибках. Подключить, проверить работоспособность.')
        ]
        return modern_tasks  
    
    @classmethod
    def get_mount_tasks(req_num: str):
        mount_tasks = [
            Task(f'Подключение оборудование {req_num}',f'Подключить оборудование, подготовить к занятию по {req_num}'),
            Task(f'Отключение оборудование {req_num}',f'Отключить оборудование после завершения занятия по {req_num}'),
        ]
        return mount_tasks


# Пример использования
if __name__ == "__main__":
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
    bt: BaseTasks = BaseTasks()

    tasks_st: List[Task] = [
        *bt.get_mount_tasks('REQ0254012'),
        Task('Восстановление работоспособности REQ0254012','Восстановить подключение к интернету на одном из ноубуков по REQ0254012. Переустановить WiFi драйвера.'),
        Task('Сопровождение учебного процесса','Оказать сопровождение учебного процесса REQ0257474 П/2 305 02.12 19:00-22:00'),
        
        *bt.get_mount_tasks('REQ0254015'),
        Task('Восстановление работоспособности REQ0259486','Заменить мышь на одном из ноубуков по REQ0259486.'),

        *bt.get_mount_tasks('REQ0257474'),
        Task('Сопровождение учебного процесса','Оказать сопровождение учебного процесса REQ0257474 П/2 305 04.12 19:00-22:00'),
        Task('Восстановление работоспособности REQ0259486','Заменить блок питания одного из ноутбуков по REQ0259486. Проверить работоспособность.'),

        *bt.get_mount_tasks('REQ0260836'),
        *bt.get_mount_tasks('REQ0262079'),
        *bt.get_mount_tasks('REQ0263788'),

        *bt.get_mount_tasks('REQ0260837'),
        *bt.get_mount_tasks('REQ0262094'),
        *bt.get_mount_tasks('REQ0263789'),


    ]
    tasks_emp = [
        Task('Замена картриджа МФУ П/2 102', 'Заменить картридж в МФУ.'),
        Task('Настройка принтера П/2 102','Подлключить, настроить принтер в офисе П/2 102. Подключить ПК сотрудников к принтеру.'),
        *bt.get_modern_tasks('AK2020003097'),
        *bt.get_modern_tasks('AK2020002924'),
        *bt.get_modern_tasks('AK2020003096'),
        *bt.get_modern_tasks('AK2020003098'),
        *bt.get_modern_tasks('AK2019059723'),
        *bt.get_modern_tasks('AK2019059711'),
    ]

    tasks_dev = [
        bt.vks,
        bt.vks,
        bt.vks,
        bt.vks,
        bt.vks,
        bt.vks_sa,
    ]

    tasks_all = {
        tasks_st,
        tasks_dev,
        tasks_emp
    }

    for tasks in tasks_all:
        try:
            response = api_client.create_itsm_request(
                subject=task.name,
                description=task.desc
            )
            print(f"Запрос успешно создан для {task.name}")
            # print(json.dumps(response, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Ошибка при создании запроса: {e}")
    
