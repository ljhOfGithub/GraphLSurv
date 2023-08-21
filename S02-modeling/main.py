"""
Entry filename: main.py

Code in this file inherts from https://github.com/hugochan/IDGL as it provides a flexible way 
to configure parameters and inspect model performance. Great thanks to the author.
"""
import argparse
import yaml
import torch
import numpy as np
from collections import defaultdict, OrderedDict

from model_handler import DRPMHandler
from utils import print_config


def main(config):
    model = DRPMHandler(config)
    metrics = model.exec()
    print('[INFO] Metrics:', metrics)

def multi_run_main(config):
    hyperparams = []
    for k, v in config.items():
        if isinstance(v, list):
            hyperparams.append(k)

    configs = grid(config)
    for cnf in configs:
        print('\n')
        for k in hyperparams:
            cnf['save_path'] += '-{}_{}'.format(k, cnf[k])
        print(cnf['save_path'])
        model = DRPMHandler(cnf)
        metrics = model.exec()
        print('[INFO] Metrics:', metrics)

    # print('[INFO] Average C-Index: {}'.format(np.mean(scores['ci'])))
    # print('[INFO] Std C-Index: {}'.format(np.std(scores['ci'])))

    # print('[INFO] Average Loss: {}'.format(np.mean(scores['loss'])))
    # print('[INFO] Std Loss: {}'.format(np.std(scores['loss'])))


def get_args():
    parser = argparse.ArgumentParser()
    # parser.add_argument('--config', '-f', required=True, type=str, help='path to the config file')
    parser.add_argument('--config', '-f', type=str, default='config/report-tcga_brca.yml', help='path to the config file') #方便调试
    # parser.add_argument('--multi_run', action='store_true', help='flag: multi run')
    parser.add_argument('--multi_run', default='True', help='flag: multi run') #方便调试
    args = vars(parser.parse_args())
    return args

def get_config(config_path="config/config.yml"):
    with open(config_path, "r") as setting:
        config = yaml.load(setting, Loader=yaml.FullLoader)
    return config

def grid(kwargs):
    """Builds a mesh grid with given keyword arguments for this Config class.
    If the value is not a list, then it is considered fixed"""

    class MncDc:
        """This is because np.meshgrid does not always work properly..."""

        def __init__(self, a):
            self.a = a  # tuple!

        def __call__(self):
            return self.a

    def merge_dicts(*dicts):
        """
        Merges dictionaries recursively. Accepts also `None` and returns always a (possibly empty) dictionary
        """
        from functools import reduce
        def merge_two_dicts(x, y):
            z = x.copy()  # start with x's keys and values
            z.update(y)  # modifies z with y's keys and values & returns None
            return z

        return reduce(lambda a, nd: merge_two_dicts(a, nd if nd else {}), dicts, {})


    sin = OrderedDict({k: v for k, v in kwargs.items() if isinstance(v, list)})
    for k, v in sin.items():
        copy_v = []
        for e in v:
            copy_v.append(MncDc(e) if isinstance(e, tuple) else e)
        sin[k] = copy_v
    # try:
    # current_locals = locals()
    # with open('./variables.txt', 'w') as f:
    #     import pprint; pprint.pprint(current_locals, stream=f)
    # import pdb; pdb.set_trace()
    grd = np.array(np.meshgrid(*sin.values()), dtype=object).T.reshape(-1, len(sin.values()))

#     except Exception as e:
#         import traceback
#         import pprint
#         import sys
#         # traceback.print_exc()
#         exc_type, exc_value, exc_traceback = sys.exc_info()

#         # 将堆栈信息写入文件
#         with open('./error_log.txt', 'w') as f:
#             traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)

#         # 获取当前变量的值
#         current_locals = locals()

#         # 将变量值写入文件
#         with open('./variables.txt', 'w') as f:
#             pprint.pprint(current_locals, stream=f)
#         return [merge_dicts(
#         {k: v for k, v in kwargs.items() if not isinstance(v, list)},
#         {k: vv[i]() if isinstance(vv[i], MncDc) else vv[i] for i, k in enumerate(sin)}
#     ) for vv in grd]
    
    return [merge_dicts(
        {k: v for k, v in kwargs.items() if not isinstance(v, list)},
        {k: vv[i]() if isinstance(vv[i], MncDc) else vv[i] for i, k in enumerate(sin)}
    ) for vv in grd]


if __name__ == '__main__':
    cfg = get_args()
    config = get_config(cfg['config'])
    print_config(config)
    if cfg['multi_run']:
        multi_run_main(config)
    else:
        main(config)
