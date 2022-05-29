---
title: '[LeetCode-周赛]295'
toc: true
tags:
  - 枚举
  - 模拟
  - 区间最值
  - 0-1BFS
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2022-05-29 11:31:58
updated:
---

**Rank** : `135 / 16846`
**Solved** : `4/4`
![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2022/5/LeetCode第295场周赛.png)

[竞赛链接](https://leetcode.com/contest/weekly-contest-295)

最近第一次做出四题, 赶紧把思路分享一下hhhhhh.

<!--more-->

## [Rearrange Characters to Make Target String](https://leetcode.com/contest/weekly-contest-295/problems/rearrange-characters-to-make-target-string/) 

### 思路

**枚举**. 分别统计一下`s`和`target`中的字符数量, 然后对于`target`中的每个字符单独考虑, 看看`s`中最多能组成几组, 最后取**每个字符对应的最小值**即可.

### Code

```cpp
class Solution {
public:
    int rearrangeCharacters(string s, string target) {
        unordered_map<char, int> cnt, ct;
        for (auto& c : s)
            cnt[c] ++ ;
        for (auto& c : target)
            ct[c] ++ ;
        int ans = INT_MAX;
        
        for (auto& [k, v] : ct)
            ans = min(ans, cnt[k] / v);
        
        if (ans == INT_MAX)
            ans = 0;
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N + M)$
- 空间复杂度$O(N + M)$
----

## [Apply Discount to Prices](https://leetcode.com/contest/weekly-contest-295/problems/apply-discount-to-prices/)

### 思路

**模拟**. 模拟题意即可. 处理字符串`c++`相对麻烦一点, 所以我这里使用了`python`. 

### Code

```python
class Solution:
    def discountPrices(self, s: str, discount: int) -> str:
        d = discount * 0.01
        words = s.split(' ')
        ans = []
        
        for word in words:
            cur = word
            if word[0] == '$' and word[1:].isnumeric():
                cur = float(cur[1:]) * (1.0 - d)
                cur = format(cur, ".2f")
                cur = '$' + str(cur)
            ans.append(cur)
        ans = " ".join(ans)
        return ans
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [Steps to Make Array Non-decreasing](https://leetcode.com/contest/weekly-contest-295/problems/steps-to-make-array-non-decreasing/)

### 思路

**区间最值**. 考虑每一个数需要几步才能删掉他, 记为`f[i]`.

1. 如果该数左边没有比它大的数, 那么该数无需删除, `f[i] = 0`.
2. 如果该数左边有比它大的数, 该数需要删除, `f[i] > 0`.


假设当前数下标为`i`, 左边第一个比它大的数下标为`j`, 那么**删除当前数的代价**为:

$$ f[i] = max(f[k]) + 1, \ k \in [j + 1, i]$$

因为只有将`[j + 1, i - 1]`之间的数全部删掉后, 才能再下一步中使用`nums[j]`去删掉`nums[i]`. 

这样问题转化成区间最值, 可以使用线段树解决.(没板子, 抄区间最值搞了老半天....)

### Code

```cpp
const int N = 1e5 + 5;

struct Node {
    int l, r;
    int v;
} tr[N * 4];

void pushup(int u) {
    tr[u].v = max(tr[u + u].v, tr[u + u + 1].v);
}

void build(int u, int l, int r) {
    tr[u] = {l, r};
    // tr[u].v = 0;
    if (l < r) {
        int mid = l + r >> 1;
        build(u + u, l, mid);
        build(u + u + 1, mid + 1, r);
        pushup(u);
    }
}

int query(int u, int l, int r) {
    if (tr[u].l == l and tr[u].r == r)
        return tr[u].v;
    int mid = tr[u].l + tr[u].r >> 1;
    int v = 0;
    if (r <= mid) 
        v = query(u + u, l, r);
    else if (l > mid)
        v = query(u + u + 1, l, r);
    else {
        v = max(query(u + u, l, mid), query(u + u + 1, mid + 1, r));
    }
    return v;
}

void modify(int u, int x, int c) {
    if (tr[u].l == x and tr[u].r == x) {
        tr[u].v = c;
        return ;
    }

    int mid = tr[u].l + tr[u].r >> 1;
    if (x <= mid)
        modify(u + u, x, c);
    else    
        modify(u + u + 1, x, c);
    pushup(u);
}

class Solution {
public:
    int totalSteps(vector<int>& nums) {
        int n = nums.size();
        vector<int> f(n + 1, 0), idx(n + 1, 0);
        stack<int> stk;
        for (int i = 1; i <= n; i ++ ) {
            int cur = nums[i - 1];
            while (stk.size() and nums[stk.top() - 1] <= cur)
                stk.pop();
            if (stk.size())
                idx[i] = stk.top();
            stk.push(i);
        }
        
        build(1, 1, n);
        for (int i = 1; i <= n; i ++ ) {
            if (idx[i] == 0)
                continue;
            // for (int j = idx[i] + 1; j < i; j ++ )
            //     ans = max(ans, f[j]);
            assert (idx[i] + 1 <= i);
            f[i] = query(1, idx[i] + 1, i) + 1;
            modify(1, i, f[i]);
        }
        
        return *max_element(f.begin(), f.end());
    }
};
```

### 复杂度分析

- 时间复杂度$O(N * logN)$
- 空间复杂度$O(N)$
----

## [Minimum Obstacle Removal to Reach Corner](https://leetcode.com/contest/weekly-contest-295/problems/minimum-obstacle-removal-to-reach-corner/)

### 思路

**经典0-1BFS**. 

把每个格子看作点, 格子与相邻格子连边. 那么**边的权重只会是0或1**. 问题转化成从起点到终点的最短路, 且边的权重只有0/1. 可以使用`0-1 BFS` / `Dijkstra`解决.

### Code

```cpp
// 0-1 BFS
using PII = pair<int, int>;
const int dx[4] = {0, 0, 1, -1}, dy[4] = {1, -1, 0, 0};
class Solution {
public:
    int minimumObstacles(vector<vector<int>>& g) {
        int n = g.size(), m = g[0].size();
        constexpr int INF = 1e9;
        vector<vector<int>> dist(n, vector<int>(m, INF));
        
        dist[0][0] = 0;
        deque<PII> qu;
        qu.emplace_front(0, 0);
        
        while (qu.size()) {
            auto [x, y] = qu.front();
            qu.pop_front();
            
            for (int i = 0; i < 4; i ++ ) {
                int nx = x + dx[i], ny = y + dy[i];
                if (nx >= 0 and nx < n and ny >= 0 and ny < m) {
                    if (g[nx][ny] == 1 and dist[nx][ny] > dist[x][y] + 1) {
                        dist[nx][ny] = dist[x][y] + 1;
                        qu.emplace_back(nx, ny);
                    } else if (g[nx][ny] == 0 and dist[nx][ny] > dist[x][y]) {
                        dist[nx][ny] = dist[x][y];
                        qu.emplace_front(nx, ny);
                    }
                }
            }
        }
        
        return dist[n - 1][m - 1];
    }
};
```

### 复杂度分析

- 时间复杂度$O(N * M)$
- 空间复杂度$O(N * M)$
----

**欢迎讨论指正**