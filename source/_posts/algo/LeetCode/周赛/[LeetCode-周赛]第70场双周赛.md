---
title: '[LeetCode-周赛]第70场双周赛'
toc: true
tags:
  - 贪心
  - 差分
  - BFS
  - 前缀和
  - 动态规划
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2022-01-22 23:26:26
updated:
---

**Rank** : `302/3638`
**Solved** : `4/4`

![](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2022/1/LeetCode第70场双周赛.png)

[竞赛链接](https://leetcode-cn.com/contest/biweekly-contest-70/)

<!--more-->

## [打折购买糖果的最小开销](https://leetcode-cn.com/contest/biweekly-contest-70/problems/minimum-cost-of-buying-candies-with-discount/)

### 思路

**贪心**. 还没有买到的糖果中, 最大和次大无法通过免费的方式获得, 必须通过买的方式, 买最大和次大的话贪心选择拿第三大作为免费的即可.

### Code

```cpp
class Solution {
public:
    int minimumCost(vector<int>& cost) {
        sort(cost.begin(), cost.end(), greater<int>());
        int ans = 0, n = cost.size();
        
        for (int i = 0; i < n; i += 3) {
            ans += cost[i];
            if (i + 1 < n)
                ans += cost[i + 1];
        }
        
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N * logN)$
- 空间复杂度$O(1)$
----

## [统计隐藏数组数目](https://leetcode-cn.com/contest/biweekly-contest-70/problems/count-the-hidden-sequences/)

### 思路

**差分**的运用. 通过对差分数组求其前缀和, 我们可以得到原数组中每个数与`hidden[0]`的差值. 然后通过枚举所有可能的`hidden[0]`, 判断`hidden[0]`在某个取值下是否符合题意. 判断的方法是判断这种情况下**最大值**和**最小值**是否在合法范围内.

### Code

```cpp
using LL = long long;
class Solution {
public:
    int numberOfArrays(vector<int>& d, int L, int R) {
        int n = d.size();
        vector<LL> sb(n);
        sb[0] = d[0];
        for (int i = 1; i < n; i ++ )
            sb[i] = sb[i - 1] + d[i];
        
        LL Mx = *max_element(begin(sb), end(sb)), Mn = *min_element(begin(sb), end(sb));
        int ans = 0;
        for (int i = L; i <= R; i ++ ) {
            LL curL = Mn + i, curR = Mx + i;
            if (curL >= L and curL <= R and curR >= L and curR <= R)
                ans += 1;
        }
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [价格范围内最高排名的 K 样物品](https://leetcode-cn.com/contest/biweekly-contest-70/problems/k-highest-ranked-items-within-a-price-range/)

### 思路

先求起点到每个点的最短路. 可以通过**BFS算法**求解. 接着按照题目的要求对**合法点**进行排序即可. `cpp`中可以使用`set`搭配使用`tuple`(结构化绑定, 写法简洁)或者`vector`实现.

### Code

```cpp
using PII = pair<int, int>;
using TII = tuple<int, int, int, int>;
const int dx[4] = {0, 0, 1, -1}, dy[4] = {1, -1, 0, 0};
const int INF = 1e9;
class Solution {
public:
    vector<vector<int>> highestRankedKItems(vector<vector<int>>& g, vector<int>& p, vector<int>& start, int k) {
        int L = p[0], R = p[1];
        int n = g.size(), m = g[0].size();

        int sx = start[0], sy = start[1];
        vector<vector<int>> dist(n, vector<int>(m, INF));
        dist[sx][sy] = 0;
        queue<PII> qu;
        qu.emplace(sx, sy);
        
        while (qu.size()) {
            auto [x, y] = qu.front();
            qu.pop();
            for (int i = 0; i < 4; i ++ ) {
                int nx = x + dx[i], ny = y + dy[i];
                if (nx >= 0 and nx < n and ny >= 0 and ny < m and g[nx][ny]) {
                    if (dist[nx][ny] == INF) {
                        dist[nx][ny] = dist[x][y] + 1;
                        qu.emplace(nx, ny);
                    }
                }
            }
        }
        set<TII> st;
        for (int i = 0; i < n; i ++ )
            for (int j = 0; j < m; j ++ ) {
                if (dist[i][j] == INF or g[i][j] > R or g[i][j] < L or g[i][j] == 1)
                    continue;
                st.emplace(dist[i][j], g[i][j], i, j);
            }
        vector<vector<int>> ans;
        for (auto& [d, p, i, j] : st) {
            if (ans.size() < k)
                ans.push_back({i, j});
            else
                break;
        }        
    
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(N * logN)$
- 空间复杂度$O(N)$
----

## [分隔长廊的方案数](https://leetcode-cn.com/contest/biweekly-contest-70/problems/number-of-ways-to-divide-a-long-corridor/)

### 思路

**前缀和优化动态规划**. 首先将`S`看成1, `P`看成0, 对原数组求其前缀和. 并将前缀和存入map中.
接着定义`f[i]`表示考虑前`i`个位置且在下标`i`的右边放屏风的方案数。为了求解`f[i]`, 需要考虑上一个屏风所放的位置. 
若`i`之前有`k`个座位, 则第一个可以放屏风的位置是$L = mp[k - 2]$, 最后一个可以放屏风的位置是$R = mp[k - 1] - 1$.
则有$f[i] = \sum_{j=L}^{R}f[j]$, 由于其是一段连续的区间和, 因此可以使用**前缀和**的技巧进行优化.

### Code

```cpp
const int MOD = 1e9 + 7;
using LL = long long;
class Solution {
public:
    int numberOfWays(string str) {
        int n = str.size();
        vector<int> s(n + 1, 0);
        unordered_map<int, int> mp;
        
        mp[0] = 0;
        for (int i = 1; i <= n; i ++ ) {
            int cur = (str[i - 1] == 'S');
            s[i] = s[i - 1] + cur;
            // 哈希表记录每个前缀和出现的坐标
            if (!mp.count(s[i]))
                mp[s[i]] = i;
        }
        
        int all = s[n];
        if (all % 2)
            return 0;
        
        int ans = 0;
        vector<LL> f(n + 1);
        // 注：根据定义, f[0] = 1.
        f[0] = 1;
        
        for (int i = 1; i <= n; i ++ ) {
            int cur = s[i];
            f[i] = f[i - 1];
            if (cur < 2)
                continue;
            int L = mp[cur - 2], R = mp[cur - 1] - 1;
            int val;
            // 会存在下标越界的情况, 根据定义L可以去到0
            if (L - 1 <= 0)
                val = f[R];
            else
                val = f[R] - f[L - 1];
            if (i == n)
                ans = val % MOD;
            // f数组自身当作其前缀和数组
            f[i] = (f[i] + val) % MOD;
        }
        // MOD成非负数
        ans = (ans + MOD) % MOD;
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(N)$
- 空间复杂度$O(N)$

----
**欢迎讨论指正**