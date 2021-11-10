# DeepL 翻译器 for nonebot2

一个基于[DeepL](https://www.deepl.com/)的[nonebot2](https://github.com/nonebot/nonebot2)翻译插件



## 安装

1. 在你的插件目录下克隆本项目

```shell
git clone https://github.com/Nova-Noir/nonebot_plugin_deepl_translator.git
```

2. 在`.env`下添加配置项

```
DEEPL_API_KEYS = ['Your_API_Here', 'Another_API']
```

3. 重启你的BOT

## 使用

你可以轻松通过使用*语言代码*来*回复你想要翻译的聊天*来翻译句子

> 例如:
>
> > A: Hello, World!
> >
> > > A: Hello, World!
> >
> > B:cn
> >
> > 
> >
> > > A: Hello, World!
> >
> > Bot： 你好，世界！
>
> 注意，这里需要使用QQ的**回复**功能，回复自带的@可以不删除。

![image](https://user-images.githubusercontent.com/68760718/141055606-a9963714-b08f-4a2d-8de5-df0508f7fbb4.png)



同时，你也可以通过在想要发送的句子之前添加*语言代码*来自动翻译你想要发送的句子

> 例如:
>
> > A: jp你好世界
> >
> >
> >
> > > A: jp你好世界
> >
> > Bot: ハロー・ワールド

![image](https://user-images.githubusercontent.com/68760718/141055694-09509677-8147-480c-bfaf-eb9a1dde221a.png)


### 语言代码

[deepl_translator](https://github.com/Nova-Noir/nonebot_plugin_deepl_translator)内置了多个常用的语言代码，语言代码对大小写不敏感，你可以在下表中找到对应

| 语言代码 | DeepL代码 |        语言        |
| :------: | :-------: | :----------------: |
|    CN    |    ZH     |      Chinese       |
|    JP    |    JA     |      Japanese      |
|    EN    |   EN-US   | English (American) |
|    FR    |    FR     |       French       |
|    RU    |    RU     |      Russian       |
|    DE    |    DE     |       German       |
|    ES    |    ES     |      Spanish       |

你也可以自主添加别名或添加新的语言，只需打开`__init__.py`，找到`country_code`并添加项目即可，他的格式应该是`'语言代码': 'DeepL代码'`

DeepL代码可以在[这里](https://www.deepl.com/zh/docs-api/translating-documents/uploading/)找到
