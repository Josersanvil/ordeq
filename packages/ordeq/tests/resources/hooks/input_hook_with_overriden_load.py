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
