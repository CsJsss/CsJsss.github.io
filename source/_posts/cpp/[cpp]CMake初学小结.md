---
title: '[cpp]CMake初学小结'
toc: true
date: 2022-07-29 23:37:23
updated:
categories:
tags:
---

最近项目中使用了CMake作为构建工具, 作为初学者, 简单总结一下所用到的知识. 并给出一个`Demo Project`覆盖这些知识, 本篇博客不对CMake知识进行总结, 只描述创建一个简单工程项目所需的一些知识. 

<!--more-->

## 简介

CMake是现代化的构建工具, 其具有跨平台的特性, 能够较好的组织构建工程项目. CMake工具包含了cmake、ctest和cpake. 其中cmake用于构建项目, ctest用于测试项目并报告测试结果.

### 官方文档

- [CMake](https://cmake.org/cmake/help/latest/)
- [CMake Tutorial](https://cmake.org/cmake/help/latest/guide/tutorial/index.html)

## 测试环境

- WSL2 
- Ubuntu
- g++ (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0

## Demo Project 结构

根据我目前的需求, 项目的结构长这样.

```bash
├── CMakeLists.txt
├── README.md
├── build           # 构建文件目录
├── include         # Code. 头文件
├── src             # Code. 源文件
├── targets         # 可执行文件
├── tests           # 单元测试文件. 使用 gtest
└── thirdparty      # 依赖的第三方文件
```

注意这里所需的第三方文件以源文件的形式包含了进来, 没有使用包管理工具或者安装到全局路径的做法.

## CMakeLists.txt

根据需求. 可将`CMakeLists.txt`分成以下子模块:

1. Basic: 包含全局基础相关的内容. 如 C++ 版本等.
2. 第三方库: 依赖的第三方库
3. 静态库: 项目中构建出来的静态库/动态库
4. targets: 项目构建出的目标文件(可单目标/也可多目标)
5. tests: 单元测试


### Basic

```cpp
cmake_minimum_required(VERSION 3.10)

project(CMakeDemoProject LANGUAGE CXX)


##### 01-Basic ######

# cpp 版本
SET(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# default build type : Debug
if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)
endif()

# 使得 include 和 src 之间能够平级 include
include_directories(${CMAKE_SOURCE_DIR})

# 生成 compile_commands.json
set(CMAKE_EXPORT_COMPILE_COMMANDS True)

# 跨平台使用 Threads 库
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)
```

### 第三方库

```bash
##### 02-第三方库 ######

# spdlog
add_subdirectory(thirdparty/spdlog)
include_directories(thirdparty/spdlog/include)

# gtest

add_subdirectory(thirdparty/googletest-release-1.12.1)
include_directories(thirdparty/googletest-release-1.12.1/googletest/include)
######################
```

### 静态库

```bash
# 查询所有在src中的 .h 和 .cpp文件
file(GLOB sources CMAKE_CONFIGURE_DEPENDS src/*.cpp include/*.hpp)

add_library(PROJECT_LIB STATIC ${sources})
# 静态库链接所需的库
target_link_libraries(PROJECT_LIB PUBLIC Threads::Threads)
######################
```

### Targets

```bash
##### 04-target ######

# 所有的 target 文件
# 这里获取路径的文件名. 比如输入是 /abc/xyz/test.cpp 则输出为: test
file(GLOB targets CMAKE_CONFIGURE_DEPENDS targets/*.cpp)
foreach(file ${targets})
    # split string in CMake
    # Link: https://stackoverflow.com/questions/5272781/what-is-common-way-to-split-string-into-list-with-cmake
    string(REPLACE "." ";" name_list ${file})
    list(GET name_list 0 prefix)
    string(REPLACE "/" ";" path_list ${prefix})
    list(GET path_list -1 current_file)

    add_executable(${current_file} ${file})
    target_link_libraries(${current_file} PROJECT_LIB)
endforeach()
######################
```

### Ctest

```bash
##### 05-ctest Related #######

enable_testing()
## 添加 test 三部曲:
# 1. add_executable(name source_file)
# 2. target_link_libraries(name gtest gtest_main 被测试模块(libaray))
# 3. add_test()

# 所有的测试文件
file(GLOB test_files CMAKE_CONFIGURE_DEPENDS tests/*.cpp)
foreach(test_file ${test_files})
    string(REPLACE "." ";" name_list ${test_file})
    list(GET name_list 0 test_prefix)
    string(REPLACE "/" ";" path_list ${test_prefix})
    list(GET path_list -1 current_test)

    add_executable(${current_test} ${test_file} ${source})
    target_link_libraries(${current_test} gtest gtest_main PROJECT_LIB)
    add_test(NAME ${current_test} COMMAND ${current_test})    
endforeach()
######################
```

## Results

![Result](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2022/7/Results.png)

## Debug / Build One Target

`Vscode`插件: `CMake`、 `CMake Tools`、`CMake Integration`、`CMake Language Support`

![Result](https://cdn.jsdelivr.net/gh/CsJsss/CsJsss.github.io@hexo/themes/icarus/source/img/2022/7/CMake.png)

## Github Repo

[Link](https://github.com/CsJsss/CMake-Demo-Project)

