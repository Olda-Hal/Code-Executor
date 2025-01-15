#!/usr/bin/env python3
import os
import sys
import shutil

def create_runner(language_name, file_extension):
    # Convert language name to lowercase for consistency
    language_name = language_name.lower()
    
    # Create runners directory if it doesn't exist
    if not os.path.exists('runners'):
        os.makedirs('runners')
    
    # Create language-specific directory
    runner_dir = f'runners/{language_name}'
    os.makedirs(runner_dir, exist_ok=True)
    
    # Create Dockerfile
    dockerfile_content = f'''FROM baserunner
WORKDIR /app/
COPY {language_name}-runner.sh .
CMD ["python3", "/usr/src/app/runnerAPI.py"]'''
    
    with open(f'{runner_dir}/Dockerfile', 'w') as f:
        f.write(dockerfile_content)
    
    # Create runner shell script
    runner_script_content = f'''#!/bin/bash

mkdir -p /run/user/$(id -u)
echo "$PROJECT" | xxd -r -p > /run/user/$(id -u)/script.tar.gz
mkdir -p /run/user/$(id -u)/project
gunzip /run/user/$(id -u)/script.tar.gz
tar --warning=no-unknown-keyword -xf /run/user/$(id -u)/script.tar -C /run/user/$(id -u)/project/
chmod -R 777 /run/user/$(id -u)/project/
output=$(exec timeout $TIMEOUT bwrap --ro-bind /usr /usr \\
    --dir /tmp \\
    --dir /var \\
    --symlink ../tmp var/tmp \\
    --proc /proc \\
    --dev /dev \\
    --ro-bind /etc/resolv.conf /etc/resolv.conf \\
    --symlink usr/lib /lib \\
    --symlink usr/lib64 /lib64 \\
    --symlink usr/bin /bin \\
    --symlink usr/sbin /sbin \\
    --bind /run/user/$(id -u) /run/user/$(id -u) \\
    --chdir / \\
    --unshare-all \\
    --die-with-parent \\
    --dir /run/user/$(id -u) \\
    --setenv XDG_RUNTIME_DIR "/run/user/$(id -u)" \\
    --setenv PS1 "bwrap-demo$ " \\
    /bin/bash echo "not implemented")
echo "$output"

rm -rf /run/user/$(id -u)'''
    
    with open(f'{runner_dir}/{language_name}-runner.sh', 'w') as f:
        f.write(runner_script_content)
    
    # Make the runner script executable
    os.chmod(f'{runner_dir}/{language_name}-runner.sh', 0o755)
    
    # Update docker-compose.yml
    docker_compose_content = f'''
  {language_name}:
    build:
      context: ./runners/{language_name}
      dockerfile: Dockerfile
    image: {language_name}runner
    depends_on:
      - baserunner
    networks:
      - network
    privileged: true'''
    
    with open('docker-compose.yml', 'a') as f:
        f.write(docker_compose_content)
    
    # Update languages.py
    language_enum_entry = f"    {language_name.upper()} = Language('{language_name}', '{file_extension}')\n"
    
    # Read existing content
    with open('languages.py', 'r') as f:
        content = f.readlines()
    
    # Find the last entry in the Language enum
    for i, line in enumerate(content):
        if 'class Languages(' in line:
            # Insert new language after the class definition
            content.insert(i + 1, language_enum_entry)
            break
    
    # Write back the updated content
    with open('languages.py', 'w') as f:
        f.writelines(content)

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 create_runner.py <language_name> <file_extension>")
        print("Example: python3 create_runner.py python py")
        sys.exit(1)
    
    language_name = sys.argv[1]
    file_extension = sys.argv[2]
    if file_extension[0] != ".":
        file_extension = "." + file_extension
    
    runner_dir = f'runners/{language_name}'
    if os.path.exists(runner_dir):
        print(f"Error: Runner for {language_name} already exists.")
        sys.exit(1)

    create_runner(language_name, file_extension)
    print(f"Successfully created runner for {language_name} with extension {file_extension}")

if __name__ == "__main__":
    main()