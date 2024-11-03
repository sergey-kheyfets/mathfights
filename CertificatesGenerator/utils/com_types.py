from typing import Callable, Protocol

class Cell(Protocol):
    Value: str

class WorkSheet(Protocol):
    Name: str
    def Activate(self) -> None: ...
    def Cells(self, row: int, col: int) -> Cell: ...

class WorkBook(Protocol):
    Sheets: list[WorkSheet]
    def Close(self, save: bool) -> None: ...

class Workbooks(Protocol):
    def Open(self, filepath: str) -> WorkBook: ...

class Worksheets(Protocol):
    def Activate(self, sheet_name: str) -> None: ...

class ExcelApp(Protocol):
    Workbooks: Workbooks
    Worksheets: Callable[[str], WorkSheet]
    ActiveSheet: WorkSheet
    Visible: bool
    def Quit(self) -> None: ...