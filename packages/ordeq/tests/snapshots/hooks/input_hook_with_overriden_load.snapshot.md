## Resource

```python
from dataclasses import dataclass

from ordeq import Input, InputHook, node, run
from ordeq_common import StringBuffer


@dataclass(frozen=True, kw_only=True)
class MyStringBuffer(StringBuffer):
    def load(self) -> str:
        print("Custom load called")
        return "Custom data: " + super().load()


class MyInputHook(InputHook[str]):
    def after_input_load(self, io: Input[str], data: str) -> None:
        print(f"Data loaded from '{io}' by hook: '{data}'")


hooked_input = MyStringBuffer("hello world").with_input_hooks(MyInputHook())


@node(inputs=[hooked_input])
def hello_world(input_data: str) -> str:
    print(f"Data loaded by node: '{input_data}'")


run(hello_world)

```

## Output

```text
Custom load called
Data loaded from 'MyStringBuffer(_buffer=<_io.StringIO object at HASH1>)' by hook: 'hello world'
Data loaded from 'MyStringBuffer(_buffer=<_io.StringIO object at HASH1>)' by hook: 'Custom data: hello world'
Data loaded by node: 'Custom data: hello world'

```

## Logging

```text
INFO	ordeq.io	Loading MyStringBuffer(_buffer=<_io.StringIO object at HASH1>)
INFO	ordeq.io	Loading MyStringBuffer(_buffer=<_io.StringIO object at HASH1>)
DEBUG	ordeq.io	Persisting data for MyStringBuffer(_buffer=<_io.StringIO object at HASH1>)
INFO	ordeq.runner	Running view 'hello_world' in module '__main__'
DEBUG	ordeq.io	Persisting data for IO(id=ID1)
DEBUG	ordeq.io	Unpersisting data for MyStringBuffer(_buffer=<_io.StringIO object at HASH1>)
DEBUG	ordeq.io	Unpersisting data for IO(id=ID1)

```

## Typing

```text
packages/ordeq/tests/resources/hooks/input_hook_with_overriden_load.py:19:31: error[too-many-positional-arguments] Too many positional arguments: expected 0, got 1
packages/ordeq/tests/resources/hooks/input_hook_with_overriden_load.py:23:37: error[invalid-return-type] Function always implicitly returns `None`, which is not assignable to return type `str`
Found 2 diagnostics

```