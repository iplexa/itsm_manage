from tasks import BaseTasks as bt
from models import Task
from datetime import date, datetime
from typing import List, Optional

def get_date(date_str: str) -> date:
    return datetime.strptime(date_str, '%d.%m.%Y').date()

tasks_st: List[Task] = [
    # *bt.get_iu_tasks('П/2 409', '30.01.2026 09:00-17:00', closure_date=get_date('01.02.2026')),
    # *bt.get_iu_tasks('П/2 409', '31.01.2026 09:00-17:00', closure_date=get_date('01.02.2026')),
    # *bt.get_rooms2(closure_date=get_date('03.02.2026')),
    # *bt.get_iu_tasks('П/2 409', '01.02.2026 09:00-17:00', closure_date=get_date('01.02.2026')),
    # *bt.get_iu_tasks('П/2 215', '01.02.2026 09:00-17:00', closure_date=get_date('01.02.2026')),
    # *bt.get_iu_tasks('П/2 310', '26.02.2026 19:00-22:00', closure_date=get_date('01.02.2026')),
    # *bt.get_iu_tasks('П/2 310', '27.02.2026 19:00-22:00', closure_date=get_date('01.02.2026')),
    # Task('Отключение оборудования REQ0279898', 'Отключение оборудования после завершения учебного процесса по REQ0279898', closure_date=get_date('02.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0285305 ', 'Отключение оборудования после завершения учебного процесса по REQ0285305', closure_date=get_date('02.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0285306', 'Отключение оборудования после завершения учебного процесса по REQ0285306', closure_date=get_date('02.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0286157', 'Отключение оборудования после завершения мероприятия по REQ0286157 (02.02.2026)', closure_date=get_date('02.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0286157', 'Отключение оборудования после завершения мероприятия по REQ0286157 (03.02.2026)', closure_date=get_date('03.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0286157', 'Отключение оборудования после завершения мероприятия по REQ0286157 (04.02.2026)', closure_date=get_date('04.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0286157', 'Отключение оборудования после завершения мероприятия по REQ0286157 (05.02.2026)', closure_date=get_date('05.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0286157', 'Отключение оборудования после завершения мероприятия по REQ0286157 (06.02.2026)', closure_date=get_date('06.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0286157', 'Отключение оборудования после завершения мероприятия по REQ0286157 (07.02.2026)', closure_date=get_date('07.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0279901', 'Отключение оборудования после завершения учебного процесса по REQ0279901', closure_date=get_date('03.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0285308', 'Отключение оборудования после завершения учебного процесса по REQ0285308', closure_date=get_date('03.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0286716', 'Отключение оборудования после завершения учебного процесса по REQ0286716', closure_date=get_date('03.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0279903', 'Отключение оборудования после завершения учебного процесса по REQ0279903', closure_date=get_date('04.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0285311', 'Отключение оборудования после завершения учебного процесса по REQ0285311', closure_date=get_date('04.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0279905', 'Отключение оборудования после завершения учебного процесса по REQ0279905', closure_date=get_date('05.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0285314', 'Отключение оборудования после завершения учебного процесса по REQ0285314', closure_date=get_date('05.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # *bt.get_iu_tasks('П/2 310', '05.02.2026 г. с 19:00 до 22:00', closure_date=get_date('05.02.2026')),
    # *bt.get_iu_tasks('П/2 305', '05.02.2026 г. с 19:00 до 22:00', closure_date=get_date('05.02.2026')),
    # *bt.get_iu_tasks('П/2 305', '07.02.2026 г. с 10:40 до 19:00', closure_date=get_date('07.02.2026')),
    # Task('Отключение оборудования REQ0279907', 'Отключение оборудования после завершения учебного процесса по REQ0279907', closure_date=get_date('06.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0280669', 'Отключение оборудования после завершения учебного процесса по REQ0280669', closure_date=get_date('06.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0283013', 'Отключение оборудования после завершения учебного процесса по REQ0283013', closure_date=get_date('06.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0285315', 'Отключение оборудования после завершения учебного процесса по REQ0285315', closure_date=get_date('06.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0286178', 'Отключение оборудования после завершения мероприятия по REQ0286178 (06.02.2026)', closure_date=get_date('06.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0286301', 'Отключение оборудования после завершения учебного процесса по REQ0286301', closure_date=get_date('06.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0288241', 'Отключение оборудования после завершения учебного процесса по REQ0288241', closure_date=get_date('06.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0289058', 'Отключение оборудования после завершения учебного процесса по REQ0289058', closure_date=get_date('06.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290137', 'Отключение оборудования после завершения учебного процесса по REQ0290137', closure_date=get_date('06.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290306', 'Отключение оборудования после завершения учебного процесса по REQ0290306', closure_date=get_date('06.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290307', 'Отключение оборудования после завершения учебного процесса по REQ0290307', closure_date=get_date('06.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # *bt.get_check_tasks(req_num='REQ0279910', closure_date=get_date('07.02.2026')),
    # *bt.get_check_tasks(req_num='REQ0283013', closure_date=get_date('07.02.2026')), 
    # *bt.get_check_tasks(req_num='REQ0285320 ', closure_date=get_date('07.02.2026')), 
    # *bt.get_check_tasks(req_num='REQ0286157 ', closure_date=get_date('07.02.2026')), 
    # *bt.get_check_tasks(req_num='REQ0286178 ', closure_date=get_date('07.02.2026')), 
    # *bt.get_check_tasks(req_num='REQ0288258 ', closure_date=get_date('07.02.2026')), 
    # *bt.get_check_tasks(req_num='REQ0290140  ', closure_date=get_date('07.02.2026')), 
    # *bt.get_check_tasks(req_num='REQ0290145  ', closure_date=get_date('07.02.2026')), 
    # *bt.get_check_tasks(req_num='REQ0290309  ', closure_date=get_date('07.02.2026')), 
    # *bt.get_check_tasks(req_num='REQ0290311  ', closure_date=get_date('07.02.2026')), 
    # Task('Отключение оборудования REQ0288259', 'Отключение оборудования после завершения учебного процесса по REQ0288259', closure_date=get_date('08.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290141', 'Отключение оборудования после завершения учебного процесса по REQ0290141', closure_date=get_date('08.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290146', 'Отключение оборудования после завершения учебного процесса по REQ0290146', closure_date=get_date('08.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290315', 'Отключение оборудования после завершения учебного процесса по REQ0290315', closure_date=get_date('08.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290316', 'Отключение оборудования после завершения учебного процесса по REQ0290316', closure_date=get_date('08.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0285322', 'Отключение оборудования после завершения учебного процесса по REQ0285322', closure_date=get_date('09.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290425', 'Отключение оборудования после завершения учебного процесса по REQ0290425', closure_date=get_date('09.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # *bt.get_iu_tasks('П/2 215', '10.02.2026 г. с 19:00 до 22:00', closure_date=get_date('10.02.2026')),
    # *bt.get_iu_tasks('П/2 215', '12.02.2026 г. с 19:00 до 22:00', closure_date=get_date('12.02.2026')),
    # *bt.get_iu_tasks('П/2 404', '14.02.2026 г. с 10:40 до 19:00', closure_date=get_date('14.02.2026')),
    # *bt.get_iu_tasks('П/2 305', '09.02.2026 г. с 19:00 до 22:00', closure_date=get_date('09.02.2026')),
    # *bt.get_iu_tasks('П/2 305', '11.02.2026 г. с 16:00 до 19:00', closure_date=get_date('11.02.2026')),
    # *bt.get_iu_tasks('П/2 310', '12.02.2026 г. с 19:00 до 22:00', closure_date=get_date('12.02.2026')),
    # *bt.get_iu_tasks('П/2 312', '14.02.2026 г. с 10:40 до 17:10', closure_date=get_date('14.02.2026')),
    # Task('Отключение оборудования REQ0285324', 'Отключение оборудования после завершения учебного процесса по REQ0285324', closure_date=get_date('10.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0289456', 'Отключение оборудования после завершения учебного процесса по REQ0289456', closure_date=get_date('10.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290505', 'Отключение оборудования после завершения учебного процесса по REQ0290505', closure_date=get_date('10.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290483', 'Отключение оборудования после завершения учебного процесса по REQ0290483', closure_date=get_date('10.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0285326', 'Отключение оборудования после завершения учебного процесса по REQ0285326', closure_date=get_date('11.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290483', 'Отключение оборудования после завершения учебного процесса по REQ0290483', closure_date=get_date('11.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0285327', 'Отключение оборудования после завершения учебного процесса по REQ0285327', closure_date=get_date('12.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290483', 'Отключение оборудования после завершения учебного процесса по REQ0290483', closure_date=get_date('12.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0288952', 'Отключение оборудования после завершения учебного процесса по REQ0288952', closure_date=get_date('12.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290167', 'Отключение оборудования после завершения учебного процесса по REQ0290167', closure_date=get_date('12.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290170', 'Отключение оборудования после завершения учебного процесса по REQ0290170', closure_date=get_date('12.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290171', 'Отключение оборудования после завершения учебного процесса по REQ0290171', closure_date=get_date('12.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290175', 'Отключение оборудования после завершения учебного процесса по REQ0290175', closure_date=get_date('12.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0290483 ', 'Отключение оборудования после завершения учебного процесса по REQ0290483 ', closure_date=get_date('12.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # Task('Отключение оборудования REQ0292384', 'Отключение оборудования после завершения учебного процесса по REQ0292384', closure_date=get_date('12.02.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    # *bt.get_check_tasks(req_num='REQ0274379 ', closure_date=get_date('14.02.2026')),
    # *bt.get_check_tasks(req_num='REQ0285330  ', closure_date=get_date('14.02.2026')),
    # *bt.get_check_tasks(req_num='REQ0290182  ', closure_date=get_date('14.02.2026')),
    # *bt.get_check_tasks(req_num='REQ0292184  ', closure_date=get_date('14.02.2026')),
    # *bt.get_check_tasks(req_num='REQ0292191  ', closure_date=get_date('14.02.2026')),
    # *bt.get_check_tasks(req_num='REQ0292255  ', closure_date=get_date('14.02.2026')),
    # *bt.get_check_tasks(req_num='REQ0292344  ', closure_date=get_date('14.02.2026')),
    # *bt.get_iu_tasks('П/2 404', '17.02.2026 г. с 19:00 до 22:00', closure_date=get_date('17.02.2026')),
    # *bt.get_iu_tasks('П/2 305', '19.02.2026 г. с 19:00 до 22:00', closure_date=get_date('19.02.2026')),
    # *bt.get_iu_tasks('П/2 409', '17.02.2026 г. с 19:00 до 22:00', closure_date=get_date('17.02.2026')),
    # *bt.get_iu_tasks('П/2 310', '21.02.2026 г. с 10:40 до 17:10', closure_date=get_date('21.02.2026')),

    # --- 02 ---
    Task('Замена лампы проектора П/2 406', 'Заменить лампу в проекторе в аудитории П/2 406, произвести настройку проектора.', closure_date=get_date('03.02.2026'), time_spent_minutes=75, closure_text='Лампа заменена.'),
    Task('Замена лампы проектора П/2 405', 'Заменить лампу в проекторе в аудитории П/2 405, произвести настройку проектора.', closure_date=get_date('03.02.2026'), time_spent_minutes=75, closure_text='Лампа заменена.'),
    Task('Замена батареек в микрофонах лофт 22', 'Заменить батарейки в микрофонах в лофте 22.', closure_date=get_date('03.02.2026'), time_spent_minutes=30, closure_text='Батарейки заменены.'),
    Task('Замена батареек в микрофонах П/2 210', 'Заменить батарейки в микрофонах в аудитории П/2 210.', closure_date=get_date('03.02.2026'), time_spent_minutes=30, closure_text='Батарейки заменены.'),
    *bt.get_iu_tasks('П/1 031', '03.03.2026 г. с 19:00 до 22:00', closure_date=get_date('03.03.2026')),
    *bt.get_iu_tasks('П/2 107', '05.03.2026 г. с 19:00 до 22:00', closure_date=get_date('05.03.2026')),
    *bt.get_rooms1(closure_date=get_date('03.03.2026')),
    *bt.get_rooms2(closure_date=get_date('05.03.2026')),
    Task('Подключение оборудования перед занятием по REQ0298832', 'Подключить оборудование перед занятием по REQ0298832', closure_date=get_date('05.03.2026'), time_spent_minutes=30, closure_text='Оборудование подключено.'),
    Task('Отключение оборудования после занятием по REQ0298832', 'Отключить оборудование после занятием по REQ0298832', closure_date=get_date('05.03.2026'), time_spent_minutes=30, closure_text='Оборудование отключено.'),
    Task('Сопровождение учебного процесса по REQ0298832', 'Сопровождение учебного процесса по REQ0298832', closure_date=get_date('05.03.2026'), time_spent_minutes=120, closure_text='Сопровождение проведено.'),
    *bt.get_check_tasks(req_num='REQ0300856', closure_date=get_date('05.03.2026')),
    Task('Подключение оборудования перед мероприятием по REQ0304822 ', 'Подключить оборудование перед мероприятием по REQ0304822 ', closure_date=get_date('05.03.2026'), time_spent_minutes=30, closure_text='Оборудование подключено.'),


    



    


    










    




]

tasks_emp = [
    # Task('Замена картриджа МФУ П/2 102', 'Заменить картридж в МФУ.', closure_date=get_date('04.12.2025'), time_spent_minutes=30, closure_text='Картридж заменен.'),
    # Task('Настройка принтера П/2 102','Подлключить, настроить принтер в офисе П/2 102. Подключить ПК сотрудников к принтеру.', closure_date=get_date('04.12.2025'), time_spent_minutes=30, closure_text='Принтер настроен.'),
    # *bt.get_modern_tasks('AK2020003097', closure_date=get_date('03.12.2025')),
    # *bt.get_modern_tasks('AK2020002924', closure_date=get_date('03.12.2025')),
    # *bt.get_modern_tasks('AK2020003096', closure_date=get_date('04.12.2025')),
    # *bt.get_modern_tasks('AK2020003098', closure_date=get_date('04.12.2025')),
    # *bt.get_modern_tasks('AK2019059723', closure_date=get_date('05.12.2025')),
    # *bt.get_modern_tasks('AK2019059711', closure_date=get_date('05.12.2025')),
]



tasks_dev = [
    # bt.get_vks(closure_date=get_date('03.02.2026')),
    # bt.get_vks(closure_date=get_date('05.02.2026')),   
    # bt.get_vks_sa(closure_date=get_date('05.02.2026')),
    # bt.get_vks(closure_date=get_date('10.02.2026')),
    # bt.get_vks(closure_date=get_date('12.02.2026')),   
    # bt.get_vks_sa(closure_date=get_date('12.02.2026')),
    # bt.get_vks(closure_date=get_date('14.02.2026')),
    # bt.get_vks(closure_date=get_date('19.02.2026')),   
    # bt.get_vks_sa(closure_date=get_date('19.02.2026')),
    # bt.get_vks(closure_date=get_date('24.02.2026')),
    # bt.get_vks(closure_date=get_date('26.02.2026')),   
    # bt.get_vks_sa(closure_date=get_date('26.02.2026')),
    # *bt.get_dev_tasks(closure_date=get_date('03.02.2026')),

    # *bt.get_dev_tasks(closure_date=get_date('05.02.2026')),
    # *bt.get_dev_tasks(closure_date=get_date('10.02.2026')),
    # *bt.get_dev_tasks(closure_date=get_date('12.02.2026')),
    # *bt.get_dev_tasks(closure_date=get_date('14.02.2026')),
    # *bt.get_dev_tasks(closure_date=get_date('17.02.2026')),
    # *bt.get_dev_tasks(closure_date=get_date('19.02.2026')),
    # *bt.get_dev_tasks(closure_date=get_date('21.02.2026')),
    # *bt.get_dev_tasks(closure_date=get_date('24.02.2026')),
    # *bt.get_dev_tasks(closure_date=get_date('26.02.2026')),

    # --- 02 ---

    *bt.get_dev_tasks(closure_date=get_date('02.03.2026')),
    *bt.get_dev_tasks(closure_date=get_date('04.03.2026')),


]

tasks_all = [
    tasks_st,
    tasks_dev,
    tasks_emp
]

if __name__ == "__main__":
    days = 21
    now_tsk = 47
    now_hrs = 67
    goal_tsk = days * 7 - now_tsk
    goal_hrs = days * 7 - now_hrs
    task_count = sum(len(tasks) for tasks in tasks_all)
    time_count_minutes = sum(task.time_spent_minutes for tasks in tasks_all for task in tasks)
    print(f"Всего задач: {task_count}")
    print(f"Всего трудозатрат: {time_count_minutes} минут ({time_count_minutes/60:.2f} часов)")
    print(f"Цель: {goal_tsk} задач, {goal_hrs} часов")
    print(f"Осталось до цели: {goal_tsk - task_count} задач, {(goal_hrs*60) - time_count_minutes} минут ({(goal_hrs*60 - time_count_minutes)/60:.2f} часов)")