import time
import ray
from ray import serve
from ray.serve.config import RequestRouterConfig

# Import mymodel and counter
from model import MyModel, ReplicaCounter


print("Starting Ray Serve...")
serve.start()

print("Creating replica counter actors...")
counter_default = ReplicaCounter.options(name="counter_default", get_if_exists=True).remote()
counter_uniform = ReplicaCounter.options(name="counter_uniform", get_if_exists=True).remote()

print("Deploying 'app_default' (Power of 2 Router)...")
app_default = MyModel.options(name="model_default").bind(counter=counter_default)
serve.run(app_default, name="app_default", route_prefix="/default")

print("Deploying 'app_uniform' (Uniform Router)...")
app_uniform = MyModel.options(
    name="model_uniform",
    request_router_config=RequestRouterConfig(
        request_router_class="custom_routers:UniformRequestRouter"
    ),
).bind(counter=counter_uniform)
serve.run(app_uniform, name="app_uniform", route_prefix="/uniform")

print("\n🎉 Deployments are live.")
print(f"   Dashboard URL: http://127.0.0.1:8265")
print("   - P2C Router: http://localhost:8000/default")
print("   - Uniform Router: http://localhost:8000/uniform")
print("\nRun 'python load_test.py' in another terminal.")
print("Press Ctrl+C to shut down.")

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("\nShutting down deployments...")
    serve.shutdown()