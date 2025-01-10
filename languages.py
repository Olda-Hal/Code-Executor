from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Language:
    name: str
    file_extension: str

    @property
    def image(self) -> str:
        return f"code-executor-{self.name}"


class Languages(Enum):
    ASM = Language("asm", ".s")
    BASH = Language("bash", ".sh")
    BRAINFUCK = Language("brainfuck", ".bf")
    C = Language("c", ".c")
    CSHARP = Language("csharp", ".cs")  # C#
    CPP = Language("cpp", ".cpp")
    GO = Language("go", ".go")
    HASKELL = Language("haskell", ".hs")
    JAVA = Language("java", ".java")
    JAVASCRIPT = Language("javascript", ".js")
    LLVM = Language("llvm", ".ll")
    MATLAB = Language("matlab", ".m")
    PYTHON = Language("python", ".py")
    QBE = Language("qbe", ".ssa")
    RUST = Language("rust", ".rs")

    __supported_languages: set[str] = set()
    __name_lookup: dict[str, Language] = {}

    def __init__(self, *args):
        cls = self.__class__
        if not cls.__supported_languages:
            cls.__supported_languages = {lang.value.name for lang in cls}

        if not cls.__name_lookup:
            cls.__name_lookup = {lang.value.name: lang.value for lang in cls}

        super().__init__()

    @classmethod
    def is_supported(cls, language: str) -> bool:
        return language in cls.__supported_languages

    @classmethod
    def get_by_name(cls, language: str) -> Language:
        return cls.__name_lookup[language]
