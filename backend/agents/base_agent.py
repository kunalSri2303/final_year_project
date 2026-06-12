from abc import ABC, abstractmethod
from typing import Any
import time

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    async def execute(self, *args, **kwargs) -> Any:
        print(f"[{self.name}] Starting execution...")
        start_time = time.time()
        
        try:
            result = await self._process(*args, **kwargs)
            duration = time.time() - start_time
            print(f"[{self.name}] Finished execution in {duration:.2f}s")
            return result
        except Exception as e:
            print(f"[{self.name}] Error during execution: {str(e)}")
            raise e

    @abstractmethod
    async def _process(self, *args, **kwargs) -> Any:
        pass
