from enum import IntEnum
from typing import Callable, Literal, Protocol

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

class WdFindWrap(IntEnum):
    wdFindStop = 0
    wdFindContinue 	= 1
    wdFindAsk = 2

class WdReplace(IntEnum):
    wdReplaceNone = 0
    wdReplaceOne = 1
    wdReplaceAll = 2

class Find(Protocol):
    def Execute(
        self,
        FindText: str,
        MatchCase: bool = False,
        MatchWholeWord: bool = False,
        MatchWildcards: bool = False,
        MatchSoundsLike: bool = False,
        MatchAllWordForms: bool = False,
        Forward: bool = False,
        Wrap: WdFindWrap = WdFindWrap.wdFindStop,
        Format: bool = False,
        ReplaceWith: str = '',
        Replace: WdReplace = WdReplace.wdReplaceOne,
        MatchKashida: bool = False,
        MatchDiacritics: bool = False,
        MatchAlefHamza: bool = False,
        MatchControl: bool = False,
        MatchPrefix: bool = False,
        MatchSuffix: bool = False,
        MatchPhrase: bool = False,
        IgnoreSpace: bool = False,
        IgnorePunct: bool = False
    ) -> None: ...

class Range(Protocol):
    Find: Find

class WdFileFormat(IntEnum):
    wdFormatDocumentDefault = 16
    wdFormatPDF = 17

class WdSaveOptions(IntEnum):
    wdSaveChanges = -1
    wdPromptToSaveChanges = -2
    wdDoNotSaveChanges =  0

class Document(Protocol):
    Content: Range
    def SaveAs(self, filepath: str, FileFormat: WdFileFormat) -> None: ...
    def Close(self, SaveChanges: WdSaveOptions) -> None: ...

class Documents(Protocol):
    def Open(self, filepath: str) -> Document: ...

class WordApp(Protocol):
    Documents: Documents
    def Quit(self) -> None: ...