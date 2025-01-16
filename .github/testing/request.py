import requests

with open('tests.tar.gz', 'rb') as file:
    project = file.read()
    project_hex = project.hex()


response = requests.post("http://localhost:8000/execute", json={
    "language": "haskell",
    "project": project_hex,
    "execfile": "testing/file.hs",
    "timeout": 100
})
if response["stdout"].strip() != "Hello, World!":
    raise Exception("Haskell language execution failed")

response = requests.post("http://localhost:8000/execute", json={
    "language": "c",
    "project": project_hex,
    "execfile": "testing/test.c",
    "timeout": 100
})

if response["stdout"].strip() != "Hello, World!":
    raise Exception("C language execution failed")

response = requests.post("http://localhost:8000/execute", json={
    "language": "python",
    "project": project_hex,
    "execfile": "testing/test.py",
    "timeout": 100
})

if response["stdout"].strip() != "Hello, World!":
    raise Exception("Python language execution failed")

response = requests.post("http://localhost:8000/execute", json={
    "language": "asm",
    "project": project_hex,
    "execfile": "testing/test.s",
    "timeout": 100
})

if response["stdout"].strip() != "Hello, World!":
    raise Exception("Assembly language execution failed")

response = requests.post("http://localhost:8000/execute", json={
    "language": "csharp",
    "project": project_hex,
    "execfile": "testing/test.csproj",
    "timeout": 100
})

if response["stdout"].strip() != "Hello, World!":
    raise Exception("C# language execution failed")