---
title: "[LeetCode-598]范围求和II"
toc: true
tags:
  - 思维
categories:
  - [algo, LeetCode, 每日一题]
date: 2021-11-07 23:19:32
updated:
---


[原题链接](https://leetcode-cn.com/problems/range-addition-ii/)

## 题目描述
多次给矩阵`M`的某个子矩阵全部加1, 求最后矩阵中最大值出现的次数

<!--more-->

## 思路
- 注意到关键的一点: 每次加的子矩阵的左上角均为`[0, 0]`, 因此n次操作后, 最大值一定`全部出现在`以`[0, 0]`为左上角的某个子矩阵中, 我们只需确定这个子矩阵的长宽即可
- 这个子矩阵其实是每次操作的`交集`, 只有这个`交集`中的位置才能保证每次都被加1
- `x`和`y`操作的`交集`是独立的, 分开求解即可

## Code

```cpp
class Solution {
public:
    int maxCount(int m, int n, vector<vector<int>>& ops) {
        int x = m, y = n;
        for (auto& op : ops) {
            x = min(x, op[0]);
            y = min(y, op[1]);
        }
        return x * y;
    }
};
```

## 复杂度分析
1. 时间复杂度$O(N * M)$: 遍历矩阵即可求出答案
2. 空间复杂度$O(1)$: 仅需常数空间存储`x`和`y`的交集

----
**欢迎讨论指正**