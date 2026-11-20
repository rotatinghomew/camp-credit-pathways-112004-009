# 中文营地学习路径比较与跨校学分承接

所有记录都是本地合成数据。CSV 为 UTF-8 且有首行字段名；JSON 空值表示未报告。

## 补充来源说明

- `catalog.json`：院校课程目录和营地任务题本。课目要求 `distinct=true` 时，目标所用作答须独立。`credit` 是申请占用的整数可转学分，不代表观察次数。`support_basis` 声明抵免须另有历史证据的目标、可比较人群、最低独立营期数以及观察类型；营期数够不等于该证据支持抵免。不同学期、不同校的版本可并行生效。
- `cohorts.json`：匿名历史学习路径，按营地开营次序分组。lesson 有多组共享教学时同 teaching_cluster；task_id 一致的多个来源是同一记录。checkpoint 在对应观察结束且 rec_date 已到时才有可见成绩。
- `registrar.json`：本期分项、学分申请和校方回执。attempt 是作答身份；group 非空表示共享支持来源。更正规则只变被指定的分项；应用时不覆盖已确认占用。

## 本地检查

使用 Python 3.11 标准库。当前可运行的是来源契约检查：

```sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
```
