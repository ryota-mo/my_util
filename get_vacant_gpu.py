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
    cmd = "nvidia-smi --query-gpu={} --format=csv,noheader{}".format(','.join(keys), nu_opt)
    output = subprocess.check_output(cmd, shell=True)
    lines = output.decode().split('\n')
    lines = [line.strip() for line in lines if line.strip() != '']
    return [{k: v for k, v in zip(keys, line.split(', '))} for line in lines]


def convert_metric_to_percent(gpu_info, metric):
    if metric == 'util_cpu':
        return float(gpu_info['utilization.gpu'])
    elif metric == 'mem_usage':
        return (float(gpu_info['memory.used']) / float(gpu_info['memory.total'])) * 100
    else:
        raise NotImplementedError("Unknown metric {}".format(metric))


def get_vacant_gpu(metric='util_cpu'):
    # metric: util_cpu, mem_usage
    vacant_gpu = '0'
    min_utilization_value = 100
    for gpu_info in get_gpu_info():
        current_utilization = convert_metric_to_percent(gpu_info, metric)
        if current_utilization < min_utilization_value:
            vacant_gpu = gpu_info['index']
            min_utilization_value = current_utilization
    return vacant_gpu


if __name__ == '__main__':
    print(get_vacant_gpu())
