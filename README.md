# Ray Serve Router Performance Test

This project demonstrates the performance difference between Ray Serve's default **Power of Two Choices (P2C)** router and a **Uniform** router, especially in a "straggler replica" scenario.

You will see that the P2C router is much faster because it intelligently avoids the slow replica, while the Uniform router gets bottlenecked.

## 📁 File Structure

You need these 4 files in the same directory:
* `model.py`: Defines the model logic and the straggler replica.
* `custom_routers.py`: Defines the uniform router.
* `deploy.py`: The server script that deploys the models.
* `load_test.py`: The client script that runs the performance test.

## 🚀 How to Run

You will need **2 separate terminal windows**.

### Step 1: Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install "ray[serve]" aiohttp
```

### Step 2: (Terminal 1) Deploy the models
```bash
python deploy.py
```

### Step 3: (Terminal 2) Run the load test
```bash
python load_test.py
```

## Expected Results
```bash
--- Testing PowerOfTwoChoicesRequestRouter (P2C) ---
Sending 30 requests to http://localhost:8000/default with 3 concurrency...
Completed in 6.15 seconds
Successes: 30, Failures: 0
Default (P2C) took: 6.15 seconds

--- Testing UniformRequestRouter ---
Sending 30 requests to http://localhost:8000/uniform with 3 concurrency...
Completed in 16.08 seconds
Successes: 30, Failures: 0
Uniform took: 16.08 seconds

--- Comparison ---
Default (P2C): 6.15s
Uniform:       16.08s

Test finished. (P2C was ~2.6x faster)
```
