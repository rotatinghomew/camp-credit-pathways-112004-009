# 交流结对续联的双向观察与跟进名额

伙伴回访以整日为单位，day 为活动结束后的天数，可有迟交；以 collected 决定决策时是否知道该记录。关系的开始和结束由双方报名约定或正式退出消息给出。 数据均为合成。

CSV 使用 UTF-8、首行字段名，`-` 表示来源未填；JSON 使用原生布尔、字符串及数字。没有另行给定时，`seq` 只用于还原各条来件的先后，不是业务日期。

## 来源说明

- `pairs.csv`：active_until 是约定随访截止，不是已经终止；一个人可在多对中。
- `observations.csv`：reporter 为签名来信者，interaction 是可匹配交流标识，起止表示那次事件可发生的日区间。group 类型是公开活动，不能算入结对双向接触。
- `permission.csv`：check 可单边确认、meeting 可安排双边会谈；exit 表示退出关系（不是权限撤回）。预约回执给出 person 所占用的自己的时段，不代替另一个人的同意。
- `slots.csv`：已经预约的单边、双边任务会占人和志愿者。past_actions 按已走完的观察窗口记录真实可确认范围，不把观察本身当实际重联。

## 数据清单

- `pairs.csv`：`pair`, `left`, `right`, `area`, `start`, `active_until`。
- `observations.csv`：`id`, `pair`, `reporter`, `kind`, `interaction`, `earliest`, `latest`, `collected`。
- `permission.csv`：`day`, `person`, `pair`, `check`, `meeting`, `exit`。
- `slots.csv`：`id`, `day`, `start`, `length`, `volunteer`。
- `bookings.csv`：`at`, `id`, `slot`, `pair`, `person`, `kind`, `state`。
- `past_actions.csv`：`action`, `type`, `region`, `lag_days`, `confirmed`, `unresolved`, `window_mature`。
- `policy.json`：配置对象。

## 本地检查

使用 Python 3.11 标准库，无需安装第三方依赖。构建检查和来源契约测试：

```sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
```
