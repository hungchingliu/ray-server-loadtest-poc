import asyncio
import time
import ray
from ray import serve
from ray.serve import get_replica_context

# --- 1. Replica Counter Actor ---
@ray.remote
class ReplicaCounter:
    """
    Assigns a unique integer ID (0, 1, 2, 3...) to each replica
    to deterministically create a straggler.
    """
    def __init__(self):
        self.count = -1
        self._lock = asyncio.Lock()

    async def get_next_id(self):
        async with self._lock:
            self.count += 1
            return self.count

# --- 2. Model Deployment ---
@serve.deployment(num_replicas=5, max_ongoing_requests=5) # Default 5
class MyModel:
    def __init__(self, counter: ray.actor.ActorHandle):
        context = get_replica_context()
        self.replica_num = ray.get(counter.get_next_id.remote())
        
        if self.replica_num == 0:
            self.is_straggler = True
            print(f"!!! Replica {context.replica_tag} (ID: 0) INITIALIZED AS CPU-BOUND STRAGGLER !!!")
        else:
            self.is_straggler = False
            print(f"Replica {context.replica_tag} (ID: {self.replica_num}) INITIALIZED AS FAST")

    async def __call__(self) -> str:
        if self.is_straggler:
            # Use a BLOCKING sleep to simulate a stuck CPU
            time.sleep(2.0) 
            return f"Response from STRAGGLER (ID: {self.replica_num})"
        else:
            # Fast replicas are non-blocking
            await asyncio.sleep(0.01)
            return f"Response from FAST replica (ID: {self.replica_num})"