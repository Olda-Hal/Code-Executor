from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Language:
    name: str
    image: str
    file_extension: str


class Languages(Enum):
    ASM = Language("asm", "code-executor-asm", ".s")
    CPP = Language("cpp", "code-executor-cpp", ".cpp")
    HASKELL = Language("haskell", "code-executor-haskell", ".hs")
    JAVASCRIPT = Language("javascript", "code-executor-node", ".js")
    LLVM = Language("llvm", "code-executor-llvm", ".ll")
    PYTHON = Language("python", "code-executor-python", ".py")

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
