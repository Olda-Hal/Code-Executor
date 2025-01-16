from typing import Optional

import docker
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from languages import Languages

app = FastAPI()
client = docker.from_env()


class CodeExecution(BaseModel):
    language: str
    project: str
    timeout: Optional[int] = 10
    execfile: str


@app.post("/execute")
async def execute_code(execution: CodeExecution):
    if not Languages.is_supported(execution.language):
        raise HTTPException(status_code=400, detail="Unsupported language")

    language_config = Languages.get_by_name(execution.language)

    execfile = execution.execfile
    if not execfile.endswith(language_config.file_extension):
        execfile += language_config.file_extension

    response = requests.post(
        language_config.http + "/execute",
        json={
            "project": execution.project,
            "script": language_config.script,
            "execfile": execfile,
            "timeout": execution.timeout,
        },
    )
    return response.json()
