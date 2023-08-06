
# Yogendra/FizzBuzz Module

This is a simple demo module to understand python module publishing system.

This module uses

- Python 3.x
- Poetry
- Pytest

## Getting Started

1. Add library to your project

    ```bash
    pip install yogendra_fizzbuzz
    ```

1. Use in your program. Following is an example in repl:

    ```bash
    >>> from yogendra_fizzbuzz import fizzbuzz_to
    >>> print(fizzbuzz_to(16))
    [ '1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz', '16']
    ```

## How to build

1. Clone the project

    ```bash
    git clone https://github.com/yogendra/pypi-yogendra_fizzbuzz.git yogendra_fizzbuzz
    cd yogendra_fizzbuzz
    ```

1. Install dependencies

    ```bash
    poetry install 
    ```

1. Build project

    ```bash
    poetry build
    ```

1. (Optional) Publish to Test PyPI

    ```bash
    poetry publish -r testpypi
    ```

1. Publish to PyPI

    ```bash
    poetry publish
    ```
