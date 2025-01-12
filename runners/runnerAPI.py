import fastapi
from pydantic import BaseModel
from typing import Optional, List
import os
import subprocess
import uvicorn


app = fastapi.FastAPI()

class CodeRequest(BaseModel):
    code: str
    script: str
    arguments: Optional[List[str]] = None

@app.post("/execute")
async def execute_code(request: CodeRequest):
    code = request.code
    script = request.script
    arguments = request.arguments if request.arguments else []
    
    os.environ['CODE'] = code
    os.environ['ARGUMENTS'] = " ".join(arguments)
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