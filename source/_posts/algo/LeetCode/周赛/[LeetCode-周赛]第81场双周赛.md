---
title: '[LeetCode-周赛]第81场双周赛'
toc: true
tags:
  - 模拟
  - 连通性
  - 动态规划
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2022-06-26 00:42:49
updated:
---


看完木鱼水心讲解的水浒传才想起来今天周六有双周赛, 赛后补题记录一下.

[竞赛链接](https://leetcode.cn/contest/biweekly-contest-81/)

<!--more-->

## [统计星号](https://leetcode.cn/problems/count-asterisks/) 

### 思路

**模拟题意即可**.

### Code

```cpp
class Solution {
public:
    int countAsterisks(string s) {
        int ans = 0, cnt = 0;

        for (auto& c : s) {
            if (c == '|')
                cnt ++ ;
            if (c == '*' and (cnt % 2 == 0))
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

## [统计无向图中无法互相到达点对数](https://leetcode.cn/problems/count-unreachable-pairs-of-nodes-in-an-undirected-graph/)

### 思路

**不同连通块之间不可达**. 使用`BFS / DFS / 并查集`等算法计算出每个连通块的大小后, 连通块`i`与其他联通块都是不可达的. 该连通块造成的不可达点对数量是:

$sz[i] * (n - sz[i]), sz[i] 表示联通块i的大小, n表示点的个数$

最终答案除以2即可, 因为每一个点对都被算了两次.

我写的是并查集(BFS / DFS均可).

### Code

```cpp
using LL = long long;
const int N = 1e5 + 5;
class Solution {
public:
    vector<int> g[N];
    int f[N], sz[N];
    int find(int x) {
        return x == f[x] ? x : f[x] = find(f[x]);
    }
    void merge(int x, int y) {
        x = find(x), y = find(y);
        if (x != y) {
            sz[x] += sz[y];
            f[y] = x;
        }
    }
    long long countPairs(int n, vector<vector<int>>& edges) {
        for (int i = 0; i < n; i ++ )
            f[i] = i, sz[i] = 1;
        for (auto& e : edges) {
            int a = e[0], b = e[1];
            merge(a, b);
        }
        vector<int> cnt;
        for (int i = 0; i < n; i ++ ) {
            if (f[i] == i)
                cnt.push_back(sz[i]);
        }
        LL ans = 0LL;
        for (int i = 0; i < cnt.size(); i ++ )
            ans += 1ll * cnt[i] * (n - cnt[i]);
        
        return ans >> 1;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N * logN)$
- 空间复杂度$O(N)$
----

## [操作后的最大异或和](https://leetcode.cn/problems/maximum-xor-after-operations/)

### 思路

`nums[i] AND (nums[i] XOR x)`的唯一作用是"选择屏蔽"`nums[i]`中的某些1(二进制表示下). 因此`nums`所有元素**最大**逐位异或和即为**所有出现过的1的二进制表示之和**, 因为我们无法在某一位不存在的1的情况下让他变成1, 因此出现过1的位置选1就是最大最优解.

### Code

```cpp
class Solution {
public:
    int maximumXOR(vector<int>& nums) {
        vector<int> cnt(32);
        for (auto& num : nums) {
            for (int i = 0; i < 32; i ++ )
                if (num >> i & 1)
                    cnt[i] = 1;
        }
        int ans = 0;
        for (int i = 0; i < 32; i ++ )
            if (cnt[i])
                ans += 1 << i;
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N * log_{10}{N})$
- 空间复杂度$O(log_{10}{N})$
----

## [不同骰子序列的数目](https://leetcode.cn/problems/number-of-distinct-roll-sequences/)

### 思路

**动态规划**. 第一个条件很好满足. 第二个条件可以使用三维DP来满足. 具体的：

- 动态规划
  - 状态定义:
    1. $f[i][j][k]$表示考虑前`i`个位置, 且`i位`放`j`, `i - 1位`放`k`的不同序列数.
  - 状态计算
    1. 对于$f[i][j][k]$
      $$
        f[i][j][k] = \sum_{l \in [1, 6]}f[i - 1][k][l]
      $$
    考虑到第一个条件: `gcd(j, k) = 1. gcd(k, l) = 1`.
    考虑到第二个条件: `j != k and k != l and j != l`.

### Code

```cpp
using LL = long long;
const int N = 1e4 + 5, M = 7, MOD = 1e9 + 7;
class Solution {
public:
    LL f[N][M][M];
    int distinctSequences(int n) {
        if (n == 1)
            return 6;
        vector<int> ok[M];
        for (int i = 1; i < M; i ++ )
            for (int j = 1; j < M; j ++ )
                if (gcd(i, j) == 1 && i != j)
                    ok[i].push_back(j), f[2][i][j] = 1;
        
        for (int i = 3; i <= n; i ++ )
            for (int j = 1; j < M; j ++ )
                for (auto& k : ok[j]) {
                    for (auto& l : ok[k]) {
                        if (j == k or j == l or k == l)
                            continue;
                        f[i][j][k] = (f[i][j][k] + f[i - 1][k][l]) % MOD;
                    }
                }
        
        LL ans = 0LL;
        for (int i = 1; i < M; i ++ )
            for (auto& j : ok[i])
                ans = (ans + f[n][i][j]) % MOD;
        
        return ans;
    }
};

```

### 复杂度分析

- 时间复杂度$O(N * M^3), M = 6$
- 空间复杂度$O(N * M^2)$
----
**欢迎讨论指正**