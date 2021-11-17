---
title: '[LeetCode]跳跃游戏合集'
toc: true
date: 2021-11-17 09:37:28
updated:
tags:
  - BFS
  - 最短路
  - 动态规划
  - 拓扑排序
  - 单调队列
  - 优先队列
  - 前缀和
categories:
  - - algo
    - LeetCode
    - 系列合集
---

简单整理一下LeetCode上`跳跃游戏`系列题目. 包含`跳跃游戏`、`跳跃游戏II`、`跳跃游戏III`、`跳跃游戏IV`、`跳跃游戏V`、`跳跃游戏VI`、`跳跃游戏VII`共七题.

<!--more-->
## [跳跃游戏](https://leetcode-cn.com/problems/jump-game/)
### 题目描述
开始位于`1`号点, 每次在`i`号点最远可以跳跃`nums[i]`单位距离, 判断能否跳到`n`号点.

### 思路
- 我们可以把每个下标看成一个**点**, 每次在`i`号点跳跃认为是从`i`连边到`j`, 且$j\in [max(1, i - nums[i],\ min(n, i + nums[i]))]$.
- 这样问题转化成判断是否存在至少一条从`1`号点到`n`号点的路径, 即`1`号点与`n`号点是否**联通**.
- 暴力使用`BFS`等算法求解的时候, 正确性是毫无疑问的, 但时间复杂度过高$O(N^2)$, 会TLE.
- 暴力时间复杂度高的原因是: 每个点会被**遍历多次**, 如果优化每个点被遍历的次数, 那么问题就得到了解决.
- 结合题意, 有以下**观察**:
    1. 如果当前位于`i`号点, 那么`1 - i`之间的所有点已经可达了(即被遍历过了). 假设是从`j`点跳到了`i`点($j < i$), 那么`j - i`之间的所有点可以被`j`遍历到, 问题规模减小到`1 - j`, 归纳下去即可证明.
    2. 有了观察`1`, 当我们位于`i`号点的时候, 只需关心它向右能跳到的点. `i`向右最远能跳到$R = min(n, i + nums[i])$. 我们从`R`倒着向`i`遍历:
        - 若某点没被访问过, 置为`True`, 继续向前遍历. 
        - 若某点已经被访问过了, 则可由观察`1`得到, 该点极其左边的点全被访问过, 退出循环即可.、
- 最终对于每个点, 我们**至多遍历一次**.

### Code
```cpp
// 写法1
class Solution {
public:
    bool canJump(vector<int>& nums) {
        int n = nums.size();
        vector<bool> f(n, false);
        f[0] = true;
        for (int i = 0; i < n; i ++ )
            if (f[i]){
                int j = min(n - 1, nums[i] + i);
                while (f[j] == false)
                    f[j --] = true;
            }
        return f[n - 1];
    }
};
```
```cpp
/* 
写法2:稍微优化上述写法
      记录可行的跳的最远的位置 Mx 是哪
      利用观察1, 只要当前点i <= Mx, 则当前点一定可达.
*/
class Solution {
public:
    bool canJump(vector<int>& nums) {
        int n = nums.size();
        vector<bool> f(n, false);
        f[0] = true;
        int Mx = nums[0];
        for (int i = 1; i < n; i ++ ) {
            if (Mx >= i) {
                f[i] = true; 
                Mx = max(Mx, i + nums[i]);                
            }
        }
        return f[n - 1];
    }
};
```
----

### 复杂度分析
- 时间复杂度$O(N)$
- 空间复杂度$O(N)$

## [跳跃游戏 II](https://leetcode-cn.com/problems/jump-game-ii/)
### 题目描述
开始位于`1`号点, 每次在`i`号点最远可以跳跃`nums[i]`单位距离, 判断跳到`n`号的最少跳跃次数(保证可以到达).

### 思路
有了第一题的分析过程, 这题可以很自然的使用第一题的分析思路: 只需求`1`号点到`n`号点的最短路.
- 利用**BFS**的性质: 每个点第一次被遍历的时候一定是该点的最短距离. 用第一题思路实现即可.

### Code
```cpp
// 解法1: 上述思路的实现
class Solution {
public:
    int jump(vector<int>& nums) {
        int n = nums.size();
        vector<int> f(n, -1);
        f[0] = 0;
        
        for (int i = 0; i < n; i ++ ) {
            int R = min(n - 1, i + nums[i]);
            while (f[R] == -1)
                f[R --] = f[i] + 1;
        }
        return f[n - 1];
    }
};
```
```cpp
/*  解法2：
    简单提一下另外一种思路: dp或者最短路的想法
    使用优先队列记录所有可达的点的信息: 最短距离以及它所能跳到的最远点
    当遍历到i的时候, 贪心的从优先队列中取最短距离最小的点：
        若它能到到达i, 则更新i
        否则直接弹出优先队列, 因为它不可能更新i之后的任意一个点.
    这样每个点最多 入/出 优先队列一次.
    时间复杂度为 O(N * logN)
    空间复杂度为 O(N)
*/
class Solution {
public:
    int jump(vector<int>& nums) {
        int n = size(nums);
        vector<int> f(n, 1e9);
        priority_queue<pair<int, int>> heap;
        heap.emplace(0, nums[0]);
        f[0] = 0;
        for (int i = 1; i < n; i ++ ){
            auto [t, ed] = heap.top();
            while (heap.size() && ed < i){
                heap.pop();
                t = heap.top().first;
                ed = heap.top().second;
            }
            f[i] = -t + 1;
            heap.emplace(-f[i], i + nums[i]);
        }
        return  f[n - 1]; 
    }
};
```
----

### 复杂度分析
- 时间复杂度$O(N)$
- 空间复杂度$O(N)$

## [跳跃游戏 III](https://leetcode-cn.com/problems/jump-game-iii/)
### 题目描述
开始位于`start`号点, 每次在`i`号点可以跳到`i + nums[i]`或`i - nums[i]`, 判断能否跳到`nums[k] = 0`的某个点.

### 思路
有了前面题目的分析, 这题就是简单的BFS. 每个点最多出去两条边, 暴力BFS即可.

### Code
```cpp
class Solution {
public:
    bool canReach(vector<int>& arr, int st) {
        int n = arr.size();
        vector<bool> f(n, false);
        queue<int> qu;
        f[st] = true;
        qu.push(st);
        
        while (qu.size()) {
            auto t = qu.front();
            qu.pop();
            if (t + arr[t] < n and t + arr[t] >= 0 and f[t + arr[t]] == false)
                f[t + arr[t]] = true, qu.push(t + arr[t]); 
            if (t - arr[t] < n and t - arr[t] >= 0 and f[t - arr[t]] == false)
                f[t - arr[t]] = true, qu.push(t - arr[t]); 
        }
        bool flag = false;
        for (int i = 0; i < n; i ++ ) {
            if (arr[i] == 0 and f[i])
                flag = true;
        }
        
        return flag;
    }
};
```
----
### 复杂度分析
- 时间复杂度$O(N)$
- 空间复杂度$O(N)$

## [跳跃游戏 IV](https://leetcode-cn.com/problems/jump-game-iv/)
### 题目描述
开始位于`1`号点, 每次在`i`号点可以跳到`i + 1`、`i - 1`、j(满足nums[i] == nums[j]), 求解跳到`n`号点的最短步数.

### 思路
题目求解的是最短路, 自然就往最短路算法上想(BFS、Dijkstra等). 由于本题边权均为1, 因此考虑使用**BFS**算法求解.
- 由题目可知, 所有值相同的点之间存在一条代价为1的边. 因此我们先使用**哈希表**得到所有值相同的点, 接着BFS即可.
- 注意优化的一点: BFS第一次遍历到的时候, 其最短路就已经确定了. 因此我们遍历了一遍某一个值相同的集合后, 直接从**哈希表**删除该集合即可.
### Code
```cpp
const int INF = 1e8;
class Solution {
public:
    int minJumps(vector<int>& arr) {
        unordered_map<int, vector<int>> mp;
        int n = arr.size();
        for (int i = 0; i < n; i ++ ) {
            int c = arr[i];
            mp[c].push_back(i);
        }
        vector<int> f(n, INF);
        queue<int> qu;
        f[0] = 0;
        qu.push(0);
        
        while (qu.size()) {
            auto t = qu.front();
            qu.pop();
            if (t + 1 < n and f[t + 1] == INF)
                f[t + 1] = f[t] + 1, qu.push(t + 1);
            if (t - 1 >= 0 and f[t - 1] == INF)
                f[t - 1] = f[t] + 1, qu.push(t - 1);
            for (auto& c : mp[arr[t]]) {
                if (f[c] == INF)
                    f[c] = f[t] + 1, qu.push(c);
            }
            mp.erase(arr[t]);
        }
        return f[n - 1];
    }
};
```
----
### 复杂度分析
- 时间复杂度$O(N)$
- 空间复杂度$O(N)$

## [跳跃游戏 V](https://leetcode-cn.com/problems/jump-game-v/)
### 题目描述
在`i`号点可以跳到`j`号的要求是:
  1. arr[i] > arr[j]
  2. $abs(i - j) <= d$
  3. $i - j$ 之间除`i`以外的点的值均小于$arr[i]$
可以从任意点开始, 求解**最多能跳多少个点**.

### 思路
- 观察到数据范围为1000, 因此使用$O(N^2)$的算法求解即可.
- 依然利用前面题目的思路, 将每个下标视作一个点. `i`号点能跳到`j`号点, 则认为存在`i`指向`j`的一条有向边.
- 关键的约束条件为$arr[i] > arr[j]$, 这样的话构建出的图一定为[有向无环图(DAG)](https://baike.baidu.com/item/%E6%9C%89%E5%90%91%E6%97%A0%E7%8E%AF%E5%9B%BE). 
- 问题转化成**求有向无环图上的一条最长路径**. 因为存在拓扑序, 因此按照序列**递推(动态规划, DP)求解**即可.
- 定义`f[u]`为走到`u`点时的最大值. 若存在有向边$v \rightarrow u$, 则有:
    $$f[u] = max(f[u], f[v] + 1)$$
- 因为按照**拓扑序**的顺序递推, 因此当计算`u`点时, 其所依赖的点`v`已经全部被计算过了, 保证了正确性.

### Code
```cpp
class Solution {
public:
    int maxJumps(vector<int>& arr, int d) {
        int n = arr.size();
        vector<vector<int>> g(n, vector<int>(n, 0));
        vector<int> in(n, 0), f(n, 1);
        // O(n^2)预处理有向边
        for (int i = 0; i < n; i ++ ) {
            // L 
            for (int j = i - 1, Mx = arr[i] - 1; j >= max(0, i - d); j -- ) {
                Mx = max(Mx, arr[j]);
                if (Mx >= arr[i])
                    break;
                g[i][j] = 1;
                in[j] ++ ;
            }
            // R
            for (int j = i + 1, Mx = arr[i] - 1; j <= min(n - 1, i + d); j ++ ) {
                Mx = max(Mx, arr[j]);
                if (Mx >= arr[i])
                    break;
                g[i][j] = 1;
                in[j] ++ ;
            }
        }
        // 拓扑排序 + 递推(DP)
        queue<int> qu;
        for (int i = 0; i < n; i ++ ) {
            if (in[i] == 0)
                qu.push(i);
        }
        
        while (qu.size()) {
            auto t = qu.front();
            qu.pop();
            for (int i = 0; i < n; i ++ ) {
                // t 能走到 i 点
                if (g[t][i]) {
                    f[i] = max(f[i], f[t] + 1);
                    if (-- in[i] == 0)
                        qu.push(i);
                }
            }
        }
        int ans = 0;
        for (int i = 0; i < n; i ++ )
            ans = max(ans, f[i]);
        return ans;
    }
};
```
### 复杂度分析
- 时间复杂度$O(N^2)$
- 空间复杂度$O(N)$

## [跳跃游戏 VI](https://leetcode-cn.com/problems/jump-game-vi/)
### 题目描述
开始位于`1`号点, 每次最多往前跳`k`步, 求跳到`n`时的最大得分(最大数字之和).

### 思路
- 动态规划:
    1. 状态表示: 定义`f[i]`为走到`i`点时的最大得分. 答案即位`f[n]`.
    2. 状态计算：依据题目要求, 最多跳`k`步, 因此
        $$ f[i] = max(f[j] + nums[i]), \ j \in [max(1, i - k), i - 1]$$
    3. 朴素状态转移复杂度是$O(K)$, 会超时. 注意到转移要求的是**滑动窗口**内的最大值. 因此可以利用**单调队列**或**优先队列**(类似第二题解法2)优化.

### Code
```cpp
class Solution {
public:
    int maxResult(vector<int>& nums, int k) {
        int n = nums.size();
        vector<int> f(n, 0);
        deque<int> dq;
        
        for (int i = 0; i < n; i ++ ) {
            if (dq.size() and i - dq.front() > k)
                dq.pop_front();
            f[i] = nums[i];
            if (dq.size())
                f[i] = nums[i] + f[dq.front()];
            while (dq.size() and f[dq.back()] < f[i])
                dq.pop_back();
            dq.push_back(i);
        }
        return f[n - 1];
    }
};
```
----
### 复杂度分析
- 时间复杂度$O(N)$(单调队列)、$O(N * logN)$(单调队列)
- 空间复杂度$O(N)$

## [跳跃游戏 VII](https://leetcode-cn.com/problems/jump-game-vii/)
### 题目描述
开始位于`1`号点, 每次向前跳的距离有限制, 判断能否跳到`n`号点.

### 思路
- 使用动态规划解决. 定义`f[i]`为是否能够跳到`i`位置, 只需判断**是否存在**$j \in [i - maxJump, i - minJump]$, 使得$f[j] = True$成立.
- 为了快速判断是否存在`j`, 使用**前缀和**的思想. 记$s[i] = \sum_{j = 0}^{i}f[i]$. 
- 这样每次只需判断是否有$s[i - minJump] - s[i - maxJump - 1] > 0$成立即可.

### Code
```cpp
class Solution {
public:
    bool canReach(string str, int Mn, int Mx) {
        int n = str.size();
        vector<int> f(n + 1, 0), s(n + 1, 0);
        f[1] = s[1] = 1;
        for (int i = 2; i <= n; i ++ ) {
            if (str[i - 1] == '0') {
                if (s[max(0, i - Mn)] - s[max(0, i - Mx - 1)])
                    f[i] = 1;
            }
            s[i] = s[i - 1] + f[i];
        }
        return f[n];
    }
};
```
----
### 复杂度分析
- 时间复杂度$O(N)$
- 空间复杂度$O(N)$