---
title: '[LeetCode-1218]最长定差子序列'
toc: true
tags:
  - 动态规划
categories:
  - - algo
    - LeetCode
    - 每日一题
date: 2021-11-08 09:59:38
updated:
---


[原题链接](https://leetcode-cn.com/problems/longest-arithmetic-subsequence-of-given-difference/)

## 题目描述
求数组中最长的等差子序列的长度, 且公差为定值

<!--more-->

## 思路
- 因为公差为`定值`, 因此当子序列最后一个数确定时, 倒数第二个数一定是确定的, 我们可以使用一个数来代表所有以`倒数第二个数`为结尾的最长等差子序列.
- 使用`动态规划`解决：
  1. 状态表示: $f[i]$表示以`i`为结尾的最长的等差子序列
  2. 状态转移: $f[i] = f[i - d] + 1$

## Code
```cpp
class Solution {
public:
    int longestSubsequence(vector<int>& arr, int d) {
        unordered_map<int, int> f;
        int ans = 0;
        for (auto& c : arr) {
            f[c] = 1 + f[c - d];
            ans = max(ans, f[c]);
        }
        return ans;
    }
};
```

## 复杂度分析
1. 时间复杂度$O(n)$
2. 空间复杂度$O(n)$

----
**欢迎讨论指正**