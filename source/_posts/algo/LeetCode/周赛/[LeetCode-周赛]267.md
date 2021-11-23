---
title: '[LeetCode-周赛]267'
toc: true
tags:
  - 周赛
  - 模拟
  - 并查集
categories:
  - - algo
    - LeetCode
    - 周赛
date: 2021-11-14 11:25:52
updated:
---

**Rank** : `131/4360`
**Solved** : `4/4`

![Rank](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2021/11/14/LeetCode周赛267.png)

[竞赛链接](https://leetcode-cn.com/contest/weekly-contest-267)

<!--more-->

## [买票需要的时间](https://leetcode-cn.com/problems/time-needed-to-buy-tickets/)

### 思路
注意到数据范围均很小, 因此直接使用双端队列(`deque`)模拟题意即可.

### Code
```cpp
using PII = pair<int, int>;
class Solution {
public:
    int timeRequiredToBuy(vector<int>& nums, int k) {
        
        deque<PII> dq;
        int n = nums.size(), ans = 0;
        for (int i = 0; i < n; i ++ )
            dq.emplace_back(nums[i], i);
        
        int cnt = 0;
        while (true) {
            auto [t, idx] = dq.front();
            dq.pop_front();
            cnt ++ ;
            if (t == 1 and idx == k)
                return cnt;
            if (t > 1)
                dq.emplace_back(t - 1, idx);
        }
        return -1;
    }
};
```

### 复杂度分析

- 时间复杂度$O(N * Max(nums))$
- 空间复杂度$O(N)$
----

## [反转偶数长度组的节点](https://leetcode-cn.com/problems/reverse-nodes-in-even-length-groups/)

### 思路
使用`vector`模拟题意, 注意反转的是偶数长度的组(错看成偶数编号的组, 白WA了两次)

### Code
```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* reverseEvenLengthGroups(ListNode* head) {
        ListNode* p = head;
        vector<int> nums;
        while (p) {
            nums.push_back(p -> val);
            p = p -> next;
        }
        int n = nums.size();
        vector<int> ans;
        // cnt是index, id是组的编号(1, 2, 3...)
        int cnt = 0, id = 1;
        
        while (cnt < n) {
            if (id & 1) {
                int len = min(n - 1, cnt + id - 1) - cnt + 1;
                if (len & 1) {
                    for (int k = cnt; k <= min(n - 1, cnt + id - 1); k ++ )
                        ans.push_back(nums[k]);
                } else {
                    for (int k = min(n - 1, cnt + id - 1); k >= cnt; k --)
                        ans.push_back(nums[k]);
                }
                cnt = min(n, cnt + id);   
            } else {
                int len = min(n - 1, cnt + id - 1) - cnt + 1;
                if (len & 1) {
                    for (int k = cnt; k <= min(n - 1, cnt + id - 1); k ++ )
                        ans.push_back(nums[k]);
                } else 
                    for (int k = min(n - 1, cnt + id - 1); k >= cnt; k --)
                        ans.push_back(nums[k]);
                cnt = min(n, cnt + id);
            }
            id += 1;
        }
        
        ListNode* ret = new ListNode();
        p = nullptr;
        for (auto& c : ans) {
            if (p == nullptr) {
                ret -> val = c;
                p = ret;
            } else {
                ListNode* nxt = new ListNode(c);
                p -> next = nxt;
                p = p -> next;
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

## [解码斜向换位密码](https://leetcode-cn.com/problems/decode-the-slanted-ciphertext/)

### 思路
模拟题意, 按照矩阵的方式填充好字符后. 遍历每条主对角线, 依次添加字符, 最后把末尾的空格去掉.

### Code
```cpp
class Solution {
public:
    string decodeCiphertext(string str, int row) {
        int len = str.size();
        int col = len / row;
        vector<vector<char>> mat(row, vector<char>(col, ' '));
        
        int x = 0, y = 0;
        for (auto& c : str) {
            mat[x][y] = c;
            y ++ ;
            if (y == col)
                y = 0, x ++ ;
        }
        string ans;
        for (int i = 0; i < col; i ++ ) {
            int x = 0, y = i;
            while (x < row and y < col) {
                ans.push_back(mat[x][y]);
                x ++, y ++;
            }
        }
        while (ans.size() and ans.back() == ' ')
            ans.pop_back();
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(N)$, N为`str`的长度
- 空间复杂度$O(N)$
----

## [处理含限制条件的好友请求](https://leetcode-cn.com/problems/process-restricted-friend-requests/)

### 思路
使用**并查集**维护连通性. 每次处理请求时, 若已经在一个联通块中则结果为`True`; 否则**暴力**判断是否有一条限制边连接了这两个连通块中的两个点.

### Code
```cpp
const int N = 1010;
int p[N];
class Solution {
public:
    int find(int x) {
        return x == p[x] ? x : p[x] = find(p[x]);
    }
    vector<bool> friendRequests(int n, vector<vector<int>>& edge, vector<vector<int>>& qu) {
        int m = edge.size();
        
        for (int i = 0; i < n; i ++ )
            p[i] = i;
        
        vector<bool> ans;
        for (auto& q : qu) {
            int x = q[0], y = q[1];
            x = find(x), y = find(y);
            if (x == y) {
                ans.push_back(true);
                continue;
            }
            // x != y
            unordered_set<int> sx, sy;
            for (int i = 0; i < n; i ++ ) {
                if (find(i) == x)
                    sx.insert(i);
                if (find(i) == y)
                    sy.insert(i);
            }
            bool flag = true;
            for (auto& e : edge) {
                int u = e[0], v = e[1];
                if ((sx.count(u) and sy.count(v)) or (sx.count(v) and sy.count(u)))
                    flag = false;
            }
            
            ans.push_back(flag);
            if (flag)
                p[y] = x;
        }
        
        return ans;
    }
};
```

### 复杂度分析
- 时间复杂度$O(N * M)$, N为点数, M为请求数.
- 空间复杂度$O(N)$


----
**欢迎讨论指正**