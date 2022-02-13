---
title: '[LeetCode-周赛]280'
toc: true
tags:
  - 模拟
  - 枚举
  - 状态压缩动态规划
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2022-02-13 16:44:04
updated:
---

**Rank** : `379/5833`
**Solved** : `3/4`

![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2022/1/LeetCode第280场周赛.png)

[竞赛链接](https://leetcode-cn.com/contest/weekly-contest-280/)

<!--more-->

## [得到 0 的操作数](https://leetcode-cn.com/contest/weekly-contest-280/problems/count-operations-to-obtain-zero/) 

### 思路

**模拟**. 按照题目要求模拟题意即可.

### Code

```cpp
class Solution {
public:
    int countOperations(int num1, int num2) {
        int step = 0;
        while (num1 and num2) {
            if (num1 >= num2)
                num1 -= num2;
            else
                num2 -= num1;
                
            step ++ ;
        }
        return step;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(1)$
----

## [使数组变成交替数组的最少操作数](https://leetcode-cn.com/problems/minimum-operations-to-make-the-array-alternating/)

### 思路

**枚举**. 首先可以发现题目要求**奇数位置**、**偶数位置**的值全部相同, 且奇数和偶数位置值不同. 因此我们只需计算最多能够保留多少个数字, 替换的次数为数组长度减去保留的数字个数。

为了计算保留了多少个数字, 枚举偶数位置保留哪一个数字, 然后计算奇数位置除去枚举数字后的频次最大值即可.

### Code

```cpp
const int N = 1e5 + 5;
class Solution {
public:
    int cnt[N], L[N], R[N];
    int minimumOperations(vector<int>& nums) {
        unordered_map<int, int> even;
        
        int n = nums.size();
        
        for (int i = 0; i < n; i ++ ) {
            if ((i & 1) == 0)
                even[nums[i]] ++ ;
            else
                cnt[nums[i]] ++ ;
        }
        
        for (int i = 1; i < N; i ++ )
            L[i] = max(L[i - 1], cnt[i]);
        for (int i = N - 2; i >= 1; i -- )
            R[i] = max(R[i + 1], cnt[i]);
        
        int mx = 0;
        
        for (auto& [k, v] : even) {
            int cur = v + max(L[k - 1], R[k + 1]);
            mx = max(mx, cur);
        }
        return n - mx;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [拿出最少数目的魔法豆](https://leetcode-cn.com/problems/removing-minimum-number-of-magic-beans/)

### 思路

**枚举**. 枚举最终的魔法豆数目, 计算小于该数目的总和以及严格大于该数目的总和.

小于该数目的总和可以使用前缀和计算. 严格大于该数目的总和部分需要预处理出个数, 然后用其前缀和减去个数乘以数目.


### Code

```cpp
using LL = long long;
const int N = 1e5 + 5;
class Solution {
public:
    LL s[N], cnt[N];
    long long minimumRemoval(vector<int>& nums) {
        
        int n = nums.size();
        
        for (int i = 0; i < n; i ++ ) {
            s[nums[i]] += nums[i];
            cnt[nums[i]] += 1;
        }
        
        for (int i = 1; i < N; i ++ )
            s[i] += s[i - 1];
        
        for (int i = N - 3; i >= 1; i -- )
            cnt[i] += cnt[i + 1];
        
        LL ans = LLONG_MAX;
        for (int i = 0; i < n; i ++ ) {
            int cur = nums[i];
            LL left = s[cur - 1];
            LL right = (s[N - 1] - s[cur]) - 1ll * cnt[cur + 1] * cur;
            ans = min(ans, left + right);
        }
        
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [数组的最大与和](https://leetcode-cn.com/problems/maximum-and-sum-of-array/)

### 思路

**状态压缩DP**. 由于每个篮子最多可以放两个, 因此构建`2 * numSlots`个篮子, 构建出的第一个和第numSlots个为原始的第一个篮子, 如果这两个篮子都放表示原来的第一个篮子放两个放满了.
- 用$f[i]$表示考虑构建出的篮子的状态为`i`, 且考虑了前`cnt[i]`个数字的最大价值.(`cnt[i]`表示状态`i`中1的个数, 即放数组的篮子个数).
- 为了计算`f[i]`, 枚举`nums[cnt[i]]`放在了哪里即可.
- 赛时dp方程多定义了一维, 导致超时.赛后参考了[0x3f佬的题解](https://leetcode-cn.com/problems/maximum-and-sum-of-array/solution/zhuang-tai-ya-suo-dp-by-endlesscheng-5eqn/)

### Code

```cpp
const int N = 20;
int f[1 << N];
class Solution{
public:
    int maximumANDSum(vector<int>& nums, int numSlots) {
        int n = nums.size();
        memset(f, 0, sizeof(f));
        
        int m = numSlots * 2;
        
        for (int i = 0; i < (1 << m); i ++ ) {
            int cnt = __builtin_popcount(i);
            if (i < 1 or cnt > n)
                continue;
            for (int k = 0; k < numSlots; k ++ ) {
                if (i >> k & 1)
                    f[i] = max(f[i], f[i - (1 << k)] + (nums[cnt - 1] & (k + 1)));
                int r = k + numSlots;
                if (i >> r & 1)
                    f[i] = max(f[i], f[i - (1 << r)] + (nums[cnt - 1] & (k + 1)));
            }
        }
        int ans = 0;
        for (int i = 0; i < 1 << m ; i ++ )
            if (__builtin_popcount(i) == n)
                ans = max(ans, f[i]);
        return ans;
    }
};
```

**赛时TLE代码**

```cpp
const int N = 20;
int f[1 << N][N];
class Solution{
public:
    int maximumANDSum(vector<int>& nums, int numSlots) {
        int n = nums.size();
        memset(f, 0, sizeof(f));
        
        int m = numSlots * 2;
        
        for (int i = 0; i < (1 << m); i ++ ) {
            for (int j = 1; j <= n; j ++ ) {
                for (int k = 0; k < numSlots; k ++ ) {
                    if (i >> k & 1)
                        f[i][j] = max(f[i][j], f[i - (1 << k)][j - 1] + (nums[j - 1] & (k + 1)));
                    int r = k + numSlots;
                    if (i >> r & 1)
                        f[i][j] = max(f[i][j], f[i - (1 << r)][j - 1] + (nums[j - 1] & (k + 1)));
                }
            }
        }
        int all = (1 << m) - 1;
        return f[all][n];
    }
};
```

### 复杂度分析
- 时间复杂度$O(N * 2^N)$
- 空间复杂度$O(2^N)$
----
**欢迎讨论指正**