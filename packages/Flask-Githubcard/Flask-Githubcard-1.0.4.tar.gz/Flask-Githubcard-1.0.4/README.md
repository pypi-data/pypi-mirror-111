# flask-githubcard
一个Flask的拓展程序，通过该程序可以快速在前端页面渲染出指定github仓库的相关信息卡片。

[English Document](https://github.com/weijiang1994/flask-githubcard/blob/main/README-EN.md)

### 快速开始
首先通过`pip`安装依赖程序`flask-githubcard`
```shell
pip install flask-githubcard
```
**初始化扩展**
```python
from flask import Flask
from flask_githubcard import GithubCard

app = Flask(__name__)
githubcard = GithubCard(app)
```

**初始化依赖**

在你基类模板的`<head>`块初始化扩展的依赖
```html
{{githubcard.init_css()}}
{{githubcard.init_js()}}
```

**渲染github卡片**
```html
<div>
    {{githubcard.generate_card()}}
</div>
```

之后访问你的页面，效果如下

![1623293427414.png](https://7.dusays.com/2021/06/10/66d2716789d8d.png)

### 进阶

在使用扩展程序的时候我们可以通过app.config[some] 来配置，配置项列表如下

|  配置项   | 说明  |  默认 | 可选 |
|  ----  | ----  | ----| ----|
| GITHUB_USERNAME  | 需要展示的github用户名 | weijiang1994| None |
| GITHUB_REPO  | 需要展示的github仓库名 | Blogin| None |
| theme  | 渲染主题配色 | default | default/darkly|

同时扩展内置了两款主题，默认的亮色，如果需要改变主题为darkly通过下面的代码即可实现
```html
<head>
    {{githubcar.init_css(theme='darkly')}}
</head>
<div>
    {{githubcard.generate_card('darkly')}}
</div>
```

darkly主题效果如下图

![1623294104103.png](https://7.dusays.com/2021/06/10/736fed4674429.png)


获取原始数据

```python
from flask import Flask
from flask_githubcard import GithubCard
app = Flask(__name__)
githubcard = GithubCard(app)

@app.route('/ajax')
def ajax():
    return jsonify(githubcard.create(theme='darkly').get_raw_data())
```

### 注意

- 由于使用了github的api在没有进行授权的情况下，唯一IP在每小时内限制的访问次数为60次，超过60次则会报403,
  如果访问频率过高，请前往github上授权账号；
- 在国内访问github会出现超时的现象，可能会导致网页一直无法打开!