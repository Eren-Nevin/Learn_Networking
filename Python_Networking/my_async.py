import asyncio


async def hello_world(second):
    # asyncio.sleep() always suspends the current task, allowing other tasks to run.
    await asyncio.sleep(second)
    print('Hello World')


async def run_parallel():
    # Tasks are used to schedule coroutines concurrently. Awaiting On A Tasks doesn't await until
    # its underlining coroutine is completed. It just does it in parallel. Tasks are wrappers
    # around coroutines.

    # Note that merely calling create_task would start the coroutine. The await keyword is only
    # for waiting for the coroutine to complete and get its return value either simple by
    # awaiting on it directly (await some_task) or using asyncio.gather

    async_task = asyncio.create_task(hello_world(1), name="A Task")
    async_task_2 = asyncio.create_task(hello_world(1), name="Another Task")
    await async_task
    await async_task_2


async def get_factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    print(result)
    return result


# If all awaitables are completed successfully, the result is an aggregate list of returned
# values. The order of result values corresponds to the order of awaitables in aws.

# If return_exceptions is False (default), the first raised exception is immediately propagated
# to the task that awaits on gather(). Other awaitables in the aws sequence won’t be cancelled
# and will continue to run.
# If return_exceptions is True, exceptions are treated the same as successful results,
# and aggregated in the result list.

# If gather() is cancelled, all submitted awaitables (that have not completed yet) are also
# cancelled.
# If any Task or Future from the aws sequence is cancelled, it is treated as if it raised
# CancelledError – the gather() call is not cancelled in this case. This is to prevent the
# cancellation of one submitted Task/Future to cause other Tasks/Futures to be cancelled.

async def run_parallel_right():
    small_computation = asyncio.create_task(get_factorial(5))
    medium_computation = asyncio.create_task(get_factorial(10))
    large_computation = asyncio.create_task(get_factorial(20))
    parallel_task = asyncio.gather(
        small_computation,
        medium_computation,
        large_computation
    )
    results = await parallel_task
    print(results)


async def run_serialized():
    await hello_world(1)
    await hello_world(1)


# Awaitables: Coroutines, Tasks, Futures
# Calling a coroutine (async func) without await won't run it at all, it just returns the coroutine
# object -> Warning


# A Future is a special low-level awaitable object that represents an eventual result of an
# asynchronous operation.
# When a Future object is awaited it means that the coroutine will wait until the Future is
# resolved in some other place.

# asyncio.run() always creates a new event loop and closes it at the end. It should
# be used as a main entry point for asyncio programs, and should ideally only be called once. No
# Thread Can have more than one of these running.


async def long():
    for i in range(10):
        print(i)
        await asyncio.sleep(1)
    return "DONE"


async def main():

    # long_task = asyncio.create_task(asyncio.shield(long()), name="LONG_TASK")
    await long()
    await asyncio.sleep(2)
    # Cancel A Task That Is Running Concurrently
    long_task.cancel()
    await asyncio.sleep(2)

asyncio.run(main())



# asyncio.run(run_parallel_right())
# Cancel Task
# long_task.cancel()
