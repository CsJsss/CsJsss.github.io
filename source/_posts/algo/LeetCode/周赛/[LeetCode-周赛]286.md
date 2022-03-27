---
title: '[LeetCode-周赛]286'
toc: true
tags:
  - 模拟
  - 贪心
  - 动态规划
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2022-03-27 11:02:24
updated:
---

**Rank** : `111/21134`
**Solved** : `4/4`

![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2022/3/LeetCode第286场周赛.png)

[竞赛链接](https://leetcode.com/contest/weekly-contest-286/)

<!--more-->

## [Find the Difference of Two Arrays](https://leetcode.com/contest/weekly-contest-286/problems/find-the-difference-of-two-arrays/)

### 思路

**模拟**题意即可. 使用哈希表`unordered_set`可以快速判断某个数是否存在.

### Code

```cpp
class Solution {
public:
    vector<vector<int>> findDifference(vector<int>& nums1, vector<int>& nums2) {
        vector<vector<int>> ret;
        // 存储nums1 和 nums2
        unordered_set<int> st1, st2;
        
        for (auto& num : nums1)
            st1.insert(num);
        for (auto& num : nums2)
            st2.insert(num); 
        
        // 存储答案
        unordered_set<int> ans1, ans2;
        for (auto& num : nums1)
            if (st2.count(num) == 0)
                ans1.insert(num);
        
        for (auto& num : nums2)
            if (st1.count(num) == 0)
                ans2.insert(num);     
        vector<int> ret1, ret2;
        for (auto& w : ans1)
            ret1.push_back(w);
        for (auto& w : ans2)
            ret2.push_back(w);        
        ret.push_back(ret1);
        ret.push_back(ret2);
        return ret;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(N)$
----

## [Minimum Deletions to Make Array Beautiful](https://leetcode.com/contest/weekly-contest-286/problems/minimum-deletions-to-make-array-beautiful/)

### 思路

**贪心**. 假设左边已经保留了`left`个数字, 当前枚举到`i`位置. 我们从`i`位置开始往右找`j`, 直到`nums[j] == nums[i]`不满足为止(*双指针算法*). 这样我们找到了一段与`nums[i]`相等的子数组. 现在我们判断:
- 如果`left`为奇数: 说明`i`是答案中的**奇数下标**, 因此我们可以**最多保留2个**nums[i]. 它两的位置是先奇数再偶数, 这样满足题意.
- 如果`left`为偶数: 说明`i`是答案中的**偶数下标**, 因此我们**只能保留1个**nums[i].

贪心选择完成后, 我们最后检查保留数组的长度是否为奇数, 如果为奇数, 去掉最后一个即可.

### Code

```cpp
class Solution {
public:
    int minDeletion(vector<int>& nums) {
        int left = 0, n = nums.size();
        
        for (int i = 0; i < n; ) {
            int j = i;
            while (j < n and nums[j] == nums[i])
                j ++ ;
            int len = j - i;
            
            if (left & 1)
                left += min(2, len);
            else
                left += 1;
            i = j;
        }
        if (left & 1)
            left -= 1;
        return n - left;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N)$
- 空间复杂度$O(1)$
----

## [Find Palindrome With Fixed Length](https://leetcode.com/contest/weekly-contest-286/problems/find-palindrome-with-fixed-length/)

### 思路

**模拟**题意. 题目限定了回文数字的长度为`intLength`, 这样我们可以自由指定的长度为 $len = \lceil intLength / 2 \rceil$. 除了首位必须大于0之外, 我们可以任意的指定其他位置数字, 并且由于回文数字的长度相等且比较数字的时候先比较高位, 因此**高位的排序就是最后回文数字的排序**. 

我们记录 $L = pow(10, len - 1), R = pow(10, len) - 1$. 如果我们要求第`k`个回文数字, 那么它的高位一定是`L + k - 1`, 然后我们根据长度是奇数还是偶数将高位和低位拼接在一起即可. 

还需要检查 $L + k - 1 <= R$ 是否满足, 若不满足则不存在这样的第`k`个回文数字, 答案为-1.

### Code

```cpp
using LL = long long;
class Solution {
public:
    vector<long long> kthPalindrome(vector<int>& qu, int alen) {
        int len = (alen + 1) / 2;
        vector<LL> ans;
        for (auto& k : qu) {
            // 计算L, R : 回文数字的下界和上界
            int L = pow(10, len - 1), R = pow(10, len) - 1;
            L += k - 1;
            // 判断是否存在解
            if (L > R) {
                ans.push_back(-1);
                continue;
            }
            // 合并高位和低位构造回文数字
            string s = to_string(L);
            string ns = s;
            reverse(ns.begin(), ns.end());
            LL cur = 0LL;
            if (alen & 1)
                cur = stoll(s + ns.substr(1));
            else
                cur = stoll(s + ns);
            ans.push_back(cur);
        }
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(N)$
- 空间复杂度$O(1)$: 常数空间存储数字, 也可以认为是$log_{10}{max(queries)}$
----

## [Maximum Value of K Coins From Piles](https://leetcode.com/contest/weekly-contest-286/problems/maximum-value-of-k-coins-from-piles/)

### 思路

**经典二维动态规划**. 

- 状态定义: 
  $f[i][j]$表示考虑了前`i`个硬币桌子, 且**总共**拿了`j`个时取得的最大价值

- 状态转移:
  1. $f[i][j] = f[i - 1][j]$: 表示第`i`个桌子一个也不拿.
  2. $f[i][j] = max(f[i][j], f[i - 1][j - u] + sum), u\in{[1, min(j, m)]}$: 表示第`i`个桌子上拿取前`u`个(其价值为`sum`), 且第`i`个桌子最多有`m`个.


### Code

```cpp
const int N = 1010, M = 2010;
int f[N][M];

class Solution {
public:
    int maxValueOfCoins(vector<vector<int>>& nums, int k) {
        memset(f, 0, sizeof(f));
        
        int n = nums.size();
        
        for (int i = 1; i <= n; i ++ )
            for (int j = 1; j <= k; j ++ ) {
                f[i][j] = f[i - 1][j];
                
                int m = nums[i - 1].size();
                for (int u = 1, sum = 0; u <= min(j, m); u ++ ) {
                    sum += nums[i - 1][u - 1];
                    f[i][j] = max(f[i][j], f[i - 1][j - u] + sum);                    
                }
                
            }
        
        return f[n][k];
    }
};
```

### 复杂度分析
- 时间复杂度$O(N * K)$
- 空间复杂度$O(N * K)$
----

**欢迎讨论指正**