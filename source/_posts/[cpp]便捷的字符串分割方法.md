---
title: '[cpp]便捷的字符串分割方法'
toc: true
date: 2021-10-27 15:52:07
updated:
categories: cpp
tags: 
    - cpp
    - 字符串分割
---

## 前言

不像python的str提供的内置`split`方法一样方便的进行字符串分割，c++的`string`模板库没有直接提供分割字符串的成员方法。偶然在看《c++prime》时看到`string`模板库提供`getline`方法, 利用方法可以实现自定义分隔符分割字符串。

## 使用getline进行分割

getline函数接受三个参数，分别是`input`(the stream to get data from), `str`(the string to put the data into), `delim`(the delimiter character) 。该函数返回值是`input`。

其中`input`是`istream`类型，比如`cin`, `istringstream`等继承自`istream`的类，分割符为`char`型字符。

为了获取带空格的字符串，一般使用`getline(cin, str)`进行读取字符串。读取待分割字串到str中后，我们需要用其实例化一个`istringstream`作为`getline`的`input`才能完成分割。

分割过程中需要注意一点: 若待分割字符串中包含连续的分割字符，这种情况会得到空字符串。多数情况下我们不期望得到空字符串，因此需要判断分割得到的字符串是否为空。

## Demo

### Code

```cpp >> folded
#include <iostream>
#include <sstream>
#include <string>

using namespace std;

int main() {
  string line, word;
  getline(cin, line);
  istringstream input(line);

  while (getline(input, word, ' ')) {
    if (!word.empty())
      cout << "word : " << word << endl;
  }
  return 0;
}

```

### 结果

<div style="align: center">
<img src="/img/2021/10/27/stringsplit.png"/>
</div>
<!-- ![result](/img/2021/10/27/stringsplit.png) -->

----

**欢迎讨论指正**


 