# 守民通识 · 搜索引擎收录提交指南

> 目标：让别人搜索「守民通识」能找到站点。
> 规范域名（canonical）：<https://shoumingeneralist.github.io>
> 备用域名：<https://shoumingeneralist.pages.dev>（已 301 跳转到规范域名）

---

## 一、已经自动完成的部分

| 项目 | 状态 |
| --- | --- |
| `robots.txt` | 原先返回 404，已补齐，并声明站点地图 |
| IndexNow 密钥文件 | 已放在站点根目录并通过 Bing 校验 |
| 全站 URL 推送 | 7 个页面已推送，6 个端点全部返回成功 |
| pages.dev 重复内容 | 已全站 301 到规范域名，保留路径 |
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
https://shoumingeneralist.github.io/sitemap-index.xml
```

### 1. Google Search Console（海外流量，必做）

1. 打开 <https://search.google.com/search-console>
2. 「添加资源」→ 网址前缀 → 填 `https://shoumingeneralist.github.io`
3. 所有权验证：推荐 **HTML 文件** 方式
   - 下载它给的 `googleXXXXXXXX.html`
   - 放进仓库的 `public/` 目录
   - 推送后回到平台点「验证」
   - 你也可以直接在 GitHub 网页端 `Add file → Upload files` 传上去，不用走命令行
4. 验证通过后：左侧「站点地图」→ 填入上面的地址 → 提交
5. 加速首页收录：顶部搜索框输入首页 URL → 「请求编入索引」

> 这一步最关键。Google 收录后，「守民通识」在海外和多数 AI 搜索里就能搜到了。

### 2. 百度搜索资源平台（国内流量，必做）

1. 打开 <https://ziyuan.baidu.com/>
2. 注册/登录 → 「添加网站」→ 填 `https://shoumingeneralist.github.io`
3. 验证站点：文件验证（把 `baidu_verify_xxx.html` 放进 `public/`）或 HTML 标签验证
4. 验证通过后两条路都走一遍：
   - **站点地图**：资源提交 → 普通收录 → Sitemap 提交 → 填上面的地址
   - **API 推送**（更快）：资源提交 → 普通收录 → API 提交 → 复制你的 token
5. 拿到 token 后，推送全部页面：

   ```bash
   python scripts/submit-indexnow.py --baidu-token 你的token
   ```

**关于百度的一个现实问题**：`github.io` 在国内访问不稳定，百度蜘蛛是从境内抓取的，
可能长期抓不到。如果提交两三周后百度仍显示 0 收录，建议：

- 在百度后台用「抓取诊断」看它到底能不能抓到，抓不到就是网络问题，不是内容问题
- 正解是绑一个自己的域名做 ICP 备案，解析到境内或中国香港节点
- 过渡方案：保留 pages.dev 而不做 301（但目前已按你的选择做了跳转）

### 3. 360 搜索站长平台（国内，推荐）

1. 打开 <https://zhanzhang.so.com/>
2. 注册 → 添加网站 → 文件验证（同样把验证文件放进 `public/`）
3. 数据提交 → Sitemap 提交 → 填上面的地址

### 4. 头条搜索站长平台（字节系）

1. 打开 <https://zhanzhang.toutiao.com/>
2. 注册 → 添加站点 → 验证
3. 数据提交 → 站点地图 → 填上面的地址

### 5. 神马搜索（UC / 移动端）

1. 打开 <https://zhanzhang.sm.cn/>
2. 注册 → 添加网站 → 验证 → 提交 sitemap

### 6. 搜狗 —— 可以跳过

搜狗已逐步整合进腾讯体系，站长工具基本停用，不建议再投入时间。

---

## 三、验证文件怎么放

各平台验证所有权时都会给你一个 `xxx.html` 文件，例如：

```
google1234567890abcdef.html
baidu_verify_abcdefg.html
so.com_verify_xxx.html
```

**放到仓库的 `public/` 目录**，推送后即可通过
`https://shoumingeneralist.github.io/google1234567890abcdef.html` 访问，
平台就能验证通过。

最简单的方式：打开 <https://github.com/shoumingeneralist/shoumingeneralist.github.io>，
进入 `public` 目录 → `Add file` → `Upload files` → 拖进去 → Commit。
不用装 git，也不用跑命令行。

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
python scripts/submit-indexnow.py https://shoumingeneralist.github.io/thought/start/
```

> 注意：IndexNow 的密钥 `2ed358c114b046318942c07080a48729` 和对应的 txt 文件
> 必须留在站点根目录，否则推送会被拒绝。这个文件可以公开，本来就是给搜索引擎读的。

---

## 五、比提交更重要的两件事

提交只是让搜索引擎「来抓」，能不能排到前面取决于外部信号。对「守民通识」
这种独创品牌名，真正起作用的是：

1. **品牌一致性**：GitHub 个人主页、各内容平台账号都统一用「守民通识」，
   并且都链回你的站点。同名的外链越多，搜索引擎越确信这是一个真实实体，
   搜品牌名时越容易出知识面板和站点名称展示。

2. **持续更新**：站点现在只有 7 个页面。日更积累到一定规模后，
   「守民通识」这个词的关联度和权重才会真正建立起来。

---

## 六、时间预期

| 引擎 | 预计生效时间 |
| --- | --- |
| Bing 及 AI 搜索 | 几天内（已推送） |
| Yandex / Seznam / Naver / Yep | 1～2 周 |
| Google | 提交后几天到几周 |
| 百度 | 几天到几周，受境内抓取影响，可能需要备案域名 |
| 360 / 头条 / 神马 | 1～4 周 |

验证方法：搜索 `守民通识`，或直接搜
`site:shoumingeneralist.github.io` 看有没有结果出来。
