---
title: '[LeetCode-周赛]第72场双周赛'
toc: true
tags:
  - 模拟
  - 贪心
  - 树状数组
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2022-02-19 23:11:32
updated:
---

**Rank** : `91/4311`
**Solved** : `4/4`

![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2022/1/LeetCode第72场双周赛.png)

[竞赛链接](https://leetcode-cn.com/contest/biweekly-contest-72/)

<!--more-->

## [统计数组中相等且可以被整除的数对](https://leetcode-cn.com/contest/biweekly-contest-72/problems/count-equal-and-divisible-pairs-in-an-array/)

### 思路

**模拟**.数据范围和数值范围都很小, 直接$O(N^2)$枚举.

### Code

```cpp
class Solution {
public:
    int countPairs(vector<int>& nums, int k) {
        int ans = 0;
        int n = nums.size();
        for (int i = 0; i < n; i ++ )
            for (int j = i + 1; j < n; j ++ ) {
                if (nums[i] == nums[j] and (i * j) % k == 0)
                    ans ++ ;
            }
        
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N^2)$
- 空间复杂度$O(1)$
----

## [找到和为给定整数的三个连续整数](https://leetcode-cn.com/contest/biweekly-contest-72/problems/find-three-consecutive-integers-that-sum-to-a-given-number/)

### 思路

如果连续整数为`x - 1`、`x`、和`x + 1`. 则和为`3x`必为3的倍数.

### Code

```cpp
class Solution {
public:
    vector<long long> sumOfThree(long long num) {
        using LL = long long;
        if (num % 3)
            return {};
        LL mid = num / 3;
        return {mid - 1, mid, mid + 1};
    }   
};
```

### 复杂度分析

- 时间复杂度$O(1)$
- 空间复杂度$O(1)$
----

## [拆分成最多数目的偶整数之和](https://leetcode-cn.com/contest/biweekly-contest-72/problems/maximum-split-of-positive-even-integers/)

### 思路

**贪心**. 
- 如果是**奇数**则无解. 
- 如果是**偶数**. 从小到大枚举`[2, 4, 6, 8, ...]`如果可以选择则贪心的选择当前数, 总和减去当前数. 如果最优解没有选择当前数, 选了比当前数大的数, 那么可以调整最优解选当前数, 这样选的可能多了1, 且选的总和多了一部分. 可以将多的这部分加到最优解的选的最大值上去. 逐步将最优解调整成贪心解.

### Code

```cpp
class Solution {
public:
    vector<long long> maximumEvenSplit(long long s) {
        using LL = long long;
        if (s % 2 or s < 0)
            return {};
        if (s == 0)
            return {0};
        vector<LL> ans;
        
        for (LL i = 2; ; i += 2) {
            if (s - i > i) {
                ans.push_back(i);
                s -= i;                
            } else {
                ans.push_back(s);
                break;
            }
        }
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(\sqrt{N})$
- 空间复杂度$O(\sqrt{N})$
----

## [统计数组中好三元组数目](https://leetcode-cn.com/contest/biweekly-contest-72/problems/count-good-triplets-in-an-array/)

### 思路

首先将问题转换成**一个数组上的问题**.
因为两个数组都是一个排列, 因此可将[0, n - 1]的值映射成其在`nums1[]`中的下标. 这样映射完成后, `nums2`中的一个数值递增三元组, 其映射前的数值在原来的`nums1`中一定是从前到后按序出现的并且在原`nums2`中是按下标递增出现的. 满足题目要求的好三元组. 另一方面, 在原`nums1[]`中的按下标递增的三元组, 按照上述映射后, 其映射值在映射后的`nums2[]`一定按值递增. 这样, 最终求**映射后数组的数值递增三元组**即可.

为了求数组的递增三元组, 枚举中间值, 求其左边严格小于当前值的个数`left`和右边严格大于当前值的个数`right`. 则以当前值为中间值的递增三元组的个数为$left * right$. 枚举所有的中间位置即可. 动态的快速求左边或者右边严格当前值的个数的方法，可以使用树状数组. 且这道题无需离散化映射, 因为是`[0, n - 1]`的排列, 将其映射成`[1, n]`即可.

### Code

```cpp

inline int lowbit(int x) {
    return x & -x;
}

void add(vector<int>& nums, int x, int c) {
    int n = nums.size();
    for (int i = x; i < n; i += lowbit(i))
        nums[i] += c;
}

int query(vector<int>& nums, int x) {
    int n = nums.size();
    int ans = 0;
    for (int i = x; i; i -= lowbit(i))
        ans += nums[i];
    return ans;
}

class Solution {
public:
    long long goodTriplets(vector<int>& nums1, vector<int>& nums2) {
        using LL = long long;
        int n = nums1.size();
        map<int, int> f;
        
        for (int i = 0; i < n; i ++ )
            f[nums1[i]] = i;
    
        for (auto& c : nums2)
            c = f[c] + 1;
        
        LL ans = 0;
        
        vector<int> L(n + 1, 0), R(n + 1, 0);
        
        for (int i = 1; i <= n; i ++ )
            add(R, i, 1);
        
        for (int i = 0; i < n; i ++ ) {
            int cur = nums2[i];
            // remove from right
            add(R, cur, -1);
            int left = query(L, cur - 1), right = query(R, n) - query(R, cur);
            ans += 1ll * left * right;
            // add to left
            add(L, cur, 1);
        }
        
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(N * logN)$
- 空间复杂度$O(N)$
----
**欢迎讨论指正**