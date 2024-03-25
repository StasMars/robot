import asyncio

async def robot(start_from=0, queue=None):
    count_value = start_from
    print('Добрый день, меня зовут Станислав и это мое тестовое задание для ИТ-стажировки Гринатом (Python разработчик RPA)')
    while True:
        print(count_value)
        count_value += 1
        await asyncio.sleep(1)
        if queue and not queue.empty():
            message = await queue.get()
            if message == "stop":
                print("Robot Stopped. Mission Complete :)")
                break