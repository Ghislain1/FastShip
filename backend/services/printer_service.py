#  passlib[bcrypt] must be installed
from rich import print
import inspect


class PrinterService:
    def print_info(self, context, msg):
        print(f"[bold green][{context}]> {msg}[/]")

    def print_error(self, context, msg):
        print(f"[bold red][{context}]> {msg}[/]")

    def print_debug(self, msg: str) -> None:
        frame = inspect.currentframe().f_back
        file = frame.f_code.co_filename
        line = frame.f_lineno
        print(f"\n[yellow]{file}:{line} {msg} [/]\n")
