# EE6129 学习站

NTU EE6129 Wireless & Mobile Radio Systems 的中文自学网页：零基础向的讲解长文（生活类比 + 逐步推导 + 带完整解题思路的例题），外加一个互动复习小程序（笔记、公式速查表、记忆卡片、自测题）。

| 文件 | 内容 |
|---|---|
| `index.html` | 入口目录 |
| `partA.html` | Part A 蜂窝移动通信系统（多址接入、1G–4G、频率复用、话务工程、切换…）— 讲解长文，共11章 |
| `partB.html` | Part B 无线系统（802.11 WLAN、自组网、无线传感器网络、LTE、物联网）— 讲解长文，共8章 |
| `partC.html` | Part C 卫星通信（GEO/MEO/LEO、链路性能、多址接入、路由与切换）— 讲解长文，共6章 |
| `app.html` | 互动复习小程序：32个知识点笔记、公式速查表、48张记忆卡片、36题自测，进度存在浏览器本地 |

静态 HTML，不依赖后端。公式用的衬线字体（Fraunces / Literata / IBM Plex Mono）从 Google Fonts 加载，首次打开需要联网；断网时会自动退回系统自带的中英文字体，内容和交互都不受影响。

## 在 Linux 上使用

```bash
git clone https://github.com/pdsky/EE6129-study.git
cd EE6129-study
xdg-open index.html
```

如果中文显示成方块，安装中文字体：

```bash
sudo apt install fonts-noto-cjk
```

以后有更新时：

```bash
git pull
```
