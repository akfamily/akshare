:orphan:

AKShare 文档源文件
===========================================

本目录是 `AKShare 在线文档 <https://akshare.akfamily.xyz/>`_ 的源文件。每次推送到 main 分支后，Read the Docs 会自动重新构建并发布文档。

本地构建
--------

在仓库根目录运行：

::

    uv run --no-project --with-requirements docs/requirements.txt sphinx-build -b html docs docs/_build/html

构建结果位于 ``docs/_build/html``，用浏览器打开其中的 ``index.html`` 即可预览。文档构建不需要安装 akshare 本身，``docs/_build/`` 已被 git 忽略。

修改 ``docs/data/`` 下的数据字典后，还需要在仓库根目录运行 ``python scripts/build_registry.py``，同步更新接口检索使用的元数据。
