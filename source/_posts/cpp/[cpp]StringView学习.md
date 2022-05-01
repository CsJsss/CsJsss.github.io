---
title: '[cpp]StringView学习'
toc: true
date: 2022-04-11 19:45:38
updated:
categories: cpp
tags: 
    - cpp
    - 语言基础
---

`string_view`是`cpp17`之后提供了一个模板类. 它维护一个对于底层字符数组的**只读视图**, 可以在多种场景下提高程序的性能.

<!--more-->

## StringView的优势

传递字符串参数的时候, 在不进行修改操作的时候通常都会使用`const string&`来接收实参, 其在接收字符串字面值、字符数组和字符串指针的时候还是会存在构造字符串的问题. 即先生成一个匿名`string`对象, 然后`const string&`绑定到该匿名对象上去. 当字符串很大时, 会存在严重的性能问题.


`substr`函数. `string`的`substr`函数会返回一个`string`对象. 该操作造成的拷贝会影响程序的性能(在**只读**要求下).

针对以上问题: `string_view`能够较好的解决. 因为其是一个**只读视图**, 用`string_view`作为参数拷贝的开销是很低的, 以及`string_view`的`substr`函数返回的还是一个`string_view`. 避免了重新生成一个新的字符串的大开销操作.

`string_view`在`cpp17`以前的一些第三方库中有自己的实现:

1. `leveldb`的[Slice实现](https://github.com/google/leveldb/blob/main/include/leveldb/slice.h).
2. `google`基础库`Abseil`的[StringView实现](https://github.com/abseil/abseil-cpp/blob/master/absl/strings/string_view.h).



## StringView的实现

### 字面值

可以使用`string_view sv = "just test"sv;`字面值来生成`string_view`.

```cpp
constexpr string_view operator"" sv(const char* _Str, size_t _Len) noexcept {
            return string_view(_Str, _Len);
        }
```

### 数据成员

`string_view`的模板类中, 只包含了两个私有数据成员`_Mydata`和`_Mysize`. `_Mydata`为指向底层字符数组的指针, 而`_Mysize`表示`string_view`的可见长度.

```cpp
// MSVC-14.30.30705: xstring
// wrapper for any kind of contiguous character buffer
using const_pointer          = const _Elem*;
using size_type              = size_t;
const_pointer _Mydata;
size_type _Mysize;
```

### 构造函数

```cpp
// 默认构造函数
constexpr basic_string_view() noexcept : _Mydata(), _Mysize(0) {}
// 拷贝构造
constexpr basic_string_view(const basic_string_view&) noexcept = default;
// 拷贝赋值
constexpr basic_string_view& operator=(const basic_string_view&) noexcept = default;

// 使用指针和长度进行构造 
constexpr basic_string_view(const const_pointer _Cts, const size_type _Count) noexcept // strengthened
        : _Mydata(_Cts), _Mysize(_Count) {}

// 只使用指针构造, 不同编译器的实现可能不同.
constexpr basic_string_view(const const_pointer _Ntcts) noexcept //strengthened
    : _Mydata(_Ntcts), _Mysize(_Traits::length(_Ntcts)) {}    
```

### 成员函数

`string_view`的成员函数几乎和`string`没有差异. 不过需要注意的是: `string_view`的成员函数无法修改底层的数据, 比如`operator[]`返回`constexpr`引用. 其能修改的只有`_Mydata`指针的指向以及`_Mysize`的大小(即`string_view`的可见范围).

```cpp
constexpr const_reference operator[]( size_type pos ) const;
```

**修改`_Mydata`指针和`_Mysize`大小的函数**:

```cpp
// Moves the start of the view forward by n characters. The behavior is undefined if n > size().
constexpr void remove_prefix( size_type n );

// Moves the end of the view back by n characters. The behavior is undefined if n > size().
constexpr void remove_suffix( size_type n );

// Exchanges the view with that of v.
constexpr void swap( basic_string_view& v ) noexcept;
```

## String和StringView的互相构造

1. string_view构造string

可以使用`string_view`直接调用`string`的构造函数来初始化一个`string`对象. 并且`string`不与`string_view`共享底层数据. 注意只能**显式**调用`string`来讲`string_view`进行转换, 因为其实对底层数据的拷贝.

```cpp
template< class StringViewLike >
explicit basic_string( const StringViewLike& t,
                       const Allocator& alloc = Allocator() );
```

**测试代码**

```cpp
// 通过字面量创建string_view, 先调用constexpr string_view operator"" sv返回string_view对象, 然后赋值拷贝
string_view sv = "abcdef"sv;
string str = string(sv);

str[0] = '1';
cout << "string = " << str << ", string_view = " << sv << endl;

/*
string = 1bcdef, string_view = abcdef
*/
```

2. string构造string_view

`string_view`可以使用`string`来构造, 原因是`string`有`string_view`的类型转换函数. 其可以进行**隐式的转换**, 因为`string`转换成`string_view`只是生成了一个**只读视图**.

```cpp
// string -> string_view 的类型转换函数
operator std::basic_string_view<CharT, Traits>() const noexcept;
```

**测试代码**

```cpp
string str = "abc";
string_view sv = str;
cout << "string_view = " << sv << endl;

/*
string_view = abc
*/
```

## StringView的使用注意事项

- 资源所有权的问题:
    > It is the programmer's responsibility to ensure that std::string_view does not outlive the pointed-to character array
    
    `string_view`的生命周期和其观察的底层字符串的生命周期是**无关**的. 因此如果底层字符串先于`string_view`析构, 那么当再次访问时, 其行为是未定义的.


- 底层字符串的修改问题:

    ```cpp
    string str = "abc";
    string_view sv(str);

    string s = move(str);

    cout << "sv = " << sv << ", str = " << str << ", s = " << s << endl;

    /*
    sv = bc, str = , s = abc
    */
    ```

    因此我们需要保证使用`string_view`观察的底层字符串其必须不能被修改, 否则会造成不可预期的后果.


- 终结符的问题:

    我们都知道`c`和`cpp`的字符串是以`\0`作为终结符的. 而`string_view`是限定了可见长度, 当我们使用`string_view`时, 需要注意其不能使用`strlen`系列的函数进行字符串的操作, 因为字符串终结符的可见性可能被`remove_suffix`移除掉了.

    ```cpp
    const string str = "abcdefg";
    string_view sv(str);
    sv.remove_prefix(1);
    sv.remove_suffix(2);

    cout << "sv = " << sv << ", strlen(sv) = " << strlen(sv.data()) << endl;

    /* Error
    sv = bcde, strlen(sv) = 6  
    */
    ```

### 总结

`string_view`解决了**只读字符串**某些场景下的性能问题. 但其在使用的时候还需要注意其引入的问题, 其不像`lock_guard`、`unique_lock`、`shared_ptr`、`weak_ptr`或`unique_ptr`等资源管理类一样和被管理资源的生命周期有着较为紧密的联系, 因此在使用的时候需要注意上述的几个问题.


### 参考
[cppreference-string_view](https://en.cppreference.com/w/cpp/string/basic_string_view)
[[现代C++]性能控的工具箱之string_view](https://segmentfault.com/a/1190000018387368)
[C++17剖析：string_view的实现，以及性能](http://t.zoukankan.com/monkeyteng-p-10304610.html)