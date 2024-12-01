
import os
import pickle
import random

import numpy as np
import torch
import torch.utils.data
import torch.backends.cudnn


# 保存训练模型
def checkpoint_save(net, optimizer, save_path):
    state = {'model': net.state_dict(), 'optimizer': optimizer.state_dict()}
    torch.save(state, save_path)


# 模型加载训练模型
def checkpoint_load(model, t_checkpoint_path, s_checkpoint_path, device):
    checkpoint_rewrite = {}
    if s_checkpoint_path:
        if not os.path.exists(s_checkpoint_path):
            assert False, "file {} does not exist.".format(s_checkpoint_path)
        else:
            print('==> loading checkpoint from {}'.format(s_checkpoint_path))
            s_checkpoint = torch.load(s_checkpoint_path)
            s_checkpoint['state_dict'].pop('fc.weight')
            s_checkpoint['state_dict'].pop('fc.bias')
            for key, value in s_checkpoint['state_dict'].items():
                key1 = 'teacher_backbone.' + key
                key2 = 'students_backbone.' + key
                checkpoint_rewrite[key1] = s_checkpoint['state_dict'][key]
                checkpoint_rewrite[key2] = s_checkpoint['state_dict'][key]
            # with open(s_checkpoint_path, 'rb') as f:
            #     obj = f.read()
            # s_checkpoint = {key: torch.from_numpy(arr) for key, arr in pickle.loads(obj, encoding='latin1').items()}
            # s_checkpoint.pop('fc.weight')
            # s_checkpoint.pop('fc.bias')
            # for key, value in s_checkpoint.items():
            #     key2 = 'students_backbone.' + key
            #     checkpoint_rewrite[key2] = s_checkpoint[key]
    else:
        print('students no checkpoint model !!!')
    # if t_checkpoint_path:
    #     if not os.path.exists(t_checkpoint_path):
    #         assert False, "file {} does not exist.".format(t_checkpoint_path)
    #     else:
    #         print('==> loading checkpoint from {}'.format(t_checkpoint_path))
    #         with open(t_checkpoint_path, 'rb') as f:
    #             obj = f.read()
    #         t_checkpoint = {key: torch.from_numpy(arr) for key, arr in pickle.loads(obj, encoding='latin1').items()}
    #         t_checkpoint.pop('fc.weight')
    #         t_checkpoint.pop('fc.bias')
    #         for key, value in t_checkpoint.items():
    #             key1 = 'teacher_backbone.' + key
    #             checkpoint_rewrite[key1] = t_checkpoint[key]
    # else:
    #     print('teacher no checkpoint model !!!')
    model.load_state_dict(checkpoint_rewrite, strict=False)


# 写入文件
def writefile(filepath, message, mode):
    with open(filepath, mode=mode) as file:
        file.writelines('\n')
        file.writelines(message)


#
def setup_seed(seed):
    # torch.manual_seed(seed)
    # torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.enable = True
    torch.backends.cudnn.benchmark = False
    # torch.backends.cudnn.deterministic = True


def check_batch(labels, num_class):
    for i in range(num_class):
        cnt = (labels == i).sum()
        if cnt.sum() < 2:
            return False
    return True