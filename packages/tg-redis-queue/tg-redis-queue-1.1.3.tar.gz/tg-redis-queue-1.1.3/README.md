# Thorgate :: Redis Queue

Redis queue, that can be easily used to store json-compatible dictionaries and is aimed to be race-condition proof.

## Installation

To use the synchronous version:

```shell
python3 -m pip install tg-redis-queue[synchronous]
```

To use asynchronous version:
```shell
python3 -m pip install tg-redis-queue[asyncio]
```

## Example usage

```python
from tg_redis_queue.sync_redis_queue import RedisObjectQueue


class MyRedisObjectQueue(RedisObjectQueue):
    # Default expiry time is 60 seconds, set it to 5 minutes for example purposes
    # so that queue doesn't expire while we're playing around with it.
    #
    # It is possible to set this to None as well, then queue will never expire and 
    # you are responsible for cleaning it up with `.prune()`
    EXPIRY_TIME = 300
    
    def _get_redis_url(self):
        # Can alternatively use base RedisObjectQueue and provide 
        # redis_url to constructor, like 
        # RedisObjectQueue(name="test", redis_url="redis://localhost:6379")
        return "redis://localhost:6379"


# Add items to the queue
queue = MyRedisObjectQueue(name='example_que')
queue.add({'key': 1})
queue.add({'key': 2})
queue.add({'key': 3})
queue.add({'key': 4})
queue.add({'key': 5})

# Can be in separate thread or process
queue = MyRedisObjectQueue(name='example_que')
# Get items with offset 0, 1 and 2
items = queue.get_items(end=2)
print([item.data for item in items])
# [{'key': 1}, {'key': 2}, {'key': 3}]

print(queue.remove(items))
# 3 - number of items removed

# Can use pop as well
item = queue.pop()
print(item.data)
# {'key': 4}

print(queue.get_total_size())
# 1 - only {'key': 5} is left

# Can prune all the data
queue.prune()
print(queue.get_total_size())
# 0 - nothing left
```

It is possible to use it the queue with async redis (with use of aioredis package).

```python
import asyncio

from tg_redis_queue.async_redis_que import AsyncRedisObjectQueue

async def enqueue_data():
    queue = await AsyncRedisObjectQueue.create(
        name="my_queue",
        redis_url="redis://localhost:6379",
    )
    
    await asyncio.gather(
        queue.add({"id": 1}),
        queue.add({"id": 2}),
        queue.add({"id": 3}),
        queue.add({"id": 4}),
        queue.add({"id": 5}),
    )
    
    await queue.cleanup_connection()
    
async def consume_queue_data():
    queue = await AsyncRedisObjectQueue.create(
        name="my_queue",
        redis_url="redis://localhost:6379",
    )
    
    print(await queue.pop())

    await queue.cleanup_connection()

loop = asyncio.get_event_loop()
loop.run_until_complete(enqueue_data())
# Queue now has 5 items

loop.run_until_complete(consume_queue_data())
# Prints first item in the queue
```

It is possible to manually set the key for queue items. Items with the same key
can only exist in the queue once, and if an item is added to the queue again with
the same key, item data will be updated but item score (position in the queue)
will be preserved - this way you can update the item in the queue without resetting
it's queue position:

```python
from tg_redis_queue.sync_redis_queue import RedisObjectQueue
from tg_redis_queue import RedisQueItem

queue = RedisObjectQueue(name="my-queue", redis_url="redis://localhost:6379")

# Add item with explicit key to the queue
queue.add(
    RedisQueItem(
        key=f"item-1",
        data={"id": 1, "message": "test"},
    )
)

# Queue now: ["item-1"]

queue.add(
    RedisQueItem(
        key=f"item-2",
        data={"id": 2, "message": "test"},
    )
)
# Queue now: ["item-1", "item-2"]

queue.add(
    RedisQueItem(
        key=f"item-1",
        data={"id": 42, "message": "test again"},
    )
)
# Queue ordering is unchanged: ["item-1", "item-2"]

item = queue.pop()
# Data is updated
assert item.data == {"id": 42, "message": "test again"}
```

## Authors

This package is developed and maintained by [Thorgate](https://thorgate.eu) as 
part of our effort to change the world with the power of technology. 

See our other projects:
* https://github.com/thorgate
* https://gitlab.com/thorgate-public

## Contributing

To start development, clone the repository and run `make setup`. It expects you to 
have python3.8 and poetry installed.

You will need to set `REDIS_URL` environment variable to run the tests:

```shell
export REDIS_URL=redis://localhost:6379
```

The easiest way to run redis is to run it with Docker:
```shell
docker run --name my-redis-container -p 6379:6379 -d redis
```

Code-formatters are available to make the code more readable and uniform, as well as 
linters to make sure the code is good quality. See Makefile for details. 

The following command will re-format the code
```shell
make black-format-all isort-fix
```

The following command will check the code with linters and tests
```shell
make quality coverage
```

For testing in different environments, tox is used. For convenience, tox is ran in
gitlab pipeline.

Please make sure your commit passes all the checks before opening a merge request.

Please consider adding yourself to authors in `pyptoject.toml` if your contribution
is beyond trivial changes.
