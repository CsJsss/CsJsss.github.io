---
title: '[LeetCode-周赛]279'
toc: true
tags:
  - 模拟
  - 贪心
  - 动态规划
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2022-02-06 11:50:30
updated:
---

**Rank** : `226/4132`
**Solved** : `4/4`

![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2022/1/LeetCode第279场周赛.png)

[竞赛链接](https://leetcode-cn.com/contest/weekly-contest-279/)

<!--more-->

## [对奇偶下标分别排序](https://leetcode-cn.com/contest/weekly-contest-279/problems/sort-even-and-odd-indices-independently/)

### 思路

使用两个数组实现分别排序, 然后奇偶拼接即可.

### Code

```cpp
class Solution {
public:
    vector<int> sortEvenOdd(vector<int>& nums) {
        int n = nums.size();
        vector<int> a, b;
        for (int i = 0; i < n; i ++ ) {
            if (i % 2)
                b.push_back(nums[i]);
            else
                a.push_back(nums[i]);
        }
        sort(begin(a), end(a));
        sort(begin(b), end(b), greater<int>());
        vector<int> ret;
        
        for (int i = 0, j = 0; i < a.size(); i ++, j ++ ) {
            ret.push_back(a[i]);
            if (j < b.size())
                ret.push_back(b[j]);
        }
        
        return ret;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N * logN)$
- 空间复杂度$O(N)$
----

## [重排数字的最小值](https://leetcode-cn.com/contest/weekly-contest-279/problems/smallest-value-of-the-rearranged-number/)

### 思路

**贪心**. 如果是负数, 则数字从大到小排序. 如果是正数, 从从小到大排序(注意前导零), 如果存在前导零, 则从小到大遍历, 将第一个非0数组与开头的0交换.

### Code

```cpp
class Solution {
public:
    long long smallestNumber(long long num) {
        string s = to_string(num);
        if (num < 0) {
            sort(begin(s), end(s), greater<char>());
            return -stoll(s);
        }
        sort(begin(s), end(s));
        for (int i = 0; i < s.size(); i ++ ) {
            if (s[i] != '0') {
                if (i == 0)
                    break;
                swap(s[i], s[0]);
                break;
            }
        }
        
        return stoll(s);
    }
};
```

### 复杂度分析

- 时间复杂度$O(N * logN)$, 其中$N = log_{10}{num}$
- 空间复杂度$O(N)$
----

## [设计位集](https://leetcode-cn.com/contest/weekly-contest-279/problems/design-bitset/)

### 思路

**模拟**. 可以通过数组`vector`以及`1`和`0`的计数器共同模拟除了`翻转`以外的所有操作.

麻烦的是翻转, 其无法暴力模拟. 因此可以设置一个`flag`, 表示是否翻转了. **某一位的值通过该位的值和`flag`共同决定**.

### Code

```cpp
class Bitset {
public:
    vector<int> s;
    int o, zero;
    int f;
    Bitset(int size) {
        f = 0;
        zero = size;
        o = 0;
        s.resize(size);
    }
    
    void fix(int idx) {
        int val = (s[idx] + f) % 2;
        if (val == 0)            
            s[idx] = 1 - s[idx], o ++ , zero -- ;
    }
    
    void unfix(int idx) {
        int val = (s[idx] + f) % 2;
        if (val)
            s[idx] = 1 - s[idx], o -- , zero ++ ;
    }
    
    void flip() {
        swap(o, zero);
        f = (f + 1) % 2;
    }
    
    bool all() {
        return o == s.size();
    }
    
    bool one() {
        return o;
    }
    
    int count() {
        return o;
    }
    
    string toString() {
        string ans;
        for (auto& c : s) {
            int cur = (c + f) % 2;
            ans.push_back(cur + '0');            
        }
        return ans;
    }
};

/**
 * Your Bitset object will be instantiated and called as such:
 * Bitset* obj = new Bitset(size);
 * obj->fix(idx);
 * obj->unfix(idx);
 * obj->flip();
 * bool param_4 = obj->all();
 * bool param_5 = obj->one();
 * int param_6 = obj->count();
 * string param_7 = obj->toString();
 */
```

### 复杂度分析
- 时间复杂度$O(M * N + P)$, 其中`M`是`toString`的调用次数, `P`是其他操作的调用次数之和. 
- 空间复杂度$O(N)$
----

## [移除所有载有违禁货物车厢所需的最少时间](https://leetcode-cn.com/contest/weekly-contest-279/problems/minimum-time-to-remove-all-cars-containing-illegal-goods/)

### 思路

首先**枚举**. 枚举`1`操作的结束位置, 对于某个`1`操作, 其对应了很多很多`2`和`3`操作的组合(`2`操作的边界以及`1`和`2`操作边界内的`3`操作), 但我们只关心其中的最少值对应的`2`和`3`操作的组合.

首先如果枚举到了`i`, 设`2`操作的边界为`j`(j > i), 则有$Cost[i, j] = (i) + (n - j + 1) + (2 * (sum[j - 1] - sum[i]))$.其中`sum`是字符串的前缀和数组.

整理可得$Cost[i, j] = i + n - 2 * sum[i] + 2 * sum[j - 1] - (j - 1), j > i$. 因此我们关心的是`2 * sum[j - 1] - (j - 1)`, 只要让其取最小值即可. 这可以通过预处理的方式轻松实现.

记`f[i] = 2 * sum[i] - i`, 计算出`f`数组后处理其后缀最小值即可.

### Code

```cpp
class Solution {
public:
    int minimumTime(string s) {
        int n = s.size();
        vector<int> sum(n + 1);
        
        for (int i = 1; i <= n; i ++ ) {
            int cur = s[i - 1] - '0';
            sum[i] = sum[i - 1] + cur;
        }
        
        // Mn: f数组的后缀最小值
        vector<int> f(n + 2), Mn(n + 2);
        for (int i = 1; i <= n; i ++ )
            f[i] = 2 * sum[i] - i;
        
        // for (int i = 1; i <= n; i ++ )
        //     cout << "f " << i << ' ' << f[i] << endl;
        
        f[n + 1]  = Mn[n + 1] = INT_MAX;
        for (int i = n; i >= 0; i -- )
            Mn[i] = min(f[i], Mn[i + 1]);
        
        // for (int i = 1; i <= n; i ++ )
        //     cout << "min " << i << ' ' << Mn[i] << endl;
        
        int ans = INT_MAX;
        for (int i = 0; i <= n; i ++ ) {
            int cur = i + n - 2 * sum[i];
            // cout << i << ' ' << cur << ' ' << Mn[i] << endl;
            cur += Mn[i];
            ans = min(ans, cur);
        }
            
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(N)$
- 空间复杂度$O(N)$

----
**欢迎讨论指正**