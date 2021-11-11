---
title: '[LeetCode-1181]使数组严格递增'
toc: true
tags:
  - 动态规划
categories:
  - - algo
    - LeetCode
    - 每日一题
date: 2021-11-11 09:11:55
updated:
---

[原题链接](https://leetcode-cn.com/problems/make-array-strictly-increasing/)

## 题目描述
给定两个数组, 计算使得数组A严格递增的操作次数。

一次操作定义为: 选数组B任意一个数, 替换数组A任意一个数。

<!--more-->

## 约定
- arr1数组认为是数组A, 其长度为`n`
- arr2数组认为是数组B, 其包含不重复的元素个数为`m`
- 数组下标均从**1**开始

## 思路
- **一些观察**:
  1. 数组B中的**重复数**是没有用的. 如果使用数组B中的重复数, 要么导致数组A不严格单调递增(操作到了不同位置), 要么导致操作次数增加(操作到了同一位置).
  2. 数组B的**顺序**是无所谓的.  

- **问题转化**
  1. 有了上述观察, 我们可以将问题首先进行转化. 首先将数组B中的重复元素去掉, 并对数组B排序, 记为$B'$.
  2. 这样问题可以转化成: 从数组$A$和数组$B'$(严格单调递增)中找到一条长度为$n$且**严格单调递增的路线**, 且路线上从`A`跳到`B'`的次数最少

![转化后问题示意图](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/hexo-theme-icarus/source/img/2021/11/11/LeetCode-1187.png)

- 转化后的问题可以使用动态规划来解决
- **动态规划**
    - 状态表示: 
        1. $f[i][j][0]$:表示路线走了长度`i`, 考虑了数组$B'$的前`j`个数, 且最后走到数组$A$的`i`位置上.
        2. $f[i][j][1]$:表示路线走了长度`i`, 考虑了数组$B'$的前`j`个数, 且最后走到数组$B'$的`j`位置上.
    - 状态计算:
        1. 根据定义首先有: $f[i][j][0]$ = $f[i][j - 1][0]$
            - 若$A[i] > A[i - 1]$, 则有$f[i][j][0]$ = $f[i - 1][j][0]$
            - 若 $A[i] > B'[j]$, 则有$f[i][j][0]$ = $f[i - 1][j][1]$
        2. 对于$f[i][j][1]$:
            - 若$B'[j] > A[i - 1]$, 则有$f[i][j][1]$ = $f[i - 1][j - 1][0] + 1$. 表示第`i`步从$A$数组的`i - 1`位置跳到了$B'$的`j`位置
            - 若$B'[j] > B[j - 1]$, 则有$f[i][j][1]$ = $f[i - 1][j - 1][1] + 1$. 表示第`i`步从$B'$数组的`j - 1`位置跳到了$B'$的`j`位置

- **最后的答案**
    1. 若最后一步在$A$数组上, 则答案为$f[n][m][0]$.
    2. 若最后一步在$B'$数组上, 枚举$f[n][j][1]$, 其中$j\in[0, m)$.


## Code
```cpp
const int N = 2010, INF = 0x3f3f3f3f;
class Solution {
public:
    int f[N][N][2];
    int makeArrayIncreasing(vector<int>& arr1, vector<int>& arr2) {
        memset(f, 0x3f, sizeof(f));
        sort(arr2.begin(), arr2.end());
        arr2.resize(unique(arr2.begin(), arr2.end()) - arr2.begin());
        
        int n = arr1.size(), m = arr2.size();
        
        for (int i = 0; i <= m; i ++ ) {
            f[0][i][0] = f[1][i][0] = 0; 
            if (i)
                f[1][i][1] = 1;
        }
        
        for (int i = 2; i <= n; i ++ )
            for (int j = 1; j <= m; j ++ ) {
                f[i][j][0] = f[i][j - 1][0];
                if (arr1[i - 1] > arr1[i - 2])
                    f[i][j][0] = min(f[i][j][0], f[i - 1][j][0]);
                if (arr1[i - 1] > arr2[j - 1])
                    f[i][j][0] = min(f[i][j][0], f[i - 1][j][1]);
                if (arr2[j - 1] > arr1[i - 2])
                    f[i][j][1] = f[i - 1][j - 1][0] + 1;
                if (j >= 2 and arr2[j - 1] > arr2[j - 2])
                    f[i][j][1] = min(f[i][j][1], f[i - 1][j - 1][1] + 1);
            }

        int ans = INF;
        for (int i = 1; i <= m; i ++ )
            ans = min({ans, f[n][i][0], f[n][i][1]});
        if (ans == INF)
            ans = -1;
        return ans;
    }
};
```

## 复杂度分析
1. 时间复杂度$O(n^2)$
2. 空间复杂度$O(n^2)$

----
**欢迎讨论指正**