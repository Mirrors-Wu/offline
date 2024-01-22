# 初始化目录
import os


def init_dir():
    os.makedirs('data/group_profile', exist_ok=True)
    os.makedirs('data/group_photo', exist_ok=True)
