
# Schedules - Create non-blocking scheduled tasks.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install schedules.

```bash
pip install schedules
```

## Usage

Here is a simple timer scheduled task example.

After 1 hour, 30 minutes and 10 seconds `task` will execute.

```python
import schedules

# example task

def task(argument):
    print(argument)

# initialize a timer

timer = schedules.timer()

# Start the timer.

# "repeat=True" means the task not execute only once,
# it will execute every 3 days, 1 hour, 30 minutes and 10 seconds infinite times.

timer.day(3).hour(1).minute(30).second(10).start(target=task, args=("Example",), repeat=True)

# NOTE:
# Because this package is non-blocking, the thread will continue.
# If the main thread is done executing all it's code, the program will exit.
# add the following code to prevent that:
while True:
    pass
```

If you don't want the task to execute at a certain time, you can use `every`.

Every time the minutes are 0 (every new hour), `task` will execute.

```python
import schedules

# example task

def task(argument):
    print(argument)

# initialize "every"

every = schedules.every()

# Start the timer.

# "repeat=True" means the task not execute only once,
# it will execute every time the minutes are 0 (every new hour) infinite times.

every.minute(0).start(target=task, args=("Example",), repeat=True)

# This code will execute the task at 2:30pm and 10 seconds everyday:

every.hour(14).minute(30).second(10).start(target=task, args=("Example",), repeat=True)

# NOTE:
# Because this package is non-blocking, the thread will continue.
# If the main thread is done executing all it's code, the program will exit.
# add the following code to prevent that:
while True:
    pass
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)