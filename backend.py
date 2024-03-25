import sqlite3
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from robot import robot
import asyncio

app = FastAPI(
    title="Добрый день! Меня зовут Станислав",
    summary="Это мое тестовое задание для ИТ-стажировки Гринатом (Python разработчик RPA)",
    license_info={
        "name": "Главная страница",
        "url": "http://127.0.0.1:8000"
    },
)
robot_queue = asyncio.Queue()


# Подключение к БД
conn = sqlite3.connect('robot_data.db') 
c = conn.cursor()

# Создание таблицы в БД
c.execute('''CREATE TABLE IF NOT EXISTS robot_runs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT,
            duration INTEGER,
            start_from INTEGER
            )'''
        )

# Функция для записи информации о запуске робота в базу данных
def log_robot_run(start_time, duration, start_from):
    c.execute("INSERT INTO robot_runs (start_time, duration, start_from) VALUES (?, ?, ?)",
              (start_time, duration, start_from))
    conn.commit()



#Главная страница
@app.get('/', tags=["Приветствие"])
async def greeting():
    html_file_path = Path(__file__).parent / 'templates/index.html'  # Путь к файлу HTML
    return FileResponse(html_file_path)


async def start_robot(start_from: int):
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await robot(start_from, robot_queue)
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    duration = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    log_robot_run(start_time, duration.total_seconds(), start_from)


# Запуск робота (Запуск асинхронной функции robot с указанным start_from)
@app.post("/start_robot/", tags=["Работа с роботом"], summary="Запуск робота")
async def start_robot_endpoint(start_from: int = 0):
    """
    Запускает робота с того числа, которое необходимо ввести ниже.\n
    После запуска просмотрите строку вывода в вашем IDE. Спасибо.
    """
    asyncio.create_task(start_robot(start_from))  
    return {"message": "Robot started"}


# Остановка робота (Помещаем сообщение "stop" в очередь)
@app.post("/stop_robot/", tags=["Работа с роботом"], summary="Остановка робота")
async def stop_robot_endpoint(): 
    """
    Останавливает робота.\n
    После остановки просмотрите строку вывода в вашем IDE еще раз. Спасибо.
    """
    robot_queue.put_nowait("stop")   
    return {"message": "Robot stopping"}


# Вывод информации о запусках робота
@app.get("/robot_runs/", tags=["Информация о запусках робота"], summary="Получение информации о запусках робота")
async def get_robot_runs(): # Вывод информации о запусках робота
    """
    Выводит информацию о всех запусках робота.\n
    Нажмите кнопку Execute для получения подробной информации. Спасибо.
    """
    c.execute("SELECT * FROM robot_runs")
    runs = c.fetchall()
    return {"robot_runs": runs}