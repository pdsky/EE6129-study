# EE6129 学习站

NTU EE6129 Wireless & Mobile Radio Systems（Part 1 + Part 2）的中文自学网页：零基础向的讲解长文（生活类比 + 逐步推导 + 带完整解题思路的例题），外加一个互动复习小程序（笔记、公式速查表、记忆卡片、自测题）。

| 文件 | 内容 |
|---|---|
| `index.html` | 入口目录 |
| `partA.html` | Part A 蜂窝移动通信系统（多址接入、1G–4G、频率复用、话务工程、切换…）— 讲解长文，共11章，章末附历年真题 |
| `partB.html` | Part B 无线系统（802.11 WLAN、DCF/PCF、自组网、无线传感器网络、LTE、物联网）— 讲解长文，开篇 + 7 章，标讲义页码，带例题和真题 |
| `partC.html` | Part C 卫星通信（轨道与覆盖几何、GEO/MEO/LEO、链路损耗、容量分配、路由与切换）— 讲解长文，开篇 + 6 章，标讲义页码，带例题和真题 |
| `app.html` | 互动复习小程序：32个知识点笔记、公式速查表、48张记忆卡片、36题自测，进度存在浏览器本地 |
| `lab/` | 无线与移动网络实验室：16个模块，17个 Canvas 动画与示意图（频率复用网格、扇区化干扰、切换门限、CSMA/CA 时序、隐藏节点、LTE 资源网格、卫星轨道…），8个公式计算器（频谱效率、路径损耗、SIR、Erlang B/C、卫星几何…），59道自测题，63张记忆卡片。入口 `lab/index.html` |
| `examples.html` | 讲义例题手册：Part A 全部15道例题按页码整理，分步解法 + 记忆方法 + 易错点 + 公式复核，带自测模式和考前速记页 |
| `hw1.html` | HW1 讲解与中英文参考答案：逐问考点、框图、六边形几何图、同频干扰图，Erlang B / SIR 计算器 |
| `p2-learn.html` | Part 2（Ser Wee，第 7–13 周）讲解长文：概率复习、无线信道、信号检测、分集、MIMO、均衡、OFDM，带 4 个计算器（公式用 MathJax），章末附历年真题 |
| `p2-practice.html` | Practice 1–7 全部 21 题逐题详解与官方答案核对，12 种题型随机练习 |
| `exams.html` | 历年期末真题：2023-24 S2、2024-25 S2、2025-26 S1、2025-26 S2 四份卷 16 道大题，英文原题逐字转录 + 中文分步解答 + 出题规律；每题也插在对应讲解章节末尾 |
| `bc-practice.html` | Part B 无线系统 + Part C 卫星通信题库：62 道选择、计算、简答题，带随机小测 |

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

## 源文件（src/）

页面是用脚本从片段拼出来的，改内容请改 `src/` 里的源文件再重新生成：

| 目录 | 内容 |
|---|---|
| `src/p2build/` | Part 2 讲解（`learn_01–08.html`）、Practice 详解（`prac_1–7.html`）、Part B/C 讲解（`pb_*.html`、`pc_*.html`）的章节片段和构建脚本；`enrich_p2.py` 给第 3–7 章加星级和重点框；`rayleigh_svg.py`、`rician_svg.py`、`doppler_svg.py`、`gauss_svg.txt` 生成第 2、3 章的示意图 |
| `src/exams/` | 四份期末卷的题目与解答数据（`data_*.py`）、数值核对脚本 `verify.py`、生成 `exams.html` 并把真题插进各讲解页章末的 `build_exams.py` |
| `src/tools/` | Part A、HW1、例题手册当初改写时用过的一次性脚本 |

重新生成（在 `src/p2build/` 下）：

```bash
/usr/bin/python3 enrich_p2.py && /usr/bin/python3 build_learn.py && /usr/bin/python3 build_bc_learn.py && /usr/bin/python3 build_bc.py
```

`build_learn.py` 和 `build_bc_learn.py` 结束时会自动调用 `../exams/build_exams.py --inject`，把历年真题重新插回章末。脚本同时会往仓库外的 `EE6129_artifacts/` 写一份网页版副本，那个目录不在仓库里。
