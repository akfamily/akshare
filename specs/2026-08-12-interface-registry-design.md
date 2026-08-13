# 接口检索层设计（Interface Registry）

- 日期：2026-08-12
- 状态：设计已确认，待实施
- 范围：新增能力，不改动任何现有数据接口的行为

## 1. 背景

AKShare 的使用者正在从「人写代码」转向「agent 调用」。当前形态对 agent 有四个断点，以下数据均为本仓库实测：

| 断点 | 实测证据 |
|---|---|
| 发现不到接口 | 1100 个导出、无 `__all__`；`docs/data/` 共 2.68 MB，`stock.md` 单文件 1.0 MB / 375 个条目，无法放进模型上下文 |
| 文档与代码已漂移 | 1015 个接口文档与导出匹配；**3 个文档有而代码无**；**75 个导出而无文档**（数据接口口径，详见第 7 节推导） |
| 文档格式不统一 | 10 个接口条目用全角冒号 `接口：`，解析器必须同时容错半角与全角，否则这些接口会从 registry 中彻底消失 |
| 错误无法分类 | 219 个模块裸调 `r.json()` 不检查状态码；仅 9 个用 `raise_for_status`；`exceptions.py` 全库仅 5 个文件用到 |
| 返回结构不可预期 | 276 个函数无返回类型注解；无 `py.typed` |

本设计只解决第一个断点，并为其余三个提供数据基础。

其中「文档与代码漂移」已产生用户可见故障，例如 `fortune_rank`：函数存在于 `akshare/fortune/fortune_500.py:40`，changelog 记录其在 0.6.98、1.8.51、1.12.87、1.14.49 共四次被修复，但当前未从 `__init__.py` 导出，用户按文档调用会得到 `AttributeError`。目前没有任何机制能发现此类回归。

## 2. 目标与非目标

### 目标

1. 提供离线可用的接口检索 API，使 agent 能从自然语言描述定位到可调用的接口。
2. 提供结构化接口元数据（参数、输出列、示例、数据源地址）。
3. 建立 CI 门禁，阻止文档与代码进一步漂移。

### 非目标（本次明确不做）

- 不修改任何现有数据接口的函数签名或运行时行为。
- 不做运行期参数枚举校验（需逐个接口改函数，且文档枚举未必准确，易误拦合法调用）。
- 不做输出列 strict 校验（文档输出表覆盖率仅 95.1% 且未必与实际一致，先做会产生大量假阳性）。
- 不修复第 11 节列出的存量漂移项，它们由门禁记录并各自单独提 PR。
- 不引入任何第三方依赖。

元数据 Schema 会完整保留输入/输出参数表，为上述后续能力预留，这部分是零成本的。

## 3. 关键决策

| 决策 | 选择 | 理由 |
|---|---|---|
| 交付形态 | 随包分发的 Python API | agent 离线可用；后续 MCP server 直接复用同一份数据 |
| 匹配策略 | 零依赖关键词打分 | 保持依赖克制；中文查询本身即连续子串，无需分词器；agent 会自行改写查询重试 |
| 交付范围 | 最小闭环（检索 + 元数据 + CI 校验） | 只新增不改动，风险最低，可独立发版 |
| 产物生成 | 构建期生成静态产物并提交进 git，CI 校验无 diff | 与现有 `package-data` / `datasets.py` 约定一致，不引入新机制 |
| 产物格式 | 纯 JSON 文本，**不额外 zip** | wheel 本身即 zip，分发体积等价；换来 git diff 可读；规避 zip 时间戳导致的字节不确定性 |

### 体积实测

| 项 | 大小 |
|---|---|
| 元数据 compact JSON（含示例） | 约 1.19 MB |
| 经 deflate 后（≈ wheel 内实际占用） | 约 0.13 MB |
| 当前 `akshare/` 包体 | 4.5 MB |

分发体积增量约 130 KB；安装后磁盘占用增加约 1.19 MB（+26%）。已接受此交换。

## 4. 架构

构建期与运行期彻底解耦：

```
[构建期 · 不进包]                    [产物]                 [运行期 · 进包]
scripts/build_registry.py    →   akshare/data/       →   akshare/registry.py
  ├─ 解析 docs/data/**/*.md        interfaces.json          ├─ 懒加载
  ├─ 读 __init__.py 导出表           (约 1.19 MB)            ├─ 关键词打分排序
  └─ 交叉校验 + 序列化                                        └─ 返回 DataFrame
                                                                    ↑
                                                            akshare/datasets.py
                                                          （复用现有路径解析机制）
```

| 组件 | 职责 | 依赖 | 预计规模 |
|---|---|---|---|
| `scripts/build_registry.py` | Markdown → 结构化记录；与导出表交叉校验；生成与 `--check` 两种模式 | 仅标准库（`re`/`ast`/`json`） | 200–250 行 |
| `akshare/data/interfaces.json` | 数据契约，提交进 git | — | — |
| `akshare/registry.py` | 懒加载、打分、格式化、异常 | `pandas` + `datasets.py` | 150–200 行 |
| `scripts/registry_baseline.json` | 存量漂移豁免清单 | — | — |
| `tests/test_registry.py` | 解析器与检索器各自的单元测试 | `pytest` | — |

### 边界规则

1. **解析器不感知 pandas，检索器不感知 Markdown。** 两者仅通过 JSON Schema 通信。将来若元数据改由装饰器提供，只需替换解析器，`registry.py` 不动。
2. **解析器不进 wheel。** 它是 `scripts/` 下的开发工具，避免包内多出仅 CI 使用的模块。
3. **数据懒加载。** `import akshare` 已需约 1.95 s，检索层不得增加启动开销。JSON 仅在首次调用检索 API 时读取并缓存至模块级变量。

## 5. 元数据 Schema

```json
{
  "schema_version": 1,
  "interfaces": [
    {
      "name": "index_all_cni",
      "module": "akshare.index.index_cni",
      "category": "index",
      "documented": true,
      "desc": "国证指数-最近交易日的所有指数的代码和基本信息",
      "url": "http://www.cnindex.com.cn/zh_indices/sese/index.html",
      "limit_desc": null,
      "params":  [{"name": "symbol", "type": "str", "desc": "symbol=\"399005\""}],
      "outputs": [{"name": "指数代码", "type": "str", "desc": "-"}],
      "example": "import akshare as ak\nindex_all_cni_df = ak.index_all_cni()\nprint(index_all_cni_df)"
    }
  ]
}
```

字段来源：`name`/`module`/`category` 来自 `__init__.py` 的 import 语句（category 取模块路径第二段）；其余字段来自 `docs/data/` 对应条目，缺失时为 `null` 或空列表。

`limit_desc` 对应文档中的「限量」字段（描述单次返回条数限制），刻意不命名为 `limit`，以免与 `ak.search(limit=20)` 的结果条数参数混淆。

### 三条不变量

**① 主键集合 = `__init__.py` 的实际导出，而非文档条目。**

以代码为准，保证 `ak.search()` 返回的每个结果都真实可调用，文档孤儿永远不会被推荐给 agent。75 个无文档接口仍然收录，标记 `documented: false`、`desc` 为空、category 由模块路径推断，使其至少可被发现。文档是可选增强，不是真相源。

非数据接口不收录，须以**显式排除清单**实现，不可依赖「category 能否推断」来判定：

```
EXCLUDE = {"__version__", "pro_api", "set_token", "get_token", "xt_api",
           "AkshareException", "APIError", "DataParsingError",
           "InvalidParameterError", "NetworkError", "RateLimitError"}
```

实测依据：1100 个顶层导出中，1094 个可从模块路径推断 category，6 个不可推断——而这 6 个**恰好只是异常类**（因其为相对导入 `from .exceptions`）。`__version__`（推断为 `_version`）、`pro_api`（推断为 `pro`）、`set_token` / `get_token`（推断为 `utils`）均在可推断的 1094 个之内，若按「不可推断即排除」实现会被错误收录。`xt_api` 位于 `try/except` 块内，不在顶层 `ImportFrom` 中，但仍应列入排除清单以防解析器将来改为遍历全部节点。

**② 产物不含时间戳、不含 akshare 版本号。**

任何随生成时刻或版本变化的字段都会制造 diff 噪声，使「重新生成无 diff」的门禁退化为每次发版必失败的噪音源。需要版本信息时运行期从 `ak.__version__` 获取。

**③ 输出按 `name` 字典序排序，JSON 序列化参数固定（`ensure_ascii=False`，固定 `separators`，末尾换行）。**

保证相同输入永远产出相同字节，这是门禁成立与 diff 可读的共同前提。

## 6. 检索算法与公开 API

### 打分：两级降级

```
第 1 级：按空白与标点切 token，逐 token 子串匹配
         "A股 历史行情" → ["A股", "历史行情"]
第 2 级：若命中接口数 < 3，降级为字符 2-gram 重试
         "A股历史行情"  → ["A股","股历","历史","史行","行情"]
```

必须逐 token 匹配再累加，否则「行情历史」无法命中描述中的「历史行情数据」。第 2 级用于救「用户不打空格」的情况，因噪音较高，仅在第 1 级结果不足时启用。

字段权重：

| 匹配位置 | 权重 | 理由 |
|---|---|---|
| `name` 完全等于查询 | 100 | 已知接口名时直接命中 |
| token 在 `name` 中 | 10 | 接口名信息密度最高 |
| token 在 `desc` 中 | 5 | 主要召回来源 |
| token 在 `category` 中 | 3 | 粗粒度过滤 |
| token 在输出列名中 | 2 | 支持「搜市盈率找返回该列的接口」的反查 |
| `example` | 0 | 不参与，噪音大 |

调节项：全部 token 命中的接口额外乘 1.5，使 AND 语义优先于 OR；`documented: false` 的接口乘 0.5 降权，可被发现但不与有文档者争排名。

### 公开 API

```python
ak.search(query, limit=20, category=None, documented_only=False) -> pd.DataFrame
# 列：接口名 / 类目 / 描述 / 有无文档 / 匹配分

ak.interface_info("stock_zh_a_hist") -> dict
# 完整元数据：params / outputs / example / url / limit_desc / module

ak.list_categories() -> pd.DataFrame
# 36 个类目及各自接口数，供 agent 粗筛
```

`search` 返回 DataFrame 与库整体风格一致；`interface_info` 返回 dict，因 params/outputs 为嵌套结构。匹配分保留在返回值中，供 agent 判断置信度并决定是否改写查询重试。

命名无冲突：现有 1100 个导出中仅 `stock_hot_search_baidu`、`stock_research_report_em` 含 "search"。这三个函数属于元 API（与 `set_token`、`pro_api` 同类），故采用短名而非 `<domain>_<topic>_<source>` 的数据接口命名惯例。

三个函数需加入 `akshare/__init__.py` 的导出，否则无法以 `ak.` 前缀调用。

## 7. CI 门禁

`scripts/build_registry.py --check` 执行三项校验：

1. **产物同步**：重新生成并与仓库中 `interfaces.json` 逐字节比对，不一致则失败，提示运行生成命令。
2. **导出但无文档**：当前 75 个存量写入 `scripts/registry_baseline.json` 豁免；新增接口无文档则失败。

   75 的推导：顶层导出 1100 个，经 `EXCLUDE` 排除 6 个异常类与 4 个非数据接口后 `exports` 为 1090；文档条目 1018 条，与 exports 交集 1015，相减得 75。

   两次修正说明：第 1 节的 95 是基于全部 1100 个导出且只匹配半角冒号的原始统计。排除非数据接口后降为 85；再修正解析器对全角冒号 `接口：` 的容错后，又有 10 个本就有文档的接口（`stock_info_global_em/sina/ths/futu/cls`、`stock_info_cjzc_em`、`stock_rank_cxg/cxd/lxsz/lxxd_ths`）被正确识别，最终为 75。
3. **文档但无导出**：当前 3 个同样计入 baseline。

**棘轮语义为双向**：缺口集合既不得超出 baseline（新增违规失败），baseline 中也不得残留已修复项（修复后未同步删除同样失败）。否则 baseline 将腐烂为无人维护的过期清单。

**作为独立 job 运行**，仅在 `ubuntu-latest` 与单一 Python 版本上执行。现有 `main_dev_check.yml` 为 3 OS × 4 Python 的 12 格矩阵，本校验与平台无关，无需重复 12 次。

## 8. 错误处理

| 场景 | 行为 |
|---|---|
| `search()` 无结果 | 返回空 DataFrame 但保留列结构，不抛异常（符合 pandas 惯例） |
| `interface_info()` 传入未知名称 | 抛 `InvalidParameterError`，并在消息中回显打分最高的 3 个候选 |
| registry 文件缺失或损坏 | 抛 `DataParsingError`，提示重装或重新生成 |

第二条复用同一打分函数，零额外成本：agent 拼错接口名时可直接从异常消息中获得正确候选并自我纠正，而非收到无信息量的 `AttributeError`。这也使 `exceptions.py` 这套目前仅 5 个文件用到的异常体系首次具备真实使用场景。

## 9. 测试策略

现有 `tests/` 仅 2 个断言且不联网。检索层测试天然无需网络，将成为本仓库第一批具备实质验证意义的 CI 测试。

1. **解析器单元测试**：以内联 Markdown 片段为输入，断言解析结果。**必须包含跨表污染回归用例**——构造「输入参数表后紧跟另一张数据表」的样本（真实形态见 `article_oman_rv`），断言不串表。原型实现在此处已知会出错（以「标题后固定字符数内的所有表格行」为界会跨表抓取），须先写出失败的测试再修复。表格边界应以「下一个标题或空行分隔的新表」为终止条件。
2. **检索器单元测试**：使用小型 fixture registry（数十条，不加载真实 1.19 MB），覆盖打分排序、2-gram 降级触发条件、category 过滤、无文档降权、三类异常。
3. **不变量集成测试**：加载真实 registry，断言其中每个 `name` 均可 `getattr(ak, name)` 成功，直接守住不变量 ①，并在将来有人删除函数而未删文档时立即报警。

## 10. 交付物清单

- `scripts/build_registry.py`（生成 + `--check` 双模式）
- `scripts/registry_baseline.json`
- `akshare/data/interfaces.json`
- `akshare/registry.py`
- `akshare/datasets.py` 新增 `get_registry_json()`
- `akshare/__init__.py` 新增三个 API 的导出，并按仓库惯例追加版本记录行
- `tests/test_registry.py`
- `.github/workflows/main_dev_check.yml` 新增独立 registry-check job
- 按仓库发布约定同步 `_version.py`、`docs/changelog.md`、`docs/introduction.md`

## 11. 验收标准

1. `ak.search("A股 历史行情")` 返回非空 DataFrame，且首条结果为可调用接口。
2. `ak.search()` 返回的全部接口名均可通过 `getattr(ak, name)` 取到。
3. `import akshare` 耗时相对当前基线无可测量增长（懒加载生效）。
4. 连续两次执行生成命令产出字节完全一致的 `interfaces.json`。
5. `--check` 在当前仓库状态下通过；人为删除任一接口的文档条目后失败。
6. `pytest` 全绿且全程无网络请求。

## 12. 已知遗留

以下为门禁将记录、但**不在本次修复范围**的存量问题，各自单独提 PR：

| 接口 | 状态 | 建议处置 |
|---|---|---|
| `fortune_rank` | 函数存在于 `fortune/fortune_500.py:40`，历史修复 4 次，当前未导出 | 补 `__init__.py` 导出 |
| `option_czce_hist` | changelog 更名表记录 1.17.68 已更名为 `option_hist_yearly_czce`，文档未同步 | 删除过期文档条目 |
| `stock_zh_a_tick_tx` | 函数存在未导出，近期仅有 docs 变更 | 需维护者判断是补导出还是正式下线 |
| 75 个导出而无文档的接口 | 见 baseline 清单 | 逐步补文档，baseline 只减不增 |
