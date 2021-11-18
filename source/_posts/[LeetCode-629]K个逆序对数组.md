---
title: '[LeetCode-629]K个逆序对数组'
toc: true
tags:
  - 动态规划
  - 前缀和
categories:
  - - algo
    - LeetCode
    - 每日一题
date: 2021-11-11 11:20:38
updated:
---

[原题链接](https://leetcode-cn.com/problems/k-inverse-pairs-array/)

## 题目描述
由 $1-n$ 组成的排列中, 有多少个排列的逆序对个数是 $k$

<!--more-->

## 思路
看完题目和数据范围基本就能确定是动态规划. 因为可行方案可能很多很多, 无法枚举. 而从`集合角度`[<sup>1</sup>](#refer-anchor-1)(动态规划)进行计算, 会帮助我们省去很多不必要的枚举. 使用一个数来表示一类有共同点的方案, 是动态规划优化问题的特点.

- **动态规划**
  - 状态表示:
    1. $f[i][j]$ : 表示考虑前 $1 - i$ 个数, 且逆序对个数为 $j$ 时的方案数. 
  - 状态计算:
    状态计算的思路是`枚举最后一个不同点`[<sup>1</sup>](#refer-anchor-1): 即考虑将数字`i`放在什么位置. 放置`i`位置的可能方式如下:
    ![状态划分](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2021/11/11/LeetCode-629.png)
    - 由上图可见, 若将 $i$ 放置在 $i - k$下标处, 这会造成 $k - 1$个逆序对(数 $i$与 下标$\in[i - k + 1, i]$处的数构成逆序对)
    - 因此可得: $f[i][j]$ = $\sum_{k=0}^{i - 1} f[i - 1][j - k]$
    - 由上分析可见, 状态为$O(n^2)$, 转移为$O(n)$, 总时间复杂度为$O(n^3)$, 会超时.
    - 利用**前缀和**优化状态转移: 记$s[i][j]$ = $\sum_{k=0}^j f[i][k]$, 可得状态计算：
    $$
    <!-- f[i][j] = \begin{cases}
    s[i - 1][j] & \text{if i > j} \\
    s[i - 1][j] - s[i - 1][j - i] & \text{if i <= j}
    \end{cases} -->
    $$

## Code
```cpp
const int N = 1010, MOD = 1e9 + 7;
class Solution {
public:
    int f[N][N], s[N][N];
    int kInversePairs(int n, int k) {
        for (int i = 0; i <= n; i ++ )
            f[i][0] = s[i][0] = 1;
        
        for (int i = 1; i <= n; i ++ ) {
            for (int j = 1; j <= k; j ++ )
                s[i - 1][j] = (s[i - 1][j - 1] + f[i - 1][j]) % MOD;
            for (int j = 1; j <= k; j ++ ) {
                if (i > j)
                    f[i][j] = s[i - 1][j];
                else
                    f[i][j] = (s[i - 1][j] - s[i - 1][j - i]) % MOD;
            }
        }
        int ans = f[n][k];
        ans = (ans + MOD) % MOD;
        return ans;
    }
};
```

## 复杂度分析
1. 时间复杂度$O(N * K)$
2. 空间复杂度$O(N * K)$

## 参考文献
- [1] [B站yxc](https://space.bilibili.com/7836741?from=search&seid=17655252112390136376)

----
**欢迎讨论指正**