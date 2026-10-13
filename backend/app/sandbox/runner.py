import json
import logging
from config import settings

logger = logging.getLogger("quantalab")

try:
    import docker
    from docker.errors import ContainerError, ImageNotFound, APIError
    DOCKER_AVAILABLE = True
except ImportError:
    docker = None
    ContainerError = Exception
    ImageNotFound = Exception
    APIError = Exception
    DOCKER_AVAILABLE = False

def execute_in_sandbox(code: str, timeout: int = None) -> dict:
    if not DOCKER_AVAILABLE:
        return {"error": "Docker is not installed or available on this system.", "status": "failed"}

    if timeout is None:
        timeout = settings.sandbox_timeout_seconds
        
    try:
        client = docker.from_env()
    except Exception as e:
        logger.error(f"Failed to connect to docker: {e}")
        return {"error": "Sandbox environment unavailable", "status": "failed"}
        
    # We will write the code to a single command that evaluates it
    # Ideally, we should map a volume or pass it via stdin
    # For a simple runner, we can pass it as a python -c string
    
    # Escape quotes
    escaped_code = code.replace("'", "'\\''")
    command = f"python -c '{escaped_code}'"
    
    try:
        container = client.containers.run(
            image=settings.sandbox_image_name,
            command=command,
            mem_limit=f"{settings.sandbox_memory_limit_mb}m",
            cpu_quota=int(settings.sandbox_cpu_limit * 100000), # 1 CPU
            network_mode="none",
            read_only=True,
            detach=True
        )
        
        try:
            result = container.wait(timeout=timeout)
            exit_code = result.get('StatusCode', 1)
            
            logs = container.logs().decode('utf-8')
            
            if exit_code == 0:
                return {"output": logs, "status": "success", "exit_code": 0}
            else:
                return {"error": logs, "status": "failed", "exit_code": exit_code}
                
        except Exception as e:
            # Timeout or other error during wait
            container.kill()
            return {"error": f"Execution timed out or failed: {e}", "status": "timeout"}
            
        finally:
            container.remove(force=True)
            
    except ImageNotFound:
        return {"error": f"Sandbox image {settings.sandbox_image_name} not found", "status": "failed"}
    except APIError as e:
        return {"error": f"Docker API error: {e}", "status": "failed"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}", "status": "failed"}
