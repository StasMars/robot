from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
from robot import robot
import asyncio

app = FastAPI(
    title="Добрый день! Меня зовут Станислав",
    summary="Это мое тестовое задание для ИТ-стажировки Гринатом (Python разработчик RPA)"
)
robot_queue = asyncio.Queue()

@app.get('/', tags=["Приветствие"])
async def greeting():
    html_file_path = Path(__file__).parent / 'index.html'  # Путь к файлу HTML
    return FileResponse(html_file_path)


async def start_robot(start_from: int):
    await robot(start_from, robot_queue)


@app.post("/start_robot/", tags=["Работа с роботом"], summary="Запуск робота")
async def start_robot_endpoint(start_from: int = 0): # Запуск робота (Запуск асинхронной функции robot с указанным start_from)
    """
    Запускает робота с того числа, которое необходимо ввести ниже.\n
    После запуска просмотрите строку вывода в вашем IDE. Спасибо.
    """
    asyncio.create_task(start_robot(start_from))  
    return {"message": "Robot started"}


@app.post("/stop_robot/", tags=["Работа с роботом"], summary="Остановка робота")
async def stop_robot_endpoint(): # Остановка робота (Помещаем сообщение "stop" в очередь)
    """
    Останавливает робота.\n
    После остановки просмотрите строку вывода в вашем IDE еще раз. Спасибо.
    """
    robot_queue.put_nowait("stop")   
    return {"message": "Robot stopping"}