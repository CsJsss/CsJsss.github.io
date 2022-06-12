---
title: '[LeetCode-周赛]297'
toc: true
tags:
  - 模拟
  - 动态规划
  - DFS
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2022-06-12 11:50:55
updated:
---

**Rank** : `218 / 5904`
**Solved** : `4/4`
![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2022/6/LeetCode第297场周赛.png)

[竞赛链接](https://leetcode.cn/contest/weekly-contest-297/)

<!--more-->

## [计算应缴税款总额](https://leetcode.cn/contest/weekly-contest-297/problems/calculate-amount-paid-in-taxes/) 

### 思路

**模拟**. 按照题意, 从前到后模拟即可.

### Code

```cpp
class Solution {
public:
    double calculateTax(vector<vector<int>>& nums, int sum) {
        double ans = 0.0;
        int prev = 0;
        
        for (auto& num : nums) {
            int cur = min(num[0] - prev, sum);
            ans += cur * num[1] * 0.01;
            prev = num[0];
            sum -= cur;
        }
        
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(1)$
----

## [网格中的最小路径代价](https://leetcode.cn/contest/weekly-contest-297/problems/minimum-path-cost-in-a-grid/)

### 思路

**动态规划**:
    1. 状态表示: 定义`f[i][j]`为走到`(i, j)`点时的最小代价. 答案即为最后一行的最小值.
    2. 状态计算: 
        用**当前行去更新下一行的状态**. 即已知`f[i][j]`, 去更新所有(i, j)能走到的位置(即下一行).
        $$ f[i + 1][k] = min(f[i + 1][k], f[i][j] + nums[i + 1][k] + cost[nums[i][j]][k]), \ k \in [0, m - 1]$$

### Code

```cpp
class Solution {
public:
    int minPathCost(vector<vector<int>>& nums, vector<vector<int>>& cost) {
        int n = nums.size(), m = nums[0].size();
        
        vector<vector<int>> f(n, vector<int>(m, 1e9));
        
        for (int i = 0; i < n - 1; i ++ )
            for (int j = 0; j < m; j ++ ) {
                if (i == 0)
                    f[i][j] = nums[i][j];
                for (int k = 0; k < m; k ++ )
                    f[i + 1][k] = min(f[i + 1][k], f[i][j] + nums[i + 1][k] + cost[nums[i][j]][k]);
            }
        
        return *min_element(f[n - 1].begin(), f[n - 1].end());
    }
};
```

### 复杂度分析

- 时间复杂度$O(N * M^2)$
- 空间复杂度$O(N * M)$
----

## [公平分发饼干](https://leetcode.cn/contest/weekly-contest-297/problems/fair-distribution-of-cookies/)

### 思路

**DFS**. 深搜剪枝.

### Code

```cpp
class Solution {
public:
    int ans;
    int n;
    
    void dfs(int u, vector<int>& cnt, int k, vector<int>& nums) {
        int mx = *max_element(cnt.begin(), cnt.end());
        if (u == n) {
            ans = min(ans, mx);
            return ;
        }
        if (mx >= ans)
            return ;
        for (int i = 0; i < k; i ++ ) {
            cnt[i] += nums[u];
            dfs(u + 1, cnt, k, nums);
            cnt[i] -= nums[u];
        }
    }
    
    int distributeCookies(vector<int>& nums, int k) {
        this -> n = nums.size();
        ans = reduce(nums.begin(), nums.end());
        vector<int> cnt(k, 0);
        dfs(0, cnt, k, nums);
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$不会分析$
- 空间复杂度$O(K)$
----

## [公司命名](https://leetcode.cn/contest/weekly-contest-297/problems/naming-a-company/)

### 思路

枚举每一个字符串作为`ideaA`, 求合法的`ideaB`.

假设当前字符串为`HaTa`(`Ha`表示首字母). 那么能作为`ideaB`的首字符的选择是有限的, 假设`ideaB`的首字符为`Hx`, 那么`HxTa`一定没出现过. 这样就知道了所有可选的`Hx`. 现在的问题是: `Hx`的可选后缀`Tx`, 多少个`HaTx`是合法的.

这个问题可以用补集的思想做. 因为我们知道全集: 以`Ha`开头的字符串的个数; 以及其补集: 出现过多少个形如`HaTx`的字符串.

全集很好处理. 补集的话直观来看, 就是`HxTx`字符串中, 出现过多少个`HaTx`. 这个我们只需对每一个后缀处理出其可能的前缀首字母(26种可能), 然后这些前缀两两之间会对补集有1的贡献.


### Code

```cpp
using LL = long long;
class Solution {
public:
    int cnt[26], sub[26][26];
    long long distinctNames(vector<string>& str) {
        memset(cnt, 0, sizeof(cnt));
        memset(sub, 0, sizeof(sub));
        
        unordered_map<string, set<int>> mp;
        for (auto& s : str) {
            string tmp = s.substr(1);
            mp[tmp].insert(s[0]);
            cnt[s[0] - 'a'] ++;
        }
        
        for (auto& [_, v] : mp) {
            for (auto& a : v)
                for (auto& b : v)
                    sub[a - 'a'][b - 'a'] ++ ;
        }
        
        LL ans = 0;
        for (auto& s : str) {
            string tmp = s.substr(1);
            int ha = s[0];
            for (char hx = 'a'; hx <= 'z'; hx ++ ) {
                if (mp[tmp].count(hx))
                    continue;
                int cur = cnt[hx - 'a'] - sub[hx - 'a'][ha - 'a'];
                ans += cur;
            }
        }
        
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(M * M * N), M = 26$
- 空间复杂度$O(M * N)$
----
**欢迎讨论指正**