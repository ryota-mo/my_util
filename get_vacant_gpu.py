import subprocess
import json

DEFAULT_ATTRIBUTES = (
    'index',
    'uuid',
    'name',
    'timestamp',
    'memory.total',
    'memory.free',
    'memory.used',
    'utilization.gpu',
    'utilization.memory'
)


def get_gpu_info(keys=DEFAULT_ATTRIBUTES, no_units=True):
    """
    return:
    [{'index': '0', 'uuid': 'GPU-88cff515-3e94-4d20-3f5d-5eaf73f59af0', 'name': 'Tesla V100-SXM2-16GB', 'timestamp': '2019/09/24 06:22:37.480', 'memory.total': '16152', 'memory.free': '14515', 'memory.used': '1637', 'utilization.gpu': '21', 'utilization.memory': '39'}, ...]
    """
    nu_opt = '' if not no_units else ',nounits'
    cmd = f"nvidia-smi --query-gpu={','.join(keys)} --format=csv,noheader{nu_opt}"
    output = subprocess.check_output(cmd, shell=True)
    lines = output.decode().split('\n')
    lines = [line.strip() for line in lines if line.strip() != '']
    return [{k: v for k, v in zip(keys, line.split(', '))} for line in lines]


def get_vacant_gpu():
    vacant_gpu = '0'
    min_gpu_utilization = 100
    for gpu_info in get_gpu_info():
        if float(gpu_info['utilization.gpu']) < min_gpu_utilization:
            vacant_gpu = gpu_info['index']
            min_gpu_utilization = float(gpu_info['utilization.gpu'])
    return vacant_gpu


if __name__ == '__main__':
    print(get_vacant_gpu())
