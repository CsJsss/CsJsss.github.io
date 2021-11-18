title: '[LeetCode-周赛]第65场双周赛'
toc: true
tags:
  - LeetCode
  - 周赛
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2021-11-14 17:31:56
updated:
---
**Rank** : `235/2676`
**Solved** : `3/4`
![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2021/11/14/LeetCode双周赛65.png)

[竞赛链接](https://leetcode-cn.com/contest/biweekly-contest-65/)

<!--more-->

## T1: 检查两个字符串是否几乎相等

### 思路
**模拟题意**. 使用哈希表或数组统计词频, 然后比较词频之差的绝对值是否超过3.

### Code
```cpp
class Solution {
public:
    bool checkAlmostEquivalent(string w1, string w2) {
        unordered_map<char, int> m1, m2;
        for (auto& c : w1)
            m1[c] ++ ;
        for (auto& c : w2)
            m2[c] ++ ;
        for (char c = 'a'; c <= 'z'; c ++ ) {
            int d = abs(m1[c] - m2[c]);
            if (d > 3)
                return false;
        }
        return true;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(\vert S\vert)$, $\vert S\vert$为字符集大小
----

## T2: 模拟行走机器人 II

### 思路
**模拟**. 一开始眼瞎没注意到数据范围, 每一步都按照题目要求模拟, 然后TLE了. 接着优化, 优化的方式写了两点。
- 一种是步长对周长取余, 因为每次都是绕外圈走, 因此可以认为余数是真正移动了的步数, 这种优化要注意移动方向的改变, 在四个角上移动了`k`圈后, 可能会发生移动方向的改变. 比如在左下角(0, 0), 只有初始朝北的时候, 绕`k`圈后会朝西; 其他朝向绕`k`圈后都会朝南. 
- 还有一种是一次走好几步, 比如当前向北, 算一下向北最多能走几步. 若可以走完, 就一次走完. 若向北走不完, 则走到上界后修改方向, 递归走剩下的步数。

### Code
```cpp
const int dx[4] = {0, 1, 0, -1}, dy[4] = {1, 0, -1, 0};
class Robot {
public:
    map<int, string> mp;
    int idx;
    int x, y;
    int W, H;
    // 周长
    int all;
    
    Robot(int width, int height) {
        W = width, H = height;
        x = 0, y = 0;
        idx = 1;
        mp[0] = "North";
        mp[1] = "East";
        mp[2] = "South";
        mp[3] = "West";
        all = 2 * (W + H) - 4;
    }
    
    bool check(int x, int y) {
        return x >= 0 and x < W and y >= 0 and y < H;
    }
    
    void move(int num) {
        num %= all;
        
        if (num == 0) {
            if (x == 0 and y == 0) {
                if (getDir() == "North") 
                    idx = 3;
                else
                    idx = 2;
            }
            if (x == 0 and y == H - 1) {
                if (getDir() == "East") 
                    idx = 0;
                else
                    idx = 3;
            }
            if (x == W - 1 and y == 0) {
                if (getDir() == "West")
                    idx = 2;
                else
                    idx = 1;
            }
            if (x == W - 1 and y == H - 1) {
                if (getDir() == "South")
                    idx = 1;
                else 
                    idx = 0;
            }
        }
        
        string c = getDir();
        if (c == "North") {
            int Mx = H - 1 - y;
            if (Mx >= num) {
                y += num;                
                return ;                
            }
            else {
                y = H - 1;
                idx = 3;
                return move(num - Mx);            
            }
        }
        if (c == "South") {
            int Mx = y;
            if (Mx >= num) {
                y -= num;
                return ;                
            }
            else {
                y = 0;
                idx = 1;
                return move(num - Mx);
            }
        }
        if (c == "West") {
            int Mx = x;
            if (Mx >= num) {
                x -= num;
                return ;                
            }
            else {
                x = 0;
                idx = 2;
                return move(num - Mx);
            }
        }
        if (c == "East") {
            int Mx = W - x - 1;
            if (Mx >= num) {
                x += num;
                return ;                
            }
            else {
                x = W - 1;
                idx = 0;
                return move(num - Mx);
            }
        }
        
        
        for (int i = 1; i <= num; ) {
            int nx = x + dx[idx], ny = y + dy[idx];
            if (check(nx, ny)) {
                i += 1;
                x = nx, y = ny;
                continue;
            }
            idx -= 1;
            if (idx == -1)
                idx = 3;
        }
    }
    
    vector<int> getPos() {
        return {x, y};
    }
    
    string getDir() {
        return mp[idx];
    }
};

/**
 * Your Robot object will be instantiated and called as such:
 * Robot* obj = new Robot(width, height);
 * obj->move(num);
 * vector<int> param_2 = obj->getPos();
 * string param_3 = obj->getDir();
 */
 ```

### 复杂度分析

- 时间复杂度$O(N)$, N次调用`move`, 每次最多走三个阶段(自身递归的次数不超过3)
- 空间复杂度$O(1)$
----

## T3: 每一个查询的最大美丽值

### 思路

经典题. 可以使用树状数组在线算法做, 也可以使用递推等离线算法做.
- 在线算法(树状数组): **离散化**查询点和价格点后, 需要查询每一个查询点之前的`前缀最大值`, 可以使用树状数组维护前缀最大值.
- 离散算法(递推):
将查询点和价格点放在一起排序, **相同价格的话查询点放在后面**. 这样每个查询点之前的价格点是确定的, 使用一个变量遍历递推一下即可.


### Code
```cpp
// 离线算法: 排序 + 递推
using TII = tuple<int, int, int>;
class Solution {
public:
    vector<int> maximumBeauty(vector<vector<int>>& nums, vector<int>& qu) {
        vector<TII> all;
        for (auto& c : nums)
            all.emplace_back(c[0], c[1], 0);
        int m = qu.size();
        for (int i = 0; i < m; i ++ )
            all.emplace_back(qu[i], INT_MAX, i);
        
        sort(all.begin(), all.end());
        int Mx = 0;
        
        vector<int> ans(m);
        
        for (auto& [c, t, idx] : all) {
            // t 指示类型
            if (t == INT_MAX) {
                ans[idx] = Mx;
            } else {
                Mx = max(Mx, t);
            }
        }
        
        return ans;
    }
};
```
```cpp
// 在线算法. 注意树状数组的范围要开到题目范围的两倍(查询点 + 价格点).
const int N = 2e5 + 5;
class Solution {
public:
    int tr[N], M;
    int lowbit(int x) {
        return x & -x;
    }
    void add(int x, int c) {
        for (int i = x; i <= M; i += lowbit(i))
            tr[i] = max(tr[i], c);
    }
    int query(int x) {
        int res = 0;
        for (int i = x; i; i -= lowbit(i))
            res = max(res, tr[i]);
        
        return res;
    }
    vector<int> maximumBeauty(vector<vector<int>>& nums, vector<int>& qu) {
        int n = nums.size();
        
        vector<int> all = qu;
        for (auto& c : nums)
            all.push_back(c[0]);
        
        sort(all.begin(), all.end());
        all.erase(unique(all.begin(), all.end()), all.end());
        M = all.size();
        
        auto get = [&] (int x) {
            return lower_bound(all.begin(), all.end(), x) - all.begin() + 1;
        };
        
        for (auto& c : nums) {
            int idx = get(c[0]), val = c[1];
            add(idx, val);
        }
        
        vector<int> ans;
        for (auto& q : qu) {
            int idx = get(q);
            int cur = query(idx);
            ans.push_back(cur);
        }
        
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(N * logN)$, 树状数组的查询和更新操作均为$logN$, 最多执行$N次$.
- 空间复杂度$O(N)$
----

## T4: 你可以安排的最多任务数目

### 思路
首先可以发现答案具有**二段性**. 若答案为`k`, 则所有小于等于`k`的任务数都能完成, 所有大于`k`的任务数均不能完成. 因此考虑二分答案. 这样问题转化成判断能否完成`mid`个任务.
首先贪心的选择最强的`mid`个工人和最弱的`mid`个任务. 我们需要找到一种方式, 使得工人和任务一一匹配. 这里贪心的**从小到大**考虑每个工人, 若当前工人可以完成当前最弱工作, 则让工人去完成它; 若无法完成, 则这位工人需要吃药, 吃完药后我们二分的找到小于等于他体力值的最大任务, 贪心的选择这个任务给他完成. 最后判断吃药次数`cnt`是否不超过`mid`.


### Code
```cpp
// 上述贪心方式
class Solution {
public:
    int maxTaskAssign(vector<int>& task, vector<int>& work, int cnt, int sth) {
        sort(task.begin(), task.end());
        sort(work.begin(), work.end());
        
        int n = task.size(), m = work.size();
        int l = 0, r = min(n, m);

        auto check = [&] (int x) {
            int need = 0;
            multiset<int> st;
            for (int i = 0; i < x; i ++ )
                st.insert(task[i]);

            for (int i = m - x; i < m; i ++ ) {
                int cur = work[i];
                if (cur >= *st.begin()) {
                    st.erase(st.begin());
                    continue;
                }
                auto idx = st.lower_bound(cur + sth + 1);
                if (idx == st.begin())
                    return false;
                -- idx;
                st.erase(idx);
                need += 1;
            }
            
            return need <= cnt;
        };
        
        while (l < r) {
            int mid = (l + r + 1) >> 1;
            if (check(mid))
                l = mid;
            else
                r = mid - 1;
        }
        
        return r;
    }
};
```
```cpp
// 题解区大佬的解法, 从大到小枚举任务, 贪心的选工人去完成它.
class Solution {
public:
    int maxTaskAssign(vector<int>& task, vector<int>& work, int cnt, int sth) {
        sort(task.begin(), task.end());
        sort(work.begin(), work.end());
        
        int n = task.size(), m = work.size();
        int l = 0, r = min(n, m);

        auto check = [&] (int x) {
            int need = 0;
            multiset<int> st;
            for (int i = m - x; i < m; i ++ )
                st.insert(work[i]);
            
            for (int i = x - 1; i >= 0; i -- ) {
                auto it = st.lower_bound(task[i]);
                if (it != st.end()) {
                    st.erase(it);
                    continue;                    
                }
                need ++ ;
                it = st.lower_bound(task[i] - sth);
                if (it == st.end())
                    return false;
                st.erase(it);
            }
            
            return need <= cnt;
        };
                
        while (l < r) {
            int mid = (l + r + 1) >> 1;
            if (check(mid))
                l = mid;
            else
                r = mid - 1;
        }
        
        return r;
    }
};
```

### 复杂度分析
- 时间复杂度$O(N * log^{2}N)$
- 空间复杂度$O(N)$

----
**欢迎讨论指正**