def get_tqdm():
    """
    返回适用于当前环境的 tqdm 对象。
    """
    try:
        # 尝试检查是否在 Jupyter notebook 环境中，有利于退出进度条
        # noinspection PyUnresolvedReferences
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            from tqdm.notebook import tqdm
        else:
            from tqdm import tqdm
    except (NameError, ImportError):
        # 如果不在 Jupyter 环境中，就使用标准 tqdm
        from tqdm import tqdm

    return tqdm
