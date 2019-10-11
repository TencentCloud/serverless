# serverless

SCF CLI 是腾讯云无服务器云函数 SCF（Serverless Cloud Function）产品的命令行工具。通过 SCF 命令行工具，您可以方便地实现函数打包、部署、本地调试，也可以方便地生成云函数的项目并基于 demo 项目进一步的开发。

SCF CLI 通过一个函数模板配置文件，完成函数及相关周边资源的描述，并基于配置文件实现本地代码及配置部署到云端的过程。

目前 SCF CLI 以开源形式发布，您可以在本项目中查看命令行源代码及更多帮助文档，并可以通过项目 issue 反馈问题。

## 功能特性

通过 SCF 命令行工具，您可以：

*   快速初始化云函数项目
*   在本地开发及测试你的云函数代码
*   使用模拟的 COS、CMQ、Ckafka、API 网关等触发器事件来触发函数运行
*   验证 TCSAM 模板配置文件
*   打包、上传函数代码、创建函数及更新函数配置
*   获取函数列表，删除指定函数

## 运行环境

SCF CLI 可以在 Windows、Linux、macOS 上运行。SCF CLI 基于 Python 开发完成，因此在安装及运行前需要系统中安装有 Python 环境，更多详细信息可参见 [安装与配置](https://cloud.tencent.com/document/product/583/33449)。

## 快速入门

您可以前往腾讯云官网查看 [SCF 快速入门](https://cloud.tencent.com/document/product/583/33446)

## 使用指导

*   [安装与配置](https://cloud.tencent.com/document/product/583/33449)
*   [初始化示例项目](https://cloud.tencent.com/document/product/583/33450)
*   [打包部署](https://cloud.tencent.com/document/product/583/33451)
*   [日志查看](https://cloud.tencent.com/document/product/583/36352)
*   [本地调试 (native invoke)](https://cloud.tencent.com/document/product/583/35402)
*   [本地调试 (local invoke)](https://cloud.tencent.com/document/product/583/35401)
*   [测试模板](https://cloud.tencent.com/document/product/583/33453)
*   [模板文件](https://cloud.tencent.com/document/product/583/33454)
*   [TCSAM 说明](https://cloud.tencent.com/document/product/583/36198)
*   [更新日志](https://cloud.tencent.com/document/product/583/36908)
*   [常见问题 FAQ](https://cloud.tencent.com/document/product/583/33456)

## 系列文章 - 玩转 Serverless 

### Serverless 技术专栏

- [Serverless 基本概念入门](https://zhuanlan.zhihu.com/p/78250791)
- [Serverless 的运行原理与组件架构](https://zhuanlan.zhihu.com/p/79214097)
- [Serverless 的开发者工具建设](https://zhuanlan.zhihu.com/p/81176864)
- [一图读懂无服务器云函数](https://cloud.tencent.com/developer/article/1450023)
- [下一代无服务器的发展形态：Serverless 2.0](https://cloud.tencent.com/developer/article/1454649)
- [Serverless - 前端 3.0时代](https://cloud.tencent.com/developer/article/1513725)
- [前端学 Serverless - 性能调优](https://cloud.tencent.com/developer/article/1449785)
- [前端学 Serverless - 如何单枪匹马实现小程序页面级版本控制](https://cloud.tencent.com/developer/article/1449782)
- [前端学 Serverless - 从开发调试到部署运维，一套完整的 Serverless 项目经验分享](https://cloud.tencent.com/developer/article/1464383)
- [前端学 Serverless - WebApplication 迁移实践](https://cloud.tencent.com/developer/article/1481095)

### Serverless 实践系列

- [Serverless 最佳实践：如何在两周内开发出用户量过亿的微信小程序](https://cloud.tencent.com/developer/article/1454651)
- [「实践」如何通过 Serverless 与自然语言处理，让搜索引擎“看”到你的博客](https://zhuanlan.zhihu.com/p/78336933)
- [「实践」为 Python 云函数打包依赖](https://zhuanlan.zhihu.com/p/82139273)
- [「实践」突破传统 OJ 瓶颈，“判题姬”接入云函数](https://zhuanlan.zhihu.com/p/82651235)
- [「实践」网站监控脚本的实现](https://zhuanlan.zhihu.com/p/83025871)
- [「实践」如何优雅地给搜索引擎去广告！](https://zhuanlan.zhihu.com/p/83222441)
- [「实践」云函数 + API，你也可以做个天气信息系统](https://zhuanlan.zhihu.com/p/83753850)
- [「实践」如何定制业务告警功能](https://zhuanlan.zhihu.com/p/84709306)
- [「实践」如何优雅地给网站图片加水印](https://zhuanlan.zhihu.com/p/85817369)
- [「实践」“灰常”简单的车牌识别 API 制作](https://cloud.tencent.com/developer/article/1508505)
- [「实践」全新命令行工具帮你快速部署云函数](https://cloud.tencent.com/developer/article/1509106)
- [云函数场景下的 DevOps 实践 - Jenkins 篇](https://cloud.tencent.com/developer/article/1461708)
- [云函数场景下的 DevOps 实践 - CODING 企业版](https://cloud.tencent.com/developer/article/1467480)
- [云函数场景下的 DevOps 实践 - 蓝盾](https://cloud.tencent.com/developer/article/1479998)
- [Serverless + puppeteer 打造云端自动化测试](https://cloud.tencent.com/developer/article/1478367)
- [云函数 + TypeScript + Node.js 最佳实践探索](https://cloud.tencent.com/developer/article/1483690)
- [基于 Node.js 的轻量级云函数功能实现](https://cloud.tencent.com/developer/article/1486296)

### User stories

- [基于「树莓派 + 腾讯云」的在线甲醛监测系统](https://cloud.tencent.com/developer/article/1458238)
- [API 网关技术最佳实践](https://cloud.tencent.com/developer/article/1467516)
- [不花钱就可以给企业微信做个提醒机器人](https://cloud.tencent.com/developer/article/1472156)
- [使用云函数快速打造公众号自动回复机器人](https://cloud.tencent.com/developer/article/1496053)
- [经验小记 | 如何使用云函数 VS Code 插件来定位问题](https://cloud.tencent.com/developer/article/1498383)
- [效率提升 50%！基于 Serverless 的视频云运营系统改造实践（上）](https://cloud.tencent.com/developer/article/1504249)

### Presentations

- [「2018 ArchSummit 全球架构师峰会」让业务感知不到服务器的存在 - 基于弹性计算的无服务器化实践](https://cloud.tencent.com/developer/article/1449789)
- [「K8S 云原生上海站」蓝鲸 DevOps 方案在游戏中的实现](https://cloud.tencent.com/developer/article/1449788)
- [「Hello Serverless」做 Serverless 开发，你需要掌握什么样的技能？](https://cloud.tencent.com/developer/article/1449786)
- [「Hello Serverless」从概念到实践，开发者如何更好地了解 Serverless](https://cloud.tencent.com/developer/article/1490971)
- [「KubeCon 2019」无服务逐渐开始承载起企业核心业务](https://cloud.tencent.com/developer/article/1454650)
- [「KubeCon 2019」腾讯云函数计算冷启动优化实践](https://cloud.tencent.com/developer/article/1461709)
- [「KubeCon 2019」腾讯云函数访问 VPC 网络架构优化](https://cloud.tencent.com/developer/article/1461707)

### 发布平台

此处做归档，发布平台：
- [知乎](https://zhuanlan.zhihu.com/ServerlessGo)
- [掘金](https://juejin.im/user/5d70b6dae51d4561fb04bfb9/posts)
- [云＋社区](https://cloud.tencent.com/developer/user/1000057/articles)
- 微信公众号：ServerlessCloudNative
