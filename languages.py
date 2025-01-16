from dataclasses import dataclass
from enum import Enum, EnumMeta
from typing import cast


@dataclass(frozen=True)
class Language:
    name: str
    file_extension: str

    @property
    def http(self) -> str:
        return f"http://{self.name}:8000"

    @property
    def script(self) -> str:
        return f"{self.name}-runner.sh"


class LanguagesMeta(EnumMeta):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls._initialize()  # type: ignore[attr-defined]


class Languages(Enum, metaclass=LanguagesMeta):
    BASH = Language("bash", ".sh")
    BRAINFUCK = Language("brainfuck", ".bf")
    C = Language("c", ".c")
    CSHARP = Language("csharp", ".csproj")  # C#
    CPP = Language("cpp", ".cpp")
    ELIXIR = Language("elixir", ".ex")
    GO = Language("go", ".go")
    HASKELL = Language("haskell", ".hs")
    JAVA = Language("java", ".java")
    JAVASCRIPT = Language("javascript", ".js")
    LISP = Language("lisp", ".lisp")
    LLVM = Language("llvm", ".ll")
    MATLAB = Language("matlab", ".m")
    PYTHON = Language("python", ".py")
    QBE = Language("qbe", ".ssa")
    RUST = Language("rust", ".rs")
    SCHEME = Language("scheme", ".scm")
    SQL = Language("sql", ".sql")
    ASM = Language("asm", ".s")

    __language_names: set[str] = set()
    __name_lookup: dict[str, Language] = {}

    @classmethod
    def _initialize(cls):
        cls.__language_names = {lang.value.name for lang in cls}
        cls.__name_lookup = cast(
            dict[str, Language], {lang.value.name: lang for lang in cls}
        )

    @classmethod
    def is_supported(cls, language: str) -> bool:
        return language in cls.__language_names

    @classmethod
    def get_by_name(cls, language: str) -> Language:
        print(cls.__name_lookup)
        return cls.__name_lookup[language]
