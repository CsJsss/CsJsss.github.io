---
title: '[LeetCode-575]分糖果'
toc: true
tags:
  - LeetCode
  - 贪心
categories:
  - - algo
    - LeetCode
    - 每日一题
date: 2021-11-01 14:25:47
updated:
---

[原题链接](https://leetcode-cn.com/problems/distribute-candies/575)

## 题目描述
总共有偶数个数字, 从中选择一半的数字且**数字的种类最多**.

<!-- more --> 

## 思路
- **贪心**: 总共选的数字的个数是固定的, 对于每一种数字可以贪心的只选择一个, 这样后面可供选择的余地就越大.

## Code

```cpp
class Solution {
public:
    int distributeCandies(vector<int>& nums) {
        // 哈希表统计每个数字的个数
        unordered_map<int, int> mp;
        for (auto& num : nums)
            mp[num] ++ ;

        int s = nums.size() / 2;
        return min(s, (int)mp.size());
    }
};
```
----

## 复杂度分析
- 时间复杂度$O(n)$, 只需遍历数组统计类别
- 空间复杂度$O(n)$, 哈希表所需空间为$O(n)$

----
**欢迎讨论指正**