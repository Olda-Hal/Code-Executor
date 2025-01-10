import asyncio
import uuid
from typing import Optional

import docker
from docker.models.containers import Container
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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

    container_name = f"execution-{str(uuid.uuid4())}"

    try:
        container = client.containers.run(
            language_config.image,
            environment={
                "CODE": execution.code,
                "INPUT": execution.input or "",
            },
            name=container_name,
            detach=True,
            mem_limit="100m",
            cpu_period=100000,
            cpu_quota=50000,
            network_mode="none",
        )

        try:
            await asyncio.wait_for(
                asyncio.to_thread(container.wait), timeout=execution.timeout
            )

            logs = container.logs().decode().strip()
            return {"status": "success", "output": logs}

        except asyncio.TimeoutError:
            container.kill()
            raise HTTPException(status_code=408, detail="Execution timeout")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        try:
            container.remove(force=True)
        except:
            pass
