---
title: 第一届ACC(AcWing Cup)全国高校联赛(决赛)题解
toc: true
tags:
  - AcWing Cup
categories:
  - - algo
    - AcWing
date: 2022-03-27 20:14:11
updated:
---

**Rank** : `57/758`
**Solved** : `3/3`

![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2022/3/AcWinCup.png)

[竞赛链接](https://www.acwing.com/activity/content/introduction/1285/)

<!--more-->

## [两个闹钟](https://www.acwing.com/problem/content/description/4382/)

### 思路

**暴力**. 应该是用扩展欧几里得, 但上来写了发暴力, 然后就过了...

### Code

```cpp
#include <bits/stdc++.h>

using namespace std;


int main() {
    int a, b, c, d;

    cin >> a >> b >> c >> d;
    
    int find = 0, res = INT_MAX;
    
    for (int i = 0; i <= 100; i ++ )
        for (int j = 0; j <= 100; j ++ ) {
            if ((b + i * a) == (d + j * c)) {
                find = 1;
                res = min(res, b + i * a);
            }
        }
        
    if (find)
        cout << res << '\n';
    else
        cout << -1 << '\n';
    return 0;
}

```

### 复杂度分析

- 时间复杂度$O(N^2)$
- 空间复杂度$O(1)$
----

## [合并石子](https://www.acwing.com/problem/content/description/4383/)

### 思路

**贪心**. 双指针扫描
- 如果当前两段相同, 则答案 + 1, 重新开始统计.
- 如果当前`a`段 < `b`段, 则加上`a`段的数.
- 如果当前`a`段 > `b`段, 则加上`b`段的数.

最后需要处理一下边界, 就如同归并排序一样.

### Code

```cpp
#include <bits/stdc++.h>

using namespace std;

const int N = 1e5 + 5;
int a[N], b[N];

int main() {
    int n, m;
    cin >> n >> m;
    
    for (int i = 1; i <= n; i ++ )
        cin >> a[i];
    
    for (int j = 1; j <= m; j ++ )
        cin >> b[j];
    
    int i = 2, j = 2, step = 0;
    int sa = a[1], sb = b[1];
    
    while (i <= n and j <= m) {
        if (sa == sb) {
            step ++ ;
            sa = 0, sb = 0;
            if (i <= n) {
                sa += a[i];
                i ++ ;
            }
            if (j <= m) {
                sb += b[j];
                j ++ ;
            } 
        } else if (sa < sb) {
            if (i <= n) {
                sa += a[i];
                i ++ ;
            }
        } else if (sa > sb) {
            if (j <= m) {
                sb += b[j];
                j ++ ;
            }            
        }
    }
    
    while (i <= n)
        sa += a[i ++ ];
    
    while (j <= m)
        sb += b[j ++ ];
    
    if (sa != sb)
        step = 0;
    else if (sa)
        step ++ ;
    
    cout << step << '\n';
    return 0;
}
```

### 复杂度分析

- 时间复杂度$O(N + M)$
- 空间复杂度$O(N + M)$
----

## [翻转树边](https://www.acwing.com/problem/content/4384/)

### 思路

**换根动态规划**. 我们首先计算以`u`为根时, `u`可以遍历其所有子节点所需的代价. 这样我们可以求出某个点的正确答案. 假设是`1`号结点.

然后我们`换根dp`, 我们从父节点`u`推算子结点`v`的正确答案. 
- 如果`u -> v的代价是0`, 那么当以`v`为根时, 我们只需要将`u -> v`翻转即可. 所以 $f[v] = f[u] + 1$. 
- 如果`u -> v的代价是1`, 那么当以`v`为根时, 这条边是无需代价的, 所以 $f[v] = f[u] - 1$. 

### Code

```cpp
#include <bits/stdc++.h>

using namespace std;
using PII = pair<int, int>;
const int N = 2e5 + 5;

vector<PII> g[N];
int f[N];

int dfs(int u, int fa) {
   int& ret = f[u];
   
   for (auto& [v, w] : g[u]) {
       if (v == fa)
            continue;
        ret += dfs(v, u) + w;
   }
   return ret;
}

void dp(int u, int fa) {
    for (auto& [v, w] : g[u]) {
        if (v == fa)
            continue;
        if (w == 0)
            f[v] = f[u] + 1;
        else
            f[v] = f[u] - 1;
        dp(v, u);
    }
}

int main() {
    int n;
    cin >> n;
    
    for (int i = 1; i < n; i ++ ) {
        int a, b;
        cin >> a >> b;
        g[a].push_back({b, 0});
        g[b].push_back({a, 1});        
    }
    
    
    dfs(1, -1);
    dp(1, -1);
    
    int mn = INT_MAX;
    
    for (int i = 1; i <= n; i ++ )
        mn = min(mn, f[i]);
    
    cout << mn << '\n';
    for (int i = 1; i <= n; i ++ )
        if (mn == f[i])
            cout << i << ' ';
    cout << '\n';
    return 0;
}
```

### 复杂度分析
- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----
**欢迎讨论指正**