Markdown漫游指南
========


Markdown 的目标是实现「易读易写」，成为一种适用于网络的书写语言。推荐写作者学会该语言。

* Markdown 的语法非常简单，全由一些精挑细选的符号所组成，其作用一目了然。
* 它实际上非常简单、容易学习。大家都可以在5分钟以内学会。是为数不多，你真地可以彻底学会的语言。
* 更重要的是，Markdown语法所有要素，是与写作的习惯一脉相承的，套用句俗语：仅为写作而生。[1][1]
* 纯文本，故兼容性极强，可以用所有文本编辑器打开。
* 格式转换方便，Markdown 的文本你可以轻松转换为 html、电子书等。
* Markdown标记语言写出的文字有极好的可读性。

学习开始~

### 标题
在行首插入 1 到 6 个 # ，对应到标题 1 到 6 级。
<pre>
# 标题 1
## 标题 2
### 标题 3
</pre>
# 标题 1
## 标题 2
### 标题 3

注：# 和「标题」之间保留一个字符的空格。


### 列表
无序列表：使用减号、加号或者星号来做为列表的项目标记(减号后要加空格)
<pre>
- 安问
- 成长
</pre>
- 安问
- 成长

有序列表则是使用一般的数字接着一个英文句点作为项目标记(句点后要加空格)
<pre>
1. Red
2. Green
3. Blue
</pre>
1. Red
2. Green
3. Blue
注：普通文本后如果需要显示列表，需要空一行

### 链接和图片
要引用网址了，就是 [显示文本](链接地址)
<pre>
[豆瓣](http://www.douban.com)  
[关于安问](/about   "可选的说明:关于安问~~~")
</pre>
[豆瓣](http://www.douban.com)  [关于安问](/about   "可选的说明:关于安问~~~")

图片的语法和链接很像, 只是前面多了一个 ！
<pre>
![](http://img1.douban.com/pics/nav/lg_main_a10.png)
![豆瓣](http://img1.douban.com/pics/nav/lg_main_a10.png  "豆瓣logo")
</pre>
![](http://img1.douban.com/pics/nav/lg_main_a10.png)
![豆瓣](http://img1.douban.com/pics/nav/lg_main_a10.png  "豆瓣logo")


### 引用
我们写作的时候有时需要引用他人的文字，在 Markdown 中，你只需要在你希望引用的文字前面加上 > 就好。 > 和文本之间要保留一个字符的空格。
如：
<pre>
> 习惯是人生最大的指导。
</pre>
> 习惯是人生最大的指导。


### 粗体和斜体
<pre>
在文字两旁加上星号，看起来就像*强调*；两个星号，**粗体**
</pre>
在文字两旁加上星号，看起来就像*强调*；两个星号，**粗体**


###  换行
Markdown 的换行稍微有点特殊。换行我们分「一般换行」和「段落换行」。  
比方说，诗的换行都是「一般换行」，也就是一行紧接着一行，中间没有段落间隔。这种「一般换行」的语法是，在每句话的末尾保留两个字符的「空格」，例如你输入：

朝辞白帝彩云间  
千里江陵一日还  
两岸猿声啼不住  
轻舟已过万重山   
注：上方的例子里面，每句话的末尾都有两个空格。

另外一种换行是「段落换行」，常用于段落，两段文本之间会有一行的间隔，这种换行的语法没有特殊之处，只需要两段之间多加一行间隔之即可，例如你输入：

朝辞白帝彩云间 ，千里江陵一日还，

两岸猿声啼不住，轻舟已过万重山。


#### 进阶
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

自动链接

Markdown 支持以比较简短的自动链接形式来处理网址和电子邮件信箱，只要是用方括号包起来， Markdown 就会自动把它转成链接。一般网址的链接文字就和链接地址一样，例如：

    <http://anwensf.com/>
会转为：
<http://anwensf.com/>

一切就这么简单。Markdown之所以越来越流行,是因为它足够简单。试试吧～

在线编辑器

-  <http://dillinger.io/>
-  <http://markable.in/editor/>
- <http://anwensf.com/edit>

浏览器插件

-  MaDe (Chrome)


参考文献：

1. [为什么Markdown+R有较大概率成为科技写作主流？][1]
2. [Markdown 语法说明(简体中文版)][2]
3. [Markdown Syntax Documentation][3]
4. [献给写作者的 Markdown 新手指南][4]

[1]:http://www.yangzhiping.com/tech/r-markdown-knitr.html
[2]:http://wowubuntu.com/markdown/basic.html
[3]:http://daringfireball.net/projects/markdown/syntax
[4]:http://jianshu.io/p/q81RER