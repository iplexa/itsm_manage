from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Tuple
from datetime import date, datetime


@dataclass
class Task:
    name: str
    desc: str
    time_spent_minutes: int = 0  # Время в минутах (будет конвертировано в часы)
    closure_text: str = ""  # Текст для закрытия заявки
    closure_date: Optional[date] = None  # Дата закрытия заявки (опционально, если указана - время закрытия 13:00)


class TaskType(Enum):
    DEV = 'Разработка'
    EDU = 'Сопровождение обучения'
    EMP = 'ПК сотрудника'


@dataclass
class Service:
    level: int
    id: str
    name: str
    parent: Optional['Service'] = field(default=None, repr=False)


class Services(Enum):
    # Услуги для сотрудников (иерархия)
    EMPLOYE_SERVICE = Service(
        level=1,
        id='174283069691576051',
        name='Сопровождение сервисов сотрудника',
        parent=None,
    )
    EMPLOYE_ACCOUNT = Service(
        level=2,
        id='171827434296827078',
        name='Учетная запись (УЗ) сотрудников',
        parent=None,  # Будет установлен после создания
    )
    EMPLOYE_ACCOUNT_RESET = Service(
        level=3,
        id='171834970892408003',
        name='Сброс пароля УЗ',
        parent=None,  # Будет установлен после создания
    )
    EMPLOYE_MAINTENANCE = Service(
        level=2,
        id='171827435390586219',
        name='Обслуживание техники на рабочих местах (ПК)',
        parent=None,  # Будет установлен после создания
    )
    EMPLOYE_MAINTENANCE_PC = Service(
        level=3,
        id='171834970892408136',
        name='Обслуживание ПК',
        parent=None,  # Будет установлен после создания
    )
    EMPLOYE_MAINTENANCE_PC_REPAIR = Service(
        level=4,
        id='171835197993241692',
        name='Восстановление работоспособности ПК',
        parent=None,  # Будет установлен после создания
    )
    EMPLOYE_PRINT = Service(
        level=3,
        id='174283120990205435',
        name='Устройство печати и сканирования',
        parent=None,  # Будет установлен после создания
    )
    EMPLOYE_PRINT_REPL = Service(
        level=4,
        id='174288745591658729',
        name='Замена расходных материалов',
        parent=None,  # Будет установлен после создания
    )
    EMPLOYE_PRINT_INST = Service(
        level=4,
        id='174288745591658729',
        name='Подключение/настройка/отключение оборудования',
        parent=None,  # Будет установлен после создания
    )

    # Услуги для обучения (иерархия)
    EDU = Service(
        level=1,
        id='174291345197423243',
        name='Сопровождение мероприятий и учебного процесса',
        parent=None,
    )
    EDU_SERVICE = Service(
        level=2,
        id='173979049797789044',
        name='Сопровождение учебного процесса',
        parent=None,  # Будет установлен после создания
    )
    EDU_MAINTENANCE = Service(
        level=3,
        id='174288904894201605',
        name='Сопровождение учебного процесса',
        parent=None,  # Будет установлен после создания
    )


# Устанавливаем иерархию родитель-ребенок для сервисов
def _setup_services_hierarchy():
    """Устанавливает иерархию родитель-ребенок для сервисов"""
    # Услуги для сотрудников
    Services.EMPLOYE_ACCOUNT.value.parent = Services.EMPLOYE_SERVICE.value
    Services.EMPLOYE_ACCOUNT_RESET.value.parent = Services.EMPLOYE_ACCOUNT.value
    Services.EMPLOYE_MAINTENANCE.value.parent = Services.EMPLOYE_SERVICE.value
    Services.EMPLOYE_MAINTENANCE_PC.value.parent = Services.EMPLOYE_MAINTENANCE.value
    Services.EMPLOYE_MAINTENANCE_PC_REPAIR.value.parent = Services.EMPLOYE_MAINTENANCE_PC.value
    Services.EMPLOYE_PRINT.value.parent = Services.EMPLOYE_SERVICE.value
    Services.EMPLOYE_PRINT_REPL.value.parent = Services.EMPLOYE_PRINT.value
    Services.EMPLOYE_PRINT_INST.value.parent = Services.EMPLOYE_PRINT.value
    # Услуги для обучения
    Services.EDU_SERVICE.value.parent = Services.EDU.value
    Services.EDU_MAINTENANCE.value.parent = Services.EDU_SERVICE.value


# Инициализируем иерархию при импорте модуля
_setup_services_hierarchy()


class HelpServices:
    """Класс для работы с иерархией сервисов"""
    
    @staticmethod
    def get_service_chain(service: Service) -> List[Service]:
        """
        Возвращает цепочку сервисов от текущего до корня (первого родителя)
        
        Args:
            service: Начальный сервис
            
        Returns:
            Список сервисов от корня до текущего (от level 1 до текущего уровня)
        """
        chain = []
        current = service
        
        # Собираем цепочку от текущего до корня
        while current is not None:
            chain.append(current)
            current = current.parent
        
        # Разворачиваем, чтобы получить от корня до текущего
        chain.reverse()
        return chain
    
    @staticmethod
    def get_service_dict(service: Service) -> dict:
        """
        Возвращает словарь с ID и названиями сервисов для удобной подстановки в запрос
        
        Args:
            service: Начальный сервис
            
        Returns:
            Словарь с полями:
            - service: ID сервиса 1-го уровня
            - service_2nd_level: ID сервиса 2-го уровня (если есть)
            - service_3rd_level: ID сервиса 3-го уровня (если есть)
            - service_4th_level: ID сервиса 4-го уровня (если есть)
            - basic_service: строка с названиями всех сервисов через точку
        """
        chain = HelpServices.get_service_chain(service)
        
        result = {
            'service': '',
            'service_2nd_level': '',
            'service_3rd_level': '',
            'service_4th_level': '',
            'basic_service': ''
        }
        
        # Заполняем ID сервисов по уровням
        service_names = []
        for svc in chain:
            if svc.level == 1:
                result['service'] = svc.id
            elif svc.level == 2:
                result['service_2nd_level'] = svc.id
            elif svc.level == 3:
                result['service_3rd_level'] = svc.id
            elif svc.level == 4:
                result['service_4th_level'] = svc.id
            
            service_names.append(svc.name)
        
        # Формируем строку с названиями
        result['basic_service'] = '. '.join(service_names) + '.'
        
        return result

