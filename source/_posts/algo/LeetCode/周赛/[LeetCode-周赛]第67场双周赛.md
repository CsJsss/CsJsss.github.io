---
title: '[LeetCode-周赛]第67场双周赛'
toc: true
tags:
  - 数据结构
  - 动态规划
  - 深度优先搜索
  - 平衡树
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2021-12-15 09:29:09
updated:
---

**Rank** :  `178/2923`
**Solved** :  `4/4`

![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2021/12/LeetCode第67场双周赛.png)

[竞赛链接](https://leetcode-cn.com/contest/biweekly-contest-67/)

<!--more-->

## [找到和最大的长度为 K 的子序列](https://leetcode-cn.com/problems/find-subsequence-of-length-k-with-the-largest-sum/)

### 思路
排序后可知最大的`k`个数是**确定**的(是哪些数以及其个数确定), 但是其相对位置是不定的. 因此需要使用某种**数据结构**确定后的k个值(必须选的)记录一下, 然后遍历原数组.
1. 若当前值还可以出现, 则加入答案, 当前值出现几次减一.
2. 若当前值不可以出现了, 跳过即可.

支持上述操作的数据结构可以是**哈希表**、**multiset**等.

### Code

```cpp
class Solution {
public:
    vector<int> maxSubsequence(vector<int>& nums, int k) {
        vector<int> cc = nums;
        sort(cc.begin(), cc.end(), greater<int>());
        unordered_map<int, int> cnt;
        int n = nums.size();
        for (int i = 0; i < k; i ++ )
            cnt[cc[i]] += 1;
        
        vector<int> ret;
        for (int i = 0; i < n; i ++ ) {
            if (cnt[nums[i]] > 0) {
                cnt[nums[i]] -= 1;
                ret.push_back(nums[i]);
            }
        }
        return ret;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N * logN)$(排序的时间复杂度)
- 空间复杂度$O(N)$
----

## [适合打劫银行的日子](https://leetcode-cn.com/problems/find-good-days-to-rob-the-bank/)

### 思路
**很有特点的一类题型**.
这类题型通常求数组中满足条件限制的所有下标. 条件限制通常为该下标处左右两边的一些性质. 本题的限制在从`i`往左右两边看, 连续`time`天都必须是非递减的.

**解决这类题型的通用方法一般是先将问题进行转化, 然后使用递推(动态规划), 最后遍历数组找符合要求的下标**. 

考虑到左右对称, 以下就以左边为例进行分析. 

1. 问题转化. `i`往坐看连续`time`天都是非递减的, 可以将问题转化成`i`往坐看, **最多**多少天非递减. 通过将问题转化成一个最值问题, 使用最值进行判定.

2. 递推. 记**L[i]**为在`i`处往左看, 非递减的最大长度. 简单动态规划即可~
  - 若$nums[i] <= nums[i - 1]$. 则 $L[i] = L[i - 1] + 1$
  - 若$nums[i] > nums[i - 1]$. 则 $L[i] = 0$

3. 遍历原数组使用 **L** 和 **R** 求解符合要求的下标即可.

### Code

```cpp
class Solution {
public:
    vector<int> goodDaysToRobBank(vector<int>& nums, int time){
        int n = nums.size();
        vector<int> L(n, 0), R(n, 0);
        
        for (int i = 1; i < n; i ++ ) {
            if (nums[i] <= nums[i - 1])
                L[i] = L[i - 1] + 1;
        }
        for (int i = n - 2; i >= 0; i -- ) {
            if (nums[i] <= nums[i + 1])
                R[i] = R[i + 1] + 1;
        }
        vector<int> ret;
        for (int i = 0; i < n; i ++ ) {
            if (i - time >= 0 and i + time < n) {
                if (L[i] >= time and R[i] >= time)
                    ret.push_back(i);
            }     
        }
        return ret;
    }
};

```
### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [引爆最多的炸弹](https://leetcode-cn.com/problems/detonate-the-maximum-bombs/)

### 思路
做题的时候题意理解错了, 上来直接并查集求最大的联通分量. WA的很快啊! 仔细看样例1才发现, `引爆`不具有对称性. `A`引爆`B`时, `B`不一定引爆`A`.

首先将问题转化成一个图论问题(**有向图**). 每个圆看作一个点, 每条引爆关系看作一条边. 若`A`能引爆`B`, 则从点`A`连出一条边指向`B`.
考虑到数据范围很小, 构建完有向图后, 直接对每个点暴力使用DFS, 计算以该点出发最多能到的点的个数.

### Code

```cpp

class Solution {
public:
    int vis[100005];
    vector<vector<int>> g;
    
    void dfs(int u) {
        vis[u] = 1;
        for (auto& v : g[u]) {
            if (vis[v] == 0)
                dfs(v);   
        }
    }
    
    int maximumDetonation(vector<vector<int>>& nums) {
        int n = nums.size();
        g.resize(n);
         
        for (int i = 0; i < n; i ++ )
            for (int j = 0; j < n; j ++ ) {
                if (i == j)
                    continue;
                long long dist = 1ll *(nums[i][0] - nums[j][0]) * (nums[i][0] - nums[j][0]) + 1ll * (nums[i][1] - nums[j][1]) * (nums[i][1] - nums[j][1]);
                long long r = 1ll * nums[i][2] * nums[i][2];
                if (dist <= r) {
                    g[i].push_back(j);                 
                    // cout << i << ' ' << j << endl;                    
                }
            }
        
        int ret = 1;
        for (int i = 0; i < n; i ++ ) {
            memset(vis, 0, sizeof(vis));
            dfs(i);
            int cur = 0;
            for (int j = 0; j < n; j ++ )
                if (vis[j] == 1)
                    cur += 1;
            ret = max(ret, cur);
        }
        return ret;
    }
};

```

### 复杂度分析
- 时间复杂度$O(N^2)$
- 空间复杂度$O(N)$
----

## [序列顺序查询](https://leetcode-cn.com/problems/sequentially-ordinal-rank-tracker/)

### 思路

使用平衡树的`Get Value By Rank`即可完成, 比赛中使用了`python`的`sortedcontainers`第三方库偷鸡了.

### Code

```python
from sortedcontainers import SortedList
class SORTracker:

    def __init__(self):
        self.sl = SortedList()
        self.idx = 0

    def add(self, name: str, score: int) -> None:
        self.sl.add((-score, name))

    def get(self) -> str:
        ret = self.sl[self.idx]
        self.idx += 1
        return ret[1]


# Your SORTracker object will be instantiated and called as such:
# obj = SORTracker()
# obj.add(name,score)
# param_2 = obj.get()

```

### 复杂度分析
- 时间复杂度$O(N * logN)$
- 空间复杂度$O(N)$
----

**欢迎讨论指正**