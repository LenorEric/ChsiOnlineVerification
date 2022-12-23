# ChsiOnlineVerification
学信网学籍/学历在线验证报告查询 API Python

## 使用方法

见 presentation.py

```Python
import chsiverify

chsiverify.verify_chsi(verify_code)
```

## 输入参数

| 名称        | 类型 | 规则                   |
| ----------- | ---- | ---------------------- |
| verify_code | str  | 通常为 16 位大写字符串 |

## 返回值

| 种类               | 类型 | 规则（内容）                               |
| ------------------ | ---- | ------------------------------------------ |
| 不符合格式的验证码 | str  | 系统检测到非法访问，不合要求的在线验证码！ |
| 无效的验证码       | str  | 此在线验证码无效！                         |
| 有效返回           | dict | 见 verify_data                             |

```
    verify_data = {
        'title': 标题,
        'name': 姓名,
        'gender': 性别,
        'pid': 身份证号,
        'ethnic': 民族,
        'birthday': 出生日期,
        'portrait': 录取照片,
        'institution': 院校,
        'degree': 层次,
        'school': 院系,
        'class': 班级,
        'major': 专业,
        'sid': 学号,
        'form': 形式,
        'admission': 入学时间,
        'system': 入学时间,
        'type': 类型,
        'state': 学籍状态
    }
```

