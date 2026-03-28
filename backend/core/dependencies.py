# Singleton using @lru_cache
from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from backend.services.printer_service import PrinterService


@lru_cache
def get_printer_service():
    return PrinterService()


PrinterDep = Annotated[PrinterService, Depends(get_printer_service)]
