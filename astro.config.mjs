// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import rehypeExternalLinks from 'rehype-external-links';
import { unified } from '@astrojs/markdown-remark';

// https://astro.build/config
export default defineConfig({
	// GitHub Pages 项目站点部署在 /ShouminGeneralist/ 子路径下，
	// 必须设置 base，否则 CSS/JS/图片等静态资源会指向根路径而 404。
	base: '/ShouminGeneralist/',
	site: 'https://shoumingeneralist.github.io',
	markdown: {
		// Astro 7 默认用 Sätteri 处理器，它不跑 rehype 插件，所以这里显式切到 unified
		// （@astrojs/markdown-remark），再把 rehype-external-links 挂上去。
		processor: unified({
			rehypePlugins: [
				// 让正文里指向外部域名的链接自动在新标签页打开，并加上
				// noopener / noreferrer，防止新页面通过 window.opener 反向控制本站。
				[
					rehypeExternalLinks,
					{
						target: '_blank',
						rel: ['noopener', 'noreferrer'],
						// 除 http(s) 外，邮件 / 电话链接也走新窗口，不在当前页跳走
						protocols: ['http', 'https', 'mailto', 'tel'],
					},
				],
			],
		}),
	},
	integrations: [
		starlight({
			title: '守民通识',
			description: '无偿分享近 20 年研发实战经验，覆盖机械、电机控制、电子、软硬件、计算机等领域。深耕家电头部企业， 80 余项专利，持续跨领域学习。秉持知识无界，属于人类共同资产的理念，以通识研发为方向，关注新知识新技术积累。AI 飞速发展，可辅助完成大量工作，但研发并非知识填鸭，重在练习内化、转化为自身能力。愿大家保有自主学习、独立思考的能力，以知识共共享，不断学习，推动共同进步。',
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/shoumingeneralist' }],
			
			 // 将网站默认语言设置为简体中文
      locales: {
        root: {
          label: '简体中文',
          lang: 'zh-CN',
        },
      },

			sidebar: [
			{
					label: '初衷',
					items: [
						// Each item here is one entry in the navigation menu.
						{ label: '关于本站', slug: 'thought/start' },
					],
				},
				{
					label: '自媒体之路',
					items: [
						{ autogenerate: { directory: 'selfmediapath' } },
					],
				},
			],
		}),
	],
});
