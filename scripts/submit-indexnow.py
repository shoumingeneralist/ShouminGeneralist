#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
守民通识 —— 搜索引擎收录提交脚本

作用：
  读取站点 sitemap，把全站 URL 主动推送给支持 IndexNow 的搜索引擎
  （Bing、Yandex、Naver、Seznam、Yep 以及基于 Bing 索引的
  ChatGPT Search / Copilot / DuckDuckGo）。

用法：
  python submit.py                      # 推送 sitemap 里的全部 URL
  python submit.py https://…/a/ https://…/b/   # 只推送指定 URL

百度不支持 IndexNow，走单独的推送接口（详见 SUBMIT_GUIDE.md）：
  python submit.py --baidu-token <你的推送token>
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request

# ---------------------------------------------------------------- 配置

SITE = "https://shoumingeneralist.pages.dev"
SITEMAP_INDEX = SITE + "/sitemap-index.xml"

# IndexNow 密钥。对应的验证文件必须放在站点根目录：
#   https://shoumingeneralist.pages.dev/2ed358c114b046318942c07080a48729.txt
# 文件内容就是密钥本身（UTF-8 无 BOM，不带换行）。
KEY = "2ed358c114b046318942c07080a48729"
KEY_LOCATION = SITE + "/" + KEY + ".txt"

# 提交到任一端点，都会与所有参与 IndexNow 的搜索引擎共享。
# 这里逐个都提交一遍，避免单端点抖动导致漏推送。
ENDPOINTS = [
    ("IndexNow 全球端点", "https://api.indexnow.org/indexnow"),
    ("Bing", "https://www.bing.com/indexnow"),
    ("Yandex", "https://yandex.com/indexnow"),
    ("Seznam", "https://search.seznam.cz/indexnow"),
    ("Naver", "https://searchadvisor.naver.com/indexnow"),
    ("Yep", "https://indexnow.yep.com/indexnow"),
]

BAIDU_PUSH_API = "http://data.zz.baidu.com/urls?site={site}&token={token}"
UA = "Mozilla/5.0 (compatible; ShouminGeneralist-IndexNow/1.0)"


# ---------------------------------------------------------------- 工具

def build_opener():
    """如果环境里配了代理就走代理，否则直连。"""
    proxy = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")
    if proxy:
        return urllib.request.build_opener(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    return urllib.request.build_opener()


def http(op, url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {"User-Agent": UA})
    try:
        resp = op.open(req, timeout=40)
        return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:400]
    except Exception as e:  # noqa: BLE001
        return 0, f"{type(e).__name__}: {e}"


def collect_urls(op):
    """从 sitemap-index.xml 递归取出全部页面 URL。"""
    status, body = http(op, SITEMAP_INDEX)
    if status != 200:
        print(f"[!] 无法读取 {SITEMAP_INDEX}（HTTP {status}）")
        return []

    child_maps = re.findall(r"<loc>\s*(.*?)\s*</loc>", body)
    urls = []
    for sm in child_maps:
        st, bd = http(op, sm)
        if st == 200:
            urls.extend(re.findall(r"<loc>\s*(.*?)\s*</loc>", bd))
        else:
            print(f"[!] 跳过 {sm}（HTTP {st}）")

    # 去重、保序、只保留主站域名
    seen, out = set(), []
    for u in urls:
        if u.startswith(SITE) and u not in seen:
            seen.add(u)
            out.append(u)
    return out


def push_indexnow(op, urls):
    payload = {
        "host": urlparse_host(SITE),
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": UA,
    }

    ok = 0
    for name, ep in ENDPOINTS:
        code, txt = http(op, ep, data=body, headers=headers)
        if code in (200, 202):
            ok += 1
            note = "已收录队列" if code == 200 else "已接收，待校验密钥"
            print(f"  [OK]   {name:<20} HTTP {code}  {note}")
        else:
            print(f"  [FAIL] {name:<20} HTTP {code}  {txt[:120]}")
    return ok


def push_baidu(op, urls, token):
    url = BAIDU_PUSH_API.format(site=SITE, token=token)
    data = "\n".join(urls).encode("utf-8")
    headers = {
        "Content-Type": "text/plain",
        "User-Agent": "curl/7.12.1",
    }
    code, txt = http(op, url, data=data, headers=headers)
    print(f"  [{'OK' if code == 200 else 'FAIL'}] 百度普通收录  HTTP {code}  {txt[:200]}")
    return code == 200


def urlparse_host(site):
    return re.sub(r"^https?://", "", site).rstrip("/")


# ---------------------------------------------------------------- 入口

def main():
    args = sys.argv[1:]
    token = None
    if "--baidu-token" in args:
        i = args.index("--baidu-token")
        token = args[i + 1]
        args = args[:i] + args[i + 2:]

    op = build_opener()

    if args:
        urls = [u for u in args if u.startswith(SITE)]
    else:
        urls = collect_urls(op)

    if not urls:
        print("没有可提交的 URL，退出。")
        return 1

    print(f"待提交 {len(urls)} 个 URL（规范域名：{SITE}）\n")
    for u in urls:
        print("   -", u)
    print()

    print("== IndexNow 推送 ==")
    ok = push_indexnow(op, urls)
    print(f"\n成功 {ok}/{len(ENDPOINTS)} 个端点")

    if token:
        print("\n== 百度普通收录推送 ==")
        push_baidu(op, urls, token)

    print("\n提示：Google 与百度都不支持 IndexNow，需要在各自站长平台"
          "提交站点地图，详见 SUBMIT_GUIDE.md。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
