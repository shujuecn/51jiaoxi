# 51jiaoxi

下载[教习网](https://www.51jiaoxi.com/)的成套试卷

示例链接：

- ```https://www.51jiaoxi.com/album-37703.html```
- ```https://www.51jiaoxi.com/album-24388.html```

## 方法

遍历每套试卷详情页，下载分试卷的预览图，合并为PDF。

## 使用

### Mac OS

```
$ git clone https://github.com/shujuecn/51jiaoxi.git
$ cd 51jiaoxi
$ python3 51jiaoxi.py
````

输入成套试卷链接后，Enter...

## Bug

- 当成套资料的详细页面中包含多个文件时，仅能下载首个文件，例如：[示例页面](https://www.51jiaoxi.com/doc-13446122.html)。

