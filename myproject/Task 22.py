# Task 1
import asyncio
from datetime import datetime
from importlib.metadata import files
from os import times
from random import random
from time import sleep
import random


async def first():
    start = datetime.now()
    print(f"First Function start: {start}")
    await asyncio.sleep(2)
    end = datetime.now()
    print(f"First Function end: {end}")


async def second():
    start = datetime.now()
    print(f"Second Function start: {start}")
    await asyncio.sleep(5)
    end = datetime.now()
    print(f"Second Function end: {end}")


async def main():
    first_ = asyncio.create_task(first())
    second_ = asyncio.create_task(second())
    await  first_
    await second_


asyncio.run(main())


# Task 2

async def rand():
    rand_time = random.randint(1, 4)
    start = datetime.now()
    await asyncio.sleep(rand_time)
    for i in range(1, 11):
        print(i)
    end = datetime.now()
    print(f"Delay time: {end - start}")


async def main_():
    rand_ = asyncio.create_task(rand())
    await rand_


asyncio.run(main_())


# Task 3

async def iseven(a):
    return a % 2 == 0


async def square(a):
    num = await iseven(a)
    if num:
        return a ** 2
    else:
        return None


async def main():
    list_ = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    numbers = []
    for i in list_:
        numbers.append(square(i))
    final = await  asyncio.gather(*numbers)

    for i in final:
        print(i)

asyncio.run(main())

#Task 4

async def write_to_file(file,txt):
    start=datetime.now()
    print(f"Start time for {file}: {start}")
    await asyncio.sleep(2)
    with open ("file.txt", "w") as f:
        f.write(txt)
    end = datetime.now()
    print(f"End time for {file}: {end}")

async def main():
    file1=write_to_file("f1.txt",'hello')
    file2 = write_to_file("f2.txt", 'World')
    file3 = write_to_file("f3.txt", 'Bye')

    lis=[file1,file2,file3]
    await asyncio.gather(*lis)

asyncio.run(main())
