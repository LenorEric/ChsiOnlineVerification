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

```python
        verify_data = {
            'portrait': portrait,  # 头像
            'title': title,  # 标题
            'name': name,  # 姓名
            'gender': gender,  # 性别
            'birthday': birthday,  # 生日
            'ethnic': ethnic,  # 民族
            'pid': pid,  # 身份证号
            'university': university,  # 学校
            'degree': degree,  # 层次
            'school': school,  # 学院
            'class': classes,  # 班级
            'major': major,  # 专业
            'sid': sid,  # 学号
            'form': forms,  # 学制
            'type': types,  # 类型
            'system': system,  # 形式
            'admission': admission,  # 入学时间
            'state': state  # 学籍状态
        }
```

