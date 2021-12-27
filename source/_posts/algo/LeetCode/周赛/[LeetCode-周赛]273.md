---
title: '[LeetCode-周赛]273'
toc: true
tags:
  - 模拟
  - 前缀和
  - 哈希表
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2021-12-27 18:25:18
updated:
---

**Rank** :  `301/4367`
**Solved** :  `4/4`
![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2021/12/LeetCode第273场周赛.png)

[竞赛链接](https://leetcode-cn.com/contest/weekly-contest-273/)

<!--more-->

## [反转两次的数字](https://leetcode-cn.com/problems/a-number-after-a-double-reversal/) 

### 思路

模拟题意. cpp可以使用`to_string`和`stoi`函数方便的进行`字符串`和`int`之间的转换.

### Code

```cpp
class Solution {
public:
    bool isSameAfterReversals(int num) {
        string nums = to_string(num);
        reverse(nums.begin(), nums.end());
        int r1 = stoi(nums);
        string r2 = to_string(r1);
        reverse(r2.begin(), r2.end());
        if (num == stoi(r2))
            return true;
        return false;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [执行所有后缀指令](https://leetcode-cn.com/problems/execution-of-all-suffix-instructions-staying-in-a-grid/)

### 思路

由于数据范围很小, 因此直接按照题意模拟.

### Code

```cpp
class Solution {
public:
    vector<int> executeInstructions(int n, vector<int>& st, string s) {
        int sx = st[0], sy = st[1];
        int m = s.size();
        vector<int> ans;
        
        for (int i = 0; i < m; i ++ ) {
            int x = sx, y = sy, cur = 0;
            for (int j = i; j < m; j ++ ) {
                if (s[j] == 'L')
                    y -= 1;
                if (s[j] == 'R')
                    y += 1;
                if (s[j] == 'U')
                    x -= 1;
                if (s[j] == 'D')
                    x += 1;
                if (x >= 0 and x < n and y >= 0 and y < n)
                    cur ++ ;
                else
                    break;
            }
            ans.push_back(cur);
        }
        
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [相同元素的间隔之和](https://leetcode-cn.com/problems/intervals-between-identical-elements/)

### 思路

首先可以将问题一分为二: **分别统计**左边和右边, 最后两者相加即可.
以左边为例. 我们可以使用**前缀和**的思想完成统计. 具体思路为:
  - 记`left[i]`为`nums[i]`左边与其的间隔之和. `cnt[nums[i]]`为`i`极其左边与`nums[i]`值相等的个数.
  - 若当前枚举到下标`i`, 其值为`nums[i]`, 若其左边最后一个与其值相同的下标为`j`, 则有:
  $$sum[i] = sum[j] + cnt[nums[i]] * (i - j) $$
  - 上式表示所有所有与`nums[i]`相同的下标, 先考虑其到`j`处的距离距离之和(由`sum`的定义可知为`sum[j]`); 然后再统计`j`到`i`处的距离之和, 其为`(i - j) * cnt[nums[i]]`. 主要思想是利用历史信息, 分两步部分统计(先到`j`, 再到`i`), 其中使用**前缀和**进行优化.

最后将`left`和`right`相加即可.

### Code

```cpp
using LL = long long;
class Solution {
public:
    vector<long long> getDistances(vector<int>& arr) {
        int n = arr.size();
        vector<LL> sum(n + 1, 0L);
        unordered_map<int, int> mp;  // 记录每个数最后一次出现的位置
        unordered_map<int, int> cnt;
        // Left
        for (int i = 1; i <= n; i ++ ) {
            int cur = arr[i - 1];
            if (mp.count(cur) == 0) {
                mp[cur] = i;
                cnt[cur] ++ ;
                continue;                
            }
            int idx = mp[cur], num = cnt[cur];
            sum[i] = sum[idx] + 1ll * num * (i - idx);
            mp[cur] = i;
            cnt[cur] ++ ;
        }
        // Right
        mp.clear();
        cnt.clear();
        vector<LL> ans(n, 0L);
        // 先把左边的加到答案里, 然后算右边的
        for (int i = 0; i < n; i ++ )
            ans[i] += sum[i + 1];
        sum = vector<LL>(n + 1, 0L);
        for (int i = n; i >= 1; i -- ) {
            int cur = arr[i - 1];
            if (mp.count(cur) == 0) {
                mp[cur] = i;
                cnt[cur] ++ ;
                continue;                
            }
            int idx = mp[cur], num = cnt[cur];
            sum[i] = sum[idx] + 1ll * num * (idx - i);
            mp[cur] = i;
            cnt[cur] ++ ;
        }
        for (int i = 0; i < n; i ++ )
            ans[i] += sum[i + 1];
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [还原原数组](https://leetcode-cn.com/problems/recover-the-original-array/)

### 思路

首先观察数据范围可知, 可以使用$O(N^2)$的算法解决.
由于将原数组左右`k`和右移`k`后, 对应位置的数差值固定为`2k`.
因此如果我们知道`k`的具体值的话, 问题就转化成: 给定`k`值的情况下, 判断数组能否还原出原数组. 
- 判断可以从贪心的小到大考虑: 若考虑到`x`了, 则将`x`放入`lower`数组, 将`x + 2k`放入`higher`数组, 若无`x + 2k`则失败。使用`map`或者`multiset`判断的时间复杂度为$O(NlogN)$
- 对于`k`值, 可以考虑枚举所有可能的`k`值. 由于数组的最大值必定为`higher`的最大值, 最小值必定为`lower`的最小值. 因此可以枚举`higher`的最小值或者`lower`的最大值, 从而计算出`k`. 时间复杂度$O(N)$.

最后算法整体时间复杂度为$O(N^2logN)$.

### Code

```cpp
class Solution {
public:
    vector<int> recoverArray(vector<int>& nums) {
        int n = nums.size();
        n /= 2;
        // Max -> higher, Min -> lower
        int HMx = *max_element(nums.begin(), nums.end());
        int LMn = *min_element(nums.begin(), nums.end());
        
        if (n == 1)
            return {LMn + (HMx - LMn) / 2};
        
        set<int> st(nums.begin(), nums.end());
        
        map<int, int> cnt;
        for (auto& num : nums)
            cnt[num] ++ ;

        // 从大到小枚举LMx, 计算k
        for (auto it = st.rbegin(); it != st.rend(); it ++ ) {
            int LMx = *it;
            if (LMx == HMx)
                continue;
            int d = HMx - LMx;
            if (d % 2 or cnt[HMx] > cnt[LMx])
                continue;
            int k = d / 2;
            bool flag = true;
            // lower
            map<int, int> exist;
            // map<int, int> cur = cnt;
            for (auto& [_k, _v] : cnt) {
                if (_v == 0)
                    continue;
                if (cnt.count(_k + 2 * k) == 0 or cnt[_k + 2 * k] < _v) {
                    flag = false;
                    break;  
                } else {
                    cnt[_k + 2 * k] -= _v;
                    exist[_k] = _v;                     
                }
            }
            // 复原全局的cnt
            for (auto& [_k, _v] : exist)
                cnt[_k + 2 * k] += _v;
            
            if (flag) {
                // cout << "find " << k << ' ' <<  HMx << ' ' << LMx << endl;
                vector<int> ans;
                // lower
                exist[LMn] = cnt[LMn];
                for (auto& [l, time] : exist)
                    ans.insert(ans.end(), time, l + k);
                return ans;
            }
        }
        return {};
    }
};
```

- 实现的过程中使用`exist`来存储`lower`数组, 如果没有找到答案, 则将`exist`的内容复原到原来的map`cnt`中, 这样可以减少`cnt`的重复拷贝, 将运行时间从超时边缘(1972ms)优化成28ms.

### 复杂度分析

- 时间复杂度$O(N^2logN)$
- 空间复杂度$O(N^2)$

----
**欢迎讨论指正**