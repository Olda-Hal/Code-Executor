from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import docker
import uuid
import asyncio
from typing import Optional

app = FastAPI()
client = docker.from_env()

class CodeExecution(BaseModel):
    language: str
    code: str
    input: Optional[str] = None
    timeout: Optional[int] = 10

@app.post("/execute")
async def execute_code(execution: CodeExecution):
    supported_languages = {
        "python": {
            "image": "code-executor-python",
            "file_extension": ".py",
            "command": "python"
        },
        "javascript": {
            "image": "code-executor-node",
            "file_extension": ".js",
            "command": "node"
        },
        "cpp": {
            "image": "code-executor-cpp",
            "file_extension": ".cpp",
            "command": "run-cpp"
        }
    }
    
    if execution.language not in supported_languages:
        raise HTTPException(status_code=400, detail="Unsupported language")
    
    language_config = supported_languages[execution.language]
    container_name = f"execution-{str(uuid.uuid4())}"
    
    try:
        container = client.containers.run(
            language_config["image"],
            environment={
                "CODE": execution.code,
                "INPUT": execution.input or "",
            },
            name=container_name,
            detach=True,
            mem_limit="100m",
            cpu_period=100000,
            cpu_quota=50000,
            network_mode="none"
        )
        
        try:
            await asyncio.wait_for(
                asyncio.to_thread(container.wait),
                timeout=execution.timeout
            )
            
            logs = container.logs().decode().strip()
            return {
                "status": "success",
                "output": logs
            }
            
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