---
title: '[LeetCode-319]灯泡开关'
toc: true
tags:
  - 思维
categories:
  - - algo
    - LeetCode
    - 每日一题
date: 2021-11-15 19:50:16
updated:
---

[原题链接](https://leetcode-cn.com/problems/bulb-switcher/)

## 题目描述
给出`n`个灯泡(初始全部熄灭)并且操作`n`次, 第`i`次把所有是`i`的倍数处的灯泡的开关状态取反. 求`n`次操作后亮着的灯泡数目.

<!--more-->

## 思路
- 考虑某一个灯泡`i`在`n`次操作中被操作的次数, 可以发现该灯泡会被它的**所有因子**操作. 比如`8`会在第1、2、4、8次操作时操作.
- 若一个灯泡被操作`k`次, 那么该灯泡一定有`k`个**不同**的因子. 且该灯泡最后的状态唯一取决于`k`的奇偶. 即若`k`为偶数则灭, `k`为奇数则亮.
- 问题转化成求$1 - N$中**含有奇数个不同因子的数的个数**. 考虑到所有因子都是成对出现的, 若数`K`有奇数个不同的因子, 那么某个因子一定出现两次, 该因子一定是$\sqrt K$, 即`K`必为完全平方数. 
- 最后问题转化成求$1 - N$中完全平方数的个数.

## Code
```cpp
using LL = long long;
class Solution {
public:
    int bulbSwitch(int n) {
        if (n == 0)
            return 0;
        int cnt = 0;
        for (LL i = 1; i * i <= n; i ++ )
            cnt ++ ;
        return cnt;
    }
};
```

## 复杂度分析
1. 时间复杂度$O(\sqrt N)$
2. 空间复杂度$O(1)$

----
**欢迎讨论指正**