import fastapi
from pydantic import BaseModel
from typing import Optional, List
import os
import subprocess
import uvicorn


app = fastapi.FastAPI()

class CodeRequest(BaseModel):
    project: str
    script: str
    execfile: str
    timeout: int

@app.post("/execute")
async def execute_code(request: CodeRequest):
    print("request")
    project = request.project
    script = request.script
    execfile = request.execfile
    timeout = request.timeout
    
    print(project)
    os.environ['PROJECT'] = project
    os.environ['EXECFILE'] = execfile
    os.environ['TIMEOUT'] = str(timeout)

    result = subprocess.run(
        ["bash", script],
        capture_output=True,
        text=True,
        env=os.environ
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.returncode
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)