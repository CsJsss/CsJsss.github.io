---
title: '[cpp]基于RAII的资源管理类的原理和实现'
toc: true
date: 2022-04-12 09:14:40
updated:
categories: cpp
tags: 
    - RAII
    - 资源管理类
---

`RAII(Resource Acquisition Is Initialization)`是`cpp`中的编程技术之一。其意义为: **资源获取就是初始化**, 保证资源在使用前获取, 使用后自动释放.降低程序因获取和释放资源导致出错的可能.

<!--more-->

> RAII, is a C++ programming technique which binds the life cycle of a resource that must be acquired before use (allocated heap memory, thread of execution, open socket, open file, locked mutex, disk space, database connection—anything that exists in limited supply) to the lifetime of an object.

`RAII`机制将**资源**(分配的堆内存、执行的线程、套接字、文件、mutex、硬盘空间、数据库连接等有限的资源)的生命周期绑定到`RAII`对象的生命周期上去.

## RAII的原理和基本流程:

1. 在`RAII`类的构造函数中申请资源(可能会抛出异常).
2. 所有可以访问`RAII`对象的地方使用资源.
3. `RAII`对象析构的时候释放所拥有的资源(不抛出异常).

## 应用

在标准库中, `RAII`技术有了广泛使用. 比如我们经常使用的`std::string`和`std::vector`. 以及管理锁相关的资源管理类`lock_guard`和`unique_lock`、管理用户自定义的资源(智能指针)`shared_ptr`、`weak_ptr`和`unique_ptr`.

## 优势

1. `RAII`机制保证所有可以访问`RAII`对象的函数都可以访问该对象所管理的资源, **减少不必要的运行时检测**. 

2. `RAII`机制还保证所有的资源在`RAII`对象的生命周期结束时被释放，与获取时相反顺序的顺序释放, **无需程序员手动释放**.

3. 在构造函数中如果发生异常导致资源获取失败, 所有已经构造完成的成员和基类对象以构造时相反的顺序进行释放, **防止资源泄漏**.

上述优势利用了`cpp`语言的核心特性: **对象的生命周期**, **构造的顺序**, **栈展开**等来避免资源泄露, 保证异常安全.

下面给出`cppreference`上给出的一个例子, 体现了`RAII资源管理类`的优势:

```cpp
std::mutex m;
 
void bad() 
{
    m.lock();                    // acquire the mutex
    f();                         // if f() throws an exception, the mutex is never released
    if(!everything_ok()) return; // early return, the mutex is never released
    m.unlock();                  // if bad() reaches this statement, the mutex is released
}
 
void good()
{
    std::lock_guard<std::mutex> lk(m); // RAII class: mutex acquisition is initialization
    f();                               // if f() throws an exception, the mutex is released
    if(!everything_ok()) return;       // early return, the mutex is released
}                                      // if good() returns normally, the mutex is released
```

### 栈展开

一旦构造出了异常对象, 控制流向上(调用堆栈)查找直到找到`try`, 此时与所有相关的`catch`块按照出现的顺序进行参数的比较,直到找到一个匹配。如果没有找到匹配，控制流继续展开堆栈，直到下一个try块，依此类推。如果找到匹配，控制流将跳转到匹配的`catch`块。

当控制流向上移动到调用堆栈时，将对所有已构造但尚未销毁的栈上的局部对象调用析构函数, 这就是栈展开.

#### 测试代码

以下代码直接参考了[StackUnwinding](https://github.com/ltimaginea/Cpp-Primer/blob/main/CppPrimer/Content/Ch18_ToolsForLargePrograms/Ch18_01_StackUnwinding.cpp).

```cpp
#include <iostream>
#include <memory>
#include <string>
#include <new>

class Except0
{
public:
	~Except0()
	{
		std::cout << "Except0's destructor is called!" << std::endl;
	}
private:
	std::string str_;
};

class Except1
{
public:
	~Except1()
	{
		std::cout << "Except1's destructor is called!" << std::endl;
	}
private:
	std::string str_;
};

class Except2
{
public:
	~Except2()
	{
		std::cout << "Except2's destructor is called!" << std::endl;
	}
private:
	std::string str_;
};

class Except3
{
public:
	~Except3()
	{
		std::cout << "Except3's destructor is called!" << std::endl;
	}
private:
	std::string str_;
};

class Except4
{
public:
	~Except4()
	{
		std::cout << "Except4's destructor is called!" << std::endl;
	}
private:
	std::string str_;
};

void Test3()
{
	Except4 ex4;
	// throw an exception
	std::string().at(1);
	Except3 ex3;
}

void Test2()
{
	Except2 ex2;
	Test3();
}

void Test1()
{
	Except1 ex1;
	Test2();
}

int main()
{
	std::cout << "Test start" << std::endl;
	try
	{
		Except0 ex0;
		Test1();
	}
	catch (const std::bad_alloc& err)
	{
		std::cout << err.what() << std::endl;
	}
	catch (const std::exception& err)
	{
		std::cout << err.what() << std::endl;
	}
	catch (...)
	{
		std::cout << "unknown exceptions" << std::endl;
	}
	std::cout << "Test end" << std::endl;
	return 0;
}

/* g++ -std=c++17
Test start
Except4's destructor is called!
Except2's destructor is called!
Except1's destructor is called!
Except0's destructor is called!
basic_string::at: __n (which is 1) >= this->size() (which is 0)
Test end
*/

// tips: 
//   1. 异常必须要被捕获处理，未捕获异常将导致不会调用局部对象的析构函数（典型情况如此，具体是否调用依赖于具体的实现）
```

#### 注意事项

注意异常必须被捕获, 否则会调用std::terminate : 终止当前的程序, 并且不会栈上调用局部对象的析构函数.

```bash
Test start
terminate called after throwing an instance of 'std::out_of_range'
  what():  basic_string::at: __n (which is 1) >= this->size() (which is 0)
```

## 实现

经过以上分析, 我们可以看到基于`RAII`技术的资源管理类主要用于标准库本身的以及向用户提供封装好的模板类. 而对用户提供的资源管理类通常可以分为`指针类型`和`锁类型`的. 我们分别实现**共享的指针类型资源管理类**和**锁资源管理类**.


### 共享的指针类型资源管理类

我们实现一个简易的`shared_ptr`模板类. `shared_ptr`使用指针用来管理用户指定的资源, 并提供和指针相同的行为: `->`, `*`操作符, 并支持拷贝赋值和拷贝构造. 并提供线程安全的资源访问和释放特性.

为了实现`shared_ptr`, 我们需要记录**引用计数**, 通过构造函数和拷贝构造等函数来维护这个引用计数即可. 而关键是如何记录这个引用计数. 这个**引用计数**应该对所有`shared_ptr`对象都是**可见**的, 这样才能正确记录. 为了实现对所有对象都可见, 我们可以在`shared_ptr`类中记录指向该**引用计数的指针**.

#### 代码实现

```cpp
// 不可拷贝基类
class noncopyable {
public:
    noncopyable(const noncopyable&) = delete;
    noncopyable operator=(const noncopyable&) = delete;
protected:
    noncopyable() = default;
    ~noncopyable() = default;
};

// 引用计数控制块
class refCount : noncopyable{
public:
    refCount () {
        _cnt.store(0);
    }

    refCount(int cnt) {
        _cnt.store(cnt);
    }

    void decRefCount() {
        _cnt.fetch_sub(1);
    }

    void incRefCount() {
        _cnt.fetch_add(1);
    }

    int getRefCount() {
        return _cnt.load();
    }

private:
    atomic_int _cnt;
};


// 简易版shared_ptr模板类
template <typename T>
class SharedPtr : noncopyable {
public:
    using value_type     = T;
    using pointer_type   = T*;
    using reference_type = T&;

    // 构造函数
    SharedPtr () : _ptr(nullptr), _ref(nullptr) {}
    SharedPtr (pointer_type ptr) : _ptr(ptr), _ref(new refCount(1)) {}
    SharedPtr (const SharedPtr& other) {
        _ptr = other._ptr;
        _ref = other._ref;
        this -> increase();
    }

    // 拷贝构造
    SharedPtr& operator = (const SharedPtr& other) {
        if (this == &other)
            return *this;
        // 先减当前的引用计数
        this -> decrease();
        // 拷贝赋值
        _ptr = other._ptr;
        _ref = other._ref;
        // 增加引用计数
        this -> increase();
    }


    // 析构函数
    ~SharedPtr() {
        cout << "~SharedPtr() called" << endl;
        decrease();
    }  

    int use_count() {
        return _ref -> getRefCount();
    }

    // Dereferences the stored pointer. The behavior is undefined if the stored pointer is null.
    pointer_type operator -> () {
        return this -> _ptr;
    }

    reference_type operator * (){
        return *(this -> _ptr);
    }

    pointer_type get() {
        return this -> _ptr;
    }

    operator bool (){
        return this -> _ptr != nullptr;
    }

private:
    // 内部实现, 不对外开放
    void decrease() {
        if (_ptr == nullptr)
            return ;
        _ref -> decRefCount();
        if (_ref -> getRefCount() == 0) {
            delete _ptr;
            cout << "free resource" << endl;
        }
    }

    void increase() {
        if (_ptr == nullptr)
            return ;
        _ref -> incRefCount();
    }

    // 指向控制块的指针, 记录引用计数
    refCount* _ref;
    // 指向共享资源的指针
    pointer_type _ptr;
};
```

#### 测试样例

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <atomic>
#include <memory>

using namespace std;

// 不可拷贝基类
class noncopyable {
public:
    noncopyable(const noncopyable&) = delete;
    noncopyable operator=(const noncopyable&) = delete;
protected:
    noncopyable() = default;
    ~noncopyable() = default;
};

// 引用计数控制块
class refCount : noncopyable{
public:
    refCount () {
        _cnt.store(0);
    }

    refCount(int cnt) {
        _cnt.store(cnt);
    }

    void decRefCount() {
        _cnt.fetch_sub(1);
    }

    void incRefCount() {
        _cnt.fetch_add(1);
    }

    int getRefCount() {
        return _cnt.load();
    }

private:
    atomic_int _cnt;
};


// 简易版shared_ptr模板类
template <typename T>
class SharedPtr : noncopyable {
public:
    using value_type     = T;
    using pointer_type   = T*;
    using reference_type = T&;

    // 构造函数
    SharedPtr () : _ptr(nullptr), _ref(nullptr) {}
    SharedPtr (pointer_type ptr) : _ptr(ptr), _ref(new refCount(1)) {}
    SharedPtr (const SharedPtr& other) {
        _ptr = other._ptr;
        _ref = other._ref;
        this -> increase();
    }

    // 拷贝构造
    SharedPtr& operator = (const SharedPtr& other) {
        if (this == &other)
            return *this;
        // 先减当前的引用计数
        this -> decrease();
        // 拷贝赋值
        _ptr = other._ptr;
        _ref = other._ref;
        // 增加引用计数
        this -> increase();
    }


    // 析构函数
    ~SharedPtr() {
        cout << "~SharedPtr() called" << endl;
        decrease();
    }  

    int use_count() {
        return _ref -> getRefCount();
    }

    // Dereferences the stored pointer. The behavior is undefined if the stored pointer is null.
    pointer_type operator -> () {
        return this -> _ptr;
    }

    reference_type operator * (){
        return *(this -> _ptr);
    }

    pointer_type get() {
        return this -> _ptr;
    }

    operator bool (){
        return this -> _ptr != nullptr;
    }

private:
    // 内部实现, 不对外开放
    void decrease() {
        if (_ptr == nullptr)
            return ;
        _ref -> decRefCount();
        if (_ref -> getRefCount() == 0) {
            delete _ptr;
            cout << "free resource" << endl;
        }
    }

    void increase() {
        if (_ptr == nullptr)
            return ;
        _ref -> incRefCount();
    }

    // 指向控制块的指针, 记录引用计数
    refCount* _ref;
    // 指向共享资源的指针
    pointer_type _ptr;
};


class Resource {
public:
    Resource () = default;
    Resource (int val) : _val(val) {}
    
    int get () const {
        return _val;
    }
private:
    int _val;
};

ostream& operator << (ostream& os, const Resource& res) {
    os << res.get();
    return os;
}


int main() {
    SharedPtr<Resource> sp(new Resource(123));

    auto nsp = sp;

    cout << sp -> get() << endl;
    cout << (*nsp).get() << endl;
    cout << nsp.use_count() << endl;

    // 使用前先判断是否为空, 调用了 operator bool
    if (nsp) {
        *nsp = 10086;
        auto p = nsp.get();
        cout << "nsp is not empty, *nsp = " << (*p) << endl;
    }

    return 0;
}

/*
123
123
2
nsp is not empty, *nsp = 10086
~SharedPtr() called
~SharedPtr() called
free resource
*/
```

### 锁资源管理类

锁资源管理类的实现较为直接, 可以使用**引用或指针**的方式去管理用户在构造函数中传入的锁资源. 通过构造函数和析构函数获取和释放资源, 并提供`lock`和`unlock`来管理锁资源, 实现了一个简易版的`unique_lock<mutex>`.

#### 代码实现

```cpp
class noncopyable {
public:
    noncopyable(const noncopyable&) = delete;
    noncopyable operator=(const noncopyable&) = delete;
protected:
    noncopyable() = default;
    ~noncopyable() = default;
};


class MutexUniqueLock: noncopyable {
public:
    MutexUniqueLock(mutex& mtx) : _mtx(mtx), _own(false) {
        _mtx.lock();
        _own = true;
    }

    void lock() {
        if (!_own) {
            _mtx.lock();
            _own = true;
        }
    }

    void unlock() {
        if (_own) {
            _mtx.unlock();
            _own = false;
        }
    }

    ~MutexUniqueLock() {
        if (_own)
            _mtx.unlock();
    }

private:
    // 指向mutex的引用
    mutex& _mtx;
    // 是否持有该锁
    bool _own;
};
```

#### 测试样例

测试样例是一个简单的**双线程奇偶交替打印**程序, 使用`CAS`和`mutex`

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <atomic>

using namespace std;

class noncopyable {
public:
    noncopyable(const noncopyable&) = delete;
    noncopyable operator=(const noncopyable&) = delete;
protected:
    noncopyable() = default;
    ~noncopyable() = default;
};


class MutexUniqueLock: noncopyable {
public:
    MutexUniqueLock(mutex& mtx) : _mtx(mtx), _own(false) {
        _mtx.lock();
        _own = true;
    }

    void lock() {
        if (!_own) {
            _mtx.lock();
            _own = true;
        }
    }

    void unlock() {
        if (_own) {
            _mtx.unlock();
            _own = false;
        }
    }

    ~MutexUniqueLock() {
        if (_own)
            _mtx.unlock();
    }

private:
    // 指向mutex的引用
    mutex& _mtx;
    // 是否持有该锁
    bool _own;
};


// 互斥锁
mutex mtx;
// 先打印奇数
atomic<bool> isOdd(true);


void printOdd() {
    for (int i = 1; i <= 100; i += 2) {
        bool want = true;
        // CAS, compare_exchange_weak会修改Expected的值, 因此需要在循环内修改
        while (isOdd.compare_exchange_weak(want, want) == false)
            want = true; 
        // 临界区
        MutexUniqueLock lock(mtx);
        cout << i << " ";
        isOdd = false;
    }
}

void printEven() {
    for (int i = 2; i <= 100; i += 2) {
        bool want = false;
        // CAS, compare_exchange_weak会修改Expected的值, 因此需要在循环内修改
        while (isOdd.compare_exchange_weak(want, want) == false)
            want = false; 
        // 临界区
        MutexUniqueLock lock(mtx);
        cout << i << " ";
        isOdd = true;
    }
}


int main() {
    
    thread oddThread(printOdd);
    thread evenThread(printEven);

    oddThread.join();
    evenThread.join();
    return 0;
}

/*
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 
26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 
50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 
76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100
*/
```

## 总结

基于`RAII`编程技术的资源管理类有着相同的思想内涵, 其在构造函数和析构函数中进行资源的获取和释放. 标准库封装了一些友好的资源管理类, 主要有基于锁机制的`lock_guard`和`unique_lock`, 还有智能指针类型的用户资源管理类`shared_ptr`、`weak_ptr`和`unique_ptr`. 针对不同语义下的应用场景, 需要重载一些函数来提供便捷的资源访问, 减轻程序编写过程中的负担.

## 参考

[RAII](https://en.cppreference.com/w/cpp/language/raii)
[栈展开](https://en.cppreference.com/w/cpp/language/throw#Stack_unwinding)
[StackUnwinding](https://github.com/ltimaginea/Cpp-Primer/blob/main/CppPrimer/Content/Ch18_ToolsForLargePrograms/Ch18_01_StackUnwinding.cpp)

----
**欢迎讨论指正**