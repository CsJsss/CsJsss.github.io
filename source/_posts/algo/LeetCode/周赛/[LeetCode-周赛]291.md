---
title: '[LeetCode-周赛]291'
toc: true
tags:
  - 枚举
  - 贪心
  - 双指针
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2022-05-01 11:30:50
updated:
---

**Rank** : `362/19115`
**Solved** : `4/4`

![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2022/5/LeetCode第291场周赛.png)

[竞赛链接](https://leetcode.com/contest/weekly-contest-291/)

<!--more-->

## [Remove Digit From Number to Maximize Result](https://leetcode.com/contest/weekly-contest-291/problems/remove-digit-from-number-to-maximize-result/)

### 思路

**枚举**. 注意到数据范围很小, 因此直接枚举删除的位置, 然后保存值最大的答案.

### Code

```cpp
class Solution {
public:
    string removeDigit(string s, char digit) {
        string ans;
        int n = s.size();

        for (int i = 0; i < n; i ++ ) {
            char cur = s[i];
            if (s[i] == digit) {
                auto str = s.substr(0, i) + s.substr(i + 1);
                if (ans == "" or str > ans)
                    ans = str;
            }
        }
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N^2)$
- 空间复杂度$O(N)$
----

## [Minimum Consecutive Cards to Pick Up](https://leetcode.com/contest/weekly-contest-291/problems/minimum-consecutive-cards-to-pick-up/)

### 思路

**贪心**. 枚举每一个匹配对的右端点, 寻找该右端点**最佳**的左端点, 即求从当前位置向左看, 最靠近当前位置的左端点, 这可以使用哈希表来完成.

### Code

```cpp
class Solution {
public:
    int minimumCardPickup(vector<int>& nums) {
        int n = nums.size();
        unordered_map<int, int> f;
        int ans = n + 1;
        
        for (int i = 0; i < n; i ++ ) {
            int cur = nums[i];
            if (f.count(cur))
                ans = min(ans, i - f[cur] + 1);
            // 更新哈希表
            f[cur] = i;
        }
        
        if (ans == n + 1)
            ans = -1;
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [K Divisible Elements Subarrays](https://leetcode.com/contest/weekly-contest-291/problems/k-divisible-elements-subarrays/)

### 思路

**枚举**. 枚举合法子串(暴力或者双指针均可), 然后去重, 计算不重复的答案. 由于**不同长度的子串**不用相互比较, 因此可以使用**N**个`set`来去重, 即先按长度分组, 然后组内使用`set`去重.

### Code

- 暴力枚举合法子串:

```cpp
const int N = 210;
class Solution {
public:
    set<vector<int>> st[N];
    int countDistinct(vector<int>& nums, int k, int p) {
        int n = nums.size();
        
        
        for (int i = 0; i < n; i ++ )
            for (int j = i, cnt = 0; j < n; j ++ ) {
                if (nums[j] % p == 0)
                    ++ cnt;
                if (cnt == k + 1)           
                    break;
                vector<int> cur(nums.begin() + i, nums.begin() + j + 1);
                int m = cur.size();
                st[m].insert(cur);
            }
        
        int ans = 0;
        for (int i = 0; i < N; i ++ )
            ans += st[i].size();
        
        return ans;
    }
};
```

- 双指针枚举合法子串:

```cpp
const int N = 210;
class Solution {
public:
    set<vector<int>> st[N];
    int countDistinct(vector<int>& nums, int k, int p) {
        int n = nums.size();
        
        for (int i = 0, j = 0, cnt = 0; i < n; i ++ ) {
            if (nums[i] % p == 0)
                ++ cnt;
            while (cnt > k) {
                if (nums[j] % p == 0)
                    -- cnt;
                ++ j;
            }
            for (int k = j; k <= i; k ++ ) {
                vector<int> cur(nums.begin() + k, nums.begin() + i + 1);
                int m = cur.size();
                st[m].insert(cur);
            }
        }
        int ans = 0;
        for (int i = 0; i < N; i ++ )
            ans += st[i].size();
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N^3*logN)$, 按长度来分, 每一组长度下子串的个数为$O(N)$, 插入`set`的时间复杂度为$O(N * logN)$.
- 空间复杂度$O(N^2)$
----

## [Total Appeal of A String](https://leetcode.com/contest/weekly-contest-291/problems/total-appeal-of-a-string/)

### 思路

**枚举**. 枚举每一个字符对于整体答案的贡献. 先预处理出`i`位置左边第一个`j`字符的位置. 记为`L[i][j]`.

那么`i`位置处字符`s[i]`对于整体答案的贡献为:

  贡献 = $(i - 0) * (n + 1 - i)$, 如果$L[i - 1][s[i]]$不存在
  贡献 = $(i - L[i - 1][s[i]]) * (n + 1 - i)$, 如果$L[i - 1][s[i]]$存在

即以左闭右开的方式处理其贡献. 这样是为了防止重复计算, 如果采用左闭右闭, 那么会少计算答案; 如果采用左开右开, 那么会多计算答案. 

### Code

```cpp
using LL = long long;
const int N = 1e5 + 5, M = 26;
class Solution {
public:
    int L[N][M];
    long long appealSum(string s) {
        int n = s.size();
        memset(L, -1, sizeof(L));
        
        for (int i = 1; i <= n; i ++ ) {
            int cur = s[i - 1] - 'a';
            for (int j = 0; j < M; j ++ )
                L[i][j] = L[i - 1][j];
            L[i][cur] = i;
        }
        
        LL ans = 0LL;
        
        for (int i = 1; i <= n; i ++ ) {
            int cur = s[i - 1] - 'a';
            int left = L[i - 1][cur], right = n + 1;
            if (left == -1)
                left = 0;
            ans += 1ll * (i - left) * (right - i); 
        }
        
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N * |S|)$, $|S|$是字符集大小.
- 空间复杂度$O(N * |S|)$

----
**欢迎讨论指正**