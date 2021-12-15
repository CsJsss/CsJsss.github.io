---
title: '[LeetCode-周赛]271'
toc: true
tags:
  - 数据结构
  - 模拟
  - 前缀和
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2021-12-15 09:29:14
updated:
---

**Rank** :  `201/4561`
**Solved** :  `4/4`
![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2021/12/LeetCode第271场周赛.png)

[竞赛链接](https://leetcode-cn.com/contest/weekly-contest-271/)

<!--more-->

## [环和杆](https://leetcode-cn.com/problems/rings-and-rods/)

### 思路

对每个`杆`使用哈希表记录出现的`环`种类即可.

### Code

```cpp
class Solution {
public:
    int countPoints(string s) {
        unordered_map<int, unordered_set<char>> cnt;
        int n = s.size();
        
        for (int i = 0; i < n; i += 2) {
            char col = s[i];
            int idx = s[i + 1];
            cnt[idx].insert(col);
        }
        int ans = 0;
        for (auto& [k, v] : cnt)
            if (v.size() == 3)
                ans += 1;
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [子数组范围和](https://leetcode-cn.com/problems/sum-of-subarray-ranges/)

### 思路

由于数据范围很小, 因此使用**暴力**的方法即可.
可以使用单调栈分开统计最小和最大值的贡献, 时间和空间复杂度均为$O(N)$. 

### Code

```cpp
using LL = long long;
class Solution {
public:
    long long subArrayRanges(vector<int>& nums) {
        int n = nums.size();
        LL ans = 0;
        for (int i = 0; i < n; i ++ ) {
            int Mn = INT_MAX, Mx = INT_MIN;
            for (int j = i; j < n; j ++ ) {
                Mn = min(Mn, nums[j]);
                Mx = max(Mx, nums[j]);
                ans += Mx - Mn;
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

## [给植物浇水 II](https://leetcode-cn.com/problems/watering-plants-ii/)

### 思路

阅读理解模拟题. 按题意模拟即可.

### Code

```cpp
class Solution {
public:
    int minimumRefill(vector<int>& nums, int a, int b) {
        int n = nums.size();
        int L = 0, R = n - 1;
        // cA cB 灌水次数
        int cA = 0, cB = 0;
        // curA curB 当前水量
        int curA = a, curB = b;
        
        while (L <= R) {
            if (L == R) {
                // Bob
                if (curB > curA) {
                    if (curB < nums[L])
                        cB += 1;
                } else {
                // Alice
                    if (curA < nums[L])
                        cA += 1;
                }
                break;
            }
            if (curA >= nums[L]) {
                curA -= nums[L];
            } else {
                curA = a - nums[L];
                cA += 1;
            }
            if (curB >= nums[R]) {
                curB -= nums[R];
            } else {
                curB = b - nums[R];
                cB += 1;
            }
            L += 1, R -= 1;
        }
        return cA + cB;
    }
};

```

### 复杂度分析
- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [摘水果](https://leetcode-cn.com/problems/maximum-fruits-harvested-after-at-most-k-steps/)

### 思路

没看清楚题目范围, 还写了个离散化, 小亏.

具体思路使用**前缀和**的技巧, 暴力枚举所有的方案, 求这些方案的最大值即可.

我的方法是**枚举终点**. 
1. 特殊计算**一直往左**走和**一直往右**走.
2. 若终点小于等于`starPos`, 则先往右走, 然后再折回到终点最优.
3. 若终点大于等于`starPos`, 则先往左走, 然后掉头往右走最优.

### Code

```cpp
using LL = long long;
class Solution {
public:
    vector<int> all;
    
    int get(int x) {
        return lower_bound(all.begin(), all.end(), x) - all.begin() + 1;
    }
    
    int maxTotalFruits(vector<vector<int>>& nums, int stP, int k) {
        int n = nums.size();
        for (int i = 0; i < n; i ++ )
            all.push_back(nums[i][0]);    
        for (int i = stP - k; i <= stP + k; i ++ )
            all.push_back(i);
        
        sort(all.begin(), all.end());
        all.erase(unique(all.begin(), all.end()), all.end());
        
    
        int M = all.size();
        
        vector<LL> sum(M + 1, 0ll);
        
        for (int i = 0; i < n; i ++ ) {
            int idx = get(nums[i][0]);
            sum[idx] = nums[i][1];
        }
        
        for (int i = 1; i <= M; i ++ )
            sum[i] += sum[i - 1];
        
        LL ans = 0;
        // Left
        int curIdx = get(stP), leftIdx = get(stP - k), rightIdx = get(stP + k);
        ans = sum[curIdx] - sum[leftIdx - 1];
        // Right
        ans = max(ans, sum[rightIdx] - sum[curIdx - 1]);
        
        
        for (int ed = stP - k + 1; ed < stP + k; ed ++ ) {
            int start;
            if (ed <= stP) {
                start = stP + (k - (stP - ed)) / 2;
                ans = max(ans, sum[get(start)] - sum[get(ed) - 1]);
                // cout << ed << ' ' << start << ' ' << ans << endl;
            }
            if (ed >= stP) {
                start = stP - (k - (ed - stP)) / 2;
                ans = max(ans, sum[get(ed)] - sum[get(start) - 1]);
                // cout << ed << ' ' << start << ' ' << ans << endl;
            }
        }
        
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(N * logN)$
- 空间复杂度$O(N)$
----

**欢迎讨论指正**