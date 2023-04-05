---
title: Spdlog日志库快速上手
toc: true
date: 2023-04-05 16:44:48
updated:
categories: cpp
tags:
    - cpp
    - Spdlog
---

简单介绍Spdlog日志库的安装与使用.

<!--more-->

## 简介


> Very fast, header-only/compiled, C++ logging library.

[Spdlog](https://github.com/gabime/spdlog)是非常快的`c++`日志库。支持编译后链接使用以及仅仅使用头文件，即快速可集成进项目。

## 下载与使用

[GitHub - gabime/spdlog: Fast C++ logging library.](https://github.com/gabime/spdlog)

### Header only version

拷贝`include`路径下的文件到项目中，注意要使用`c++11`.

### 编译

```bash
$ git clone https://github.com/gabime/spdlog.git
$ cd spdlog
$ cmake -B build
$ cmake --build build
```

### CMake中使用spdlog

#### 方法一

`spdlog`路径任意

```cmake
# include spdlog 
include_directories(/path/to/your/spdlog/include/)

# target link library
target_link_libraries(target /path/to/your/spdlog/build/libspdlog.a)
```

#### 方法二

`spdlog`在当前项目的`thirdpatry`文件夹下

```cmake
# 使用了相对路径
add_subdirectory(thirdparty/spdlog)
include_directories(thirdparty/spdlog/include)
```

#### 方法三

- 首先安装spdlog到全局路径如: `/usr/local/include`
    ```bash
    $ git clone https://github.com/gabime/spdlog.git
    $ cd spdlog
    $ cmake -B build
    $ cmake --build build
    $ cd build
    $ sudo cmake --install . --config Debug
    ```
- 然后在项目里直接使用即可

## Spdlog日志库的特性

### 支持多线程

可以创建线程安全的logger, 如:

```cpp
    auto logger = spdlog::basic_logger_mt(...);
```

以`_mt`结尾意味着`multi thread`。以`_st`结尾意味着`single thread`, 如：

```cpp
    auto logger = spdlog::basic_logger_st(...);
```

### 自定义日志格式以及等级

[官方文档连接](https://github.com/gabime/spdlog/wiki/3.-Custom-formatting)

```cpp
    // 日志等级
    spdlog::level::level_enum level = spdlog::level::level_enum::debug
    logger->set_level(level);
    // 日志格式
    logger->set_pattern("[%D %H:%M:%S.%f] [thread %t] [%l] %v");
```

### fmt格式的输出

[Format String Syntax ‒ fmt 9.1.0 documentation](https://fmt.dev/latest/syntax.html)

```cpp
std::string str = "abc";
spdlog::info("str = {}, size = {}", str, str.size());
```

还支持用户自定义数据结构的fmt输出. [文档连接](https://github.com/gabime/spdlog#user-defined-types)


### 多种logger类型

有控制台、文件、异步等logger，详情见：https://github.com/gabime/spdlog/wiki/2.-Creating-loggers


### 自定义刷新

支持手动刷盘以及定时刷盘，详情见：https://github.com/gabime/spdlog/wiki/7.-Flush-policy

### 替换默认的logger

- 默认的logger输出到控制台，支持替换默认的logger.
- `spdlog::info`和`spdlog::debug`等会使用默认的logger.

```cpp
spdlog::set_default_logger(some_other_logger);
spdlog::info("Use the new default logger");
```