import asyncio
import concurrent.futures
import time

def cpu_bound_task(name):
    print(f"{name}: Start heavy CPU work")
    count = 0
    for _ in range(10 ** 7):
        count += 1
    print(f"{name}: End heavy CPU work")
    return count

async def io_bound_task(name):
    print(f"{name}: Start I/O task")
    await asyncio.sleep(0.1)
    print(f"{name}: End I/O task")

async def main(executor):
    loop = asyncio.get_running_loop()

    # CPU 바운드 작업 2개 + I/O 바운드 작업 2개 실행
    tasks = [
        loop.run_in_executor(executor, cpu_bound_task, "CPU-1"),
        loop.run_in_executor(executor, cpu_bound_task, "CPU-2"),
        asyncio.create_task(io_bound_task("IO-1")),
        asyncio.create_task(io_bound_task("IO-2"))
    ]

    start = time.time()
    results = await asyncio.gather(*tasks)
    end = time.time()

    print(f"Results: {results}")
    print(f"Total time: {end - start:.2f} seconds")

if __name__ == "__main__":
    print("=== ThreadPoolExecutor ===")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        asyncio.run(main(executor))

    # print("\n=== ProcessPoolExecutor ===")
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     asyncio.run(main(executor))