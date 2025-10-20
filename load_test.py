import asyncio
import time
import aiohttp # Using aiohttp for async requests

# --- Client Settings ---
NUM_REQUESTS = 30
MAX_CONCURRENCY = 3
URL_DEFAULT = "http://localhost:8000/default"
URL_UNIFORM = "http://localhost:8000/uniform"
# --- End Settings ---

async def fetch(url: str, session, semaphore):
    """A single request, guarded by the semaphore."""
    async with semaphore:
        try:
            async with session.get(url) as response:
                await response.text()
                return True
        except Exception:
            return False

async def _run_load_test_async(url: str, num_requests: int):
    """Sends requests with limited concurrency."""
    print(f"Sending {num_requests} requests to {url} with {MAX_CONCURRENCY} concurrency...")
    
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)
    tasks = []
    
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        for _ in range(num_requests):
            tasks.append(fetch(url, session, semaphore))
        
        results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    
    failures = sum(1 for r in results if r is False)
    successes = num_requests - failures
    total_duration = end_time - start_time
    
    print(f"Completed in {total_duration:.2f} seconds")
    print(f"Successes: {successes}, Failures: {failures}")
    return total_duration

async def main_test_logic():
    """Main async function for the load test client."""
    
    print("--- Testing PowerOfTwoChoicesRequestRouter (P2C) ---")
    duration_default = await _run_load_test_async(URL_DEFAULT, NUM_REQUESTS)
    print(f"Default (P2C) took: {duration_default:.2f} seconds")
    
    print("\n--- Testing UniformRequestRouter ---")
    duration_uniform = await _run_load_test_async(URL_UNIFORM, NUM_REQUESTS)
    print(f"Uniform took: {duration_uniform:.2f} seconds")
    
    print("\n--- Comparison ---")
    print(f"Default (P2C): {duration_default:.2f}s")
    print(f"Uniform:       {duration_uniform:.2f}s")
    
    if duration_default > 0 and duration_uniform > 0:
        print(f"\nTest finished. (P2C was ~{(duration_uniform / duration_default):.1f}x faster)")
    else:
        print("\nTest finished.")

if __name__ == "__main__":
    try:
        asyncio.run(main_test_logic())
    except aiohttp.client_exceptions.ClientConnectorError:
        print("\nError: Could not connect to endpoints.")
        print("Please ensure 'ray start --head' and 'python deploy.py' are running.")