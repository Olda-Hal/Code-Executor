import asyncio
import uuid
from typing import Optional

import docker
from docker.models.containers import Container
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

from languages import Language, Languages

app = FastAPI()
client = docker.from_env()


class CodeExecution(BaseModel):
    language: str
    code: str
    input: Optional[str] = None
    timeout: Optional[int] = 10


@app.post("/execute")
async def execute_code(execution: CodeExecution):
    if not Languages.is_supported(execution.language):
        raise HTTPException(status_code=400, detail="Unsupported language")

    language_config = Languages.get_by_name(execution.language)
    print(language_config)
    if execution.input is not None:
        if " " in execution.input:
            code_input = execution.input.split(" ")
        else:
            code_input = [execution.input]
    else:
        code_input = None

    response = requests.post(language_config.http + "/execute", json={
        "code": execution.code,
        "script": language_config.script,
        "arguments": code_input

    })
    print(response.content)
    return response.content