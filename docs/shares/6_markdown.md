Markdown漫游指南
========


Markdown 的目标是实现「易读易写」，成为一种适用于网络的书写语言。

* Markdown 的语法全由一些精挑细选的符号所组成，其作用一目了然。
* 它实际上是个非常简单、非常容易学习的语法。这个语法简单到每个人都可以在5分钟以内学会。应该是为数不多，你真的可以彻底学会的语言。
* 更重要的是，Markdown语法所有要素，是与写作的习惯一脉相承的，套用句俗语：仅为写作而生。[1][1]


比如：

在文字两旁加上星号，看起来就像*强调*；两个星号，**粗体**。

<pre>*强调*  **粗体**</pre>

要写引用网址了，就是这么写[]再加个()，如：[豆瓣](http://www.douban.com)  [关于安问](/about   "可选的说明:关于安问~~~")

<pre>
[豆瓣](http://www.douban.com)
[关于安问](/about   "可选的说明:关于安问~~~")
</pre>

要引用大段文字，就是直接 >后面写引用
>习惯是人生最大的指导。

<pre>>习惯是人生最大的指导。</pre>

标题：在行首插入 1 到 6 个 # ，对应到标题 1 到 6 阶
# 标题 1
## 标题 2
### 标题 3

<pre>
# 标题 1
## 标题 2
### 标题 3
</pre>

无序列表：在使用星号、加号或者减号来做为列表的项目标记(星号后要加空格)

* 安问
* 柏舟
* 成长

<pre>
* 安问
* 柏舟
* 成长
</pre>

有序列表则是使用一般的数字接着一个英文句点作为项目标记：

1. Red
2. Green
3. Blue

<pre>
1. Red
2. Green
3. Blue
</pre>

图片

图片的语法和链接很像。（title 是选择性的）：

![豆瓣](http://img1.douban.com/pics/nav/lg_main_a10.png "豆瓣logo")

<pre>
![豆瓣](http://img1.douban.com/pics/nav/lg_main_a10.png "豆瓣logo")
</pre>

####进阶

参考形式的链接让你可以为链接定一个名称，之后你可以在文件的其他地方定义该链接的内容：

<pre>
I get 10 times more traffic from [Google][1] than from
[Yahoo][2] or [MSN][3].

[1]: http://google.com/ "Google"
[2]: http://search.yahoo.com/ "Yahoo Search"
[3]: http://search.msn.com/ "MSN Search"
</pre>

代码块

<pre>
```python
def hello():
    return True
```
</pre>

一切就这么简单。Markdown之所以越来越流行,是因为它足够简单。

参考文献：

1. [为什么Markdown+R有较大概率成为科技写作主流？][1]

2. [Markdown 语法说明(简体中文版)][2]

3. [Markdown Syntax Documentation][3]

[1]:http://www.yangzhiping.com/tech/r-markdown-knitr.html
[2]:http://wowubuntu.com/markdown/basic.html
[3]:http://daringfireball.net/projects/markdown/syntax