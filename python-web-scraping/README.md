# Git, GitHub and Web Scraping Study
A personal study 
- origin
- simple


## 2024.10.28
- 使用多进程加速爬虫程序，默认为5进程
- 想要学习Xpath自动搜寻目录url的功能

## 2024.11.15
- 分离程序并重命名main与tools
- 创建广泛获取小说的策略类

## 2025.5.26
- 学习xpath与深入xml,进一步学习爬虫

## 2025.6.12
- 修复初始化tools中部分问题，修改部分类属性和方法

## 2025.7.1
- 分离ChapterUrlExtractor为独立类，创建最简单策略

## 2025.7.26
- 完成最简单策略框架

## 2025.7.27
- 建立url补全尝试，应对部分网页使用路由url的形式而非a标签中直接带有全部url
- 修改代码错误，更安全的获取信息和报错
- 重命名策略1为"strategy_first"

## 2025.8.1
- 获取url后6位模糊搜索，修复url初始就无法获取的问题

## 2025.8.4
### 学习urllib库常用用法:处理url并获取相关内容
- (f"scheme: {parsed.scheme}")      # https  !常用***
- (f"netloc: {parsed.netloc}")      # www.example.com:8080 !常用****
- (f"path: {parsed.path}")          # /path/to/page
- (f"params: {parsed.params}")      # (通常为空)
- (f"query: {parsed.query}")        # query=string附加
- (f"fragment: {parsed.fragment}")  # fragment
- (f"hostname: {parsed.hostname}")  # www.example.com
- (f"port: {parsed.port}")          # 8080

## 2025.9.5
- 学会了更规范的书写格式:表明了返回类型和输入类型
- 将策略类改为实例化类,对类的实例化还是直接调用类属性有了更加深刻的理解:反复运行还是要将类实例化避免上次属性残留问题
- 新增策略2：直接搜索最常用的盒子命名搜索,更换两个策略名称
- 分离get_meta与etree的获取，避免meta获取失败使得程序报错
### ~~发现策略1好像更好用,大多数免费网站其实都用一个框架~~
