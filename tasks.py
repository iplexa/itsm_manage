from typing import List, Optional
from datetime import date
from models import Task


class BaseTasks:

    @classmethod
    def get_vks(cls, closure_date: Optional[date] = None) -> Task:
        """
        Получить задачу ВКС этапы автоматизации сброса паролей сотрудников
        
        Args:
            closure_date: Опциональная дата закрытия заявки (если указана, время будет 13:00)
        """
        return Task('ВКС этапы автоматизации сброса паролей сотрудников', 'посещение ВКС', closure_date=closure_date, time_spent_minutes=30, closure_text='ВКС посещено')
    
    @classmethod
    def get_vks_sa(cls, closure_date: Optional[date] = None) -> Task:
        """
        Получить задачу ВКС автомаизация сброса паролей сотрудников
        
        Args:
            closure_date: Опциональная дата закрытия заявки (если указана, время будет 13:00)
        """
        return Task('ВКС автомаизация сброса паролей сотрудников', 'посещение ВКС', closure_date=closure_date, time_spent_minutes=60, closure_text='ВКС посещено')

    @classmethod
    def get_rooms2(cls, closure_date: Optional[date] = None) -> List[Task]:
        """
        Получить список задач по регламентным работам для П/2
        
        Args:
            closure_date: Опциональная дата закрытия заявок (если указана, время будет 13:00)
        """
        return [
            Task("Регламентные работы", "Совершить обход всех аудиторий П/2 1,2 этаж", closure_date=closure_date, time_spent_minutes=60, closure_text='Обход произведён.'),
            Task("Регламентные работы", "Совершить обход всех аудиторий П/2 3 этаж", closure_date=closure_date, time_spent_minutes=60, closure_text='Обход произведён.'),
            Task("Регламентные работы", "Совершить обход всех аудиторий П/2 4 этаж", closure_date=closure_date, time_spent_minutes=60, closure_text='Обход произведён.'),
        ]
    
    @classmethod
    def get_rooms1(cls, closure_date: Optional[date] = None) -> List[Task]:
        """
        Получить список задач по регламентным работам для П/1
        
        Args:
            closure_date: Опциональная дата закрытия заявок (если указана, время будет 13:00)
        """
        return [
            Task("Регламентные работы", "Совершить обход всех аудиторий П/1 1,2 этаж", closure_date=closure_date, time_spent_minutes=60, closure_text='Обход произведён.'),
            Task("Регламентные работы", "Совершить обход всех аудиторий П/1 3 этаж", closure_date=closure_date, time_spent_minutes=60, closure_text='Обход произведён.'),
            Task("Регламентные работы", "Совершить обход всех аудиторий П/1 4 этаж", closure_date=closure_date, time_spent_minutes=60, closure_text='Обход произведён.'),
        ]

    @classmethod
    def get_modern_tasks(cls, inv_num: str, closure_date: Optional[date] = None):
        """
        Получить список задач по модернизации моноблока
        
        Args:
            inv_num: Инвентарный номер моноблока
            closure_date: Опциональная дата закрытия заявок (если указана, время будет 13:00)
        """
        modern_tasks = [
            Task('Подготовка моноблока к модернизации',f'Подготовить моноблок {inv_num} к модернизации: собрать данные у пользователя, сжать раздел диска C до 500гб. Транспортировать моноблок в кабинет для последющей модернизаци.', closure_date=closure_date, time_spent_minutes=30, closure_text='Моноблок подготовлен к модернизации.'),
            Task('Модернизация моноблока, замена диска',f'Провести модернизацию моноблока {inv_num}. Установить M2 SSD накопитель.', closure_date=closure_date, time_spent_minutes=30, closure_text='Моноблок модернизирован.'),
            Task('Провести клонирование системы моноблока после модернизации',f'Клонировать раздел и все файлы старого накопителя на новый. Настроить и подготовить моноблок {inv_num} к использованию после замены (обновить драйвера, выставить порядок загрузки в BIOS). Демонтировать старый накопитель из моноблока после установки.', closure_date=closure_date, time_spent_minutes=60, closure_text='Моноблок клонирован.'),
            Task('Установка моноблока после модернизации',f'Установить моноблок {inv_num} в кабинет. Проинформировать пользователя о проведенных работах и возможных ошибках. Подключить, проверить работоспособность.', closure_date=closure_date, time_spent_minutes=30, closure_text='Моноблок установлен.')
        ]
        return modern_tasks  
    
    @classmethod
    def get_mount_tasks(cls, req_num: str, closure_date: Optional[date] = None):
        """
        Получить список задач по подключению/отключению оборудования
        
        Args:
            req_num: Номер заявки
            closure_date: Опциональная дата закрытия заявок (если указана, время будет 13:00)
        """
        mount_tasks = [
            Task(f'Подключение оборудование {req_num}',f'Подключить оборудование, подготовить к занятию по {req_num}', closure_date=closure_date, time_spent_minutes=30, closure_text='Оборудование подключено.'),
            Task(f'Отключение оборудование {req_num}',f'Отключить оборудование после завершения занятия по {req_num}', closure_date=closure_date, time_spent_minutes=30, closure_text='Оборудование отключено.'),
        ]
        return mount_tasks
    
    @classmethod
    def get_edu_tasks(cls, place: str, datetime: str, closure_date: Optional[date] = None):
        """
        Получить список задач по сопровождению учебного процесса
        
        Args:
            closure_date: Опциональная дата закрытия заявок (если указана, время будет 13:00)
        """
        edu_tasks = [
            Task('Сопровождение учебного процесса',f'Оказать сопровождение учебного процесса {place} {datetime}', closure_date=closure_date, time_spent_minutes=60, closure_text='Сопровождение проведено.'),
        ]
        return edu_tasks

    @classmethod
    def get_iu_tasks(cls, place: str, datetime: str, closure_date: Optional[date] = None):
        """
        Получить список задач по сопровождению учебного процесса ИУ
        
        Args:
            place: Корпус, аудитория            
            datetime: Дата и время учебного процесса
            closure_date: Опциональная дата закрытия заявок (если указана, время будет 13:00)
        """
        iu_tasks = [
            Task('Установка оборудования для проведения учебного процесса', f'Установить оборудование для проведения учебного процесса {place} {datetime}', closure_date=closure_date, time_spent_minutes=30, closure_text='Оборудование установлено.'),
            cls.get_edu_tasks(place, datetime, closure_date=closure_date)[0],
            Task('Демонтаж оборудования после учебного процесса', f'Демонтировать оборудование после завершения учебного процесса {place} {datetime}', closure_date=closure_date, time_spent_minutes=30, closure_text='Оборудование демонтировано.'),

        ]

        return iu_tasks
    
    @classmethod
    def get_check_tasks(cls, req_num: str, closure_date: Optional[date] = None):
        """
        Получить список задач по проверке оборудования
        
        Args:
            closure_date: Опциональная дата закрытия заявок (если указана, время будет 13:00)
        """
        check_tasks = [
            Task(f'Проверка оборудования {req_num}',f'Проверить работоспособность оборудования по {req_num} перед началом занятия', closure_date=closure_date, time_spent_minutes=30, closure_text='Оборудование проверено.'),
            Task(f'Отключение оборудование {req_num}',f'Отключить оборудование после завершения занятия по {req_num}', closure_date=closure_date, time_spent_minutes=30, closure_text='Оборудование отключено.'),
        ]
        return check_tasks
    
    @classmethod
    def get_dev_tasks(cls, closure_date: Optional[date] = None) -> List[Task]:
        """
        Получить список задач по разработке
        
        Args:
            closure_date: Опциональная дата закрытия заявок (если указана, время будет 13:00)
        """
        return [
            Task(f'Работы по разработке, поддержки, внедрению системы по автоматизации сброса паролей ({closure_date.strftime("%d/%m/%Y")}) ', 'Провести необходимые ежедневные работы по системе автоматизации сброса паролей сотрудников', closure_date=closure_date, time_spent_minutes=120, closure_text='Работы проведены.'),
        ]

