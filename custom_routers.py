import random
from typing import List, Optional

from ray.serve.request_router import (
    PendingRequest,
    RequestRouter,
    RunningReplica,
)

class UniformRequestRouter(RequestRouter):
    """
    A "true" blind uniform router that selects exactly one replica
    at random and forces the request to go there.
    """
    async def choose_replicas(
        self,
        candidate_replicas: List[RunningReplica],
        pending_request: Optional[PendingRequest] = None,
    ) -> List[List[RunningReplica]]:
        
        chosen_replica = random.choice(candidate_replicas)
        return [[chosen_replica]]