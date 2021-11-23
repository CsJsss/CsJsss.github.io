---
title: '[LeetCode-周赛]266'
toc: true
tags:
  - 周赛
  - 枚举
  - 二分搜索
  - 状态压缩
  - 动态规划
categories:
  - [algo, LeetCode, 周赛]
date: 2021-11-07 23:54:32
updated:
---

Rank : `152/4384`
Solved: `4/4`

![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2021/11/8/LeetCode_周赛266.png)

[竞赛链接](https://leetcode-cn.com/contest/weekly-contest-266/)
<!--more-->

## [统计字符串中的元音子字符串](https://leetcode-cn.com/problems/count-vowel-substrings-of-a-string/)

### 思路
- 注意到数据范围很小, 直接$O(n^2)$枚举所有子串, 然后$O(n)$判断该子串是否符合要求即可

### Code
```cpp
class Solution {
public:
    int countVowelSubstrings(string s) {
        int ans = 0, n = s.size();
        for (int i = 0; i < n; i ++ ) 
            for (int j = i; j < n; j ++ ) {
                string tmp = s.substr(i, j - i + 1);
                int cnt = 0;
                bool flag = true;
                for (auto& c : {'a', 'e' ,'i' ,'o', 'u'}) {
                    int cur = count(tmp.begin(), tmp.end(), c);
                    cnt += cur;
                    // 子串不含某个元音字母则不满足条件
                    if (cur == 0)
                        flag = false;
                }
                // cnt记录字符串中所有元音字符的数量
                if (flag)
                    ans += cnt == tmp.size();
            }
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(n^3)$
- 空间复杂度$O(1)$
----

## [所有子字符串中的元音](https://leetcode-cn.com/problems/vowels-of-all-substrings/)

### 思路
- 遍历字符串, 枚举每个元音字符对`答案的贡献`
- 某个`i`位置的元音字符贡献为`包含i位置的所有子串的个数`
- 由乘法原理, 子串的个数为$(i + 1) * (n - i)$

### Code
```cpp
using LL = long long;
class Solution {
public:
    long long countVowels(string s) {
        set<int> str = {'a', 'e' ,'i' ,'o', 'u'};
        LL ans = 0, n = s.size();
        
        for (int i = 0; i < n; i ++ ) {
            char cur = s[i];
            int l = i;
            int r = n - i - 1;
            if (str.count(cur)) 
                ans += 1ll * (l + 1) * (r + 1);
        }
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(n)$
- 空间复杂度$O(1)$
----

## [分配给商店的最多商品的最小值](https://leetcode-cn.com/problems/minimized-maximum-of-products-distributed-to-any-store/)

### 思路
- 看到`最大值最小`立马想到`二分`
- 二分答案: 对于答案`x`, 所有的商店的上界不超过`x`
- 枚举所有商品, `i`号商品至少需要$\lceil \frac{quantities[i]}{x} \rceil$ 个商店

### Code
```cpp
class Solution {
public:
    int minimizedMaximum(int n, vector<int>& nums) {
        int m = nums.size();
        
        int l = 1, r = 1e5;
        while (l < r) {
            int mid = (r - l) / 2 + l;
            int cnt = 0;
            // cpp上取整方式之一
            for (auto& num : nums) 
                cnt += (num + mid - 1) / mid;
            if (cnt <= n)
                r = mid;
            else
                l = mid + 1;
        }
        return r;
    }
};
```

### 复杂度分析
- 时间复杂度$O(N * log1e5)$
- 空间复杂度$O(1)$
----

## [最大化一张图中的路径价值](https://leetcode-cn.com/problems/maximum-path-quality-of-a-graph/)
### 思路
- 动态规划:
  - $dist[i][j][k]$: 表示当前在`i`点, 还剩余`j`时间，走过的点的状态是`k`时候的最大价值 
  - 由于只能按照`时间递减`的顺序走, 因此`从大到小`遍历时间
- 状态转移:
  - 若当前状态是$dist[i][j][k]$, 枚举`i`号点的所有邻接点`u`, 更新$dist[u][j - costTime][k']$
    1. 若已经走过了`u`点, 即`k[u] = true`, 则$dist[u][j - costTime][k] = max(dist[u][j - costTime][k], dist[i][j][k])$
    2. 若没有走过`u`点, 即`k[u] = false`, 则$dist[u][j - costTime][k'] = max(dist[u][j - costTime][k'], dist[i][j][k] + value[u])$, 其中$k' = k | (1 << u)$
- 实现细节:
  用二进制表示状态`k`, 但无法用`int`或者`long long`等基础数据类型存储, 这里我使用了[bitset](https://en.cppreference.com/w/cpp/utility/bitset)存储状态

### Code
```cpp
const int N = 1005, M = 105;
using PII = pair<int, int>;

class Solution {
public:
    unordered_map<bitset<N>, int> dist[N][M];
    int maximalPathQuality(vector<int>& val, vector<vector<int>>& edge, int Mx) {
        int n = val.size();
        vector<vector<PII>> g(n);
        
        for (auto& e : edge) {
            int a = e[0], b = e[1], c = e[2];
            g[a].emplace_back(b, c);
            g[b].emplace_back(a, c);
        }
        
        dist[0][Mx][bitset<N>(1)] = val[0];
        
        for (int Time = Mx; Time >= 0; Time -- ) {
            for (int i = 0; i < n; i ++ )
                for (auto& [st, v] : dist[i][Time])
                    for (auto& [nxt, cost] : g[i]) {
                        if (Time < cost)
                            continue;
                        if (st[nxt] == 0) {
                            bitset<N> tmp = st;
                            tmp[nxt] = 1;
                            dist[nxt][Time - cost][tmp] = max(dist[nxt][Time - cost][tmp], dist[i][Time][st] + val[nxt]); 
                        }
                        else
                            dist[nxt][Time - cost][st] = max(dist[nxt][Time - cost][st], dist[i][Time][st]); 

                    }
        }
        // 最后答案枚举0号点的状态即可
        int ans = val[0];
        for (int r = Mx; r >= 0; r -- ) 
            for (auto& [_, v] : dist[0][r])
                ans = max(ans, v);
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(M * N * C)$: `M`为`maxTime`, `N`为点数, `C`为有效状态数
- 空间复杂度$O(M * N * C)$: `M`为`maxTime`, `N`为点数, `C`为有效状态数

----
**欢迎讨论指正**