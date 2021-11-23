---
title: '[LeetCode-237]删除链表中的节点'
toc: true
tags:
  - LeetCode
  - 链表
categories:
  - - algo
    - LeetCode
    - 每日一题
date: 2021-11-02 09:10:25
updated:
---

[原题链接](https://leetcode-cn.com/problems/delete-node-in-a-linked-list/)

## 题目描述

给出单链表的某个非尾节点, 删除该节点
<!--more-->

## 思路
- 由于给出的是单链表, 所以我们无法得知**被删除节点的前驱节点**信息, 只能"曲线救国"

- 可以将值向前平移一个单位, 删除末尾节点即可

## Code

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    void deleteNode(ListNode* node) {
        // 当前节点不为尾节点, 所以一定有后继节点
        ListNode* Nxt = node -> next;
        ListNode* cur = node;
        ListNode* prev = nullptr;
        // 还有后继节点的时候, 进行值前移
        while (Nxt) {
            cur -> val = Nxt -> val;
            prev = cur;
            cur = Nxt;
            Nxt = Nxt -> next;
        }
        // 最后删除尾节点即可（退出循环的时候, cur指向尾节点, Nxt为nullptr, 而prev指向尾节点之前的节点）
        prev -> next = nullptr;
    }
};
```
----
## 复杂度分析
1. 时间复杂度$O(N)$, 遍历一遍链表即可完成删除操作
2. 空间复杂度$O(1)$, 只使用常数空间存储指针变量`Nxt`、`cur`、`prev`即可
