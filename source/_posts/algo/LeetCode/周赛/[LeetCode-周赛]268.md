---
title: '[LeetCode-周赛]268'
toc: true
tags:
  - 周赛
  - 模拟
  - 二分搜索
  - 枚举
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2021-11-23 12:11:03
updated:
---

**Rank** : `228/4397`
**Solved** : `4/4`

![](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/hexo-theme-icarus/source/img/2021/11/23/LeetCode周赛268.png)

[竞赛链接](https://leetcode-cn.com/contest/weekly-contest-268/)

<!--more-->

## [两栋颜色不同且距离最远的房子](https://leetcode-cn.com/problems/two-furthest-houses-with-different-colors/) 

### 思路
注意到数据范围很小, 两重循环枚举即可.

### Code
```cpp
class Solution {
public:
    int maxDistance(vector<int>& c) {
        unordered_map<int, int> mp;
        int n = c.size();
        int ans = 0;
        for (int i = 0; i < n; i ++ ) {
            int col = c[i];
            for (auto& [cc, idx] : mp) {
                if (cc != col)
                    ans = max(ans, i - idx);
            }
            if (mp.count(col) == 0)
                mp[col] = i;
        }
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N^2)$
- 空间复杂度$O(N)$
----

## [给植物浇水](https://leetcode-cn.com/problems/watering-plants/)

### 思路
按照题意模拟即可.

### Code
```cpp
class Solution {
public:
    int wateringPlants(vector<int>& nums, int cap) {
        int n = nums.size();
        // all : 当前剩余
        int ret = 0, all = cap;
        for (int i = 0; i < n; i ++ ) {
            int cur = nums[i];
            if (all >= cur) {
                all -= cur;
                ret += 1;
            } else {
                all = cap;
                ret += i + i + 1;
                all -= cur;
            }
        }
        return ret;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(1)$
----

## [区间内查询数字的频率](https://leetcode-cn.com/problems/range-frequency-queries/)

### 思路
以**值**作为`key`, 以下标作为`val`, 构建哈希表.
每次查询在递增的下标上**二分搜索**即可

### Code
```cpp
class RangeFreqQuery {
public:
    unordered_map<int, vector<int>> mp;
    RangeFreqQuery(vector<int>& arr) {
        int n = arr.size();
        for (int i = 0; i < n; i ++ )
            mp[arr[i]].push_back(i);
    }
    
    int query(int l, int r, int val) {
        auto L = lower_bound(mp[val].begin(), mp[val].end(), l) - mp[val].begin();
        auto R = upper_bound(mp[val].begin(), mp[val].end(), r) - mp[val].begin();
        return R - L;
    }
};

/**
 * Your RangeFreqQuery object will be instantiated and called as such:
 * RangeFreqQuery* obj = new RangeFreqQuery(arr);
 * int param_1 = obj->query(left,right,value);
 */
```

### 复杂度分析
- 时间复杂度$O(N)$
- 空间复杂度$O(Q * logN)$
----

## [k 镜像数字的和](https://leetcode-cn.com/problems/sum-of-k-mirror-numbers/)

### 思路
**打表**. 由于数据范围很小, 考虑枚举长度不超过`12`的十进制回文数(复杂度为`1e6`), 然后暴力判断每个10进制下的回文数是否在`2-9`进制下也回文.

### Code
```cpp
const int M = 30;
using LL = long long;
vector<vector<LL>> nums;

class Solution {
public: 
    void dfs(int len, int cur, string& num) {
        int R = (len + 1) / 2;
        if (cur == R + 1) {
            string ss = num;
            if (len & 1) {
                for (int idx = R - 1; idx >= 1; idx -- )
                    ss.push_back(num[idx - 1]);
            } else {
                for (int idx = R; idx >= 1; idx -- )
                    ss.push_back(num[idx - 1]);
            }
            LL val = stoll(ss);
            for (int k = 2; k <= 9; k ++ ) {
                if (nums[k].size() == M)
                    continue;
                LL cv = val;
                string s;
                while (cv) {
                    s.push_back(char(cv % k + '0'));
                    cv /= k;
                }
                string rs = s;
                reverse(rs.begin(), rs.end());
                if (s == rs and rs[0] != '0')
                    nums[k].push_back(val);
            }
            return ;
        }
        for (int i = 0; i <= 9; i ++ ) {
            num.push_back(char(i + '0'));
            dfs(len, cur + 1, num);
            num.pop_back();
        }
    }
    void init() {
        if (nums.size())
            return ;
        nums.resize(10);
        for (int len = 1; len <= 12; len ++ ) { 
            for (int i = 1; i <= 9; i ++ ) {
                string s = to_string(i);
                dfs(len, 2, s);                
            }
        }
            
    }
    
    long long kMirror(int k, int n) {
        init();
        LL ret = 0ll;
        for (int i = 0; i < n; i ++ )
            ret += nums[k][i];
        
        return ret;
    }
};
```

### 复杂度分析
- 时间复杂度$O(1e6)$
- 空间复杂度$O(N * K)$

----
**欢迎讨论指正**