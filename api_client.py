import requests
from typing import Dict, Any, Optional
from datetime import date, datetime
from models import Service
from models import HelpServices


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
            service: Optional[Service] = None,
            service_2nd_level: Optional[str] = None,
            service_3rd_level: Optional[str] = None,
            service_4th_level: Optional[str] = None,
            basic_service: Optional[str] = None,
            auto_assign: bool = True,
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
            service: Объект Service (если указан, автоматически заполняются все уровни и basic_service)
            service_2nd_level: Услуга 2-го уровня (используется только если service не указан)
            service_3rd_level: Услуга 3-го уровня (используется только если service не указан)
            service_4th_level: Услуга 4-го уровня (используется только если service не указан)
            basic_service: Строка с названиями сервисов (используется только если service не указан)
            auto_assign: Автоматически брать заявку в работу после создания (по умолчанию True)
            **additional_fields: Дополнительные поля для записи
            
        Returns:
            Ответ от API (если auto_assign=True, возвращает ответ от assign_itsm_request)
        """
        # Если передан объект Service, используем HelpServices для получения всех данных
        if service is not None:
            service_dict = HelpServices.get_service_dict(service)
            service_id = service_dict['service']
            service_2nd_level = service_dict.get('service_2nd_level', '') or service_2nd_level or ''
            service_3rd_level = service_dict.get('service_3rd_level', '') or service_3rd_level or ''
            service_4th_level = service_dict.get('service_4th_level', '') or service_4th_level or ''
            basic_service = service_dict.get('basic_service', '') or basic_service or ''
        else:
            # Значения по умолчанию, если service не указан
            service_id = "174291345197423243"
            service_2nd_level = service_2nd_level or "173979049797789044"
            service_3rd_level = service_3rd_level or "174288904894201605"
            service_4th_level = service_4th_level or ""
            basic_service = basic_service or "Сопровождение мероприятий и учебного процесса. Сопровождение учебного процесса. Сопровождение учебного процесса."
        
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
            "service": service_id,
            "service_2nd_level": service_2nd_level,
            "service_3rd_level": service_3rd_level,
            "service_4th_level": service_4th_level,
            "link_task": "https://tracker.yandex.ru/",
            "admissions_committee": 0,
            "attention_required": 0,
            "task_confidentiality": 0,
            "first_line_task": 0,
            "processed_ai_cb": 0,
            "faq_article": "",
            "additional_comments": "",
            "work_notes": "",
            "basic_service": basic_service,
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
        response_data = response.json()
        
        # Если нужно автоматически взять заявку в работу
        if auto_assign:
            # Извлекаем ID заявки из ответа
            # Структура ответа: {"data": {"record_id": "176502815797512384", ...}, ...}
            request_id = None
            if isinstance(response_data, dict):
                # Проверяем стандартную структуру ответа
                if 'data' in response_data and isinstance(response_data['data'], dict):
                    request_id = response_data['data'].get('record_id')
                
                # Если не нашли, пробуем альтернативные варианты (для обратной совместимости)
                if not request_id:
                    request_id = response_data.get('id') or response_data.get('record_id')
                    if not request_id and 'record' in response_data:
                        record = response_data.get('record')
                        if isinstance(record, dict):
                            request_id = record.get('id')
                        elif isinstance(record, list) and len(record) > 0:
                            request_id = record[0].get('id')
            
            if request_id:
                try:
                    # Берем заявку в работу
                    assign_response = self.assign_itsm_request(request_id, assigned_user)
                    return assign_response
                except Exception as e:
                    print(f"Предупреждение: не удалось взять заявку {request_id} в работу: {e}")
                    # Возвращаем исходный ответ, если не удалось взять в работу
                    return response_data
            else:
                print(f"Предупреждение: не удалось извлечь ID заявки из ответа: {response_data}")
                return response_data
        
        return response_data
    
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
    
    def assign_itsm_request(self, request_id: str, assigned_user: str = "172604794594718175") -> Dict[str, Any]:
        """
        Взятие ITSM запроса в работу
        
        Args:
            request_id: ID запроса для взятия в работу
            assigned_user: ID пользователя, который берет заявку в работу
            
        Returns:
            Ответ от API
        """
        endpoint = f"record/itsm_request/{request_id}?form_id=&form_view=Default&open_first_rel_list=0&is_service_portal=0"
        
        request_data = {
            "record": {
                "state": "2",
                "assigned_user": assigned_user
            },
            "rem_attributes": []
        }
        
        response = self._make_request('POST', endpoint, request_data)
        return response.json()
    
    def log_time_spent(
            self,
            request_id: str,
            time_spent_minutes: int,
            closure_text: str = "",
            user_id: str = "172604794594718175",
            type_work: str = "173865532591825881",
            status: str = "7",
            work_date: Optional[date] = None
            ) -> Dict[str, Any]:
        """
        Списание трудозатрат по заявке
        
        Args:
            request_id: ID заявки
            time_spent_minutes: Время в минутах (будет конвертировано в часы)
            closure_text: Текст для закрытия заявки (комментарий)
            user_id: ID пользователя
            type_work: ID типа работы (по умолчанию "По умолчанию")
            status: Статус заявки
            work_date: Дата выполнения работы (опционально, если указана - время будет 13:00, иначе текущая дата/время)
            
        Returns:
            Ответ от API
        """
        # Конвертируем минуты в миллисекунды (для currentTimeSpent)
        # API ожидает время в миллисекундах
        time_spent_ms = time_spent_minutes * 60 * 1000
        
        # Конвертируем минуты в часы для timeInt (формат "0.25" для 15 минут)
        time_spent_hours = time_spent_minutes / 60
        
        endpoint = "widget/run-server-script/172682807793900660"
        
        # Формируем дату и время для списания
        if work_date:
            # Если указана дата, используем её с временем 13:00
            work_datetime = datetime.combine(work_date, datetime.min.time().replace(hour=13, minute=0))
            current_datetime = work_datetime.strftime("%Y-%m-%d %H:%M:%S")
        else:
            # Иначе используем текущую дату и время
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        request_data = {
            "description": closure_text,
            "closure_code": "2",
            "quick-type": "default",
            "tableName": "itsm_request",
            "recordId": request_id,
            "isVisible": True,
            "isShowModal": True,
            "userId": user_id,
            "taskId": request_id,
            "status": status,
            "action": "saveAndClose",
            "isLocked": False,
            "isLockedButton": False,
            "translations": {
                "specifyingTimeSpent": "Списание трудозатрат",
                "specifyingTimeSpentText": "Укажите время, затраченное на выполнение задачи за текущий день",
                "timeSpentIsSaved": "Трудозатраты списаны",
                "comment": "Комментарий",
                "save": "Сохранить",
                "cancel": "Отменить",
                "time": "Время"
            },
            "condition_work": "((groups_idsHAS171034687395428925^ORgroups_idsHAS173822703391995789^ORgroups_idsISEMPTY)^category=type^nameNOTLIKEАРХИВ^state=active)",
            "currentAllTimeSpentInit": 0,
            "datetime": current_datetime,
            "one_typework": type_work,
            "display_name_typework": "По умолчанию",
            "headerTitle": "Быстрые ответы",
            "searchStringLabel": "Поиск",
            "favoriteHeaderTitle": "Избранное",
            "categoriesHeaderTitle": "Категории",
            "emptySearchResult": "Ничего не найдено",
            "tableID": "156950616617772294",
            "userID": user_id,
            "isVisibleMainButton": True,
            "default_store": {
                "quickResponses": [],
                "categories": [],
                "favoriteIds": []
            },
            "closure_notes_store": {
                "quickResponses": [],
                "categories": [],
                "favoriteIds": []
            },
            "isShow": True,
            "type_work": {
                "database_value": type_work,
                "display_value": "По умолчанию"
            },
            "isVisibleBackButton": False,
            "areVisibleFavorites": False,
            "condition_typework": "((groups_idsHAS171034687395428925^ORgroups_idsHAS173822703391995789^ORgroups_idsISEMPTY)^category=view^parentHAS173865532591825881^state=active)",
            "typework_count": 0,
            "open_typework": False,
            "view_work": {
                "database_value": "",
                "display_value": ""
            },
            "currentTimeSpent": time_spent_ms,
            "timeInt": str(time_spent_hours),
            "closingInfo": closure_text
        }
        
        response = self._make_request('POST', endpoint, request_data)
        return response.json()
    
    def close_itsm_request(
            self,
            request_id: str,
            closure_text: str = "",
            closure_code: str = "2",
            state: str = "7"
            ) -> Dict[str, Any]:
        """
        Закрытие ITSM заявки
        
        Args:
            request_id: ID заявки для закрытия
            closure_text: Текст для закрытия заявки (closure_notes)
            closure_code: Код закрытия (по умолчанию "2")
            state: Статус заявки при закрытии (по умолчанию "7" - закрыта)
            
        Returns:
            Ответ от API
        """
        endpoint = f"record/itsm_request/{request_id}?form_id=&form_view=Default&open_first_rel_list=0&is_service_portal=0"
        
        request_data = {
            "record": {
                "state": state,
                "closure_code": closure_code,
                "closure_notes": closure_text
            },
            "rem_attributes": []
        }
        
        response = self._make_request('POST', endpoint, request_data)
        return response.json()

