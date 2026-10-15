#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EmbeddedNote bilingual privacy policy installer: place beside package.json.
from pathlib import Path
import sys

EN = '---\ntitle: Privacy Policy\ndescription: How EmbeddedNote handles website access information, cookies, email enquiries, optional comments and future advertising.\nlocale: en\n---\n# Privacy Policy\n\n**Effective date: October 15, 2026**  \n**Last updated: October 15, 2026**\n\nEmbeddedNote ("we", "us", or "our") publishes the website [embeddednote.com](https://embeddednote.com/), a bilingual publication about embedded systems, hardware, semiconductors and open-source engineering. This Policy explains how information may be collected, used and shared when you visit our website or contact us. For privacy enquiries, please email **[xden2019@gmail.com](mailto:xden2019@gmail.com)**.\n\n## 1. Information we process\n\n**Website access and security information.** When you visit the site, our hosting and security providers may process technical information such as your IP address, browser and device information, requested URLs, approximate location derived from your IP address, referring pages, access times and security events. We use such information as needed to deliver the site, maintain availability, troubleshoot problems and protect it from abuse.\n\n**Messages you send.** If you email us, we receive your email address and whatever information you choose to include. We use it to respond, deal with editorial corrections or enquiries, and retain a record where reasonably necessary.\n\n**On-site search.** Our site uses Pagefind, a browser-based search interface operating with a published search index. Search terms entered into the built-in search are not intentionally sent to EmbeddedNote as a separate search-query service. Normal web requests for search assets may still be recorded by hosting infrastructure.\n\n**Optional comments.** Where discussion features are enabled, comments are provided using Giscus and GitHub Discussions. Your interaction with those features may involve GitHub account information, cookies and requests to GitHub/Giscus services. Such processing is governed in part by the relevant providers\' policies. You can read technical articles without creating a website account.\n\n## 2. Cookies and similar technologies\n\nThe website or its service providers may use cookies or similar technologies needed for security, network delivery and optional features. Third-party features may use their own cookies or other identifiers. You can control or delete cookies using your browser settings. Blocking some cookies may affect optional functionality.\n\nIf we introduce non-essential analytics, advertising or other tracking, we will update this Policy and provide any notices and consent controls required by applicable law. A privacy policy by itself is **not** a cookie-consent mechanism.\n\n## 3. Advertising, including Google AdSense\n\nWe may enable advertising, including Google AdSense, in the future. **When advertising is enabled**, Google and other advertising partners may use cookies, web beacons, IP addresses or other identifiers to collect information about visits, deliver and measure ads, limit repeated ads and help prevent fraud. Third-party vendors, including Google, may place or read cookies in your browser and serve ads based on your visits to this website and other websites.\n\nGoogle\'s advertising cookies enable Google and its partners to serve ads based on users\' visits to this site and/or other sites on the internet. You may manage personalized advertising through [Google My Ad Center](https://myadcenter.google.com/) and, for participating vendors, [aboutads.info](https://www.aboutads.info/choices/). Learn [how Google uses information from partner sites and apps](https://policies.google.com/technologies/partner-sites).\n\nWhere required, we will request consent for non-essential advertising technologies and relevant personal-data processing **before** enabling them for affected visitors. For advertising in the European Economic Area, the United Kingdom and Switzerland, we will implement the consent-management arrangements required by Google\'s publisher policies before serving ads there. Those controls are separate from this Policy.\n\n## 4. Why we process information\n\nOur purposes include providing and securing the website, responding to messages, maintaining technical and editorial quality, meeting legal obligations, and—if activated—supporting measurement and advertising subject to required choices. Where applicable, we rely on legitimate interests for routine site operation and security; on your request to respond to enquiries; on legal obligations when required; and on consent where law requires it for non-essential cookies, advertising personalization or similar processing.\n\n## 5. Service providers, disclosures and international processing\n\nWe use **Cloudflare** for website hosting, content delivery and associated security features. Optional discussions may rely on **GitHub/Giscus**. If enabled, advertising involves **Google** and its advertising partners. These providers may process technical information under their own applicable terms and privacy policies, and information may be processed in countries other than your own. We may also disclose information when legally required or reasonably necessary to protect the website or users. We do not sell visitor contact lists.\n\nYou can review [Cloudflare\'s privacy policy](https://www.cloudflare.com/privacypolicy/) and [GitHub\'s privacy statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).\n\n## 6. Retention and security\n\nWe keep correspondence only for as long as reasonably needed to respond, maintain editorial records, resolve disputes or comply with applicable legal requirements. Hosting and security logs are retained according to the relevant provider\'s settings and retention practices. We use reasonable safeguards, but no online transmission or storage method is completely secure.\n\n## 7. Your privacy choices and rights\n\nDepending on your location and applicable law, you may have rights to request access, correction or deletion of personal information, object to or restrict certain processing, or withdraw consent where processing is based on consent. To make a request, email [xden2019@gmail.com](mailto:xden2019@gmail.com). We may need to verify your request and will respond as required by applicable law. Browser controls and any consent-management interface made available on the website can also be used to manage applicable cookie choices.\n\n## 8. Children and external links\n\nEmbeddedNote is intended for a general technical readership, not specifically for children. We do not knowingly request personal information from children through the website. Articles may link to external sites, which have their own privacy practices; we do not control those sites.\n\n## 9. Changes and contact\n\nWe may revise this Policy as services or legal requirements change. The updated version and date will be shown on this page. For questions, corrections or privacy requests, contact **[xden2019@gmail.com](mailto:xden2019@gmail.com)**.\n'
ZH = '---\ntitle: 隐私政策\ndescription: EmbeddedNote（嵌入式杂谈）网站访问数据、Cookie、邮件联系、可选评论功能及未来广告服务的隐私说明。\nlocale: zh\n---\n# 隐私政策\n\n**生效日期：2026年10月15日**  \n**最后更新：2026年10月15日**\n\nEmbeddedNote（以下简称“我们”）运营 [embeddednote.com](https://embeddednote.com/) 中英双语嵌入式技术网站，内容涵盖嵌入式系统、芯片、硬件和开源工程。本文说明你访问网站或联系我们时，相关信息可能如何被收集、使用及共享。隐私问题请发送至 **[xden2019@gmail.com](mailto:xden2019@gmail.com)**。\n\n## 一、我们处理哪些信息\n\n**网站访问及安全信息：** 网站托管及安全服务商可能处理IP地址、浏览器及设备信息、访问的URL、根据IP推测的大致地区、来源页面、访问时间、安全事件等技术数据，用于提供网页、维持可用性、排查故障及防范滥用。\n\n**你主动发送的信息：** 如果你发送邮件，我们会收到你的邮箱地址及邮件中自愿提供的内容，用于回复问题、核对技术勘误或合作咨询，以及在合理必要的范围内保留相关记录。\n\n**站内搜索：** 网站使用 Pagefind 提供基于公开索引的浏览器端搜索。用户输入的搜索词不会被我们有意作为独立的搜索查询发送至专用搜索服务；但获取搜索资源时的常规网络请求仍可能由托管服务记录。\n\n**可选评论：** 如网站启用了评论功能，相关讨论通过 Giscus 和 GitHub Discussions 实现。使用时可能涉及GitHub账号信息、Cookie及与第三方服务的通信，并部分适用相关服务商的隐私政策。阅读技术文章不需要注册本站账号。\n\n## 二、Cookie 与类似技术\n\n网站或其服务商可能使用保障安全、内容分发及可选功能所需的Cookie或类似技术；第三方功能也可能使用自身的Cookie或其他标识符。你可以通过浏览器设置管理或删除Cookie，禁用部分Cookie可能影响可选功能。\n\n如果未来增加非必要的统计分析、广告或其他跟踪功能，我们会更新本政策，并根据适用法律提供相应的告知及同意管理。**隐私政策本身不等于Cookie同意管理功能。**\n\n## 三、广告与 Google AdSense\n\n网站未来可能接入 Google AdSense 等广告服务。**相关广告功能启用后**，Google及其他广告合作方可能使用Cookie、网络信标（Web Beacon）、IP地址或其他标识符，了解广告展示和访问情况、衡量广告表现、控制广告频次及防范欺诈。包括Google在内的第三方广告服务商，可能在访问者浏览器中放置或读取Cookie，并根据访问者曾访问本站或其他网站的情况展示广告。\n\nGoogle及其合作方可使用广告Cookie，根据用户对本站及互联网其他网站的访问情况提供广告。用户可前往 [Google My Ad Center](https://myadcenter.google.com/) 管理个性化广告偏好，也可通过 [aboutads.info](https://www.aboutads.info/choices/) 管理部分参与该机制的第三方广告商。另可查看 [Google如何使用合作伙伴网站和应用的数据](https://policies.google.com/technologies/partner-sites?hl=zh-CN)。\n\n对于法律要求事先同意的非必要广告技术和相关个人信息处理，我们将在面向相关用户启用前提供适用的同意管理。面向欧洲经济区、英国和瑞士的广告服务，我们会在投放前落实Google发布商政策要求的同意管理安排。该功能需要单独实施，并非发布本政策即可自动实现。\n\n## 四、信息处理目的与依据\n\n我们处理必要信息的目的包括网站运行与安全维护、回复咨询、提升技术内容准确性、履行法律义务，以及在相关功能启用后进行合规的广告展示与效果衡量。在适用法律要求下，常规运营及安全处理可能基于合法利益，咨询回复依据用户请求，法律义务依据法定要求，而非必要Cookie、广告个性化等处理依据法律要求取得的同意。\n\n## 五、服务提供方与跨境处理\n\n本站使用 **Cloudflare** 提供网站托管、内容分发及相关安全服务。启用评论功能时可能使用 **GitHub/Giscus**；启用广告时涉及 **Google** 及其广告合作方。这些服务商可能根据各自的条款及隐私政策处理技术信息，处理地点可能位于访问者所在国家或地区以外。法律要求或保护网站及用户所必需的情况下，我们也可能披露有关信息。我们不会出售访问者邮件联系名单。\n\n参考：[Cloudflare隐私政策](https://www.cloudflare.com/privacypolicy/)；[GitHub隐私声明](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement)。\n\n## 六、保存期限与安全\n\n我们仅在回复邮件、保存必要编辑记录、处理争议或满足法律要求所需的合理期限内保留往来信息。托管及安全日志的保存依相关服务商的配置及保存规则执行。我们采取合理措施保护相关信息，但无法保证任何互联网传输或存储方式绝对安全。\n\n## 七、你的选择与权利\n\n根据你所在地区的适用法律，你可能享有查询、更正、删除个人信息，反对或限制特定处理，以及在以同意为依据时撤回同意等权利。可通过 [xden2019@gmail.com](mailto:xden2019@gmail.com) 提交请求。我们可能需要核验请求，并按适用法律处理。你也可通过浏览器设置及网站实际提供的同意管理界面调整相应Cookie偏好。\n\n## 八、未成年人及外部链接\n\n本网站面向一般技术读者，并非专门为未成年人提供服务，也不会主动要求儿童通过网站提交个人信息。文章中的第三方网站链接适用其自身隐私规则，我们无法控制第三方网站的具体做法。\n\n## 九、政策更新与联系方式\n\n当网站服务或相关法律要求发生变化时，我们可能更新本政策，并在本页标明更新日期。如对信息处理有疑问，或希望提出更正、删除等请求，请联系 **[xden2019@gmail.com](mailto:xden2019@gmail.com)**。\n'
ROOT = Path(__file__).resolve().parent

PRIVACY_PAGE = """---
import Base from '../../layouts/Base.astro';
import {getCollection, render} from 'astro:content';
export async function getStaticPaths() {
  const policies = await getCollection('privacy');
  return policies.map(entry => ({params:{lang:entry.data.locale},props:{entry}}));
}
const {entry} = Astro.props;
const lang = entry.data.locale;
const {Content} = await render(entry);
---
<Base lang={lang} title={entry.data.title} description={entry.data.description} translations={{en:'/en/privacy/', zh:'/zh/privacy/'}}>
  <article class="prose about-prose" data-pagefind-body>
    <Content />
  </article>
</Base>
"""

CMS_BLOCK = """  - name: privacy_en
    label: Privacy Policy (English)
    type: file
    path: src/content/privacy/en.md
    format: yaml-frontmatter
    fields:
      - {name: title, label: Title, type: string, required: true}
      - {name: description, label: Description, type: text, required: true}
      - {name: locale, label: Language, type: string, default: en, required: true}
      - {name: body, label: Policy Content, type: rich-text}
  - name: privacy_zh
    label: 隐私政策（中文）
    type: file
    path: src/content/privacy/zh.md
    format: yaml-frontmatter
    fields:
      - {name: title, label: 标题, type: string, required: true}
      - {name: description, label: 描述, type: text, required: true}
      - {name: locale, label: 语言, type: string, default: zh, required: true}
      - {name: body, label: 政策正文, type: rich-text}
"""


def read(path):
    return (ROOT/path).read_text(encoding='utf-8')


def replace_once(content, old, new, path):
    if new in content:
        return content
    if content.count(old) != 1:
        raise ValueError(f'文件版本与预期不符，已停止：{path}（预期匹配1处，实际{content.count(old)}处）')
    return content.replace(old, new, 1)


def install():
    if not (ROOT/'package.json').is_file() or not (ROOT/'astro.config.mjs').is_file():
        raise ValueError('请把本脚本放到 embeddednote-website 的根目录，与 package.json 同一级，再运行。')
    for path in ['src/content.config.ts','src/layouts/Base.astro','.pages.yml','scripts/check-dist.mjs']:
        if not (ROOT/path).is_file():
            raise ValueError(f'缺少工程文件：{path}。请先在 GitHub Desktop 中 Fetch / Pull。')

    updates = {
        'src/content/privacy/en.md': EN,
        'src/content/privacy/zh.md': ZH,
        'src/pages/[lang]/privacy.astro': PRIVACY_PAGE,
    }

    conf=read('src/content.config.ts')
    if 'const privacy = defineCollection(' not in conf:
        conf=replace_once(
            conf, 'export const collections = {articles,about};',
            "const privacy = defineCollection({\n"
            "  loader: glob({pattern:'*.md',base:'./src/content/privacy'}),\n"
            "  schema: z.object({title:z.string(),description:z.string(),locale:z.enum(['en','zh'])})\n"
            "});\n"
            "export const collections = {articles,about,privacy};",
            'src/content.config.ts')
    updates['src/content.config.ts']=conf

    base=read('src/layouts/Base.astro')
    before='<a href={`/${lang}/about/`}>{dict.about}</a>'
    after=before+" · <a href={`/${lang}/privacy/`}>{lang === 'zh' ? '隐私政策' : 'Privacy Policy'}</a>"
    base=replace_once(base,before,after,'src/layouts/Base.astro') if after not in base else base
    updates['src/layouts/Base.astro']=base

    config=read('.pages.yml')
    if 'name: privacy_en' not in config and 'name: privacy_zh' not in config:
        sep='\r\n' if b'\r\n' in (ROOT/'.pages.yml').read_bytes() else '\n'
        new_config=config.rstrip('\n')+'\n'+CMS_BLOCK.rstrip('\n')+'\n'
        updates['.pages.yml']=new_config.replace('\n',sep)
    elif 'name: privacy_en' not in config or 'name: privacy_zh' not in config:
        raise ValueError('Pages CMS 隐私配置只存在一个语言版本，请手动检查 .pages.yml。')

    checks=read('scripts/check-dist.mjs')
    if 'const privacy = `${lang}/privacy/index.html`;' not in checks:
        checks=replace_once(checks,
          '  const about = `${lang}/about/index.html`;',
          '  const about = `${lang}/about/index.html`;\n  const privacy = `${lang}/privacy/index.html`;',
          'scripts/check-dist.mjs')
        checks=replace_once(checks,
          'for (const path of [home, about, ...categories.map',
          'for (const path of [home, about, privacy, ...categories.map',
          'scripts/check-dist.mjs')
        check_policy = """  if (has(privacy)) {
    const htmlPolicy = read(privacy);
    const otherLang = lang === 'en' ? 'zh' : 'en';
    check(htmlPolicy.includes('rel="canonical"') && htmlPolicy.includes(`/${lang}/privacy/`), `${lang} privacy canonical`);
    check(htmlPolicy.includes('hreflang=') && htmlPolicy.includes(`/${otherLang}/privacy/`), `${lang} privacy language alternate`);
    check(htmlPolicy.includes('data-pagefind-body'), `${lang} privacy indexed content`);
  }
"""
        checks=replace_once(checks,
          '  check(!has(oldWelcome),', check_policy+'  check(!has(oldWelcome),',
          'scripts/check-dist.mjs')
        old="    check(html.includes('rel=\"canonical\"'), `${lang} homepage canonical`);"
        new=old+"\n    check(html.includes(`/${lang}/privacy/`), `${lang} privacy footer link`);"
        checks=replace_once(checks,old,new,'scripts/check-dist.mjs')
        updates['scripts/check-dist.mjs']=checks

    # Every modification is validated before the first write; changes are idempotent.
    changed=[]
    for path,contents in updates.items():
        f=ROOT/path
        raw=contents.encode('utf8')
        if f.exists() and f.read_bytes()==raw:
            continue
        f.parent.mkdir(parents=True,exist_ok=True)
        f.write_bytes(raw)
        changed.append(path)

    print('\n✅ 已添加中英文隐私政策，修改文件总数：',len(changed))
    for path in changed:
        print('  -',path)
    print('\n下一步：回到 GitHub Desktop → Changes 查看差异 → Commit → Push origin。')
    print('请取消勾选临时脚本 apply_embeddednote_privacy.py，无需提交到网站。')
    print('网站上线后访问 /en/privacy/ 与 /zh/privacy/。')
    print('重要：启用 AdSense 前仍需要配置适用地区的 CMP / Cookie 同意管理。')

if __name__ == '__main__':
    try:
        install()
    except Exception as exc:
        print('\n❌ 安装未完成：',exc,file=sys.stderr)
        sys.exit(1)
