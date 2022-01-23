---
title: '[LeetCode-周赛]277'
toc: true
tags:
  - 模拟
  - 枚举
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2022-01-23 21:58:51
updated:
---

**Rank** : `859/5059`
**Solved** : `4/4`

![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2022/1/LeetCode第277场周赛.png)

[竞赛链接](https://leetcode-cn.com/contest/weekly-contest-277/)

<!--more-->

## [元素计数](https://leetcode-cn.com/contest/weekly-contest-277/problems/count-elements-with-strictly-smaller-and-greater-elements/) 

### 思路

**模拟**.统计严格大于最小值且严格小于最大值的数的个数.

### Code

```cpp
class Solution {
public:
    int countElements(vector<int>& nums) {
        int Mx = *max_element(begin(nums), end(nums)), Mn = *min_element(begin(nums), end(nums));
        int ans = 0;
        for (auto& c : nums) {
            if (c != Mx and c != Mn)
                ans ++ ;
        }
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(1)$
----

## [按符号重排数组](https://leetcode-cn.com/contest/weekly-contest-277/problems/rearrange-array-elements-by-sign/)

### 思路

**模拟**. 将正数和负数分开存入数组, 然后按序构造答案.

### Code

```cpp
class Solution {
public:
    vector<int> rearrangeArray(vector<int>& nums) {
        vector<int> neg, pos;
        for (auto& c : nums)
            if (c > 0)
                pos.push_back(c);
            else
                neg.push_back(c);
        vector<int> ans;
        int n = pos.size();
        for (int i = 0; i < n; i ++ ) {
            ans.push_back(pos[i]);
            ans.push_back(neg[i]);
        }
        
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [找出数组中的所有孤独数字](https://leetcode-cn.com/contest/weekly-contest-277/problems/find-all-lonely-numbers-in-the-array/)

### 思路

**模拟**. 使用哈希表计数并且判断`x + 1`和`x - 1`是否存在.

### Code

```cpp
class Solution {
public:
    vector<int> findLonely(vector<int>& nums) {
        unordered_map<int, int> mp;
        for (auto& c : nums)
            mp[c] ++ ;
        vector<int> ans;
        for (auto& [k, v] : mp) {
            if (v > 1)
                continue;
            if (mp.count(k + 1) == 0 and mp.count(k - 1) == 0)
                ans.push_back(k);
        }
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [基于陈述统计最多好人数](https://leetcode-cn.com/contest/weekly-contest-277/problems/maximum-good-people-based-on-statements/)

### 思路

**枚举**. 使用二进制枚举好人可能的方案, 然后判断好人的陈述是否存在矛盾。坏人的陈述是不需要判断的, 因为他可能说真, 也可能说假, 即陈述对好坏划分是没有影响的。(比赛的时候理解错题了, 以为要么全真, 要么全假, 搞晕了)

### Code

```cpp
class Solution {
public:
    int maximumGood(vector<vector<int>>& nums) {
        int n = nums.size();
        int ans = 0;
        
        vector<vector<int>> state(n);
        
        for (int i = 0; i < n; i ++ ) {
            int good = 0, bad = 0;
            for (int j = 0; j < n; j ++ ) {
                if (nums[i][j] == 1)
                    good |= (1 << j);
                if (nums[i][j] == 0)
                    bad |= (1 << j);
            }
            state[i].push_back(good);
            state[i].push_back(bad);
        }
        
        for (int i = 0; i < 1 << n; i ++ ) {
            int cnt = __builtin_popcount(i);
            int good = 0, bad = 0;
            for (int j = 0; j < n; j ++ ) {
                if (i >> j & 1)
                    good |= (1 << j);
                else
                    bad |= (1 << j);
            }
            bool flag = true;
            for (int j = 0; j < n; j ++ ) {
                if (i >> j & 1) {
                    if ((state[j][0] | good) != good)
                        flag = false;
                    if ((state[j][1] | bad) != bad)
                        flag = false;
                }
            }
            if (flag)
                ans = max(ans, cnt);
        }
        
        return ans;
    }
};
```


### 复杂度分析
- 时间复杂度$O(N * 2^N)$
- 空间复杂度$O(N)$

----
**欢迎讨论指正**