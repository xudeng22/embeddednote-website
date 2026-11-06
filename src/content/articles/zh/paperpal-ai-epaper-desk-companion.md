---
title: 一只会动的电子纸 AI 桌宠，帮你记住、提醒、陪你完成每天最重要的事
description: '电子纸桌面提醒设备的产品概念、界面展示、设计权衡与尚待验证的问题，区分原型图片与实测结果。'
locale: zh
translationKey: paperpal-ai-epaper-desk-companion
pubDate: '2026-10-15'
category: display
tags:
- E-Paper
- AI
- Desk Companion
- Productivity
draft: false
seoTitle: 一只会动的电子纸 AI 桌宠，帮你记住、提醒、陪你完成每天最重要的事
seoDescription: '电子纸桌面提醒设备的产品概念、界面展示、设计权衡与尚待验证的问题，区分原型图片与实测结果。'
updatedDate: '2026-11-06'
---

待办事项记在手机里，不代表坐回工位时就会想起来。PaperPal 想解决的是这个很具体的问题：把最需要处理的一件事，留在桌面上一张持续可见的电子纸卡片上，而不是再增加一个手机通知。

这篇文章介绍的是**产品概念与交互界面**。以下图片来自项目展示资料，用来说明设备外观和应用交互；它们不等于已经完成的续航测试、量产验证或 AI 服务实测报告。

![PaperPal 桌面电子纸设备概念展示](/uploads/paperpal-ai-epaper-desk-companion/paperpal-ai-epaper-desk-companion-01.webp)

![PaperPal 设备概念图二](/uploads/paperpal-ai-epaper-desk-companion/paperpal-ai-epaper-desk-companion-02.webp)

![PaperPal 设备概念图三](/uploads/paperpal-ai-epaper-desk-companion/paperpal-ai-epaper-desk-companion-03.webp)

![PaperPal 设备概念图四](/uploads/paperpal-ai-epaper-desk-companion/paperpal-ai-epaper-desk-companion-04.webp)

## 为什么用电子纸显示一件事

桌面提醒器不一定需要不断更新的彩色动画。对“下一步做什么”这种低频变化的信息，电子纸在更新后可以保持画面，比较适合做常驻提示。不过，这只能解释选型思路，不能直接推导出具体待机电流、使用天数或刷新速度，仍然需要按面板和整机分别测试。

卡片内容最好控制在普通坐姿能看清的范围：一句简短标题、一条下一步动作，再加上截止时间或任务状态。字太多时，优先精简文字，不要无限缩小字号。若最终产品带动作机构，也应该让动作对应重要提醒，而不是一直摆动分散注意力。

## 应用界面展示了什么

项目资料说明有 iOS、Android 的中英文界面，支持语音录入，并展示了 Web 端。需要区分**功能描述**和**已验证的发布能力**：截图本身不能证明各个平台的功能完全一致，也不能证明后台提醒在断网、切后台或设备重启后都可靠。

![PaperPal 英文应用界面示例一](/uploads/paperpal-ai-epaper-desk-companion/paperpal-ai-epaper-desk-companion-05.webp)

![PaperPal 英文应用界面示例二](/uploads/paperpal-ai-epaper-desk-companion/paperpal-ai-epaper-desk-companion-06.webp)

![PaperPal 英文应用界面示例三](/uploads/paperpal-ai-epaper-desk-companion/paperpal-ai-epaper-desk-companion-07.webp)

![PaperPal 英文应用界面示例四](/uploads/paperpal-ai-epaper-desk-companion/paperpal-ai-epaper-desk-companion-08.webp)

![PaperPal Web 界面示例](/uploads/paperpal-ai-epaper-desk-companion/paperpal-ai-epaper-desk-companion-09.webp)

## 量产前更值得做的六项验证

1. **屏幕数据格式。** 记录实际分辨率、颜色索引、旋转方向、行步长及支持的刷新模式，先验证黑白文字与边框是否完整。
2. **任务状态同步。** 手机改了任务、标记完成或删除后，设备端如何同步？连接中断时保留什么状态？
3. **文件传输完整性。** 是否有总长度、分包序号及接收端校验？手机端回调成功不代表屏幕图片已经完整保存。
4. **提醒可靠性。** 时区变化、免打扰、重复提醒、断电恢复和用户确认，分别要有可复现的测试用例。
5. **功耗拆分。** 待机、无线收发、图像刷新和机械动作需要分别测量，不能简单拿屏幕“保持画面不耗电”代替整机续航数据。
6. **隐私与语音。** 需要说明语音在本地还是云端处理、是否保存原始录音，以及用户如何删除数据。

如果先验证显示与通信链路，可以用站内的 [E-Paper Image Converter](/zh/tools/epaper-image-converter/) 检查图像编码，用 [BLE Transfer Planner](/zh/tools/ble-throughput-calculator/) 推算理论传输预算；两者都不代表这台产品已经完成硬件实测。

## 当前资料的边界

本文没有可公开复核的刷新时间、无线吞吐、整机续航与提醒成功率测试结果，因此不写具体性能承诺。真正值得继续验证的是：用户坐回工位时，这张电子纸能否稳定、清晰、及时地显示他下一步该做的事。

<!-- editorial-v3-20261106 -->
