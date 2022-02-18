---
title: '[cpp]语言基础'
toc: true
date: 2022-02-16 16:19:19
updated:
categories: cpp
tags: 
    - cpp
    - 语言基础
---

## cpp语言的特点

- cpp是一个语言联邦. 其是**过程式**语言（兼容包含c语言）、**面向对象**语言（有面向对象语言的封装、继承和多态的特点）、**泛型**语言（包含标准模板库STL, 有容器、迭代器、算法、适配器、仿函数和分配器）、**函数式**语言（cpp11引入匿名函数的特性）和**元编程**语言（**TODO**: 不懂). 
- cpp是不断发展的语言, cpp11、cpp14、cpp17、cpp20引入了很多新的特性.

<!--more-->

## cpp中struct和class的区别

在cpp中struct和class只有很细微的差别. 
- 从使用习惯上来说. strcut一般用作数据结构集合的描述, class用作类的定义（对象的封装）.
- struct中默认访问控制权限是 public 的, 而class默认访问控制权限是 private 的. 如:
    ```cpp
    struct A{
        int iNum;    // 默认访问控制权限是 public
    }
    class B{
        int iNum;    // 默认访问控制权限是 private
    }
  ```
- class 继承默认是 private 继承，而 struct 继承默认是 public 继承
- class 支持泛型模板编程. 如STL.

## include头文件的顺序以及双引号""和尖括号<>的区别
1. 区别：
    - 尖括号<>的头文件是系统文件，双引号""的头文件是自定义文件。
    - 编译器预处理阶段查找头文件的路径不一样。
2. 查找路径：
    - 使用尖括号<>的头文件的查找路径：编译器设置的头文件路径(g++中通过-I参数, 如include opencv等第三方库时)-->系统变量(如iostream、algorithm等编译器自带头文件)。
    - 使用双引号""的头文件的查找路径：当前目录-->编译器设置的头文件路径-->系统变量

## cpp结构体和C结构体的区别

区别：
1. C的结构体内不允许有函数存在，cpp允许有内部成员函数，且允许该函数是虚函数。
2. C的结构体对内部成员变量的访问权限只能是public，而cpp允许public,protected,private三种。
3. C语言的结构体是不可以继承的，cpp的结构体是可以从其他的结构体或者类继承过来的。
4. C 中使用结构体需要加上 struct 关键字，或者对结构体使用 typedef 取别名，而 cpp 中可以省略 struct 关键字直接使用。

## 导入C函数的关键字是什么，cpp编译时和C有什么不同？

1. 关键字：在cpp中，导入C函数的关键字是extern，表达形式为extern “C”， extern "C"的主要作用就是为了能够正确实现cpp代码调用其他C语言代码。加上extern "C"后，会指示编译器这部分代码按C语言的进行编译，而不是cpp的。
2. 编译区别：由于cpp支持函数重载，因此编译器编译函数的过程中会将函数的参数类型也加到编译后的代码中，而不仅仅是函数名；而C语言并不支持函数重载，因此编译C语言代码的函数时不会带上函数的参数类型，一般只包括函数名。

    ```cpp
    // 1. extern.h
    #ifndef __EXTERN

    #define __EXTERN

    // extern 声明
    extern int x;

    int mul(int x, int y);

    #endif  /* __EXTERN */

    // 2. extern.cpp 
    #include "extern.h"

    // 变量x的定义
    int x = 10;

    int mul(int x, int y) {
        return x * y;
    }

    // 3. main.cpp

    #include <iostream>

    using namespace std;

    // 声明是外部变量和函数, 在链接的时候重解析
    extern int x;
    extern int mul(int x, int y);

    int main() {
        cout << x << endl;
        cout << mul(x, x) << endl;
        return 0;
    }

    /* 
    最终的效果: main.cpp 没有直接include extern.h, 通过 extern 方法访问了其函数和变量
    */
    ```

编译命令和执行结果

```bash
$ g++ main.cpp extern.cpp -o main.exe
$ ./main.exe
10
100
```

## cpp从代码到可执行二进制文件的过程

cpp和C语言类似，一个cpp程序从源码到执行文件，有四个过程，**预编译**、**编译**、**汇编**、**链接**.

1. 预编译：这个过程主要的处理操作如下：
（1） 将所有的#define删除，并且展开所有的宏定义
（2） 处理所有的条件预编译指令，如#if、#ifdef
（3） 处理#include预编译指令，将被包含的文件插入到该预编译指令的位置。
（4） 过滤所有的注释
（5） 添加行号和文件名标识。

2. 编译：这个过程主要的处理操作如下：
（1） 词法分析：将源代码的字符序列分割成一系列的记号。
（2） 语法分析：对记号进行语法分析，产生语法树。
（3） 语义分析：判断表达式是否有意义。
（4） 代码优化：
（5） 目标代码生成：生成汇编代码。
（6） 目标代码优化：

3. 汇编：这个过程主要是将汇编代码转变成机器可以执行的指令。

4. 链接：将不同的源文件产生的目标文件进行链接，从而形成一个可以执行的程序。

链接分为**静态链接**和**动态链接**。

**静态链接**，是在链接的时候就已经把要调用的函数或者过程链接到了生成的可执行文件中，就算你在去把静态库删除也不会影响可执行程序的执行；生成的静态链接库，Windows下以.lib为后缀，Linux下以.a为后缀。
  - 优点: 速度快
  - 缺点: 多次复制, 浪费空间

**动态链接**，是在链接的时候没有把调用的函数代码链接进去，而是在执行的过程中，再去找要链接的函数，生成的可执行文件中没有函数代码，只包含函数的重定位信息，所以当你删除动态库时，可执行程序就不能运行。生成的动态链接库，Windows下以.dll为后缀，Linux下以.so为后缀。
  - 优点: 节省空间
  - 缺点: 执行时才链接, 需要重定位寻址, 速度较慢.

## static关键字的作用

cpp中**static**有**限定作用域**和**改变存储特性**的作用.

1. 全局静态变量: static作用于全局变量时, 限定了该变量的作用范围为本文件. 若未初始化, 则存储于全局未初始化段(bss), 并初始化为0. 若初始化了, 则存储于data段.
2. 局部静态变量: static作用于局部变量时, 改变了该变量的存储特性, 若未初始化, 则存储于全局未初始化段(bss), 并初始化为0. 若初始化了, 则存储于data段. 且该变量只会初始化一次. 这样的效果像是限定了作用域的全局变量, 而且避免了全局变量在其他区域被访问和修改.
3. 静态函数: static作用于函数时, 限定了该函数的作用域, 其只能作用于该文件.
4. 静态成员变量: static作用于类成员变量时, 其是申明, 必须要在外部进行定义. 这种方式改变了该变量的存储特性, 变成了类变量, 无需通过对象即可访问, 即变成了只能通过类进行访问的全局变量.
5. 静态成员函数: static作用域类成员函数时, 该函数即为类函数, 无需通过对象即可访问, 而且只能访问静态成员变量, 且不能是虚函数, 且没有this指针.

## 数组和指针的区别

1. 赋值：同类型指针变量可以相互赋值；数组不行，只能一个一个元素的赋值或拷贝
2. 存储方式: 
   1. 数组：数组在内存中是连续存放的，开辟一块连续的内存空间。数组是根据数组的下进行访问的，数组的存储空间，不是在静态区就是在栈上。
   2. 指针：指针很灵活，它可以指向任意类型的数据。指针的类型说明了它所指向地址空间的内存。由于指针本身就是一个变量，再加上它所存放的也是变量，所以指针所指向的存储空间大小不能确定, 而指针自身的存储空间大小是确定的。
3. 求sizeof: 
   1. 数组所占存储空间的内存大小：sizeof（数据类型）* 数组大小, $数组大小=sizeof(数组名) / sizeof(数据类型)$
   2. 在32位平台下，无论指针的类型是什么，sizeof（指针名）都是4，在64位平台下，无论指针的类型是什么，sizeof（指针名）都是8。

## 什么是函数指针，如何定义函数指针，有什么使用场景

1. 概念：函数指针就是指向函数的指针变量。每一个函数都有一个入口地址，该入口地址就是函数指针所指向的地址。
2. 定义形式如下:
   ```cpp
   int func(int a);  
   int (*f)(int a);  // 定义函数指针变量f
   f = &func;  
   ```
3. 函数指针的应用场景：**回调（callback）**。我们调用别人提供的 API函数(Application Programming Interface,应用程序编程接口)，称为Call；如果别人的库里面调用我们的函数，就叫Callback。

```cpp
#include <iostream>

using namespace std;

// 定义函数指针类型, 参数为一个int, 返回值为int
typedef int (*FuncPointer) (int x);

int addOne(int x) {
    return x + 1;
}

int addTwo(int x) {
    return x + 2;
}

// 函数指针作为函数的参数
int addYouWant(FuncPointer fp, int x) {
    return fp(x);
}

int main() {
    FuncPointer fp;
    fp = addOne;
    cout << fp(5) << endl;
    fp = addTwo;
    cout << fp(5) << endl;

    cout << addYouWant(addOne, 5) << endl;

    cout << fp << endl;
    return 0;
}
```

## 静态变量什么时候初始化

作用域：cpp里作用域可分为6种：全局，局部，类，语句，命名空间和文件作用域。

对于C语言的全局和静态变量(int, char, double等)，初始化发生在任何代码执行之前，属于**编译期初始化**.而cpp标准规定：全局或静态对象当且仅**当对象首次用到时才进行构造初始化**。

cpp规定，const的静态成员可以直接在类内初始化(*编译器初始化*)，而非const的静态成员需要在类外声明以初始化。对于后一种情况，我们一般选择在类的实现文件中初始化(*运行期初始化*)。

**生命周期**：静态全局变量、静态局部变量都在静态存储区，直到程序结束才会回收内存。类静态成员变量在静态存储区，当超出类作用域时回收内存。

## nullptr调用成员函数可以吗？为什么？

```cpp
#include <iostream>

using namespace std;

class animal {
public:
  void sleep() { cout << "animal sleep" << endl; }
  void breathe() { cout << "animal breathe haha" << endl; }
};
class fish : public animal {
public:
  void breathe() { cout << "fish bubble" << endl; }
};
int main() {
  animal *pAn = nullptr;
  // 编译器静态绑定: animal::breathe(pAn)  animal::breathe 不是虚函数且没有解引用的行为, 因此可以正常运行
  pAn->breathe(); // 输出：animal breathe haha

   // fish::breathe(pFish) 不是虚函数且没有解引用的行为, 因此可以正常运行
  fish *pFish = nullptr;
  pFish->breathe(); // 输出：fish bubble
  return 0;
}
```

这是**cpp的静态绑定**, 因为在编译时对象就绑定了函数地址，和指针空不空没关系。pAn->breathe();编译的时候，函数的地址就和指针pAn绑定了；调用breath(*this), this就等于pAn。由于函数中没有需要解引用this的地方，所以函数运行不会出错，但是若用到this，因为this=nullptr，运行出错。

## 什么是野指针，怎么产生的，如何避免？

1. 概念：野指针就是**指针指向的位置是不可知的**（随机的、不正确的、没有明确限制的）
2. 产生原因：释放内存后指针不及时置空（野指针），依然指向了该内存，那么可能出现非法访问的错误, 或者返回了函数中的指向栈中变量的指针(**指针指向的内存被释放掉了**)。或者使用未初始化的指针(**指针未初始化**)。
3. **避免办法**：
（1）初始化置NULL
（2）申请内存后判空
（3）指针释放后置NULL
（4）使用智能指针

## 内联函数和宏函数的区别

**宏定义不是函数，但是使用起来像函数**。预处理器用复制宏代码的方式代替函数的调用，省去了函数压栈退栈过程，提高了效率；而**内联函数本质上是一个函数**，内联函数一般用于函数体的代码比较简单的函数，不能包含复杂的控制语句，while、switch，并且内联函数本身不能直接调用自身。
宏函数是在**预编译**的时候把所有的宏名用宏体来替换，简单的说就是**字符串替换** ；而内联函数则是在**编译**的时候进行代码插入，编译器会在每处调用内联函数的地方直接把内联函数的**内容展开**，这样可以省去函数的调用的开销，提高效率
宏定义是没有**类型检查**的，无论对还是错都是直接替换；而内联函数在编译的时候会进行类型的检查，内联函数满足函数的性质，比如有返回值、参数列表等

- 1、使用时的一些注意事项：

  使用宏定义一定要注意错误情况的出现，比如**宏定义函数没有类型检查**，可能传进来任意类型，从而带来错误，如举例。还有就是括号的使用，宏在定义时要小心处理宏参数，一般用括号括起来，否则容易出现二义性
  inline函数一般用于比较小的，频繁调用的函数，这样可以减少函数调用带来的开销。只需要在函数返回类型前加上关键字inline，即可将函数指定为inline函数。
  同其它函数不同的是，最好将inline函数定义在头文件，而不仅仅是声明，因为编译器在处理inline函数时，需要在调用点内联展开该函数，所以仅需要函数声明是不够的。

- 2、内联函数使用的条件：

  内联是以代码膨胀（**复制**）为代价，仅仅省去了函数调用的开销，从而提高函数的执行效率。如果执行函数体内代码的时间，相比于函数调用的开销较大，那么效率 的收获会很少。另一方面，每一处内联函数的调用都要复制代码，将使程序的总代码量增大，消耗更多的内存空间。以下情况不宜使用内联：
  （1）如果函数体内的代码比较长，使用内联将导致内存消耗代价较高。
  （2）如果函数体内出现循环，那么执行函数体内代码的时间要比函数调用的开销大。
  内联不是什么时候都能展开的，一个好的编译器将会根据函数的定义体，自动地取消不符合要求的内联, 即**inline为内联建议**。

```cpp
#include <cstdio>

// 宏函数
#define MAX(a, b) ((a) > (b) ? (a) : (b))

// 内联函数
inline int max(int a, int b) {
    if (a > b)
        return a;
    return b;
} 

int main() {
    printf("macro function %d\n", MAX(10, 5));
    printf("inline function %d\n", max(10, 5));
}
```

## 运算符i++和++i的区别

- 赋值顺序不同：++ i 是先加后赋值；i ++ 是先赋值后加；++i和i++都是分两步完成的。

- 效率不同：后置++执行速度比前置的慢。

- i++ 不能作为左值，而 ++i 可以

- 两者都不是原子操作

```cpp
#include <iostream>
#include <ostream>

using namespace std;

template <typename T>
class Interger {
    T val;
public:
    Interger (T v) : val(v){}

    T getVal() const {
        return this -> val;
    }

    // ++ i
    Interger& operator ++ () {
        this -> val += 1;
        return *this;
    }

    // i ++ 
    Interger operator ++ (int) {
        Interger<T> tmp(this -> val);
        this -> val += 1;
        return tmp;
    }
};

template <typename T>
ostream& operator << (ostream& os, const Interger<T>& u) {
    os << u.getVal();
    return os;
}

int main() {
    Interger<int> a(10), b(10);
    cout << a ++ << endl;
    cout << ++ b << endl;

    Interger<float> c(3.14);
    cout << c ++ << endl;
    cout << ++ c << endl;

    return 0;

/* 输出
10
11
3.14
5.14
*/
}
```

## new和malloc的区别，各自底层实现原理

1. new是操作符(cpp关键字)，而malloc是c语言的库函数(cstdlib)。
2. new在调用的时候先分配内存，在调用构造函数，释放的时候调用析构函数；而malloc没有构造函数和析构函数。
3. malloc需要给定申请内存的大小，返回的指针(void *)需要强转；new会调用构造函数，不用指定内存的大小，返回指针不用强转。
4. new可以被重载(operator new)；malloc不行
5. new分配内存更直接和安全。
6. new发生错误抛出异常(bad_alloc)，malloc失败返回值为NULL
7. new支持数组, 使用`new[]`和`delete[]`支持.
8. new和delete在**自由存储区**上动态申请和分配内存, malloc和free在**操作系统堆上**动态申请和分配内存
9. new和delete可以调用malloc和free, 反之则否.

malloc和free搭配使用. 其从操作系统的堆(Heap)内存区动态申请和释放内存空间. 当开辟的空间小于 128K 时，调用 brk（）函数；当开辟的空间大于 128K 时，调用mmap（）。malloc采用的是内存池的管理方式，以减少内存碎片。先申请大块内存作为堆区，然后将堆区分为多个内存块。当用户申请内存时，直接从堆区分配一块合适的空闲快。采用隐式链表将所有空闲块，每一个空闲块记录了一个未分配的、连续的内存地址（有点像操作系统的空闲区链表）。

new和delete搭配使用. 其从 **自由存储区** 动态分配内存. 自由存储区是cpp中new和delete运算符分配和释放对象抽象出的概念. 操作系统的堆(Heap)和自由存储区并不等价. 大多数情况下, cpp编译器默认使用堆作为自由存储区, 也即是缺省的全局运算符new和delete也许会按照malloc和free的方式来实现. 而可以通过重载new运算符, 改用其他内存来实现内存的分配, 例如全局变量做的对象池，这时自由存储区就区别于堆了。

**new底层实现**：关键字new在调用构造函数的时候实际上进行了如下的几个步骤：

1. 通过`operator new`函数动态申请一块内存.
2. 调用构造函数初始化这块内存（为这个新对象添加属性）
3. 返回指向对象的指针


```cpp
#include <iostream>
#include <new>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

class MyString {
private:
    string str;
public:
    MyString (const string& s): str(s) {
        cout  << endl << "call mystring constructor function" << endl;
    } 

    ~MyString () = default;

    
    static void* operator new (size_t size) throw() {
        cout  << endl <<  "call mystring operator new function!" << endl;
        // maclloc 函数实现 operator new
        void* p = malloc(size);
        // 编译器自带的全局operator new 实现
        // void *p = ::operator new(size);
        if (p == NULL)
            throw bad_alloc();
        return p;
    }

    static void* operator new (size_t size, void* p) {
        cout << endl << "place ment new called!" << endl;
        return p;
    }

    // 通过getline实现字符串分割
    vector<string> split(char delim) {
        stringstream ss(this -> str);
        string word;
        vector<string> ans;
        while (getline(ss, word, delim))
            ans.emplace_back(word);
        return ans;
    }

};

void printSplit(MyString* s, char delim) {
    // 通过delim字符进行分隔
    auto ans = s -> split(delim);
    cout << "string split result : " << endl;
    for (auto& c : ans)
        cout << c << endl;
    cout << "split string end !" << endl;
}

int main() {
    MyString* s = new MyString("I am using cpp.");

    printSplit(s, ' ');

    // placement new: 在一块已经分配好的内存上调用构造函数, 不涉及内存的动态申请
    s = new (s) MyString("Testing,PlaceMent,New!");

    printSplit(s, ',');

    return 0;
}

/* 输出
call mystring operator new function!

call mystring constructor function
string split result :
I
am
using
cpp.
split string end !

place ment new called!

call mystring constructor function
string split result :
Testing
PlaceMent
New!
split string end !
*/
```

## const和define的区别

const用于**定义常量**；而define用于**定义宏**，而宏也可以用于定义常量。都用于常量定义时，它们的区别有：

- const生效于**编译**的阶段；define生效于**预处理**阶段。
- const定义的常量，在C语言中是**存储在内存**中、需要额外的内存空间的；define定义的常量，运行时是**直接的操作数**，并不会存放在内存中。
- const定义的常量是带**类型**的；define定义的常量不带类型。因此define定义的常量不利于类型检查。

## 函数指针和指针函数的区别

1. **定义**: 
   - 指针函数本质是一个函数，其返回值为指针。
   - 函数指针本质是一个指针，其指向一个函数。

2. **写法**
   ```cpp
    指针函数：int *func(int x,int y);
    函数指针：int (*func)(int x,int y)
   ```

## Top-Level Const和Low-Level Const

- **顶层const**表示指针是个常量, 这种指针称为**指针常量**.
- **底层const**表示指针所指的对象是常量, 称为**常量指针**.

**用于声明引用的const都是底层const**, 简称为**常量引用**, 其能绑定到非常量对象、字面值和一般表达式上。

```cpp
#include <iostream>

using namespace std;

int main() {
    int i = 0;
    int* const p1 = &i; // 顶层const, 常量指针, p1是常量
    const int ci = 42; // 顶层const, 无法修改ci的值
    const int *p2 = &ci; // 底层const, 允许修改p2的值, 无法修改p2指向的值
    const int* const p3 = p2; // 左边是底层const, 右边是顶层const, 无法修改p3以及修改p3指向的内容
    const int& r = ci; // 用于声明引用的const都是底层const


    int x = 10;
    // 常量引用绑定到左值上, 无法通过引用修改该变量
    const int& r1 = x;

    // 常量引用绑定到表达式上, 该表达式为右值, 因此常量引用绑定到了一个临时对象上
    const int& r2 = x ++ ;

    cout << "x = " << x << endl;
    
    x = 1234;
    cout << "修改原变量 x 为 " << x  << " 后, 常量引用r1值变成 " << r1 << " , 常量引用r2值变成 " << r2 << endl;

    float f = 3.14;
    // 常量引用类型和原始类型不匹配
    const int& r3 = f;

    f = 4.567;
    cout << "修改f后, r3值为: " << r3 << endl;

    // 常量引用绑定到类型匹配的const对象上去
    const int cx = 4;
    const int& r4 = cx;

    // 常量引用绑定到字面量上
    const int& r5 = 9527;

    return 0;

/* 输出
x = 11
修改原变量 x 为 1234 后, 常量引用r1值变成 1234 , 常量引用r2值变成 10
修改f后, r3值为: 3
*/
}
```

## 使用指针需要注意什么

1. 定义指针时，先初始化为NULL, 防止使用未初始化的指针(野指针).
2. 调用函数返回指针后, 判断指针是否为NULL, 如`malloc`. `new`一般不需要, 其失败的话会触发`bad_alloc`异常.
3. 指针指向的内存回收后, 置指针为NULL. 如`free`一块动态内存后, 需要置NULL. 不返回指针栈区的指针. 防止指针悬挂.
4. 指针作为访问数组的方式时, 需要**自行确定**访问区域是否合法, 访问越界的内存空间会造成不可预知的问题.

## 内联函数和函数的区别，内联函数的作用

1. 内联函数比普通函数多了关键字inline
2. 内联函数避免了**函数调用**的开销；普通函数有调用的开销
3. 普通函数在被调用的时候，需要寻址（函数入口地址）；内联函数不需要寻址。
4. 内联函数有一定的限制，内联函数体要求代码简单，不能包含复杂的结构控制语句；普通函数没有这个要求。

内联函数的作用：内联函数在调用时，是将调用表达式用内联函数体来替换(展开)。避免函数调用的开销。

## cpp有几种传值方式，之间的区别是什么？

传参方式有这三种：**值传递**、**引用传递**、**指针传递**
- 值传递：形参即使在函数体内值发生变化，也不会影响实参的值（**拷贝**）；

- 引用传递：形参在函数体内值发生变化，会影响实参的值；

- 指针传递：在指针指向没有发生改变的前提下，形参在函数体内值发生变化，会影响实参的值；

值传递用于对象时，整个对象会拷贝一个副本，这样效率低；而引用传递用于对象时，不发生拷贝行为，只是绑定对象，更高效；指针传递同理，但不如引用传递安全。

## c语言函数调用中参数入栈顺序

```c
#include <stdio.h>

void foo(int x, int y, int z)
{
        printf("x = %d at [%X]\n", x, &x);
        printf("y = %d at [%X]\n", y, &y);
        printf("z = %d at [%X]\n", z, &z);
}

int main(int argc, char *argv[])
{
    foo(100, 200, 300);
    return 0;
    
/* 输出
x = 100 at [61FF10]
y = 200 at [61FF14]
z = 300 at [61FF18]
*/
}
```

系统栈是向低地址方向生长的. 因此`z`在栈底, 而`x`在栈顶. 从而可以推断出参数的入栈顺序是**从右到左**. 一般c/cpp编译器都用`cdecl`函数调用约定: 函数参数按照从右向左的顺序入栈，函数调用者负责清除栈中的参数.

从右到左的原因是可以方便的**处理可变参数**的问题(如printf函数). 这样栈顶就是最左边的参数, 在编译器就可以确定函数的参数相对于栈顶的相对地址[reference](https://www.quora.com/Why-are-parameters-of-a-function-pushed-right-to-left-in-a-function-stack).

## 参考资料

[牛客网](https://www.nowcoder.com/tutorial/10069/07544e20b1de404caf88fdef78624daa)
[dian神](https://dianhsu.top/cplusplus/index.html)