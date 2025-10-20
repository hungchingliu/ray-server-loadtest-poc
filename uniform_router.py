import random
from typing import List, Optional

from ray.serve.request_router import (
    PendingRequest,
    RequestRouter,
    RunningReplica,
)

# Define the router in its own file
class UniformRequestRouter(RequestRouter):
    """A custom router that randomly selects a replica for each request."""

    async def choose_replicas(
        self,
        candidate_replicas: List[RunningReplica],
        pending_request: Optional[PendingRequest] = None,
    ) -> List[List[RunningReplica]]:
        
        # 1. Pick *one* replica completely at random.
        chosen_replica = random.choice(candidate_replicas)
        
        # 2. Return it as the *only* option.
        # Ray Serve now has no other choice but to send the request
        # to this specific replica, regardless of its queue length.
        return [[chosen_replica]]