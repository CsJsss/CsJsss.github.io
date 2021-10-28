---
title: '[LeetCode-869]重新排序得到2的幂'
tags:
  - LeetCode
  - 每日一题
date: 2021-10-28 10:51:44
updated:
categories:
  - [algo, LeetCode, 每日一题]
---

[原题链接](https://leetcode-cn.com/problems/reordered-power-of-2/)

## 题目描述

判断一个数字重新排列后能否成为2的某个幂次.

## 思路

1. 模拟: 考虑到`数据范围`很小, 我们可以暴力枚举该数的所有排列, 然后判断该数是否为2的幂次.
2. 模拟: 考虑到`2的幂次的个数`很少, 我们可以首先`预处理`出来所有的2的幂次, 然后判断该数是否为某个2的幂次。由于数字可以重新排列, 因此只需记录`词频`, 即若两个数词频相同, 则一个数一定可以通过重新排列变成另外一个数.

## Code

```cpp
// 解法1
class Solution {
public:
    static const int M = 11;
    // 辅助函数: 获取x的十进制表示
    vector<int> get(int x) {
        vector<int> ret;
        while (x) {
            ret.push_back(x % 10);
            x /= 10;
        }
        return ret;
    }
    bool reorderedPowerOf2(int n) {
        // 记录所有合法方案的十进制表示
        set<vector<int>> st;
        for (int i = 0; i < 31; i ++ ) 
            st.insert(get(1 << i));

        vector<int> cur = get(n);
        sort(cur.begin(), cur.end());

        int ret = 0;
        // cpp利用next_permutation()函数暴力枚举该数的所有排列
        do {
            ret += st.count(cur);
        } while (next_permutation(cur.begin(), cur.end())) ;

        return ret;
    }
};
```

```cpp 
// 解法2
class Solution {
public:
    static const int M = 11;
    // 辅助函数: 统计数x的词频
    vector<int> get(int x) {
        vector<int> ret(M, 0);
        while (x) {
            ret[x % 10] ++ ;
            x /= 10;
        }
        return ret;
    }
    bool reorderedPowerOf2(int n) {
        // 预处理所有合法的方案的词频
        set<vector<int>> st;
        for (int i = 0; i < 31; i ++ ) 
            st.insert(get(1 << i));
        // 获得当前数的词频
        vector<int> cur = get(n);
        if (st.find(cur) != st.end())
            return true;
        return false;
    }
};
```
----

## 复杂度分析

其中C为30, N为1e9.

1. 时间复杂度$O(ClogN)$, 首先预处理所有合法方案$O(ClogN)$, 接着查`set`表$O(logC * logN)$
2. 空间复杂度$O(ClogN)$, 使用`set`存储所有合法的2的幂次的词频, 共有C个合法方案, 每个方案的长度不超过`logN`

----
**欢迎讨论指正**