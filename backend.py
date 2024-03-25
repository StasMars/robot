from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from robot import robot
import asyncio

app = FastAPI()
robot_queue = asyncio.Queue()

@app.get('/')
async def greeting():
    content = """
<body>
    <h2>Добрый день! Меня зовут Станислав</h2>
    <p>Это мое тестовое задание для ИТ-стажировки Гринатом (Python разработчик RPA)</p>
    <p><a href="http://127.0.0.1:8000/docs">Ссылка на Swagger UI</a></p>
</body>
    """
    return HTMLResponse(content=content)

async def start_robot(start_from: int):
    await robot(start_from, robot_queue)

@app.post("/start_robot/")
async def start_robot_endpoint(start_from: int = 0):
    asyncio.create_task(start_robot(start_from))  # Запуск асинхронной функции robot с указанным start_from
    return {"message": "Robot started"}

@app.post("/stop_robot/")
async def stop_robot_endpoint():
    robot_queue.put_nowait("stop")   # Помещаем сообщение "stop" в очередь
    return {"message": "Robot stopping"}