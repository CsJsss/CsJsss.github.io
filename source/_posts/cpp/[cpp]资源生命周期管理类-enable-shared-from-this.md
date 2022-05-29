---
title: '[cpp]资源生命周期管理类:enable_shared_from_this'
toc: true
date: 2022-04-26 22:12:50
updated:
categories: cpp
tags: 
    - 资源管理类
    - enable_shared_from_this
---

`enable_shared_from_this`模板类能够帮助我们轻松的用对象在其方法中获取`指向对象的shared_ptr`, 从而在并行编程中安全的管理资源的生命周期, 避免跨线程调用中资源的提前释放导致程序出错的危害.

<!--more-->

我们在之前简单学习了[基于RAII的资源管理类的原理和实现](https://csjsss.github.io/2022/04/12/cpp/%5Bcpp%5D%E5%9F%BA%E4%BA%8ERAII%E7%9A%84%E8%B5%84%E6%BA%90%E7%AE%A1%E7%90%86%E7%B1%BB%E7%9A%84%E5%8E%9F%E7%90%86%E5%92%8C%E5%AE%9E%E7%8E%B0/), 并实现了一个简易的`shared_ptr`类来安全的管理资源. `shared_ptr`模板类使用`共享的Control Block`来管理资源的生命周期, `Control Block`记录了引用计数、`weak`引用计数和其他必要的信息来管理资源. 当使用`raw`指针构造一个`shared_ptr`对象时, 新的`Control Block`就会被创建. 因此为了保证只有唯一一个`Control Block`来管理资源, 必须用已有的`shared_ptr对象`使用拷贝构造\拷贝赋值的方式创建新的`shared_ptr对象`. 从而**避免资源被多次释放**造成的程序出错.

下面给出一个典型的错误使用场景:

```cpp
#include <iostream>
#include <memory>

using namespace std;

int main() {
     {
         int* p = new int(1234);
         shared_ptr<int> sp1 {p};
         shared_ptr<int> sp2 {p};
         cout << "ref Count = " << sp1.use_count() << endl;
     }
     cout << "Done\n";
     return 0;
}

/* Output on Linux Ubuntu g++ 9.4.0
ref Count = 1
free(): double free detected in tcache 2
已放弃 (核心已转储)
*/
```

因此我们必须避免同一个资源被多个`shared_ptr`对象管理, 这会造成程序出错.

## 对象的生命周期

在并行(异步)编程中, 一个线程可能会调用其他线程的函数异步的完成某些任务, 而该任务依赖于当前线程所用的对象资源, 这种情况下, 必须保证**该对象资源的生命周期必须比异步函数的生命周期要长**, 因为如果在异步函数执行的过程中它所用的对象被其他线程析构了, 那么会造成程序崩溃. 因此我们必须使用一些方法保证对象资源的生命周期, 一般实践中使用对象的`this`指针来传递对象的上下文, 保证该对象的跨线程生命周期. 简单来说, 我们使用`this`指针保证`A`线程中的对象资源在调用`B`线程中的异步方法, 且该方法使用该对象资源时, 该对象资源的生命周期必须长于`B`线程中的异步函数, 即其在`B`线程中异步函数生命周期中不可被其他线程释放.

为了实现上述需求, 我们可以使用`shared_ptr`来管理`this`指针(管理对象资源). 那么该如何管理呢？
我们考虑从该对象本身构造出指向其自身的`shared_ptr`对象. 我们需要从`shared_ptr`所管理的对象中获取其指向自身的`shared_ptr`对象时, 如果我们简单的使用类的成员函数返回指向自身的`shared_ptr`对象, 那么根据以上分析, 这将会导致程序出错.

```cpp
#include <iostream>
#include <memory>

using namespace std;

class Resource {
public:
    Resource (int res) : _res(res) {}
    ~Resource () {
        cout << "called dest." << endl;
    }
    shared_ptr<Resource> getObject() {
        return shared_ptr<Resource>(this);
    }

private:
    int _res;
};

int main() {
     {
         shared_ptr<Resource> sp = make_shared<Resource>(10);
         auto objSp = sp -> getObject();
     }
     cout << "Done\n";
     return 0;
}

/* Output on Linux Ubuntu g++ 9.4.0
called dest.
double free or corruption (out)
已放弃 (核心已转储)
*/
```

上面错误使用场景和最开始提到的场景是一模一样的,即都用了多个`Control Block`来管理指针资源, 从而导致重复释放. 这种情况下, 我们就需要`enable_shared_from_this`来实现上述需求. 

```cpp
#include <iostream>
#include <memory>

using namespace std;

class Resource : public enable_shared_from_this<Resource> {
public:
    Resource(int res) :
        _res(res) {
    }
    ~Resource() {
        cout << "called dest." << endl;
    }
    shared_ptr<Resource> getObject() {
        return shared_from_this();
    }

private:
    int _res;
};

int main() {
    {
        shared_ptr<Resource> sp = make_shared<Resource>(10);
        cout << "ref cnt = " << sp.use_count() << endl;
        auto objSp = sp->getObject();
        cout << "ref cnt = " << sp.use_count() << endl;
    }
    cout << "Done\n";
    return 0;
}

/* Output on Linux Ubuntu g++ 9.4.0
ref cnt = 1
ref cnt = 2
called dest.
Done
*/
```

需要实现上述需求的资源类需要**公有继承**`enable_shared_from_this`模板类, 然后使用`shared_from_this`方法(`enable_shared_from_this`模板类的公有方法)来获取一个指向其**对象自身**的`shared_ptr`对象.

我们简单来看以下`enable_shared_from_this`模板类的源码, 看看其是如何实现的上述功能的.

```cpp
/**
 *  @brief Base class allowing use of member function shared_from_this.
 */
template <typename _Tp>
class enable_shared_from_this {
protected:
    constexpr enable_shared_from_this() noexcept {
    }

    enable_shared_from_this(const enable_shared_from_this &) noexcept {
    }

    enable_shared_from_this &
    operator=(const enable_shared_from_this &) noexcept {
        return *this;
    }

    ~enable_shared_from_this() {
    }

public:
    /* 公有方法 */
    shared_ptr<_Tp>
    shared_from_this() {
        return shared_ptr<_Tp>(this->_M_weak_this);
    }

    shared_ptr<const _Tp>
    shared_from_this() const {
        return shared_ptr<const _Tp>(this->_M_weak_this);
    }

#if __cplusplus > 201402L || !defined(__STRICT_ANSI__) // c++1z or gnu++11
#define __cpp_lib_enable_shared_from_this 201603
    weak_ptr<_Tp>
    weak_from_this() noexcept {
        return this->_M_weak_this;
    }

    weak_ptr<const _Tp>
    weak_from_this() const noexcept {
        return this->_M_weak_this;
    }
#endif

private:
    template <typename _Tp1>
    void
    _M_weak_assign(_Tp1 *__p, const __shared_count<> &__n) const noexcept {
        _M_weak_this._M_assign(__p, __n);
    }

    // Found by ADL when this is an associated class.
    friend const enable_shared_from_this *
    __enable_shared_from_this_base(const __shared_count<> &,
                                   const enable_shared_from_this *__p) {
        return __p;
    }

    template <typename, _Lock_policy>
    friend class __shared_ptr;

    mutable weak_ptr<_Tp> _M_weak_this;
};
```

以上源码我们发现三点:

- `enable_shared_from`存在一个**mutable**成员变量`weak_ptr<_Tp> _M_weak_this`, 这样`const`对象也能够对其进行修改.
- `enable_shared_from`含有**友元类**`__shared_ptr`, 这样`shared_ptr`类能够访问`enable_shared_from`的私有成员变量.
- `cpp17`添加了`weak_from_this()`方法返回`weak_ptr`的拷贝, 然后使用`weak_ptr.lock()`就能安全的获取`shared_ptr`对象.

具体`shared_from_this()`函数的实现是很简单的, 其通过私有成员变量来构造`shared_ptr`对象然后返回. 那么该私有成员变量是何时初始化的呢? 

它是在构造`shared_ptr`对象的时候被初始化的, 在初始化构造一个`shared_ptr`对象的时候, 可以根据`type traits`(`std::enable_if` 和 `std::is_convertible`)来实现. 如果这个资源类**公有继承**了`std::enable_shared_from_this`模板类, 那么就将父类中的`_M_weak_this`初始化绑定到创建出来的`shared_ptr`对象上去(**友元类**的声明让其能够访问私有成员变量), 这样就实现了`_M_weak_this`的安全初始化. 这种设计对于`shared_ptr`模板类来说是侵入式的.

最后给出一个[讲解很好博客](https://www.nextptr.com/tutorial/ta1414193955/enable_shared_from_this-overview-examples-and-internals)的图示和代码.

```cpp
struct Article : std::enable_shared_from_this<Article> {
 //stuff..
};

void foo() {
 //Step 1
 // '_M_weak_this' 是空的, 没有和 Control Block 相关联
 auto pa = new Article;

 //Step 2
 // '_M_weak_this' 被初始化, 与 Control Block 相关联
 auto spa = std::shared_ptr<Article>(pa);
}
```

![图示](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2022/5/enable_shared_from_this.png)


需要注意的是, **公有继承**的原因是`_M_weak_this`的初始化是在`shared_ptr`对象的构造函数中初始化的, 必须能够检测到该类是继承了`enable_shared_from_this`基类的. 另外, **必须通过shared_ptr来调用对象的shared_from_this**, 因为`_M_weak_this`的初始化是在`shared_ptr`对象的构造函数中进行的, 如果还没有`shared_ptr`对象被构造, 那么调用`shared_from_this()`使用`_M_weak_this`来构造`shared_ptr`会造成`std::bad_weak_ptr`异常, 原因是`_M_weak_this`还没有和某个`Contorl Block`相关联. 当然如果使用`cpp17`, 可以用`weak_from_this()`来获取`weak_ptr`自行`lock()`并判断来保证安全, 不过还是建议统一先构造`shared_ptr`对象, 再安全的使用`shared_from_this`方法.

## 总结

当一个类需要"共享自己"的时候, `enable_shared_from_this`模板类就是标准库提供的强大工具. 它可以安全的管理和构造我们所需的`shared_ptr`对象, 不过还是有一些问题是需要注意的. 首先我们必须先构造`shared_ptr`对象, 然后使用类的`shared_from_this`方法, 因为必须保证`enable_shared_from_this`基类的`_M_weak_this`被初始化. 其次我们不能在类的构造函数中调用`shared_from_this`, 因为此时`_M_weak_this`可能还未初始化. 而且必须**公有继承**`enable_shared_from_this`. 

最后**对象的生命周期管理**是多线程(异步)编程中必须关注的一个问题, `cpp`提供的智能指针和`enable_shared_from_this`等模板类很友好的实现了我们的需求, 不过仍然需要注意一些坑点. 向往侯捷老师说的**胸中自有丘壑**的境界水平, 努力做到**知其然知其所以然**, 才能提升自身的视野和水平呀.


## 参考

[cppRef](https://en.cppreference.com/w/cpp/memory/enable_shared_from_this)
[图文讲解blog](https://www.nextptr.com/tutorial/ta1414193955/enable_shared_from_this-overview-examples-and-internals)
