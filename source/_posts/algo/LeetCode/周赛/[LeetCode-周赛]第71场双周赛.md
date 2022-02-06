---
title: '[LeetCode-周赛]第71场双周赛'
toc: true
tags:
  - 枚举
  - 递推
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2022-02-05 23:51:53
updated:
---

**Rank** : `239/3028`
**Solved** : `4/4`

![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2022/1/LeetCode第71场双周赛.png)

[竞赛链接](https://leetcode-cn.com/contest/biweekly-contest-71/ranking/3/)

<!--more-->

## [拆分数位后四位数字的最小和](https://leetcode-cn.com/contest/biweekly-contest-71/problems/minimum-sum-of-four-digit-number-after-splitting-digits/)

### 思路

使用双重循环枚举`new1`, 然后使用单循环枚举`new2`, 注意此时每个`new1`对应两个`new2`.

### Code

```cpp
class Solution {
public:
    int minimumSum(int num) {
        int ans = INT_MAX;
        string s = to_string(num);
        int n = s.size();
        for (int i = 0; i < n; i ++ )
            for (int j = 0; j < n; j ++ )  {
                if (i == j)
                    continue;
                string s1;
                s1.push_back(s[i]);
                s1.push_back(s[j]);
                string s2;
                for (int k = 0; k < n; k ++ ) {
                    if (k != i and k != j)
                        s2.push_back(s[k]);
                }
                ans = min(ans, stoi(s1) + stoi(s2));
                reverse(begin(s2), end(s2));
                ans = min(ans, stoi(s1) + stoi(s2));
            }
        
        return ans;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N^3)$
- 空间复杂度$O(N)$
----

## [根据给定数字划分数组](https://leetcode-cn.com/contest/biweekly-contest-71/problems/partition-array-according-to-given-pivot/)

### 思路

枚举. 将小于`pivot`、等于`pivot`和大于`pivot`的分别插入`vector`中, 然后合并即可.

### Code

```cpp
class Solution {
public:
    vector<int> pivotArray(vector<int>& nums, int p) {
        vector<int> a, b, c;
        for (auto& num : nums) {
            if (num < p)
                a.push_back(num);
            if (num == p)
                b.push_back(num);
            if (num > p)
                c.push_back(num);            
        }
        for (auto& num : b)
            a.push_back(num);
        for (auto& num : c)
            a.push_back(num);    
        return a;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [设置时间的最少代价](https://leetcode-cn.com/contest/biweekly-contest-71/problems/minimum-cost-to-set-cooking-time/)

### 思路

枚举时间, 首先注意前导0可以不要, 因此长度不足4的时候要注意**分和秒**的计算. 最后注意`push`的顺序(读错题WA了一发).

### Code

```cpp
const int M = 10;
class Solution {
public:
    int minCostSetTime(int start, int moveCost, int pushCost, int tar) {
        int ans = INT_MAX;
        
        for (int i = 1; i < 10000; i ++ ) {
            string s = to_string(i);
            string mill, sec;
            for (int j = s.size() -1; j >= 0; j -- ) {
                if (sec.size() < 2)
                    sec.push_back(s[j]);
                else
                    mill.push_back(s[j]);
            }
            
            reverse(begin(sec), end(sec));
            reverse(begin(mill), end(mill));
            
            int time = stoi(sec);
            if (mill.size())
                time += stoi(mill) * 60;
            
            if (time != tar)
                continue;
            
            vector<int> cnt(M);
            for (auto& c : s)
                cnt[c - '0'] ++ ;
            
            int cur = 0, prev = start + '0';
            
            for (int j = 0; j < s.size(); j ++) {
                cur += pushCost;
                if (s[j] != prev)
                    cur += moveCost;
                prev = s[j];
            }
            ans = min(ans, cur);
            // cout << i << ' ' << cur << endl;                
        }
        
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(M * N)$, M = 10, N = 10000
- 空间复杂度$O(M)$
----

## [删除元素后和的最小差值](https://leetcode-cn.com/contest/biweekly-contest-71/problems/minimum-difference-in-sums-after-removal-of-elements/)

### 思路

首先枚举切割的位置, 右数组的开头可取的范围是从`n + 1`到`2n + 1`. 接着对于某个位置, 其差值的最小值是: **左边取最大的n个数, 而右边取最小的n个数**.
由于需要动态计算, 因此可以使用**递推**(动态规划)的思想提前预处理出来.

### Code

```cpp
using LL = long long;
class Solution {
public:
    long long minimumDifference(vector<int>& nums) {
        multiset<int> left, right;
        int n = nums.size() / 3;
        vector<LL> L(3 * n + 1), R(3 * n + 1);

        LL sl = 0, sr = 0;

        for (int i = 1; i <= n; i ++ )
            left.insert(nums[i - 1]), sl += nums[i - 1], L[i] = sl;
        
        for (int i = 3 * n; i > 2 * n; i -- )
            right.insert(nums[i - 1]), sr += nums[i - 1], R[i] = sr;
        
        for (int i = n + 1; i <= 2 * n; i ++ ) {
            int cur = nums[i - 1], Mx = *left.rbegin();
            if (cur < Mx) {
                sl = sl - Mx + cur;
                left.erase(left.find(Mx));
                left.insert(cur);
            }
            L[i] = min(L[i - 1], sl);
        }
        
        for (int i = 2 * n; i > n; i -- ) {
            int cur = nums[i - 1], Mn = *right.begin();
            if (cur > Mn) {
                sr = sr - Mn + cur;
                right.erase(right.find(Mn));
                right.insert(cur);                
            }
            R[i] = max(R[i + 1], sr);
        }
        
        LL ans = LLONG_MAX;
        
        for (int i = n + 1; i <= 2 * n + 1; i ++ ) 
            ans = min(ans, L[i - 1] - R[i]);            
        
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(N * logN)$
- 空间复杂度$O(N)$
----
**欢迎讨论指正**