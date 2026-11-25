[A.1 网络环境、AI 开发工具、Linux 与 Git 配置.md](https://github.com/user-attachments/files/35392397/A.1.AI.Linux.Git.md)
# A\.1 网络环境、AI 开发工具、Linux 与 Git 配置

# A1 基础环境与 AI 工具 实训报告

|姓名|高怡彤|
|---|---|
|仓库|[https://github\.com/yig51502\-ops/zhize\-training\-2026](https://github.com/yig51502-ops/zhize-training-2026%E3%80%91)|
|本节目录 |`A1_Base_and_AI_Tool/`|
|完成日期 |2026\-11\-25|

## 环境与完成情况

|项目|实际情况|
|---|---|
|宿主机|Windows 11（64 位操作系统, 基于 x64 的处理器）|
|Linux 环境|VMware＋Ubuntu 26\.04\.1|
|网络代理|Clash Verge Rev，TUN 模式 \+ 系统代理|
|AI 开发工具|VS Code \+ Cline，接入 DeepSeek API|
|Python |3\.12，由 `uv venv` 创建的 `.venv` 隔离|
|版本控制 |Git \+ GitHub CLI（`gh auth setup-git`）|

## 宿主机网络配置与账号准备

### 2\.1 配置过程

Clash Verge 启动后先确认节点可用，再在设置中开启系统代理，然后用浏览器直接验证：

```Plain Text

https://github.com → 正常打开

https://www.google.com → 正常打开
```

浏览器能访问，说明宿主机的浏览器流量已经走通代理。但这一步必须理解**系统代理与 TUN 模式的差别**，

因为它直接决定了后面 Linux 终端能不能联网。

### 2\.2 系统代理与 TUN 模式

- **系统代理**：只写入系统代理设置（或 `HTTP_PROXY` / `HTTPS_PROXY` 环境变量），只有主动读取这些配置的程序才会走代理。

浏览器通常会读取，所以「浏览器能上 GitHub」不能推出「终端里的 `curl`、`git`、`pip` 也能上。

- **TUN 模式**：在虚拟网卡层接管流量，程序无需知道代理存在，因此不读取代理配置的命令行工具也能被带出去。

代价是需要管理员权限，且可能影响局域网访问。

### 2\.3 账号与密钥

GitHub 账号注册后开启两步验证；DeepSeek 开放平台申请 API Key。密钥只填进 Cline 的配置，

**不写入仓库、不出现在截图中**；需要时通过环境变量传入：

```Bash
export DEEPSEEK_API_KEY="sk-***" # 仅当前 shell 生效，不落盘到仓库
```

## AI 开发工具先行接入

### 3\.1 接入步骤

1. 在 VS Code 扩展市场安装 Cline；

2. API Provider 选择 `OpenAI Compatible`，填入 DeepSeek 的 Base URL（`https://api.deepseek.com/v1`）、API Key 与模型名；

### 3\.2 工作机制

网页对话 AI 的输出只有文字；Cline 的输出中可以包含**工具调用**：读文件、写文件、执行终端命令。

工具在本机真实执行，返回结果（文件内容、stdout、退出码）回填给模型，模型据此决定下一步。

## Linux 环境搭建与终端网络打通

### 4\.1 方案选型

|方案|优点|代价|适合阶段|
|---|---|---|---|
|WSL2|启动快、与 Windows 文件互通、资源占用低|内核由微软维护，与原生 Ubuntu 有细微差异；硬件直通较弱|入门与日常开发（本次选择）|
|虚拟机|环境完全隔离，可快照回滚|内存占用高、与宿主机传文件麻烦、GPU 加速弱|需要干净复现的实验|
|Ubuntu 双系统|最接近真实机器人开发环境，驱动与实时性最好|分区有风险、切换系统麻烦|后续 ROS 2 大型仿真与实机联调|

本次选择 虚拟机：现阶段主要写 Python 脚本、跑 Git，与 Windows 的文件互通更重要；后续做 ROS 2 仿真再考虑双系统。

### 4\.2 终端联网

**Windows 中打开 Clash Verge**

确认节点已连接、允许局域网连接（Allow LAN）已开启，混合端口为 `7897`。

**在 Ubuntu 普通终端逐行执行**

若还在 OpenCode 中，先输入 `/exit` 退出。

```Plain Text
export http_proxy=http://192.168.84.1:7897
export https_proxy="$http_proxy"
curl -I --connect-timeout 5 --max-time 15 https://github.com
```

### 4\.3 验证与判断

```Bash
curl -I https://github.com

# HTTP/2 200env | grep -i proxy

curl -v https://github.com 2>&1 | grep -i -E 'proxy|connected'
```

**`HTTP/2 200`**** 只证明请求成功，不能证明走了代理。** 判断直连还是代理，要看环境变量与 `curl -v` 中的连接目标。

## Linux 基础操作与 Python 虚拟环境

### 5\.1 常用命令的分级

- 必须熟练：`cd`、`ls -la`、`pwd`、`mkdir -p`、`rm -rf`（谨慎）、`cp` / `mv`、`cat` / `less`、`grep -r`、`ps aux`、`kill`、`df -h`、`du -sh`；

- 理解含义：`chmod` / `chown` 的 `rwx` 表示法（如 `755`、`644`）。注意目录的 `x` 表示「能否进入」，`r` 表示「能否列出内容」，与文件的含义不同；

- 用到再查：`systemctl`、APT 源配置、软链接。

### 5\.2 创建并使用虚拟环境

```Bash

uv venv .venv

source .venv/bin/activate

which python # .../A1_Base_and_AI_Tool/.venv/bin/python

python -V

uv pip install requests

deactivate
```

### 5\.3 为什么必须隔离

1. 不同项目依赖的版本会冲突，装进系统 Python 会造成全局污染；

2. 有 `pyproject.toml` / `uv.lock` 之后，他人可以复现同样的环境；

3. 环境目录可整体删除重建，不会破坏系统。

### 5\.4 「找不到 python」的真实原因

在终端执行 `python` 报 `command not found`，第一反应是「没装 Python」。实际上 Ubuntu 的系统解释器名为 `python3`，

`python` 这个名字本就不存在。激活 `.venv` 后能运行，是因为激活脚本把 `.venv/bin` **插入 ****`PATH`**** 最前面**，

终端按顺序查找时优先命中 `.venv/bin/python`。

因此准确的说法是：**不是「装了 Python 才能运行」，而是「命令查找顺序改变，****`python`**** 现在指向虚拟环境中的解释器」**。

这也解释了 `deactivate` 之后为何又找不到 `python`——查找顺序恢复了。

实操细节：若激活前执行过 `python` 并失败，bash 可能缓存了查找结果，激活后仍报错，执行 `hash -r` 清除缓存即可。

## Git 协作规范与脚本闭环

### 6\.1 身份与认证

```Bash
git config --global user.name "yig51502-ops"
git config --global user.email "yig51502@gmail.com"

gh auth login # GitHub.com → HTTPS → 浏览器授权

gh auth setup-git # 为 git 配置 credential helpergit push -u origin main # 推送成功才算认证真正可用
```

`gh auth setup-git` 的作用是为 Git 配置 **credential helper**：`git` 需要凭据时向 `gh` 请求，`gh` 用已登录的 token 应答，

因此无需在终端明文保存 token。注意 `gh auth status` 显示已登录**不等于**对目标仓库有写权限；

只有一次成功的 `push` 能同时验证三件事：认证有效、远程地址正确、账号具备写权限。

### 6\.2 四个区域

|区域|是什么|如何进入|
|---|---|---|
|工作区|磁盘上正在编辑的文件|检出后直接修改|
|暂存区（`.git/index`）|下一次提交的清单|`git add`|
|本地仓库（`.git/objects` \+ refs）|不可变的提交历史，`HEAD` 只是指针|`git commit`|
|远程仓库 |另一台机器上的裸仓库（`origin`）|`git push`|

```Bash
git diff # 工作区 vs 暂存区git diff --cached # 暂存区 vs HEADgit push -u origin main
```

两个容易混淆的点：

- **`commit`**** ≠ ****`push`**：提交只写入本地 `.git`，此时远程仓库没有任何变化；

- **`git add`**** 保存的是当时的内容**：之后继续修改文件不会自动进入暂存区，同一文件可以同时存在三种状态。

### 6\.3 `.gitignore`

```Plain Text

.venv/

__pycache__/

*.py[cod]

.pytest_cache/

.DS_Store
```

`.gitignore` 并不会让文件消失，它的作用是让 Git 在**枚举未跟踪文件**时（`status`、`add`、`clean`）按规则跳过。

`.venv/` 结尾的 `/` 表示只匹配目录，开头没有 `/` 表示任意层级均匹配；命中目录后 Git 直接剪枝，不再遍历 `site-packages`，

因此一行即可覆盖上万个文件。

排查某个文件为何被忽略：

```Bash
git check-ignore -v .venv/bin/python

# .gitignore:1:.venv/ .venv/bin/python
```

**规则只对未跟踪文件生效。** 我专门做了验证：用 `git add -f` 把 `.venv` 中的一个文件强制加入并提交，之后修改它，

`git status` 仍显示 modified，`git check-ignore` 返回 1（未匹配）。因为索引中已有记录，Git 只比较内容，不会查询 `.gitignore`。

补救方式：

```Bash
git rm -r --cached .venv

git commit -m "chore: 不再跟踪虚拟环境"
```

`--cached` 不能省略，否则会连同本地环境一起删除。同时应明确：该操作**不会清除历史提交中的 blob**；

若已推送到远程，彻底清理需要重写历史，属于影响所有协作者的操作，不可随意执行。

### 6\.4 脚本与提交

`src/count_files.py` 的功能：统计指定目录的文件数量与总行数，按扩展名分组并输出前 N 名。核心是带剪枝的遍历：

```Python
for root, dirs, files in os.walk(target):# 必须原地修改 dirs 才能阻止继续下钻；写成 dirs = [...] 无效

dirs[:] = [d for d in dirs if d not in {".git", ".venv", "__pycache__", "node_modules"}]for name in files:

path = Path(root) / name

...
```

**此处踩的坑**：不剪枝时 `os.walk` 会进入 `.venv` 的 `site-packages`，把几万个第三方库文件统计进来，结果既慢又失真。

修正即上面两行；注意必须用切片赋值 `dirs[:]`，直接给 `dirs` 重新赋值只是替换了局部变量。

提交遵循「一件事一个提交」：

```Plain Text

feat: 添加文件统计脚本与命令行参数

fix: 遍历时剪枝虚拟环境与缓存目录

docs: 补充 README 运行说明

chore: 添加 .gitignore 忽略虚拟环境
```

## 问题与处理记录

|现象|真实原因|处理方式|
|---|---|---|
|`python: command not found`<br>|系统只有 `python3`，且未激活虚拟环境|`source .venv/bin/activate`；理解为 PATH 顺序变化 |
|`.venv 出现在 git status 中`|先 `add` 后写 `.gitignore`，或规则写错|`git check-ignore -v` 查规则；已跟踪的用 `git rm -r --cached`|
|Cline 试用时多出临时测试文件|工具按指令新建文件，未及时清理 |`rm` 后重新执行 `git status` 确认工作区干净|

## 思考与总结

### 8\.1 两类 AI 工具的差异

**文件访问。** 网页对话中，AI 只能看到我粘贴的片段：大文件被截断、跨文件关系丢失、仓库结构完全不可见，

因此建议常出现「局部正确、整体跑不通」。Cline 这类工具在当前工作区与授权范围内直接列目录、读文件、写文件，

看到的是真实仓库结构与真实内容。但也应清楚：它看到的是**某一时刻的快照**，且**只能访问被授权的范围**，并非整台电脑。

**命令执行。** 网页对话给出的是命令文本，由我复制、执行，再把报错贴回——中间每一步都可能失真，

例如漏掉 stderr、只贴了最后一行。Cline 直接在终端执行，能拿到 stdout、stderr 与退出码，形成「改—跑—看」闭环，

因此可以自行发现参数错误、路径不存在并修正。代价是副作用真实存在：删除文件、改写 git 历史、安装全局依赖、发起网络请求，均立即生效。

**开发流程。** 网页对话的产物是**建议**，串接流程、执行与验证都在人这一侧；本地工具的产物是**已经发生的事实**，

编排由它完成，人转为验收方。责任也随之转移：网页对话出错最多是代码贴错，本地工具出错则磁盘上已经发生改动。

因此工具越强，抽查要越具体——看 `git diff` 而不是听它复述，看完事后的 `git status` 而不是相信「已删除」。

### 8\.2个人体会

本次最大的收获不是记住几条命令，而是学会用证据判断环境状态：网络是否通畅看 `curl` 的真实响应与代理变量；

认证是否有权限看一次成功的 `push`；`python` 指向谁看 `which python`；忽略规则是否生效看 `git check-ignore -v`。

AI 工具让这些验证变得廉价（它可以自己执行、自己查看输出），同时也让错误操作变得廉价。

因此流程应为：**先小范围试验，再确认结果，最后才扩大范围**；不可逆操作始终由人决定。

另一体会是：AI 给出的结论必须落到一条可验证的命令上才算数。它说「应该是代理没生效」，就去执行 `env | grep -i proxy`；

它说「文件已删除」，就再执行一次 `git status` 确认。

## 附录 A 常用命令速查

|用途|命令|
|---|---|
|创建并激活虚拟环境|`uv venv .venv` \&\& `source .venv/bin/activate`|
|查看当前解释器|`which python`|
|退出虚拟环境|`deactivate`（必要时 `hash -r` 清缓存）|
|终端连通性验证|`curl -I ``https://github.com`|
|GitHub 认证|`gh auth login` \&\& `gh auth setup-git`|
|查看暂存区内容 |`git ls-files --stage`|
|比较工作区与暂存区|`git diff`|
|比较暂存区与 HEAD|`git diff --cached`|
|查看被忽略的文件|`git status --ignored` |
|查询忽略规则来源|`git check-ignore -v <路径>`|
|取消跟踪但保留文件 |`git rm -r --cached <路径>`|
|推送并设置上游分支 |`git push -u origin main`|



