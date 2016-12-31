if(typeof yiel === 'undefined'){
  var yiel = {};
  var _snaq = _snaq || []; //Analytic requests handler

  yiel = {"website":{"id":1909,"name":"peachpit.com","track_yieldify_only":"false","use_snowplow":"","infrequent_basket_updates":"","shopping_class":"","shopping_selector":"","shopping_cart_multiple":"","shopping_initial":-1,"coupon_selector":"","submit_coupon_selector":"","submit_coupon_just_click":"","shopping_cart_seperator":".","track_visited_pages":"","track_visited_pages_expire":2592000000,"sign_out_class":"","campaigns_protocol":"//","watchdogs":"","cam_ids":"106075,99106,50016,18278","campaigns":"106075,99106,50016,18278","track_products":"true","products_url_pattern":"http://www.peachpit.com/articles/()","product_image_css_path":".productArea.graydient.clearfix .product:first","form_targeting":"","afiliate_block":"","cookie_block":"","cookie_block_expire":"","referring_traffic_block":"","referring_traffic_expire":"","text_grabb_condition":"no","text_grabb_options":"","track_sale":"","track_sale_expire":2592000000,"track_impression_sale":"","track_impression_sales_expire":1209600000,"thanks_page_pattern":",,false,,,,,,;;","sales_extra_details":"","sale_ajax_update":"","track_sale_ajax":"","sub_domains":"","track_purchases":"","last_price_pattern":"","last_price_selector":"","sale_value_multiplier":1.0,"browser_not_target":"","browser_target":"msie|chrome|firefox|safari|opera","delayed_start":0,"iv_delay":10000,"iv_delay_all":"","mouse_hh":0,"aa_delay":0,"bbb_margin":null,"bbb_ratio":8,"bbb_all_location":"","bbb_all_margin":"","bbb_all_ratio":"","exit_margin":"","exit_margin_right":"true","exit_margin_left":"true","exit_margin_right_val":null,"exit_margin_left_val":null,"exit_margin_right_unit":"px","exit_margin_left_unit":"px","show_powerd_by":"","close_image":"","delay":1800000,"encrypt_userinfo":"true","inactivity_period":15,"sale_display_type":"sale","website_sale_display_value":"1.5","block_script":"yieoptout","heatmap_script":"//linkshare yieldify override fix - antony\r\nif (/site_id=8\\*9oyGPgP3Y/.test(window.location.href) || document.referrer.match(/8\\*9oyGPgP3Y/) || document.referrer.match(/t\\=t/) || document.referrer.match(/yie_coupon/) || (!!document.cookie.match(/yieldify_frequency_click/))) {\r\n    yiel.fn.deleteYieldifyCookie('ab');\r\n    yiel.md.website.website.affiliate_blocker = \"\";\r\n}\r\n\r\nfunction bindEvent(element, type, handler) {\r\n    if (element.addEventListener) {\r\n        element.addEventListener(type, handler, false);\r\n    } else {\r\n        element.attachEvent(\"on\" + type, handler);\r\n    }\r\n}\r\n\r\nbindEvent(window, \"message\", function(event) {\r\nconsole.log(event.data);\r\n    var data = event.data.split(',');\r\n    if (data[0] === \"topbar\") {\r\n       yiel.is_overlay_on = false;\r\n    }\r\n    if (data[0] === \"topbarclose\") {\r\n       yiel.is_overlay_on = false;\r\n    }\r\n});\r\n\r\n// FUNCTION: URL BLOCKING AT WEBSITE LEVEL\r\nyiel.$(function() {\r\n\tvar blockMatchingUrls = \r\n\t    [\r\n\t      \"/promotions\"\r\n\t    ];\r\n\r\n\tvar allowMatchingUrls = [];\r\n\r\n\tvar exactUrls = [];\r\n\r\n\tvar matchUrls = blockMatchingUrls.filter(function(val, ind) {\r\n\t    return(window.location.pathname.match(val));\r\n\t});\r\n\r\n\tvar isUrls = exactUrls.filter(function(val, ind) {\r\n\t    return val === window.location.host + window.location.pathname;\r\n\t});\r\n\r\n\tfunction isHome() {\r\n\t    return window.location.pathname === \"/\";\r\n\t}\r\n\r\n\tfunction stopCampaigns() {\r\n\t    yiel.md.campaigns.load = function() {};\r\n\t    setTimeout(function(){\r\n\t    \tyiel.is_overlay_on = true;\r\n\t    },1000);\r\n\t}\r\n\r\n\tif(matchUrls.length == 1 || isHome() ) {\r\n\t    stopCampaigns();\r\n\t}\r\n});","ajax_coupon_selector":"","max_products_store":5,"analytics_events":"","analytics_events_category_name":"Yieldify","affiliate_blocker":"siteID=,siteid=,siteId=,Siteid=,ranSiteID=,ranMID=,ranEAID=,mid=,MID=,affiliateID=,clickID=,=Linkshare,=Rakutenmarketing,=Rakutenaffiliatenetwork,=Ls,=Ran,=Rakutenlinkshare,linkshare,LinkShare,Linkshare,affiliate,siteID=,aff=LS,aff=ls","affiliate_block_expire":2592000000,"form_refill":"","url_pattern":"","form_refill_fields":"","form_refill_expire":null,"website_version":2,"shopping_item_selector":"","data_fields":[],"data_events":[],"basket_fields":[],"form_fields":[]},"info":{"cr":118,"env":"production","dms":{"gls":"geo.yieldify.com","evc":"b.yieldify.com","rt":"rt-proxy.yieldify.com","es":"email-service.yieldify.com"},"request_host_with_port":"app.yieldify.com","src":"//d33wq5gej88ld6.cloudfront.net/code_revisions/000/000/118/original/yieldify_1472724462.js?1472724467"}};

  yiel.md = {};

  //load Yieldify here
  if (yiel.info.src) {
    var e = document.createElement('script');
    e.src = yiel.info.src;
    e.async = true;
    document.getElementsByTagName("head")[0].appendChild(e);
  }
}