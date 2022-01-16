---
title: '[LeetCode-周赛]276'
toc: true
tags:
  - 模拟
  - 贪心
  - 动态规划
  - 二分
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2022-01-16 11:40:16
updated:
---

**Rank** : `273/5243`
**Solved** : `4/4`
![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2021/12/LeetCode第273场周赛.png)

[竞赛链接](https://leetcode-cn.com/contest/weekly-contest-276/)

<!--more-->

## [https://leetcode-cn.com/contest/weekly-contest-276/problems/divide-a-string-into-groups-of-size-k/](https://leetcode-cn.com/contest/weekly-contest-276/problems/divide-a-string-into-groups-of-size-k/) 

### 思路
模拟题意, 如果最后一段的长度不足就补齐.

### Code

```cpp
class Solution {
public:
    vector<string> divideString(string s, int k, char fill) {
        vector<string> ans;
        string cur;
        int n = s.size();
        for (int i = 0; i < n; i ++ ) {
            cur.push_back(s[i]);
            if (cur.size() == k)
                ans.push_back(cur), cur = "";
        }
        while (cur.size() and cur.size() < k)
            cur.push_back(fill);
        if (cur.size() == k)
            ans.push_back(cur);
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [得到目标值的最少行动次数](https://leetcode-cn.com/contest/weekly-contest-276/problems/minimum-moves-to-reach-target-score/)

### 思路
写完记忆化才发现其实是**贪心**. 首先倒着做, 求从`target`变成1的最小花费. 然后贪心的做
1. 当前数能被2整除且有整除次数, 则整除
2. 否则就减一 (无整除次数直接可以返回答案)

### Code

```cpp
const int INF = 1e9;
class Solution {
public:
    unordered_map<int, unordered_map<int,int>> f;
    int dfs(int x, int cnt) {
        if (cnt == 0)
            return x - 1;
        if (f.count(x) and f[x].count(cnt))
            return f[x][cnt];
        int& v = f[x][cnt];
        // cout << x << ' ' << cnt << endl;
        v = INF;
        if ((x % 2) == 0 and cnt)
            v = min(v, dfs(x / 2, cnt - 1) + 1);
        else
            v = min(v, dfs(x - 1, cnt) + 1);
        return v;
    }
    
    int minMoves(int tar, int cnt) {
        if (cnt == 0)
            return tar - 1;
        int ans = INF;
        for (int i = 0; i <= cnt; i ++ )
            f[1][i] = 0;
        ans = dfs(tar, cnt);
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(logN)$
- 空间复杂度$O(logN * maxDoubles)$
----

## [解决智力问题](https://leetcode-cn.com/contest/weekly-contest-276/problems/solving-questions-with-brainpower/)

### 思路
首先可以想到使用**动态规划**, 因为选的方式无法穷举, 而且选与不选之间的状态转移也比较清楚.
麻烦的是如果正向做, 求`f[i]`的时候, 计算选择`i`的时候, 我们要找一个`j`, 使得在`j`处选择后可以在`i`处选择, 且`f[j]`最大.
反向做就比较友好, 避免了找`j`的过程.

动态规划:
  1. 状态定义:  f[i]表示考虑$i ~ n - 1$之间物品时候的最大价值.
  2. 状态转移:  
    - 可以不拿`i`处的或只拿`i`处的: $f[i] = max(f[i + 1], cur)$
    - 可以拿了`i`处后继续拿后面的:  $f[i] = max(f[i], f[i + questions[i][1] + 1] + cur)$

### Code

```cpp
using LL = long long;
class Solution {
public:
    long long mostPoints(vector<vector<int>>& qu) {
        int n = qu.size();
        vector<LL> f(n);
        f[n - 1] = qu[n - 1][0];
        for (int i = n - 2; i >= 0; i -- ) {
            int r = i + qu[i][1] + 1;
            LL cur = qu[i][0];
            f[i] = max(f[i + 1], cur);
            // 不越界才可以拿后面的
            if (r < n)
                f[i] = max(f[i], f[r] + cur);
        }
        return f[0];
    }
};
```

### 复杂度分析
- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [同时运行 N 台电脑的最长时间](https://leetcode-cn.com/contest/weekly-contest-276/problems/maximum-running-time-of-n-computers/)

### 思路

**没有思路的时候就想想二分** 哈哈!
答案具有**二段性**, 如果答案为`k`, 则所有小于等于`k`的都能被凑出来, 而大于`k`的无法凑出来.
因此可以二分答案, 然后判断这个数组能否凑出`n`个`mid`. 判断过程中, 如果某个值大于等于`mid`, 则凑出个数 + 1;否则双指针连续求和, 求出一段之和大于等于`mid`, 然后**关键**是这一段之和大于`mid`的部分可以被其他电脑所使用. 因此大于`mid`的部分的可以继续使用.

### Code

```cpp
using LL = long long;
class Solution {
public:
    long long maxRunTime(int n, vector<int>& nums) {
        int m = nums.size();
        if (m < n)
            return 0;
        sort(nums.begin(), nums.end());
        LL sum = 0;
        for (auto& c : nums)
            sum += c;
        LL L = 0, R = sum;
        
        while (L < R) {
            LL mid = (L + R + 1) >> 1;
            LL cur = 0, cnt = 0;
            
            for (int i = 0; i < m; ) {
                if (nums[i] >= mid) {
                    cnt ++ ;
                    i ++ ;
                    continue;
                }
                int j = i;
                while (j < m and cur < mid) {
                    cur += nums[j];
                    j ++ ;
                }
                if (cur >= mid) {
                    cnt ++ ;
                    cur -= mid;
                }
                i = j;
            }
            if (cnt >= n)
                L = mid;
            else
                R = mid - 1;
        }
        return R;
    }
};
```

### 复杂度分析
- 时间复杂度$O(NlogN)$
- 空间复杂度$O(1)$

----
**欢迎讨论指正**