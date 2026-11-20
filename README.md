# 中文营地学习路径比较与跨校学分承接

所有记录都是本地合成数据。CSV 为 UTF-8 且有首行字段名；JSON 空值表示未报告。

## 补充来源说明

- `catalog.json`：院校课程目录和营地任务题本。课目要求 `distinct=true` 时，目标所用作答须独立。`credit` 是申请占用的整数可转学分，不代表观察次数。`support_basis` 声明抵免须另有历史证据的目标、可比较人群、最低独立营期数以及观察类型；营期数够不等于该证据支持抵免。不同学期、不同校的版本可并行生效。
- `cohorts.json`：匿名历史学习路径，按营地开营次序分组。多组共享教学时使用同一 `teaching_cluster`；`task_id` 一致的多个来源是同一记录。`checkpoint` 的 `available_after` 是成绩可见时点；`evidence` 是原作答编号，不由成绩行号代替。
- `registrar.json`：本期分项、学分申请和校方回执。`attempt` 是作答身份；`group` 非空表示共享支持来源。更正规则只变被指定的分项。`confirmed` 是学校已入账的回执，`enrolled` 是实际入班回执，两者不等价。
- `followup_exchange.json`：晚到的一批历史后测、相关受理资料和后测勘误通知。`cohorts` 延用历史学习路径的字段；`profiles` 以 `person` 引用本期分项和申请，`level_at_entry` 和 `orientation` 与历史同口径。仅观察时间在 `archive_day_offset + 查询时点` 之前或正好到达的后测可用于查询；本期受理日和档案日的换算取自这里的日历。`corrections.recv_at` 用本期受理日，`effective_archive_day` 用档案日。相同 `observation` 下的更正只改其 `changes` 所列来源事实；不同观察记录不因恰好同分而相同。
- `makeup_offers.json`：院校补测的登记资料。`windows` 中 `result_due` 是预计可用日，不代表成绩已出。`recognition.open_from` 指认定适用于在该日或其后开始的考试，同校也按所列目标和考试模式认定。已 `reserved`、`confirmed` 的同一 `booking` 只占一个座位，直到提供方收到 `released`；`requested` 只表示打算报名。`person`、`application` 回指教务来源。补测资料的日期都在本期受理日历上。

## 本地检查

使用 Python 3.11 标准库。当前可运行的是来源契约检查：

```sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
```
