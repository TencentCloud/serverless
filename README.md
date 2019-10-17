# Serverless

腾讯云 Severless 是腾讯云提供的安全稳定、管理简化、高效易用且低成本的无服务器产品平台。它通过多种 Serverless 产品组合，快速落地 Serverless 架构及应用，加速互联网和传统企业的业务迭代与升级，让您全面享受 Serverless 架构带来的弹性伸缩、秒级部署、按需付费、免运维等好处。 

#### [云函数 SCF](https://cloud.tencent.com/product/scf)

云函数（Serverless Cloud Function，SCF）是腾讯云为企业和开发者们提供的无服务器执行环境，帮助您在无需购买和管理服务器的情况下运行代码。您只需使用平台支持的语言编写核心代码并设置代码运行的条件，即可在腾讯云基础设施上弹性、安全地运行代码。SCF 是实时文件处理和数据处理等场景下理想的计算平台。

#### Serverless framework

Serverless framework 是无服务器应用框架和生态系统，允许开发者将资源编排、自动伸缩、事件驱动等功能部署上云。该框架旨在简化开发和部署腾讯云函数的工作，而无需管理底层基础架构，帮助开发者通过优秀的 Serverless 计算服务迅速地构建应用。

#### [TSF Serverless](https://cloud.tencent.com/document/product/649/13005)

TSF Serverless（Tencent Service Framework Serverless）是腾讯云面向应用和微服务的高性能 Serverless 平台，提供按需使用、按量计费、免运维的使用体验。支持南北向 Web 应用场景和东西向的 Spring Cloud 和 Service Mesh 微服务场景。

## 开始使用

#### 快速入门

您可通过如下示例进一步熟悉云函数的使用流程：

*   [基于控制台开发 Hello World Web 服务](https://cloud.tencent.com/document/product/583/37509)
*   [基于 CLI 开发 Hello World Web 服务](https://cloud.tencent.com/document/product/583/37510)（推荐）
*   [基于 VS Code 开发 Hello World Web 服务](https://cloud.tencent.com/document/product/583/37511)
*   [基于控制台创建基于 Node.js Web 框架（Express、Koa、Egg）的服务型云函数快速入门](https://cloud.tencent.com/document/product/583/37278)

#### 开发者工具

腾讯云 Serverless 团队提供了丰富的开发者工具帮助您使用云函数：

* [SCF CLI](https://github.com/TencentCloud/Serverless-cli)

> SCF CLI 是腾讯云函数产品的命令行工具。通过该命令行工具，您可以方便地实现函数打包、部署、本地调试，也可以方便地生成腾讯云函数的项目并基于 demo 项目进一步的开发。
SCF CLI 通过一个函数模板配置文件，完成函数及相关周边资源的描述，并基于配置文件实现本地代码及配置部署到云端的过程。

* [SCF VS Code 插件](https://cloud.tencent.com/document/product/583/38106)

> Tencent Serverless Toolkit for VS Code 是腾讯云函数产品的 VS Code（Visual Studio Code）IDE 的插件。该插件可以让您更好地在本地进行 Serverless 项目开发和代码调试，并且轻松将项目部署到云端。

* [Serverless-go-lib](https://github.com/TencentCloud/Serverless-go-lib)

> 用于云函数 SCF GO 环境的库及工具

* [Serverless-java-lib](https://github.com/TencentCloud/Serverless-java-lib)

> 用于云函数 SCF Java 环境的库及工具

#### 更多示例

- 查看[腾讯云函数 demo 库](https://github.com/TencentCloud/Serverless-examples)

## 系列文章

#### Serverless 技术专栏

- [Serverless 基本概念入门](https://zhuanlan.zhihu.com/p/78250791)
- [Serverless 的运行原理与组件架构](https://zhuanlan.zhihu.com/p/79214097)
- [Serverless 的开发者工具建设](https://zhuanlan.zhihu.com/p/81176864)
- [一图读懂无服务器云函数](https://cloud.tencent.com/developer/article/1450023)
- [下一代无服务器的发展形态：Serverless 2.0](https://cloud.tencent.com/developer/article/1454649)
- [Serverless - 前端 3.0 时代](https://cloud.tencent.com/developer/article/1513725)
- [前端学 Serverless - 性能调优](https://cloud.tencent.com/developer/article/1449785)
- [前端学 Serverless - 如何单枪匹马实现小程序页面级版本控制](https://cloud.tencent.com/developer/article/1449782)
- [前端学 Serverless - 从开发调试到部署运维，一套完整的 Serverless 项目经验分享](https://cloud.tencent.com/developer/article/1464383)
- [前端学 Serverless - WebApplication 迁移实践](https://cloud.tencent.com/developer/article/1481095)

#### Serverless 实践系列

- [Serverless 最佳实践：如何在两周内开发出用户量过亿的微信小程序](https://cloud.tencent.com/developer/article/1454651)
- [「实践」如何通过 Serverless 与自然语言处理，让搜索引擎“看”到你的博客](https://zhuanlan.zhihu.com/p/78336933)
- [「实践」为 Python 云函数打包依赖](https://zhuanlan.zhihu.com/p/82139273)
- [「实践」突破传统 OJ 瓶颈，“判题姬”接入云函数](https://zhuanlan.zhihu.com/p/82651235)
- [「实践」网站监控脚本的实现](https://zhuanlan.zhihu.com/p/83025871)
- [「实践」如何优雅地给搜索引擎去广告！](https://zhuanlan.zhihu.com/p/83222441)
- [「实践」云函数 + API，你也可以做个天气信息系统](https://zhuanlan.zhihu.com/p/83753850)
- [「实践」如何定制业务告警功能](https://zhuanlan.zhihu.com/p/84709306)
- [「实践」如何优雅地给网站图片加水印](https://zhuanlan.zhihu.com/p/85817369)
- [「实践」“灰常”简单的车牌识别 API 制作](https://zhuanlan.zhihu.com/p/86194163)
- [「实践」全新命令行工具帮你快速部署云函数](https://zhuanlan.zhihu.com/p/87146209)
- [云函数场景下的 DevOps 实践 - Jenkins 篇](https://cloud.tencent.com/developer/article/1461708)
- [云函数场景下的 DevOps 实践 - CODING 企业版](https://cloud.tencent.com/developer/article/1467480)
- [云函数场景下的 DevOps 实践 - 蓝盾](https://cloud.tencent.com/developer/article/1479998)
- [Serverless + puppeteer 打造云端自动化测试](https://cloud.tencent.com/developer/article/1478367)
- [云函数 + TypeScript + Node.js 最佳实践探索](https://cloud.tencent.com/developer/article/1483690)
- [基于 Node.js 的轻量级云函数功能实现](https://cloud.tencent.com/developer/article/1486296)

#### User stories

- [基于「树莓派 + 腾讯云」的在线甲醛监测系统](https://cloud.tencent.com/developer/article/1458238)
- [API 网关技术最佳实践](https://cloud.tencent.com/developer/article/1467516)
- [不花钱就可以给企业微信做个提醒机器人](https://cloud.tencent.com/developer/article/1472156)
- [使用云函数快速打造公众号自动回复机器人](https://cloud.tencent.com/developer/article/1496053)
- [经验小记 | 如何使用云函数 VS Code 插件来定位问题](https://cloud.tencent.com/developer/article/1498383)
- [效率提升 50%！基于 Serverless 的视频云运营系统改造实践（上）](https://cloud.tencent.com/developer/article/1504249)

#### Presentations

- [「2018 ArchSummit 全球架构师峰会」让业务感知不到服务器的存在 - 基于弹性计算的无服务器化实践](https://cloud.tencent.com/developer/article/1449789)
- [「K8S 云原生上海站」蓝鲸 DevOps 方案在游戏中的实现](https://cloud.tencent.com/developer/article/1449788)
- [「Hello Serverless」做 Serverless 开发，你需要掌握什么样的技能？](https://cloud.tencent.com/developer/article/1449786)
- [「Hello Serverless」从概念到实践，开发者如何更好地了解 Serverless](https://cloud.tencent.com/developer/article/1490971)
- [「KubeCon 2019」无服务逐渐开始承载起企业核心业务](https://cloud.tencent.com/developer/article/1454650)
- [「KubeCon 2019」腾讯云函数计算冷启动优化实践](https://cloud.tencent.com/developer/article/1461709)
- [「KubeCon 2019」腾讯云函数访问 VPC 网络架构优化](https://cloud.tencent.com/developer/article/1461707)

#### 发布平台

此处做归档，发布平台：
- [知乎](https://zhuanlan.zhihu.com/ServerlessGo)
- [掘金](https://juejin.im/user/5d70b6dae51d4561fb04bfb9/posts)
- [云＋社区](https://cloud.tencent.com/developer/user/1000057/articles)
- 微信公众号：ServerlessCloudNative
