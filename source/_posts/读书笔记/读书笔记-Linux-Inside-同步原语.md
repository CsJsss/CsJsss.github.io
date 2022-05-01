---
title: '[读书笔记]Linux Inside: 同步原语01-Spinlocks'
toc: true
date: 2022-04-20 16:21:34
updated:
categories:
    - - 读书笔记
tags:
    - Linux
    - 同步原语
---

本系列博客为[Linux Inside](https://0xax.gitbooks.io/linux-insides/content/SyncPrim/)文章中`Linux同步原语`的阅读笔记. 主要包含了`Spinlocks`、`Semaphores`、`Mutex`、`Reader/Writer semaphores`、`SeqLock`、`RCU`和`Lockdep`.

<!--more-->

Linux内核提供了多种同步原语为防止多进程或多线程情况下的`Race Condition`. 这些同步原语的使用在内核代码中随处可见. 他们主要有:

- spinlocks;
- mutex;
- semaphores;
- seqlocks;
- atomic operations;


## Spinlocks

`Spinlocks`是一种低阶的同步机制, 其用一个变量表示该锁的状态: **acquired**、**released**. 任何一个想要获得该锁的进程都必须向该变量写入值表示该锁被某进程**acquired**, 或想要释放锁的进程都必须向该变量写入值表示该锁被某进程**released**, 即其用变量表示锁的状态. 因此所有相关(写入变量)的操作必须是**atomic**的以防止出现数据竞争问题. 

### 结构体定义

Linux内核中`SpinLocks`由`spinlock_t`结构体来表示. 该结构体的定义为:

```cpp
typedef struct spinlock {
        union {
              struct raw_spinlock rlock;

#ifdef CONFIG_DEBUG_LOCK_ALLOC
# define LOCK_PADSIZE (offsetof(struct raw_spinlock, dep_map))
                struct {
                        u8 __padding[LOCK_PADSIZE];
                        struct lockdep_map dep_map;
                };
#endif
        };
} spinlock_t;
```

该结构体的定义位于 [include/linux/spinlock_types.h](https://github.com/torvalds/linux/blob/master/include/linux/spinlock_types.h) 头文件中. 如果内核中`CONFIG_DEBUG_LOCK_ALLOC`设置被禁用, 那么`spintlock_t`包含一个联合体, 该Union只有一个字段: **raw_spinlock**.

**raw_spinlock**的表示`spinlock`的具体实现结构体. 该结构体的定义如下:

```cpp
typedef struct raw_spinlock {
        arch_spinlock_t raw_lock;
#ifdef CONFIG_DEBUG_SPINLOCK
    unsigned int magic, owner_cpu;
    void *owner;
#endif
#ifdef CONFIG_DEBUG_LOCK_ALLOC
    struct lockdep_map dep_map;
#endif
} raw_spinlock_t;
```

其中`arch_spinlock_t`代表架构相关的`Spinlocks`的具体实现. `x86_64`架构中的具体实现为:

```cpp
typedef struct qspinlock {
        union {
        atomic_t val;
        struct {
            u8    locked;
            u8    pending;
        };
        struct {
            u16    locked_pending;
            u16    tail;
        };
        };
} arch_spinlock_t;
```

### 相关处理函数

内核提供的自旋锁相关的函数有:

- `spin_lock_init`: 对给定的`spinlock`初始化.
- `spin_lock`: 锁定给定的`spinlock`.
- `spin_unlock`: 释放给定的`spinlock`.
- `spin_is_locked`: 检查给定的`spinlock`的状态.
- `spin_lock_bh`: 禁止软件中断并锁定给定的`spinlock`.
- `spin_unlock_bh`: 释放给定的`spinlock`并允许软件中断.

#### 初始化Spinlocks

其中`spin_lock_init`宏在[include/linux/spinlock.h](https://github.com/torvalds/linux/blob/master/include/linux/spinlock.h)头文件中声明, 它的具体实现为:

```cpp
# define spin_lock_init(_lock)			\
do {						\
	spinlock_check(_lock);			\
	*(_lock) = __SPIN_LOCK_UNLOCKED(_lock);	\
} while (0)
```

该宏定义执行了两个操作: 检查给定的`spinlock`并且执行`__SPIN_LOCK_UNLOCKED`. 检查`spinlock`的具体实现很简单, 该函数仅仅返回`raw_spinlock_t`以保证我们得到`normal raw spinlock`.

```cpp
static __always_inline raw_spinlock_t *spinlock_check(spinlock_t *lock)
{
    return &lock->rlock;
}
```

正如`__SPIN_LOCK_UNLOCKED`的名字所示, 该宏初始化给定的`spinlock`并且将其中变量设置为`released`状态. 该宏定义在[include/linux/spinlock_types.h](https://github.com/torvalds/linux/blob/master/include/linux/spinlock_types.h)头文件中, 具体实现为:

```cpp
#define ___SPIN_LOCK_INITIALIZER(lockname)	\
	{					\
	.raw_lock = __ARCH_SPIN_LOCK_UNLOCKED,	\
	SPIN_DEBUG_INIT(lockname)		\
	SPIN_DEP_MAP_INIT(lockname) }

#define __SPIN_LOCK_INITIALIZER(lockname) \
	{ { .rlock = ___SPIN_LOCK_INITIALIZER(lockname) } }

#define __SPIN_LOCK_UNLOCKED(lockname) \
	(spinlock_t) __SPIN_LOCK_INITIALIZER(lockname)
```

我们无需关系`DEBUG`相关的初始化(`SPIN_DEBUG_INIT(lockname)`和`SPIN_DEP_MAP_INIT(lockname)`). 因此`__SPIN_LOCK_UNLOCKED`宏定义将会被展开成:
 
`*(_lock) = (spinlock_t) { .rlock = {.raw_lock = __ARCH_SPIN_LOCK_UNLOCKED} }`.

其中`x86_64`架构的`__ARCH_SPIN_LOCK_UNLOCKED`的宏定义为:

`#define __ARCH_SPIN_LOCK_UNLOCKED       { { .val = ATOMIC_INIT(0) } }`.

因此经过一系列的宏定义展开后, `spin_lock_init`宏将给定的`spin_lock`的`atomic`状态变量设置为0, 表示`unlocked`状态.


#### 对Spinlocks上锁

`spin_lock`函数定义在[include/linux/spinlock.h](https://github.com/torvalds/linux/blob/master/include/linux/spinlock.h)文件中.

```cpp
static __always_inline void spin_lock(spinlock_t *lock)
{
	raw_spin_lock(&lock->rlock);
}
```

其中`raw_spin_lock`的宏定义在相同的文件中. 其宏定义为:

`#define raw_spin_lock(lock)    _raw_spin_lock(lock)`

如果允许[SMP](https://en.wikipedia.org/wiki/Symmetric_multiprocessing)并且设置了`CONFIG_INLINE_SPIN_LOCK`. 那么`_raw_spin_lock`的定义为:

`#define _raw_spin_lock(lock) __raw_spin_lock(lock)`

该宏对应的函数定义为:

```cpp
static inline void __raw_spin_lock(raw_spinlock_t *lock)
{
        preempt_disable();
        spin_acquire(&lock->dep_map, 0, 0, _RET_IP_);
        LOCK_CONTENDED(lock, do_raw_spin_trylock, do_raw_spin_lock);
}
```

该函数首先调用`preempt_disable`宏来禁用抢占. 当释放该自旋锁的时候, 抢占将会被允许:

```cpp
static inline void __raw_spin_unlock(raw_spinlock_t *lock)
{
	spin_release(&lock->dep_map, _RET_IP_);
	do_raw_spin_unlock(lock);
	preempt_enable();
}
```

需要通过禁用抢占来防止其他进程抢占该锁. `spin_acquire`通过一系列的宏展开为:

`#define spin_acquire(l, s, t, i)                lock_acquire_exclusive(l, s, t, NULL, i)`
`#define lock_acquire_exclusive(l, s, t, n, i)           lock_acquire(l, s, t, 0, 1, n, i)`

其中`lock_acquire`函数的实现为:

```cpp
void lock_acquire(struct lockdep_map *lock, unsigned int subclass,
                  int trylock, int read, int check,
                  struct lockdep_map *nest_lock, unsigned long ip)
{
         unsigned long flags;

         if (unlikely(current->lockdep_recursion))
                return;

         raw_local_irq_save(flags);
         check_flags(flags);

         current->lockdep_recursion = 1;
         trace_lock_acquire(lock, subclass, trylock, read, check, nest_lock, ip);
         __lock_acquire(lock, subclass, trylock, read, check,
                        irqs_disabled_flags(flags), nest_lock, ip, 0, 0);
         current->lockdep_recursion = 0;
         raw_local_irq_restore(flags);
}
```

`lock_acquire`通过`raw_local_irq_save`宏来关闭硬件中断. 因为给定的自旋锁可能通过开启硬件中断来获取. 这样该进程就不会被抢占, 在该函数的最后通过`raw_local_irq_restore`来重新开启中断. 主要的功能在`__lock_acquire`函数中完成(作者说到会在之后的章节解读该函数). 

在`__raw_spin_lock`函数的最后, 会执行`LOCK_CONTENDED(lock, do_raw_spin_trylock, do_raw_spin_lock);`

`LOCK_CONTENDED`该宏定义在[include/linux/lockdep.h](https://github.com/torvalds/linux/blob/master/include/linux/lockdep.h)头文件中, 并只是调用给定的函数. 

```cpp
#define LOCK_CONTENDED(_lock, try, lock) \
	lock(_lock)
```

此时`lock`是`do_raw_spin_lock`函数, `_lock`是给定的`raw_spinlock_t`:

```cpp
static inline void do_raw_spin_lock(raw_spinlock_t *lock) __acquires(lock)
{
        __acquire(lock);
         arch_spin_lock(&lock->raw_lock);
}
```

其中`arch_spin_lock`宏定义为:

`#define arch_spin_lock(l)               queued_spin_lock(l)`

下一节中将深入了解`queued spinlocks`的工作原理和相关概念.
