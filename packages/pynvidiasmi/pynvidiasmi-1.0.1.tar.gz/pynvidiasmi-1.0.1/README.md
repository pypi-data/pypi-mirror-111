# pynvidiasmi
Query `nvidia-smi` command and return its output as a list of dictionaries.

```python
>> from pynvidiasmi import query, get_available_gpus
>> # 'query' returns a dictionary with the queried fields
>> # Possible fields can be obtained via nvidia-smi --help-query-gpu
>> query(fields=["index", "name", "pstate", "utilization.gpu", "utilization.memory"])
[{'index': 0, 'name': 'A100-SXM4-40GB', 'pstate': 'P0', 'utilization.gpu': 0, 'utilization.memory': 0}, {'index': 1, 'name': 'A100-SXM4-40GB', 'pstate': 'P0', 'utilization.gpu': 47, 'utilization.memory': 10}]
>> # 'get_available_gpus' queries the gpu 'times' times, waiting 'sleep' seconds between queries
>> # and returns the GPUs that satisfy the memory and compute constraints all the times.
>> # This helps in obtaining the GPUs that are available for starting a computation.
>> get_available_gpus(memory_threshold=0, compute_threshold=0, times=3, sleep=1.0)
[0]
```
