"""
    Пример использования конструкций asyncio/await.
    Каждую секунду в консоле печатаются целые числа (по порядку) от 0 до бесконечности,
    а на каждой секунде, кратной 3, выводится запись сколько прошло времени   
"""
import asyncio

async def print_nums():
    """ Подгенератор, который выполняет вывод чисел
        с инетервалом времени 1 секунда
    """
    num = 0
    while True:
        print(num)
        num += 1
        await asyncio.sleep(1)
async def print_time():
    """ Подгенератор, который выполняет вывод записи:
        "<time in seconds> seconds passed" каждую секунду, кратную 3
    """
    count = 0
    while True:
        if count % 3 == 0:
            print(f".... {count} seconds passed")
        count += 1
        await asyncio.sleep(1)

async def main():
    """Выполняет функции делегирующего генератора"""
    task1 = asyncio.create_task(print_time())
    task2 = asyncio.create_task(print_nums())
    await asyncio.gather(task1, task2)
    
if __name__ == "__main__":
    asyncio.run(main())
