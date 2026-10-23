# 守民通识 · 搜索引擎收录提交指南

> 目标：让别人搜索「守民通识」能找到站点。
> 规范域名（canonical）：<https://shoumingeneralist.pages.dev>
> 备用域名：<https://shoumingeneralist.github.io>

---

## 〇、两个域名怎么分工

```
https://shoumingeneralist.pages.dev   ← 规范域名，对外宣传、提交给搜索引擎、被收录
https://shoumingeneralist.github.io   ← 备用入口，同一份内容，正常可访问
```

两份代码完全一样（同一个仓库、同一条流水线构建部署），区别只在
`astro.config.mjs` 里的 `site` 字段写的是 pages.dev。Astro 会据此在**两个域名的
每一个页面**上都生成：

```html
<link rel="canonical" href="https://shoumingeneralist.pages.dev/...">
```

这一行告诉搜索引擎「不管你从哪个域名抓到这份内容，主版本都在 pages.dev」，
从而避免重复内容、把「守民通识」的排名权重集中到一个域名上。

> **为什么这里没有做 301？**
> GitHub Pages 不支持服务端重定向——它既没有 `.htaccess` 之类的配置，
> 也不认 `_redirects` 文件（那是 Cloudflare Pages 的私有特性）。
> 之前 pages.dev → github.io 能做 301，是因为重定向发生在 Cloudflare 那一侧；
> 现在方向反过来，要由 GitHub Pages 发起，它做不到。
>
> 硬要做只能靠 JS 或 `<meta http-equiv="refresh">`，但那样
> **备用域名就不再是备用**：一旦 pages.dev 挂了，用户访问 github.io
> 反而被弹到一个打不开的地址。所以这里保留两个入口都能正常访问，
> 仅靠 canonical 去重。如果你更在意「搜索结果里绝对只出现一个域名」，
> 告诉我，我换成 meta refresh 方案。

---

## 一、已经自动完成的部分

| 项目 | 状态 |
| --- | --- |
| `robots.txt` | 原先返回 404，已补齐并声明规范域名站点地图 |
| IndexNow 密钥文件 | 已放在站点根目录并通过 Bing 校验 |
| 全站 URL 推送 | 7 个页面已推送，6 个端点全部返回成功 |
| 重复内容处理 | 全站 canonical 统一指向 pages.dev |
| 结构化数据 | 已注入 WebSite / Organization JSON-LD |
| 站点描述 | 精简到 155 字符内，品牌名前置 |
| 持续推送 | CI 里加了 indexnow job，以后推 master 自动推送 |

**已覆盖的搜索引擎**（通过 IndexNow，提交一次全共享）：

- Bing（同时供给 ChatGPT Search、Microsoft Copilot、DuckDuckGo、Yahoo）
- Yandex、Naver、Seznam、Yep

---

## 二、需要你本人登录完成的部分

Google 和百度都不支持 IndexNow，必须到各自站长平台验证所有权后提交站点地图。
这一步我无法代劳（涉及你的账号登录），但流程很短，每个平台 3～5 分钟。

### 通用站点地图地址

```
https://shoumingeneralist.pages.dev/sitemap-index.xml
```

### 1. Google Search Console（必做）

1. 打开 <https://search.google.com/search-console>
2. 「添加资源」→ 网址前缀 → 填 `https://shoumingeneralist.pages.dev`
3. 所有权验证：推荐 **HTML 文件** 方式
   - 下载它给的 `googleXXXXXXXX.html`
   - 放进仓库的 `public/` 目录
   - 推送后回到平台点「验证」
   - 也可以直接在 GitHub 网页端 `public` → `Add file` → `Upload files` 上传，不用命令行
4. 验证通过后：左侧「站点地图」→ 填入上面的地址 → 提交
5. 加速首页收录：顶部搜索框输入首页 URL → 「请求编入索引」

> 这一步最关键。Google 收录后，「守民通识」在海外和多数 AI 搜索里就能搜到了。

### 2. 百度搜索资源平台（国内流量，必做）

1. 打开 <https://ziyuan.baidu.com/>
2. 注册/登录 → 「添加网站」→ 填 `https://shoumingeneralist.pages.dev`
3. 验证站点：文件验证（把 `baidu_verify_xxx.html` 放进 `public/`）或 HTML 标签验证
4. 验证通过后两条路都走一遍：
   - **站点地图**：资源提交 → 普通收录 → Sitemap 提交 → 填上面的地址
   - **API 推送**（更快）：资源提交 → 普通收录 → API 提交 → 复制你的 token
5. 拿到 token 后，推送全部页面：

   ```bash
   python scripts/submit-indexnow.py --baidu-token 你的token
   ```

### 3. 360 搜索站长平台（推荐）

打开 <https://zhanzhang.so.com/> → 注册 → 添加网站 → 文件验证 → 数据提交 → Sitemap

### 4. 头条搜索站长平台（字节系）

打开 <https://zhanzhang.toutiao.com/> → 注册 → 添加站点 → 验证 → 数据提交 → 站点地图

### 5. 神马搜索（UC / 移动端）

打开 <https://zhanzhang.sm.cn/> → 注册 → 添加网站 → 验证 → 提交 sitemap

### 6. 搜狗 —— 可以跳过

搜狗已逐步整合进腾讯体系，站长工具基本停用，不建议再投入时间。

---

## 三、验证文件怎么放

各平台验证所有权时会给你一个 `xxx.html`，例如：

```
google1234567890abcdef.html
baidu_verify_abcdefg.html
so.com_verify_xxx.html
```

**放到仓库的 `public/` 目录**，推送后即可通过
`https://shoumingeneralist.pages.dev/google1234567890abcdef.html` 访问。

最简单的方式：打开 <https://github.com/shoumingeneralist/shoumingeneralist.github.io>，
进入 `public` 目录 → `Add file` → `Upload files` → 拖进去 → Commit。

---

## 四、以后发新文章怎么办

什么都不用做。推到 master 后 CI 会自动构建、部署、并把新的 sitemap 推送给
所有 IndexNow 搜索引擎。

想手动立刻推一次：

```bash
python scripts/submit-indexnow.py
```

只推某几篇：

```bash
python scripts/submit-indexnow.py https://shoumingeneralist.pages.dev/thought/start/
```

> 注意：IndexNow 的密钥 `2ed358c114b046318942c07080a48729` 和对应的 txt 文件
> 必须留在站点根目录，否则推送会被拒绝。这个文件可以公开，本来就是给搜索引擎读的。

---

## 五、一个必须提前告诉你的风险

你把 pages.dev 设为规范域名，理由是 github.io 不稳定——这个判断对了一半。

现实情况是：**pages.dev（Cloudflare）和 github.io 在国内都不算可靠**，
Cloudflare 的 IP 在境内同样经常丢包、被限速。百度蜘蛛从境内抓取，
两个域名都有抓不到的可能。

如果两三周后百度仍显示 0 收录：

1. 先在百度后台用「抓取诊断」确认到底是抓不到（网络问题）还是抓到了没收录（内容问题）
2. 如果是网络问题，**唯一的根治方案**是绑自有域名做 ICP 备案，
   解析到境内或中国香港节点。备案通常 1～3 周，建议尽早启动
3. 备案完成前，Google / Bing 这条路不受影响，可以先把海外流量跑起来

---

## 六、比提交更重要的两件事

提交只是让搜索引擎「来抓」，能不能排到前面取决于外部信号。对「守民通识」
这种独创品牌名，真正起作用的是：

1. **品牌一致性**：GitHub 个人主页、各内容平台账号都统一用「守民通识」，
   并且都链回 pages.dev。同名的外链越多，搜索引擎越确信这是一个真实实体，
   搜品牌名时越容易出知识面板和站点名称展示。

2. **持续更新**：站点现在只有 7 个页面。日更积累到一定规模后，
   「守民通识」这个词的关联度和权重才会真正建立起来。

---

## 七、时间预期

| 引擎 | 预计生效时间 |
| --- | --- |
| Bing 及 AI 搜索 | 几天内（已推送） |
| Yandex / Seznam / Naver / Yep | 1～2 周 |
| Google | 提交后几天到几周 |
| 百度 | 几天到几周，受境内抓取影响，可能需要备案域名 |
| 360 / 头条 / 神马 | 1～4 周 |

验证方法：搜索 `守民通识`，或直接搜
`site:shoumingeneralist.pages.dev` 看有没有结果出来。
