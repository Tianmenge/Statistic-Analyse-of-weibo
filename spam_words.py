#coding=utf-8

"""用于计算敏感度的敏感词权值表
"""

spam_words = {
1: u"微信 OR 代理 OR 包邮 OR 代购 OR 赚钱 OR 发财 OR 致富 OR 股票 OR 基金 OR 代开 OR 热销 OR 法宝 OR 宝典 OR 免费 OR \
     优惠 OR 特惠 OR 特价 OR 便宜 OR 廉价 OR 实拍 OR 限量 OR 买家秀 OR 热卖款 OR 订制 OR 断货 OR 定制 OR 原版 OR 预定 OR \
     现货 OR 必备 OR 微商 OR 微店 OR 兼职 OR 推广 OR 男款 OR 女款 OR 男鞋 OR 女鞋 OR 情侣款 OR 潮款 OR 爆款 OR 新款 OR 走秀款 OR 限量版 OR 明星款 OR  \
     畅销款 OR 同款 OR 威信 OR v信 OR 正品 OR 诚招 OR 总代 OR WeChat OR 直邮 OR 全新 OR 联保 OR 货源 OR 海外购 OR 进口 OR 下单 OR 专柜 OR \
     新品 OR 新版 OR 独家 OR 百搭 OR 代里 OR 纪念版 OR 定制款 OR 必备款 OR 童鞋 OR 无痕接发 OR 蜜乐儿 OR 小金花面膜 OR 娇玛仕 OR 爱美肌 OR 巨惠 OR \
     江诗丹顿 OR 热销款 OR 面膜 OR 秀场款 OR 客服 OR 型号 OR 款号"}
##spam_words = {
##1: u"微信 OR 包邮 OR 股票 OR 基金 OR 免费 OR 优惠 OR 正品 OR 推广 OR 独家"} 
##     优惠 OR 特惠 OR 特价 OR 便宜 OR 廉价 OR 实拍 OR 限量 OR 买家秀 OR 热卖款 OR 订制 OR 断货 OR 定制 OR 原版 OR 预定 OR \
##     现货 OR 必备 OR 微商 OR 微店 OR 兼职 OR 推广 OR 男款 OR 女款 OR 男鞋 OR 女鞋 OR 情侣款 OR 潮款 OR 爆款 OR 新款 OR 走秀款 OR 限量版 OR 明星款"}  
##     畅销款 OR 同款 OR 威信 OR v信 OR 正品 OR 诚招 OR 总代 OR WeChat OR 直邮 OR 全新 OR 联保 OR 货源 OR 海外购 OR 进口 OR 下单 OR 专柜 OR \
##     新品 OR 新版 OR 独家 OR 百搭 OR 代里 OR 纪念版 OR 定制款 OR 必备款 OR 童鞋 OR 无痕接发 OR 蜜乐儿 OR 小金花面膜 OR 娇玛仕 OR 爱美肌 OR 巨惠 OR \
##     江诗丹顿 OR 热销款 OR 面膜 OR 秀场款 OR 客服 OR 型号 OR 款号"}
##     OR 代购 OR 赚钱 OR 发财 OR 致富 OR 股票 OR 基金 OR 代开 OR 热销 OR 法宝 OR 宝典 OR 免费
