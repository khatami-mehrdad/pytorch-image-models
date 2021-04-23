""" Summary utilities

Hacked together by / Copyright 2020 Ross Wightman
"""
import csv
import os
from collections import OrderedDict
try: 
    import wandb
except ImportError:
    pass

def get_outdir(path, *paths, inc=False):
    outdir = os.path.join(path, *paths)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    elif inc:
        count = 1
        outdir_inc = outdir + '-' + str(count)
        while os.path.exists(outdir_inc):
            count = count + 1
            outdir_inc = outdir + '-' + str(count)
            assert count < 100
        outdir = outdir_inc
        os.makedirs(outdir)
    return outdir

def output_dir(output_path, model_name, input_size, train_test = 'train'):
    output_dir = ''
    output_base = output_path if output_path else './output'
    exp_name = '-'.join([
        datetime.now().strftime("%Y%m%d-%H%M%S"),
        model_name,
        str(input_size)
    ])
    output_dir = get_outdir(output_base, train_test, exp_name)
    return output_dir

def update_summary(epoch, train_metrics, eval_metrics, filename, write_header=False, log_wandb=False, layer_name=None):
    rowd = OrderedDict(epoch=epoch)
    if (layer_name != None):
        rowd.update( [('layer_name', layer_name)] )

    rowd.update([('train_' + k, v) for k, v in train_metrics.items()])
    rowd.update([('eval_' + k, v) for k, v in eval_metrics.items()])
    if log_wandb:
        wandb.log(rowd)
    with open(filename, mode='a') as cf:
        dw = csv.DictWriter(cf, fieldnames=rowd.keys())
        if write_header:  # first iteration (epoch == 1 can't be used)
            dw.writeheader()
        dw.writerow(rowd)
