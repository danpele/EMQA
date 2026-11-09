/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ 177
(module) {

/**
 * tracking logic 
 */
let thirdPartyDomainExceptions = [{
  from: '^www\\.google\\.[^.]{2,3}(?:\.[^.]{2,3})?$',
  to: ['ssl.gstatic.com', 'www.gstatic.com', 'fonts.gstatic.com', 'encrypted-(.+)\\.gstatic.com', 'apis.google.com', 'fonts.googleapis.com', '(.+)\\.googleusercontent\\.com$']
}, {
  from: 'drive.google.com',
  to: ['ssl.gstatic.com', 'www.gstatic.com', 'fonts.gstatic.com', 'fonts.googleapis.com', '(.+)\\.googleusercontent\\.com$']
}, {
  from: 'docs.google.com',
  to: ['ssl.gstatic.com', 'www.gstatic.com', 'fonts.gstatic.com', 'fonts.googleapis.com', '(.+)\\.googleusercontent\\.com$']
}, {
  from: '(.+)\\.googleusercontent\\.com$',
  to: ['ssl.gstatic.com', 'www.gstatic.com', 'www.google.com', 'drive.google.com', 'docs.google.com', 'accounts.google.com', 'play.google.com', 'clients([0-9]+)\\.google\\.com$']
}, {
  from: 'accounts.google.com',
  to: ['(.+)\\.googleusercontent\\.com$']
}, {
  from: '^www\\.facebook\\.[^.]{2,3}(?:\.[^.]{2,3})?$',
  to: ['static.xx.fbcdn.net', 'fbcdn.net']
}, {
  from: '^www\\.twitter\\.[^.]{2,3}(?:\.[^.]{2,3})?$',
  to: ['abs.twimg.com']
}, {
  from: '\\.*',
  to: ['challenges.cloudflare.com']
}, {
  from: '^(.+\\.)?wordpress\\.(com|org)$',
  to: ['^(.+\\.)?gravatar\\.com$']
}];
let cookiesSet = new Set(['nosdn.127.net', 'bnet.163.com', '123greetings.com', '122.2o7.net', '112.2o7.net', '5min.com', 'accuweather.com', 'actionnetwork.org', 'imagesrv.adition.com', 'auth.adobe.com', 'wwwimages.adobe.com', 'xsdownload.adobe.com', 'assets.adobedtm.com', 'affirm.com', 'akamai.net', 'akamaihd.net', 'akamaized.net', 'al.com', 'alert60.com', 'alexa.com', 'ally.com', 's3.amazonaws.com', 'amazonaws.com', 'coin.amazonpay.com', 'coin-eu.amazonpay.com', 'americanhomecomings.com', 'ancestry.com', 'angularjs.org', 'anonymto.me', 'up.anv.bz', 'anvato.net', 'tkx-acc.apis.anvato.net', 'cdn.anvato.net', 'tkx2-prod.anvato.net', 'mcp-media5.anvato.net', 'aol.com', 'aolcdn.com', 'ap.org', 'apnewsregistry.com', 'hiroservers.appspot.com', 'snapabug.appspot.com', 'appspot.com', 'arcgis.com', 'arcgisonline.com', 'archive.org', 'secure5.arcot.com', 'arcot.com', 'cdn.arstechnica.net', 'art19.com', 'aspnetcdn.com', 'c64.assets-yammer.com', 'assetfiles.com', 'assets-cdk.com', 'auth0.com', 'authorize.net', 'autoforums.com', 'azureedge.net', 'bac-assets.com', 'api.map.baidu.com', 'sapi.map.baidu.com', 'bandcamp.com', 'bankid.no', 'bankrate.com', 'bazaarvoice.com', 'bcbits.com', 'betterttv.net', 'static.beyondmenu.com', 'www.beyondmenu.com', 'bigcommerce.com', 'www.bing.com', 'bit.ly', 'bizrate.com', 'blockstack.org', 'blogblog.com', 'blogger.com', 'blogher.org', 'blogspot.com', 'bp.blogspot.com', 'bloxcms.com', 'boldchat.com', 'bootstrapcdn.com', 'braintreegateway.com', 'brcdn.com', 'break.com', 'breakingburner.com', 'brightcove.com', 'players.brightcove.net', 'bungie.net', 'buzzfed.com', 'buzzfeed.com', 'cachefly.net', 'cardinalcommerce.com', 'cars.com', 'cbsi.com', 'cbsimg.net', 'cbsistatic.com', 'cdninstagram.com', 'cdnpk.com', 'cern.ch', 'charter.com', 'pwc.chase.com', 'civicscience.com', 'cleanprint.net', 'cleveland.com', 'cloudflare.com', 'cloudfront.net', 'cloudinary.com', 'bbb.org', 'grapeshot.co.uk', 'w.graphiq.com', 's.graphiq.com', 's2.graphiq.com', 's3.graphiq.com', 'files.graphiq.com', 'gr-assets.com', 'guardian.co.uk', 'media-imdb.com', 'mediaworks.co.nz', 'cc.cnetcontent.com', 'cdn.cnetcontent.com', 'ws.cnetcontent.com', 'com.com', 'complex.com', 'convio.net', 'copyscape.com', 'corporate-ir.net', 'coupons.com', 'craveonline.com', 'creativecommons.org', 'crowdynews.com', 'cstv.com', 'cursecdn.com', 'custhelp.com', 'd3js.org', 'dailymotion.com', 'danid.dk', 'dealer.com', 'dealerinspire.com', 'delicious.com', 'delvenetworks.com', 'denverpost.com', 'deviantart.com', 'deviantart.net', 'digitalriver.com', 'digitalrivercontent.net', 'cdn.discourse.org', 'discovery.com', 'disqus.com', 'disquscdn.com', 'a.disquscdn.com', 'uploads.disquscdn.com', 'dmcdn.net', 'dmcdn.com', 'screendoor.dobt.co', 'documentcloud.org', 'domainnamesales.com', 'donorbox.org', 'dotsub.com', 'dl.dropboxusercontent.com', 'dudamobile.com', 'dumpert.nl', 'duosecurity.com', 'cdn.dynamicyield.com', 'cdn-eu.dynamicyield.com', 'rcom.dynamicyield.com', 'rcom-eu.dynamicyield.com', 'static.dynamicyield.com', 'st.dynamicyield.com', 'st-eu.dynamicyield.com', 'ebayimg.com', 'ebayrtm.com', 'ebaystatic.com', 'ecwid.com', 'edgecastcdn.net', 'edgefcs.net', 'edgekey.net', 'editmysite.com', 'files.edx.org', 'ehc.com', 'elasticbeanstalk.com', 'eltrafiko.com', 'api-cdn.embed.ly', 'api.embed.ly', 'cdn.embed.ly', 'cdn.embedly.com', 'i-cdn.embed.ly', 'i.embed.ly', 'epoch.com', 'epoq.de', 'estara.com', 'et4.de', 'ethn.io', 'evcdn.com', 'ebmedia.eventbrite.com', 'everyaction.com', 's-static.ak.facebook.com', 'staticxx.facebook.com', 'fansonly.com', 'travis-ci-org.global.ssl.fastly.net', 'fastly.net', 'fbcdn.net', 'attachment.fbsbx.com', 'feedburner.com', 'filepicker.io', 'financialcontent.com', 'findnsave.com', 'firstlook.org', 'flipcause.com', 'framasoft.org', 'frz.io', 'build.origami.ft.com', 'fz.io', 'fzcdn.net', 'hello.firefox.com', 'flattr.com', 'flickr.com', 'fling.com', 'flowplayer.org', 'flyertown.ca', 'adm.fwmrm.net', 'fontawesome.com', 'fontdeck.com', 'fonts.com', 'fonts.net', 'force.com', 'fuseservice.com', '140cc.v.fwmrm.net', 'fyre.co', 'gannett-cdn.com', 'gannettonline.com', 'gannett-tv.com', 'gasbuddy.com', 'gawkerassets.com', 'geenstijl.nl', 'geetest.com', 'geoplugin.net', 'geotrust.com', 'getpocket.com', 'giant.gfycat.com', 'gfycat.com', 'ggpht.com', 'gigya.com', 'giphy.com', 'github.com', 'githubusercontent.com', 'gmodules.com', 'go.com', 'godaddy.com', 'godatafeed.com', 'gogousenet.com', 'apis.google.com', 'books.google.com', 'calendar.google.com', 'checkout.google.com', 'clients1.google.com', 'clients6.google.com', 'consent.google.com', 'cse.google.com', 'developers.google.com', 'docs.google.com', 'drive.google.com', 'feedburner.google.com', 'feedproxy.google.com', 'fonts.google.com', 'fusiontables.google.com', 'kh.google.com', 'khms0.google.com', 'khms1.google.com', 'khms2.google.com', 'khms3.google.com', 'khms4.google.com', 'labs.google.com', 'mapsengine.google.com', 'maps.google.com', 'mt0.google.com', 'mt1.google.com', 'mts0.google.com', 'mts1.google.com', 'mw1.google.com', 'mw2.google.com', 'pay.google.com', 'picasaweb.google.com', 'play.google.com', 'plus.google.com', 'sites.google.com', 'smartlock.google.com', 'spreadsheets.google.com', 'talkgadget.google.com', 'translate.google.com', 'trends.google.com', 'video.google.com', 'ajax.googleapis.com', 'storage.googleapis.com', 'googleapis.com', 'googlecode.com', 'googlecommerce.com', 'googletagservices.com', 'cdn.leafletjs.com', 'lh4.googleusercontent.com', 'googleusercontent.com', 'googlevideo.com', 'governmentjobs.com', 'gravatar.com', 'greenhouse.io', 'gscdn.nl', 'gstatic.com', 'guildwars2.com', 'hackerone-user-content.com', 'helium.com', 'hellobar.com', 'herokuapp.com', 'code.highcharts.com', 'homestead.com', 'cdn.hometogo.net', 'honcode.ch', 'hootsuite.com', 'howaboutwe.com', 'hwcdn.net', 'hypothes.is', 'ibsys.com', 'ibtimes.com', 'icbdr.com', 'mpsnare.iesnare.com', 'imagecorn.com', 'imageg.net', 'imagehost123.com', 'images-amazon.com', 'imageshack.us', 'imagetwist.com', 'imagevenue.com', 'www.img-bahn.de', 'imgchili.com', 'imgfarm.com', 'imgspice.com', 'imgur.com', 'imgix.net', 'imshopping.com', 'indeed.com', 'inergizedigital.com', 'inq.com', 'instagram.com', 'instantservice.com', 'instapaper.com', 'intellicast.com', 'intensedebate.com', 'intercom.io', 'members.internetdefenseleague.org', 'investingchannel.com', 'script.ioam.de', 'issuu.com', 'janrain.com', 'jquery.com', 'jquerytools.org', 'jsdelivr.net', 'jsonip.com', 'jtvnw.net', 'justin.tv', 'jwpcdn.com', 'jwpltx.com', 'content.jwplatform.com', 'jwpsrv.com', 'cdnapi.kaltura.com', 'cdnapisec.kaltura.com', 'cdnbakmi.kaltura.com', 'cdnsecakmi.kaltura.com', 'cfvod.kaltura.com', 'www.kaltura.com', 'kampyle.com', 'kataweb.it', 'kickapps.com', 'kickstarter.com', 'kickstatic.com', 'kingfeatures.com', 'kinja-static.com', 'klarna.com', 'klarnacdn.net', 'klm.com', 'kxcdn.com', 'ddragon.leagueoflegends.com', 'libsyn.com', 'licdn.com', 'licensebuttons.net', 'addon.lidl.de', 'media.lidl.com', 'linkwithin.com', 'list-manage.com', 'i.lithium.com', 'messenger.live.com', 'officeapps.live.com', 'onedrive.live.com', 'livechatinc.com', 'livefyre.com', 'livehelpnow.net', 'liveperson.net', 'livestream.com', 'llnwd.net', 'loggly.com', 'logos.com', 'lphbs.com', 'mail.ru', 'mailchimp.com', 'mapbox.com', 'mapquestapi.com', 'marketo.com', 'masslive.com', 'mathjax.org', 'maxmind.com', 'mcclatchyinteractive.com', 'meebocdn.net', 'mfstatic.cz', 'mlive.com', 'mncdn.com', 'mobify.com', 'verify.monzo.com', 'loop.services.mozilla.com', 'mozilla.net', 'mozilla.org', 'mozu.com', 'mqcdn.com', 'msecnd.net', 'msn.com', 'mtv.com', 'mtvnservices.com', 'mycapture.com', 'myportfolio.com', 'myshopify.com', 'mzstatic.com', 'nationbuilder.com', 'nationalgeographic.com', 'nbcuni.com', 'neighborsink.com', 'netdna-cdn.com', 'netdna-ssl.com', 'nos.netease.com', 'networksolutions.com', 'newsinc.com', 'newslook.com', 'newstogram.com', 'nextopiasoftware.com', 'nfl.com', 'nflcdn.com', 'assets.nflxext.com', 'cdn3.nflxext.com', 'nflxext.com', 'ngfiles.com', 'ngpvan.com', 'nj.com', 'nmcdn.us', 'nola.com', 'npmcdn.com', 'nrcdn.com', 'nsimg.net', 'media.nu.nl', 'nyt.com', 'nytimes.com', 'c.o0bg.com', 'ocdn.eu', 'ocsn.com', 'olark.com', 'omroep.nl', 'amazoncustomerservice.d2.sc.omtrdc.net', 'omny.fm', 'attservicesinc.tt.omtrdc.net', 'dsw.tt.omtrdc.net', 'onswipe.com', 'api.ooyala.com', 'c.ooyala.com', 'l.ooyala.com', 'opf.ooyala.com', 'player.ooyala.com', 'secure-cf-c.ooyala.com', 'tile.opencyclemap.org', 'tile2.opencyclemap.org', 'openlayers.org', 'openlibrary.org', 'openload.co', 'tile.openstreetmap.fr', 'openstreetmap.org', 'optimizely.com', 'oregonlive.com', 'outlook.com', 'paddle.com', 'pandacommerce.net', 'parastorage.com', 'passwordbox.com', 'paypal.com', 'paypalobjects.com', 'pdf.yt', 'pennlive.com', 'performgroup.com', 'pgcdn.com', 'phncdn.com', 'photobucket.com', 'phplist.com', 'piclens.com', 'pinimg.com', 'piratebay.org', 'pistachio-cdn.graze.com', 'pixietrixcomix.com', 'plex.tv', 'plot.ly', 'web.poecdn.com', 'poll.fm', 'polldaddy.com', 'postimg.org', 'powerreviews.com', 'pricegrabber.com', 'printfriendly.com', 'prismic.io', 'providesupport.com', 'psswrdbx.com', 'publiekeomroep.nl', 'img.purch.com', 'qualtrics.com', 'quotemedia.com', 'api.razorpay.com', 'checkout.razorpay.com', 'razorpay.com', 'rackcdn.com', 'rackspacecloud.com', 'radikal.ru', 'rambler.ru', 'images.rapgenius.com', 'readability.com', 'readthedocs.org', 'recaptcha.net', 'recurly.com', 'redcdn.pl', 'redefine.pl', 'cdngeneral.rentcafe.com', 'resellerratings.com', 'resultspage.com', 'rewardstyle.com', 'rpxnow.com', 'rssinclude.com', 'salesforce.com', 'salesforceliveagent.com', 'salsalabs.com', 'sbnation.com', 'schd.ws', 'sched.org', 'schibsted.com', 'schibsted.io', 'schibsted.no', 'schibsted.tech', 'scribd.com', 'scribdassets.com', 'www.searchanise.com', 'securesuite.co.uk', 'securitymetrics.com', 'seeclickfix.com', 'sgizmo.com', 'shopping.com', 'shop-pro.jp', 'shoprunner.com', 'sidearmsports.com', 'siteimprove.com', 'shield.sitelock.com', 'sketchfab.com', 'slidedeck.com', 'public.slidesharecdn.com', 's-msft.com', 's-msn.com', 'smugmug.com', 'snapengage.com', 'sndcdn.com', 'auth.api.sonyentertainmentnetwork.com', 'cdn-a.sonyentertainmentnetwork.com', 'api.soundcloud.com', 'feeds.soundcloud.com', 'springboardplatform.com', 'squarespace.com', 'squareup.com', 'squirt.io', 'ssl-images-amazon.com', 'cdn.sstatic.net', 'sstatic.net', 'stackexchange.com', 'stackoverflow.com', 'staticamzn.com', 'cdn.static-economist.com', 'staticflickr.com', 'steampowered.com', 'store.akamai.steamstatic.com', 'steamusercontent.com', 'stellaservice.com', 'stripe.com', 'stripecdn.com', 'surveygizmo.com', 'surveymonkey.com', 'swiftype.com', 'syracuse.com', 'public.tableausoftware.com', 'c.tadst.com', 'taleo.net', 'uploads.tapatalk-cdn.com', 'targetimg1.com', 'targetimg2.com', 'technorati.com', 'tegna-media.com', 'textalk.se', 'theplatform.com', 'tile.thunderforest.com', 'timeinc.net', 'tinypass.com', 'tinypic.com', 'tinyurl.com', 'tiqcdn.com', 'tmsbuyatoyota.com', 'torbit.com', 'townnews.com', 'cookieblock.trackersimulate.org', 'tradingview.com', 'trb.com', 'trbimg.com', 'trumba.com', 'privacy-policy.truste.com', 'trustkeeper.net', 'trustwave.com', 'ttvnw.net', 'tumblr.com', 'turner.com', 'turnto.com', 'twimg.com', 'api.twisto.cz', 'static.twisto.cz', 'api.twisto.pl', 'twitch.tv', 'twitter.com', 'platform.twitter.com', 'syndication.twitter.com', 'typeform.com', 'typekit.com', 'typekit.net', 'typepad.com', 'typography.com', 'assets.ubuntu.com', 'uicdn.com', 'ui-portal.de', 'ultimedia.com', 'ultraimg.com', 'unicornmedia.com', 'uplynk.com', 'usa.gov', 'viafoura.net', 'viddler.com', 'videobash.com', 'vidible.tv', 'viduki.com', 'vimeo.com', 'vimeocdn.com', 'virtualearth.net', 'visa.com', 'vmixcore.com', 'voxmedia.com', 'vox-cdn.com', 'w3.org', 'wallst.com', 'weather.com', 'weather.gov', 'weatherbug.com', 'weathernationtv.com', 'weatherzone.com.au', 'webflow.com', 'webs.com', 'websimages.com', 'webtype.com', 'weebly.com', 'where.com', 'widgetserver.com', 'wikidata.org', 'wikimedia.org', 'wikipedia.org', 'wildapricot.org', 'windy.com', 'wishabi.com', 'wistia.net', 'wistia.com', 'wix.com', 'wixapps.net', 'gatherer.wizards.com', 's.w.org', 'ts.w.org', 'ps.w.org', 'wnyc.org', 'wordpress.com', 'worldnow.com', 'wp.com', 'wpengine.com', 'wufoo.com', 'wunderground.com', 'wxc.com', 'wxug.com', 'y3.analytics.yahoo.com', 'pipes.yahoo.com', 'search.yahoo.com', 'yahooapis.com', 'api-maps.yandex.ru', 'img-fotki.yandex.ru', 'yardbarker.com', 'yastatic.net', 'yellowpages.com', 'seatme.yelp.com', 'yelpcdn.com', 'yimg.com', 'yottaa.net', 'youku.com', 'youtube-nocookie.com', 'youwatch.org', 'ytimg.com', 'zap2it.com', 'zdassets.com', 'zencdn.net', 'zendesk.com', 'ziplist.com', 'zlcdn.com', 'zoho.com', 'zoho.eu', 'zohopublic.com', 'zohostatic.com', 'zombaio.com', 'zope.net', 'zopim.com', 'zvents.com']);
let trackersMap = new Map();
module.exports = {
  categories: {
    ADS: 1,
    SITE_ANALYTICS: 2,
    CUSTOMER_INTERACTION: 4,
    SOCIAL_MEDIA: 8,
    ESSENTIAL: 16,
    COOKIE: 32,
    UNKNOWN: 64
  },
  rulesets: {
    advertising: "advertising",
    //static category
    analytics: "analytics",
    //static category
    customer_interaction: "customer_interaction",
    //static category
    social_media: "social_media",
    //static category
    essential: "essential",
    //static category

    domain_cookies: "domain_cookies",
    //static category

    exceptions: "exceptions",
    //static category
    special_offers: "special_offers" //static category
  },
  rule_ids: {
    advertising: 10000,
    analytics: 20000,
    customer_interaction: 30000,
    social_media: 40000,
    essential: 50000,
    domain_cookies: 80000,
    exceptions: 100000,
    special_offers: 110000,
    user_exceptions: 150000,
    session_exceptions: 200000
  },
  rule_priorities: {
    domain_cookies: 1,
    categories: 2,
    exceptions: 10,
    special_offers: 100,
    user_exceptions: 150,
    session_exceptions: 200
  },
  categoryStringToId: function (categ) {
    switch (categ) {
      case "advertising":
        return this.categories.ADS;
      case "analytics":
        return this.categories.SITE_ANALYTICS;
      case "customer_interaction":
        return this.categories.CUSTOMER_INTERACTION;
      case "social_media":
        return this.categories.SOCIAL_MEDIA;
      case "essential":
        return this.categories.ESSENTIAL;
      case "domain_cookies":
        return this.categories.COOKIE;
    }
    return this.categories.UNKNOWN;
  },
  categoryIdToString: function (categ) {
    switch (categ) {
      case this.categories.ADS:
        return this.rulesets.advertising;
      case this.categories.SITE_ANALYTICS:
        return this.rulesets.analytics;
      case this.categories.CUSTOMER_INTERACTION:
        return this.rulesets.customer_interaction;
      case this.categories.SOCIAL_MEDIA:
        return this.rulesets.social_media;
      case this.categories.ESSENTIAL:
        return this.rulesets.essential;
      case this.categories.COOKIE:
        return this.rulesets.domain_cookies;
    }
    return "";
  },
  categoriesToRulesetOptions: function (categ) {
    let allCategories = [this.categories.ADS, this.categories.SITE_ANALYTICS, this.categories.CUSTOMER_INTERACTION, this.categories.SOCIAL_MEDIA, this.categories.ESSENTIAL, this.categories.COOKIE];
    let disableRulesetIds = [];
    let enableRulesetIds = [];
    allCategories.forEach(c => {
      if (categ & c) {
        enableRulesetIds.push(this.categoryIdToString(c));
      } else {
        disableRulesetIds.push(this.categoryIdToString(c));
      }
    });
    return {
      disableRulesetIds: disableRulesetIds,
      enableRulesetIds: enableRulesetIds
    };
  },
  urlListToAllowRulesOptions: function (urls, baseIndex, priority) {
    let addRules = [];
    let index = baseIndex;
    urls.forEach(url => {
      index++;
      addRules.push({
        "id": index,
        "priority": priority,
        "action": {
          "type": "allowAllRequests"
        },
        "condition": {
          "urlFilter": "||" + url,
          "resourceTypes": ["main_frame", "sub_frame"]
        }
      });
      index++;
      addRules.push({
        "id": index,
        "priority": priority,
        "action": {
          "type": "allowAllRequests"
        },
        "condition": {
          "initiatorDomains": [url],
          "resourceTypes": ["main_frame", "sub_frame"]
        }
      });
    });
    return {
      addRules: addRules
    };
  },
  urlFilterRulesToUrlList: function (rules) {
    let urls = [];
    rules.forEach(rule => {
      try {
        urls.push(rule.condition.urlFilter);
      } catch (ex) {}
    });
    return urls;
  },
  /**
   * 
   * @param {*} trackers_list 
   * @param {Number} category 
   */
  loadCatTrackers: function (trackers_list, category) {
    for (let i = 0; i < trackers_list.length; i++) {
      trackersMap.set(trackers_list[i], category);
    }
  },
  /**
   * 
   * @param {JSON} trackersJson 
   */
  loadTrackers: function (trackersJson) {
    if (undefined === trackersJson) {
      return;
    }
    trackersMap.clear();

    //advertising trackers
    if (trackersJson.hasOwnProperty('advertising')) {
      this.loadCatTrackers(trackersJson.advertising, this.categories.ADS);
    }

    //analytics trackers
    if (trackersJson.hasOwnProperty('analytics')) {
      this.loadCatTrackers(trackersJson.analytics, this.categories.SITE_ANALYTICS);
    }

    //customer_interaction trackers
    if (trackersJson.hasOwnProperty('customer_interaction')) {
      this.loadCatTrackers(trackersJson.customer_interaction, this.categories.CUSTOMER_INTERACTION);
    }

    //social_media trackers
    if (trackersJson.hasOwnProperty('social_media')) {
      this.loadCatTrackers(trackersJson.social_media, this.categories.SOCIAL_MEDIA);
    }

    //essential trackers
    if (trackersJson.hasOwnProperty('essential')) {
      this.loadCatTrackers(trackersJson.essential, this.categories.ESSENTIAL);
    }
  },
  /**
   * 
   * @param {String} url 
   * @param {Number} categories 
   */
  isTracker: function (url, categories) {
    if (null === url || 0 === trackersMap.size) {
      return this.categories.NO_FILTER;
    }
    for (let [tracker, cat] of trackersMap) {
      if (categories & cat) {
        if (new RegExp(tracker).test(url)) {
          return cat;
        }
      }
    }
    return this.categories.NO_FILTER;
  },
  /**
   * 
   * @param {String} domain 
   */
  blockDomainCookie: function (domain) {
    if (undefined === domain || null === domain) {
      return false;
    }
    if (cookiesSet.has(domain)) {
      return true;
    }
    return false;
  },
  getDomainCookies: function () {
    return Array.from(cookiesSet);
  },
  isThirdPartyDomainException: function (toHost, fromHost) {
    let ret = false;
    thirdPartyDomainExceptions.forEach(function (exc) {
      if (exc.from === fromHost || exc.from.includes('\\') && new RegExp(exc.from).test(fromHost)) {
        exc.to.forEach(function (toExc) {
          if (toExc === toHost || toExc.includes('\\') && new RegExp(toExc).test(toHost)) {
            ret = true;
          }
        });
      }
    });
    return ret;
  }
};

/***/ },

/***/ 585
(module) {

/**
 * Helpers.
 */

var s = 1000;
var m = s * 60;
var h = m * 60;
var d = h * 24;
var w = d * 7;
var y = d * 365.25;

/**
 * Parse or format the given `val`.
 *
 * Options:
 *
 *  - `long` verbose formatting [false]
 *
 * @param {String|Number} val
 * @param {Object} [options]
 * @throws {Error} throw an error if val is not a non-empty string or a number
 * @return {String|Number}
 * @api public
 */

module.exports = function(val, options) {
  options = options || {};
  var type = typeof val;
  if (type === 'string' && val.length > 0) {
    return parse(val);
  } else if (type === 'number' && isFinite(val)) {
    return options.long ? fmtLong(val) : fmtShort(val);
  }
  throw new Error(
    'val is not a non-empty string or a valid number. val=' +
      JSON.stringify(val)
  );
};

/**
 * Parse the given `str` and return milliseconds.
 *
 * @param {String} str
 * @return {Number}
 * @api private
 */

function parse(str) {
  str = String(str);
  if (str.length > 100) {
    return;
  }
  var match = /^(-?(?:\d+)?\.?\d+) *(milliseconds?|msecs?|ms|seconds?|secs?|s|minutes?|mins?|m|hours?|hrs?|h|days?|d|weeks?|w|years?|yrs?|y)?$/i.exec(
    str
  );
  if (!match) {
    return;
  }
  var n = parseFloat(match[1]);
  var type = (match[2] || 'ms').toLowerCase();
  switch (type) {
    case 'years':
    case 'year':
    case 'yrs':
    case 'yr':
    case 'y':
      return n * y;
    case 'weeks':
    case 'week':
    case 'w':
      return n * w;
    case 'days':
    case 'day':
    case 'd':
      return n * d;
    case 'hours':
    case 'hour':
    case 'hrs':
    case 'hr':
    case 'h':
      return n * h;
    case 'minutes':
    case 'minute':
    case 'mins':
    case 'min':
    case 'm':
      return n * m;
    case 'seconds':
    case 'second':
    case 'secs':
    case 'sec':
    case 's':
      return n * s;
    case 'milliseconds':
    case 'millisecond':
    case 'msecs':
    case 'msec':
    case 'ms':
      return n;
    default:
      return undefined;
  }
}

/**
 * Short format for `ms`.
 *
 * @param {Number} ms
 * @return {String}
 * @api private
 */

function fmtShort(ms) {
  var msAbs = Math.abs(ms);
  if (msAbs >= d) {
    return Math.round(ms / d) + 'd';
  }
  if (msAbs >= h) {
    return Math.round(ms / h) + 'h';
  }
  if (msAbs >= m) {
    return Math.round(ms / m) + 'm';
  }
  if (msAbs >= s) {
    return Math.round(ms / s) + 's';
  }
  return ms + 'ms';
}

/**
 * Long format for `ms`.
 *
 * @param {Number} ms
 * @return {String}
 * @api private
 */

function fmtLong(ms) {
  var msAbs = Math.abs(ms);
  if (msAbs >= d) {
    return plural(ms, msAbs, d, 'day');
  }
  if (msAbs >= h) {
    return plural(ms, msAbs, h, 'hour');
  }
  if (msAbs >= m) {
    return plural(ms, msAbs, m, 'minute');
  }
  if (msAbs >= s) {
    return plural(ms, msAbs, s, 'second');
  }
  return ms + ' ms';
}

/**
 * Pluralization helper.
 */

function plural(ms, msAbs, n, name) {
  var isPlural = msAbs >= n * 1.5;
  return Math.round(ms / n) + ' ' + name + (isPlural ? 's' : '');
}


/***/ },

/***/ 736
(module, __unused_webpack_exports, __webpack_require__) {


/**
 * This is the common logic for both the Node.js and web browser
 * implementations of `debug()`.
 */

function setup(env) {
	createDebug.debug = createDebug;
	createDebug.default = createDebug;
	createDebug.coerce = coerce;
	createDebug.disable = disable;
	createDebug.enable = enable;
	createDebug.enabled = enabled;
	createDebug.humanize = __webpack_require__(585);
	createDebug.destroy = destroy;

	Object.keys(env).forEach(key => {
		createDebug[key] = env[key];
	});

	/**
	* The currently active debug mode names, and names to skip.
	*/

	createDebug.names = [];
	createDebug.skips = [];

	/**
	* Map of special "%n" handling functions, for the debug "format" argument.
	*
	* Valid key names are a single, lower or upper-case letter, i.e. "n" and "N".
	*/
	createDebug.formatters = {};

	/**
	* Selects a color for a debug namespace
	* @param {String} namespace The namespace string for the debug instance to be colored
	* @return {Number|String} An ANSI color code for the given namespace
	* @api private
	*/
	function selectColor(namespace) {
		let hash = 0;

		for (let i = 0; i < namespace.length; i++) {
			hash = ((hash << 5) - hash) + namespace.charCodeAt(i);
			hash |= 0; // Convert to 32bit integer
		}

		return createDebug.colors[Math.abs(hash) % createDebug.colors.length];
	}
	createDebug.selectColor = selectColor;

	/**
	* Create a debugger with the given `namespace`.
	*
	* @param {String} namespace
	* @return {Function}
	* @api public
	*/
	function createDebug(namespace) {
		let prevTime;
		let enableOverride = null;
		let namespacesCache;
		let enabledCache;

		function debug(...args) {
			// Disabled?
			if (!debug.enabled) {
				return;
			}

			const self = debug;

			// Set `diff` timestamp
			const curr = Number(new Date());
			const ms = curr - (prevTime || curr);
			self.diff = ms;
			self.prev = prevTime;
			self.curr = curr;
			prevTime = curr;

			args[0] = createDebug.coerce(args[0]);

			if (typeof args[0] !== 'string') {
				// Anything else let's inspect with %O
				args.unshift('%O');
			}

			// Apply any `formatters` transformations
			let index = 0;
			args[0] = args[0].replace(/%([a-zA-Z%])/g, (match, format) => {
				// If we encounter an escaped % then don't increase the array index
				if (match === '%%') {
					return '%';
				}
				index++;
				const formatter = createDebug.formatters[format];
				if (typeof formatter === 'function') {
					const val = args[index];
					match = formatter.call(self, val);

					// Now we need to remove `args[index]` since it's inlined in the `format`
					args.splice(index, 1);
					index--;
				}
				return match;
			});

			// Apply env-specific formatting (colors, etc.)
			createDebug.formatArgs.call(self, args);

			const logFn = self.log || createDebug.log;
			logFn.apply(self, args);
		}

		debug.namespace = namespace;
		debug.useColors = createDebug.useColors();
		debug.color = createDebug.selectColor(namespace);
		debug.extend = extend;
		debug.destroy = createDebug.destroy; // XXX Temporary. Will be removed in the next major release.

		Object.defineProperty(debug, 'enabled', {
			enumerable: true,
			configurable: false,
			get: () => {
				if (enableOverride !== null) {
					return enableOverride;
				}
				if (namespacesCache !== createDebug.namespaces) {
					namespacesCache = createDebug.namespaces;
					enabledCache = createDebug.enabled(namespace);
				}

				return enabledCache;
			},
			set: v => {
				enableOverride = v;
			}
		});

		// Env-specific initialization logic for debug instances
		if (typeof createDebug.init === 'function') {
			createDebug.init(debug);
		}

		return debug;
	}

	function extend(namespace, delimiter) {
		const newDebug = createDebug(this.namespace + (typeof delimiter === 'undefined' ? ':' : delimiter) + namespace);
		newDebug.log = this.log;
		return newDebug;
	}

	/**
	* Enables a debug mode by namespaces. This can include modes
	* separated by a colon and wildcards.
	*
	* @param {String} namespaces
	* @api public
	*/
	function enable(namespaces) {
		createDebug.save(namespaces);
		createDebug.namespaces = namespaces;

		createDebug.names = [];
		createDebug.skips = [];

		let i;
		const split = (typeof namespaces === 'string' ? namespaces : '').split(/[\s,]+/);
		const len = split.length;

		for (i = 0; i < len; i++) {
			if (!split[i]) {
				// ignore empty strings
				continue;
			}

			namespaces = split[i].replace(/\*/g, '.*?');

			if (namespaces[0] === '-') {
				createDebug.skips.push(new RegExp('^' + namespaces.slice(1) + '$'));
			} else {
				createDebug.names.push(new RegExp('^' + namespaces + '$'));
			}
		}
	}

	/**
	* Disable debug output.
	*
	* @return {String} namespaces
	* @api public
	*/
	function disable() {
		const namespaces = [
			...createDebug.names.map(toNamespace),
			...createDebug.skips.map(toNamespace).map(namespace => '-' + namespace)
		].join(',');
		createDebug.enable('');
		return namespaces;
	}

	/**
	* Returns true if the given mode name is enabled, false otherwise.
	*
	* @param {String} name
	* @return {Boolean}
	* @api public
	*/
	function enabled(name) {
		if (name[name.length - 1] === '*') {
			return true;
		}

		let i;
		let len;

		for (i = 0, len = createDebug.skips.length; i < len; i++) {
			if (createDebug.skips[i].test(name)) {
				return false;
			}
		}

		for (i = 0, len = createDebug.names.length; i < len; i++) {
			if (createDebug.names[i].test(name)) {
				return true;
			}
		}

		return false;
	}

	/**
	* Convert regexp to namespace
	*
	* @param {RegExp} regxep
	* @return {String} namespace
	* @api private
	*/
	function toNamespace(regexp) {
		return regexp.toString()
			.substring(2, regexp.toString().length - 2)
			.replace(/\.\*\?$/, '*');
	}

	/**
	* Coerce `val`.
	*
	* @param {Mixed} val
	* @return {Mixed}
	* @api private
	*/
	function coerce(val) {
		if (val instanceof Error) {
			return val.stack || val.message;
		}
		return val;
	}

	/**
	* XXX DO NOT USE. This is a temporary stub function.
	* XXX It WILL be removed in the next major release.
	*/
	function destroy() {
		console.warn('Instance method `debug.destroy()` is deprecated and no longer does anything. It will be removed in the next major version of `debug`.');
	}

	createDebug.enable(createDebug.load());

	return createDebug;
}

module.exports = setup;


/***/ },

/***/ 833
(module, exports, __webpack_require__) {

/* eslint-env browser */

/**
 * This is the web browser implementation of `debug()`.
 */

exports.formatArgs = formatArgs;
exports.save = save;
exports.load = load;
exports.useColors = useColors;
exports.storage = localstorage();
exports.destroy = (() => {
	let warned = false;

	return () => {
		if (!warned) {
			warned = true;
			console.warn('Instance method `debug.destroy()` is deprecated and no longer does anything. It will be removed in the next major version of `debug`.');
		}
	};
})();

/**
 * Colors.
 */

exports.colors = [
	'#0000CC',
	'#0000FF',
	'#0033CC',
	'#0033FF',
	'#0066CC',
	'#0066FF',
	'#0099CC',
	'#0099FF',
	'#00CC00',
	'#00CC33',
	'#00CC66',
	'#00CC99',
	'#00CCCC',
	'#00CCFF',
	'#3300CC',
	'#3300FF',
	'#3333CC',
	'#3333FF',
	'#3366CC',
	'#3366FF',
	'#3399CC',
	'#3399FF',
	'#33CC00',
	'#33CC33',
	'#33CC66',
	'#33CC99',
	'#33CCCC',
	'#33CCFF',
	'#6600CC',
	'#6600FF',
	'#6633CC',
	'#6633FF',
	'#66CC00',
	'#66CC33',
	'#9900CC',
	'#9900FF',
	'#9933CC',
	'#9933FF',
	'#99CC00',
	'#99CC33',
	'#CC0000',
	'#CC0033',
	'#CC0066',
	'#CC0099',
	'#CC00CC',
	'#CC00FF',
	'#CC3300',
	'#CC3333',
	'#CC3366',
	'#CC3399',
	'#CC33CC',
	'#CC33FF',
	'#CC6600',
	'#CC6633',
	'#CC9900',
	'#CC9933',
	'#CCCC00',
	'#CCCC33',
	'#FF0000',
	'#FF0033',
	'#FF0066',
	'#FF0099',
	'#FF00CC',
	'#FF00FF',
	'#FF3300',
	'#FF3333',
	'#FF3366',
	'#FF3399',
	'#FF33CC',
	'#FF33FF',
	'#FF6600',
	'#FF6633',
	'#FF9900',
	'#FF9933',
	'#FFCC00',
	'#FFCC33'
];

/**
 * Currently only WebKit-based Web Inspectors, Firefox >= v31,
 * and the Firebug extension (any Firefox version) are known
 * to support "%c" CSS customizations.
 *
 * TODO: add a `localStorage` variable to explicitly enable/disable colors
 */

// eslint-disable-next-line complexity
function useColors() {
	// NB: In an Electron preload script, document will be defined but not fully
	// initialized. Since we know we're in Chrome, we'll just detect this case
	// explicitly
	if (typeof window !== 'undefined' && window.process && (window.process.type === 'renderer' || window.process.__nwjs)) {
		return true;
	}

	// Internet Explorer and Edge do not support colors.
	if (typeof navigator !== 'undefined' && navigator.userAgent && navigator.userAgent.toLowerCase().match(/(edge|trident)\/(\d+)/)) {
		return false;
	}

	// Is webkit? http://stackoverflow.com/a/16459606/376773
	// document is undefined in react-native: https://github.com/facebook/react-native/pull/1632
	return (typeof document !== 'undefined' && document.documentElement && document.documentElement.style && document.documentElement.style.WebkitAppearance) ||
		// Is firebug? http://stackoverflow.com/a/398120/376773
		(typeof window !== 'undefined' && window.console && (window.console.firebug || (window.console.exception && window.console.table))) ||
		// Is firefox >= v31?
		// https://developer.mozilla.org/en-US/docs/Tools/Web_Console#Styling_messages
		(typeof navigator !== 'undefined' && navigator.userAgent && navigator.userAgent.toLowerCase().match(/firefox\/(\d+)/) && parseInt(RegExp.$1, 10) >= 31) ||
		// Double check webkit in userAgent just in case we are in a worker
		(typeof navigator !== 'undefined' && navigator.userAgent && navigator.userAgent.toLowerCase().match(/applewebkit\/(\d+)/));
}

/**
 * Colorize log arguments if enabled.
 *
 * @api public
 */

function formatArgs(args) {
	args[0] = (this.useColors ? '%c' : '') +
		this.namespace +
		(this.useColors ? ' %c' : ' ') +
		args[0] +
		(this.useColors ? '%c ' : ' ') +
		'+' + module.exports.humanize(this.diff);

	if (!this.useColors) {
		return;
	}

	const c = 'color: ' + this.color;
	args.splice(1, 0, c, 'color: inherit');

	// The final "%c" is somewhat tricky, because there could be other
	// arguments passed either before or after the %c, so we need to
	// figure out the correct index to insert the CSS into
	let index = 0;
	let lastC = 0;
	args[0].replace(/%[a-zA-Z%]/g, match => {
		if (match === '%%') {
			return;
		}
		index++;
		if (match === '%c') {
			// We only are interested in the *last* %c
			// (the user may have provided their own)
			lastC = index;
		}
	});

	args.splice(lastC, 0, c);
}

/**
 * Invokes `console.debug()` when available.
 * No-op when `console.debug` is not a "function".
 * If `console.debug` is not available, falls back
 * to `console.log`.
 *
 * @api public
 */
exports.log = console.debug || console.log || (() => {});

/**
 * Save `namespaces`.
 *
 * @param {String} namespaces
 * @api private
 */
function save(namespaces) {
	try {
		if (namespaces) {
			exports.storage.setItem('debug', namespaces);
		} else {
			exports.storage.removeItem('debug');
		}
	} catch (error) {
		// Swallow
		// XXX (@Qix-) should we be logging these?
	}
}

/**
 * Load `namespaces`.
 *
 * @return {String} returns the previously persisted debug modes
 * @api private
 */
function load() {
	let r;
	try {
		r = exports.storage.getItem('debug');
	} catch (error) {
		// Swallow
		// XXX (@Qix-) should we be logging these?
	}

	// If debug isn't set in LS, and we're in Electron, try to load $DEBUG
	if (!r && typeof process !== 'undefined' && 'env' in process) {
		r = "bdat:*";
	}

	return r;
}

/**
 * Localstorage attempts to return the localstorage.
 *
 * This is necessary because safari throws
 * when a user disables cookies/localstorage
 * and you attempt to access it.
 *
 * @return {LocalStorage}
 * @api private
 */

function localstorage() {
	try {
		// TVMLKit (Apple TV JS Runtime) does not have a window object, just localStorage in the global context
		// The Browser also has localStorage in the global context.
		return localStorage;
	} catch (error) {
		// Swallow
		// XXX (@Qix-) should we be logging these?
	}
}

module.exports = __webpack_require__(736)(exports);

const {formatters} = module.exports;

/**
 * Map %j to `JSON.stringify()`, since no Web Inspectors do that by default.
 */

formatters.j = function (v) {
	try {
		return JSON.stringify(v);
	} catch (error) {
		return '[UnexpectedJSONParseError]: ' + error.message;
	}
};


/***/ }

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry needs to be wrapped in an IIFE because it needs to be in strict mode.
(() => {
"use strict";

// EXTERNAL MODULE: ./src/tracking/tracking.js
var tracking_tracking = __webpack_require__(177);
var tracking_default = /*#__PURE__*/__webpack_require__.n(tracking_tracking);
;// ./src/storage/defaults.js
let defaultState = {
  featureStatus: true,
  enabled: true,
  specialOffers: true,
  categories: 127,
  globalBlocked: 0,
  whitelist: [],
  mustSyncWhitelist: false,
  acceptedAppPolicy: false
};
function loadAndInitStoredState(callback) {
  chrome.storage.local.get(storedState => {
    let initialState = {
      ...defaultState,
      ...storedState
    };
    if (storedState) {
      if (storedState.whitelist && storedState.whitelist.length > 0) {
        if (!storedState.hasOwnProperty('mustSyncWhitelist')) {
          initialState.mustSyncWhitelist = true;
        }
      }
      if (!storedState.hasOwnProperty('acceptedAppPolicy')) {
        initialState.acceptedAppPolicy = false;
      }
    }
    callback(initialState);
  });
}
// EXTERNAL MODULE: ./node_modules/debug/src/browser.js
var browser = __webpack_require__(833);
var browser_default = /*#__PURE__*/__webpack_require__.n(browser);
;// ./src/logger/log.js

const BASE = 'bdat';
const COLOURS = {
  trace: 'lightblue',
  info: 'purple',
  warn: 'orange',
  error: 'red'
};
class BdLogging {
  constructor() {}
  restore() {
    chrome.storage.local.get('debug', value => {
      if (value) {
        if (value.hasOwnProperty('debug')) {
          let namespace = value['debug'];
          browser_default().enable(namespace);
        }
      }
    });
  }
  disable() {
    chrome.storage.local.remove('debug');
    browser_default().disable();
  }
  enable() {
    chrome.storage.local.set({
      'debug': 'bdat:*'
    });
    browser_default().enable('bdat:*');
  }
}
var bdLogging = self.bdLogging = new BdLogging();
if (false) // removed by dead control flow
{} else {
  bdLogging.restore();
}
class log_Log {
  constructor() {
    this.source = null;
  }
  init(source) {
    this.source = source;
  }
  generateMessage(level, message) {
    // Set the prefix which will cause debug to enable the message
    const namespace = `${BASE}:${level}`;
    const createDebug = browser_default()(namespace);

    // Set the colour of the message based on the level
    createDebug.color = COLOURS[level];
    if (this.source) {
      createDebug(this.source, message);
    } else {
      createDebug(message);
    }
  }
  trace(message) {
    return this.generateMessage('trace', message);
  }
  info(message) {
    return this.generateMessage('info', message);
  }
  warn(message) {
    return this.generateMessage('warn', message);
  }
  error(message) {
    return this.generateMessage('error', message);
  }
}
/* harmony default export */ const log = (new log_Log());
;// ./src/localization/locale_lang.js
/**
 * get lang Map
 * @param {*} langJson 
 */
function getLangMap(langJson) {
  let langMap = new Map();
  let keys = Object.keys(langJson);
  for (let index = 0; index < keys.length; index++) {
    let key = keys[index];
    if (null != key) {
      langMap.set(key, langJson[key]["message"]);
    }
  }
  return langMap;
}
function extensionLangFromProductLang(productLang) {
  let extensionLang = productLang;
  if (!extensionLang.startsWith('pt')) {
    extensionLang = extensionLang.substring(0, 2);
  } else {
    extensionLang = extensionLang.replace("-", "_");
  }
  return extensionLang;
}
class BdLang {
  constructor() {
    this.langMap = null;
  }
  init(_langMap) {
    this.langMap = _langMap;
  }
  getString(message) {
    if (null != this.langMap) {
      if (this.langMap.has(message)) {
        return this.langMap.get(message);
      }
    }
    return chrome.i18n.getMessage(message);
  }
}
/* harmony default export */ const locale_lang = (new BdLang());
;// ./src/utils/parseUrl.js

const emptyUrlParts = () => ({
  schema: '',
  hostname: '',
  port: '',
  pathname: '',
  search: '',
  hash: ''
});
/* harmony default export */ const parseUrl = (url => {
  if (null === url || '' === url) {
    return emptyUrlParts();
  }
  try {
    var uri = new URL(url);
    return {
      // URL.protocol keeps a trailing ':' (e.g. "https:"); strip it
      schema: uri.protocol.slice(0, -1),
      hostname: uri.hostname,
      port: uri.port,
      pathname: uri.pathname,
      search: uri.search,
      hash: uri.hash
    };
  } catch (ex) {
    log.warn('[parseUrl] invalid url "' + url + '": ' + ex);
  }
  return emptyUrlParts();
});
;// ./src/utils/domain.js
/**
 * Registrable-domain helper, replacing urijs's domain() so third-party
 * detection keeps the exact same behavior (see getDomain in helpers.js).
 * SLD list taken from URI.js v1.19.11 SecondLevelDomains.js (MIT License,
 * http://medialize.github.io/URI.js/).
 */

// list of known Second Level Domains
// converted list of SLDs from https://github.com/gavingmiller/second-level-domains
const SLD_LIST = {
  'ac': ' com gov mil net org ',
  'ae': ' ac co gov mil name net org pro sch ',
  'af': ' com edu gov net org ',
  'al': ' com edu gov mil net org ',
  'ao': ' co ed gv it og pb ',
  'ar': ' com edu gob gov int mil net org tur ',
  'at': ' ac co gv or ',
  'au': ' asn com csiro edu gov id net org ',
  'ba': ' co com edu gov mil net org rs unbi unmo unsa untz unze ',
  'bb': ' biz co com edu gov info net org store tv ',
  'bh': ' biz cc com edu gov info net org ',
  'bn': ' com edu gov net org ',
  'bo': ' com edu gob gov int mil net org tv ',
  'br': ' adm adv agr am arq art ato b bio blog bmd cim cng cnt com coop ecn edu eng esp etc eti far flog fm fnd fot fst g12 ggf gov imb ind inf jor jus lel mat med mil mus net nom not ntr odo org ppg pro psc psi qsl rec slg srv tmp trd tur tv vet vlog wiki zlg ',
  'bs': ' com edu gov net org ',
  'bz': ' du et om ov rg ',
  'ca': ' ab bc mb nb nf nl ns nt nu on pe qc sk yk ',
  'ck': ' biz co edu gen gov info net org ',
  'cn': ' ac ah bj com cq edu fj gd gov gs gx gz ha hb he hi hl hn jl js jx ln mil net nm nx org qh sc sd sh sn sx tj tw xj xz yn zj ',
  'co': ' com edu gov mil net nom org ',
  'cr': ' ac c co ed fi go or sa ',
  'cy': ' ac biz com ekloges gov ltd name net org parliament press pro tm ',
  'do': ' art com edu gob gov mil net org sld web ',
  'dz': ' art asso com edu gov net org pol ',
  'ec': ' com edu fin gov info med mil net org pro ',
  'eg': ' com edu eun gov mil name net org sci ',
  'er': ' com edu gov ind mil net org rochest w ',
  'es': ' com edu gob nom org ',
  'et': ' biz com edu gov info name net org ',
  'fj': ' ac biz com info mil name net org pro ',
  'fk': ' ac co gov net nom org ',
  'fr': ' asso com f gouv nom prd presse tm ',
  'gg': ' co net org ',
  'gh': ' com edu gov mil org ',
  'gn': ' ac com gov net org ',
  'gr': ' com edu gov mil net org ',
  'gt': ' com edu gob ind mil net org ',
  'gu': ' com edu gov net org ',
  'hk': ' com edu gov idv net org ',
  'hu': ' 2000 agrar bolt casino city co erotica erotika film forum games hotel info ingatlan jogasz konyvelo lakas media news org priv reklam sex shop sport suli szex tm tozsde utazas video ',
  'id': ' ac co go mil net or sch web ',
  'il': ' ac co gov idf k12 muni net org ',
  'in': ' ac co edu ernet firm gen gov i ind mil net nic org res ',
  'iq': ' com edu gov i mil net org ',
  'ir': ' ac co dnssec gov i id net org sch ',
  'it': ' edu gov ',
  'je': ' co net org ',
  'jo': ' com edu gov mil name net org sch ',
  'jp': ' ac ad co ed go gr lg ne or ',
  'ke': ' ac co go info me mobi ne or sc ',
  'kh': ' com edu gov mil net org per ',
  'ki': ' biz com de edu gov info mob net org tel ',
  'km': ' asso com coop edu gouv k medecin mil nom notaires pharmaciens presse tm veterinaire ',
  'kn': ' edu gov net org ',
  'kr': ' ac busan chungbuk chungnam co daegu daejeon es gangwon go gwangju gyeongbuk gyeonggi gyeongnam hs incheon jeju jeonbuk jeonnam k kg mil ms ne or pe re sc seoul ulsan ',
  'kw': ' com edu gov net org ',
  'ky': ' com edu gov net org ',
  'kz': ' com edu gov mil net org ',
  'lb': ' com edu gov net org ',
  'lk': ' assn com edu gov grp hotel int ltd net ngo org sch soc web ',
  'lr': ' com edu gov net org ',
  'lv': ' asn com conf edu gov id mil net org ',
  'ly': ' com edu gov id med net org plc sch ',
  'ma': ' ac co gov m net org press ',
  'mc': ' asso tm ',
  'me': ' ac co edu gov its net org priv ',
  'mg': ' com edu gov mil nom org prd tm ',
  'mk': ' com edu gov inf name net org pro ',
  'ml': ' com edu gov net org presse ',
  'mn': ' edu gov org ',
  'mo': ' com edu gov net org ',
  'mt': ' com edu gov net org ',
  'mv': ' aero biz com coop edu gov info int mil museum name net org pro ',
  'mw': ' ac co com coop edu gov int museum net org ',
  'mx': ' com edu gob net org ',
  'my': ' com edu gov mil name net org sch ',
  'nf': ' arts com firm info net other per rec store web ',
  'ng': ' biz com edu gov mil mobi name net org sch ',
  'ni': ' ac co com edu gob mil net nom org ',
  'np': ' com edu gov mil net org ',
  'nr': ' biz com edu gov info net org ',
  'om': ' ac biz co com edu gov med mil museum net org pro sch ',
  'pe': ' com edu gob mil net nom org sld ',
  'ph': ' com edu gov i mil net ngo org ',
  'pk': ' biz com edu fam gob gok gon gop gos gov net org web ',
  'pl': ' art bialystok biz com edu gda gdansk gorzow gov info katowice krakow lodz lublin mil net ngo olsztyn org poznan pwr radom slupsk szczecin torun warszawa waw wroc wroclaw zgora ',
  'pr': ' ac biz com edu est gov info isla name net org pro prof ',
  'ps': ' com edu gov net org plo sec ',
  'pw': ' belau co ed go ne or ',
  'ro': ' arts com firm info nom nt org rec store tm www ',
  'rs': ' ac co edu gov in org ',
  'sb': ' com edu gov net org ',
  'sc': ' com edu gov net org ',
  'sh': ' co com edu gov net nom org ',
  'sl': ' com edu gov net org ',
  'st': ' co com consulado edu embaixada gov mil net org principe saotome store ',
  'sv': ' com edu gob org red ',
  'sz': ' ac co org ',
  'tr': ' av bbs bel biz com dr edu gen gov info k12 name net org pol tel tsk tv web ',
  'tt': ' aero biz cat co com coop edu gov info int jobs mil mobi museum name net org pro tel travel ',
  'tw': ' club com ebiz edu game gov idv mil net org ',
  'mu': ' ac co com gov net or org ',
  'mz': ' ac co edu gov org ',
  'na': ' co com ',
  'nz': ' ac co cri geek gen govt health iwi maori mil net org parliament school ',
  'pa': ' abo ac com edu gob ing med net nom org sld ',
  'pt': ' com edu gov int net nome org publ ',
  'py': ' com edu gov mil net org ',
  'qa': ' com edu gov mil net org ',
  're': ' asso com nom ',
  'ru': ' ac adygeya altai amur arkhangelsk astrakhan bashkiria belgorod bir bryansk buryatia cbg chel chelyabinsk chita chukotka chuvashia com dagestan e-burg edu gov grozny int irkutsk ivanovo izhevsk jar joshkar-ola kalmykia kaluga kamchatka karelia kazan kchr kemerovo khabarovsk khakassia khv kirov koenig komi kostroma kranoyarsk kuban kurgan kursk lipetsk magadan mari mari-el marine mil mordovia mosreg msk murmansk nalchik net nnov nov novosibirsk nsk omsk orenburg org oryol penza perm pp pskov ptz rnd ryazan sakhalin samara saratov simbirsk smolensk spb stavropol stv surgut tambov tatarstan tom tomsk tsaritsyn tsk tula tuva tver tyumen udm udmurtia ulan-ude vladikavkaz vladimir vladivostok volgograd vologda voronezh vrn vyatka yakutia yamal yekaterinburg yuzhno-sakhalinsk ',
  'rw': ' ac co com edu gouv gov int mil net ',
  'sa': ' com edu gov med net org pub sch ',
  'sd': ' com edu gov info med net org tv ',
  'se': ' a ac b bd c d e f g h i k l m n o org p parti pp press r s t tm u w x y z ',
  'sg': ' com edu gov idn net org per ',
  'sn': ' art com edu gouv org perso univ ',
  'sy': ' com edu gov mil net news org ',
  'th': ' ac co go in mi net or ',
  'tj': ' ac biz co com edu go gov info int mil name net nic org test web ',
  'tn': ' agrinet com defense edunet ens fin gov ind info intl mincom nat net org perso rnrt rns rnu tourism ',
  'tz': ' ac co go ne or ',
  'ua': ' biz cherkassy chernigov chernovtsy ck cn co com crimea cv dn dnepropetrovsk donetsk dp edu gov if in ivano-frankivsk kh kharkov kherson khmelnitskiy kiev kirovograd km kr ks kv lg lugansk lutsk lviv me mk net nikolaev od odessa org pl poltava pp rovno rv sebastopol sumy te ternopil uzhgorod vinnica vn zaporizhzhe zhitomir zp zt ',
  'ug': ' ac co go ne or org sc ',
  'uk': ' ac bl british-library co cym gov govt icnet jet lea ltd me mil mod national-library-scotland nel net nhs nic nls org orgn parliament plc police sch scot soc ',
  'us': ' dni fed isa kids nsn ',
  'uy': ' com edu gub mil net org ',
  've': ' co com edu gob info mil net org web ',
  'vi': ' co com k12 net org ',
  'vn': ' ac biz com edu gov health info int name net org pro ',
  'ye': ' co com gov ltd me net org plc ',
  'yu': ' ac co edu gov org ',
  'za': ' ac agric alt bourse city co cybernet db edu gov grondar iaccess imt inca landesign law mil net ngo nis nom olivetti org pix school tm web ',
  'zm': ' ac co com edu gov net org sch ',
  // https://en.wikipedia.org/wiki/CentralNic#Second-level_domains
  'com': 'ar br cn de eu gb gr hu jpn kr no qc ru sa se uk us uy za ',
  'net': 'gb jp se uk ',
  'org': 'ae',
  'de': 'com '
};
function isIpHostname(hostname) {
  if (hostname.indexOf(':') >= 0) {
    // IPv6 literal ("[::1]" from URL.hostname, or a raw one)
    return true;
  }
  // deliberately loose — identical to URI.js ip4_expression; input comes
  // from URL.hostname, so this classifies IP-shaped strings rather than
  // validating octet ranges (keeps parity with the urijs behavior)
  return /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(hostname);
}

// same semantics as URI.js SecondLevelDomains.get(): returns "co.uk" for
// "www.example.co.uk" when the last two labels are a known SLD pair
function getSld(hostname) {
  const tldOffset = hostname.lastIndexOf('.');
  if (tldOffset <= 0 || tldOffset >= hostname.length - 1) {
    return null;
  }
  const sldOffset = hostname.lastIndexOf('.', tldOffset - 1);
  if (sldOffset <= 0 || sldOffset >= tldOffset - 1) {
    return null;
  }
  const sldList = SLD_LIST[hostname.slice(tldOffset + 1)];
  if (!sldList) {
    return null;
  }
  if (sldList.indexOf(' ' + hostname.slice(sldOffset + 1, tldOffset) + ' ') < 0) {
    return null;
  }
  return hostname.slice(sldOffset + 1);
}

/**
 * Same semantics as URI.js domain(): "example.org" from "www.example.org",
 * "example.co.uk" from "www.example.co.uk", '' for IPs and empty hostnames.
 * @param {String} hostname
 */
function getRegistrableDomain(hostname) {
  if (!hostname || isIpHostname(hostname)) {
    return '';
  }

  // if hostname consists of 1 or 2 segments, it must be the domain
  const dots = hostname.match(/\./g);
  if (!dots || dots.length < 2) {
    return hostname;
  }

  // grab tld and add another segment
  const pos = hostname.lastIndexOf('.');
  let tld = hostname.substring(pos + 1);
  if (SLD_LIST[tld.toLowerCase()]) {
    tld = getSld(hostname) || tld;
  }
  let end = hostname.length - tld.length - 1;
  end = hostname.lastIndexOf('.', end - 1) + 1;
  return hostname.substring(end) || '';
}
;// ./src/scripts/compat.js
/**
 * Manifest v3 and v2 compatibility
 */
class compat_compat {
  constructor() {
    this.action = this.getBrowserAction();
    this.dnr = {
      available: this.getDnrAvailable(),
      debug: {
        available: this.getDnrDebugAvailable()
      },
      action: {
        available: this.getDnrActionAvailable()
      },
      rules: {
        rulesets: {
          available: this.getDnrRulesetsAvailable()
        },
        dynamic: {
          available: this.getDnrDynamicRulesAvailable()
        },
        session: {
          available: this.getDnrSessionRulesAvailable()
        }
      },
      declarativeNetRequest: this.getDnrApi()
    };
  }
  getDnrApi = () => {
    if (true) {
      if (typeof chrome.declarativeNetRequest !== 'undefined') return chrome.declarativeNetRequest;
    }
    return undefined;
  };
  getDnrAvailable = () => {
    return typeof this.getDnrApi() !== 'undefined';
  };
  getDnrDebugAvailable = () => {
    return this.getDnrAvailable() && typeof this.getDnrApi().onRuleMatchedDebug !== 'undefined';
  };
  getDnrActionAvailable = () => {
    return this.getDnrAvailable() && typeof this.getDnrApi().setExtensionActionOptions !== 'undefined';
  };
  getDnrRulesetsAvailable = () => {
    return this.getDnrAvailable() && typeof this.getDnrApi().updateEnabledRulesets !== 'undefined';
  };
  getDnrDynamicRulesAvailable = () => {
    return this.getDnrAvailable() && typeof this.getDnrApi().updateDynamicRules !== 'undefined';
  };
  getDnrSessionRulesAvailable = () => {
    return this.getDnrAvailable() && typeof this.getDnrApi().updateSessionRules !== 'undefined';
  };
  getBrowserAction = () => {
    if (typeof chrome.action !== 'undefined') {
      return chrome.action;
    }
    if (typeof chrome.browserAction !== 'undefined') {
      return chrome.browserAction;
    }
    return null;
  };
  executeScript(tabId, frameIds, files, callback) {
    if (typeof chrome.scripting !== 'undefined') {
      chrome.scripting.executeScript({
        target: {
          tabId: tabId,
          frameIds: frameIds
        },
        files: files
      }, callback);
      return;
    }
    if (typeof chrome.tabs.executeScript !== 'undefined') {
      frameIds.forEach(frameId => {
        files.forEach(file => {
          chrome.tabs.executeScript(tabId, {
            file: file,
            frameId: frameId
          }, callback);
        });
      });
      return;
    }
  }
}
/* harmony default export */ const scripts_compat = (new compat_compat());
;// ./src/utils/helpers.js






/**
 * helpers functions
 */

//chrome.extension.getBackgroundPage().
function CategoryInfo() {
  this.name = '';
  this.blocked = '';
  this.icon = '';
  this.className = '';
}
function setCategoryInfo(bdLang, catTitle, pageTitle, catIcon, catClassName) {
  let catInfo = new CategoryInfo();
  catInfo.name = bdLang.getString(catTitle);
  catInfo.blocked = bdLang.getString(pageTitle);
  catInfo.icon = catIcon;
  catInfo.className = catClassName;
  return catInfo;
}
function setCategoryStatus(bdLang, catStatus, catEnabled, catDisabled) {
  let status = '';
  if (catStatus) {
    status = bdLang.getString(catEnabled);
  } else {
    status = bdLang.getString(catDisabled);
  }
  return status;
}

/**
 * get trackers category name
 * @param {*} trackerCategoryType 
 */
function getTrackerCategoryName(bdLang, trackerCategoryType) {
  let catInfo = new CategoryInfo();
  switch (trackerCategoryType) {
    case '1':
      {
        catInfo = setCategoryInfo(bdLang, 'advertising_category_title', 'advertising_page_title', 'advertising-icon', 'category-trackers-list advertising');
        break;
      }
    case '2':
      {
        catInfo = setCategoryInfo(bdLang, 'analytics_category_title', 'analytics_page_title', 'analytics-icon', 'category-trackers-list analytics');
        break;
      }
    case '4':
      {
        catInfo = setCategoryInfo(bdLang, 'interaction_category_title', 'interaction_page_title', 'customer-icon', 'category-trackers-list customer');
        break;
      }
    case '8':
      {
        catInfo = setCategoryInfo(bdLang, 'social_category_title', 'social_page_title', 'social-icon', 'category-trackers-list social');
        break;
      }
    case '16':
      {
        catInfo = setCategoryInfo(bdLang, 'essential_category_title', 'essential_page_title', 'essentials-icon', 'category-trackers-list essentials');
        break;
      }
    case '32':
      {
        catInfo = setCategoryInfo(bdLang, 'cookies_category_title', 'cookies_page_title', 'cookies-icon', 'category-trackers-list cookies');
        break;
      }
  }
  return catInfo;
}

/**
 * getTrackerCategoryDescription
 * @param {*} trackerCategoryType 
 */
function getTrackerCategoryDescription(bdLang, trackerCategoryType) {
  let description = '';
  switch (trackerCategoryType) {
    case '1':
      {
        description = bdLang.getString("advertising_category_desc");
        break;
      }
    case '2':
      {
        description = bdLang.getString("analytics_category_desc");
        break;
      }
    case '4':
      {
        description = bdLang.getString("interaction_category_desc");
        break;
      }
    case '8':
      {
        description = bdLang.getString("social_category_desc");
        break;
      }
    case '16':
      {
        description = bdLang.getString("essential_category_desc");
        break;
      }
    case '32':
      {
        description = bdLang.getString("cookies_category_desc");
        break;
      }
  }
  return description;
}

/**
 * getTrackerCategoryTooltip
 * @param {*} trackerCategoryType 
 */
function getTrackerCategoryTooltip(bdLang, trackerCategoryType) {
  let tooltip = '';
  switch (trackerCategoryType) {
    case '1':
      {
        tooltip = bdLang.getString("advertising_category_tooltip");
        break;
      }
    case '2':
      {
        tooltip = bdLang.getString("analytics_category_tooltip");
        break;
      }
    case '4':
      {
        tooltip = bdLang.getString("interaction_category_tooltip");
        break;
      }
    case '8':
      {
        tooltip = bdLang.getString("social_category_tooltip");
        break;
      }
    case '16':
      {
        tooltip = bdLang.getString("essential_category_tooltip");
        break;
      }
    case '32':
      {
        tooltip = bdLang.getString("cookies_category_tooltip");
        break;
      }
  }
  return tooltip;
}

/**
 * getTrackerCategoryStatus
 * @param {*} trackerCategoryStatus 
 */
function getTrackerCategoryStatus(bdLang, trackerCategoryType, trackerCategoryStatus) {
  let status = '';
  switch (trackerCategoryType) {
    case '1':
      {
        status = setCategoryStatus(bdLang, trackerCategoryStatus, 'advertising_page_button_block', 'advertising_page_button_unblock');
        break;
      }
    case '2':
      {
        status = setCategoryStatus(bdLang, trackerCategoryStatus, 'analytics_page_button_block', 'analytics_page_button_unblock');
        break;
      }
    case '4':
      {
        status = setCategoryStatus(bdLang, trackerCategoryStatus, 'interaction_page_button_block', 'interaction_page_button_unblock');
        break;
      }
    case '8':
      {
        status = setCategoryStatus(bdLang, trackerCategoryStatus, 'social_page_button_block', 'social_page_button_unblock');
        break;
      }
    case '16':
      {
        status = setCategoryStatus(bdLang, trackerCategoryStatus, 'essential_page_button_block', 'essential_page_button_unblock');
        break;
      }
    case '32':
      {
        status = setCategoryStatus(bdLang, trackerCategoryStatus, 'cookies_page_button_block', 'cookies_page_button_unblock');
        break;
      }
  }
  return status;
}
function getTrackerPieCountText(trackersBlocked) {
  if (trackersBlocked >= 99000) return "99k";
  if (trackersBlocked >= 1000) return Math.floor(trackersBlocked / 1000) + "k";
  return trackersBlocked.toString();
}
function setBadgeColor() {
  scripts_compat.action.setBadgeBackgroundColor({
    color: "rgb(0,0,255)"
  });
}

/* setBadgeMessage
 * @param {*} currentTabId, nrTrackers
 */
function setBadgeMessage(currentTabId, nrTrackers) {
  scripts_compat.action.setBadgeText({
    text: nrTrackers.toString(),
    tabId: currentTabId
  });
}
function clearBadgeMessage(currentTabId) {
  compat.action.setBadgeText({
    text: "",
    tabId: currentTabId
  });
}
function getBadgeMessage(currentTabId, callback) {
  compat.action.getBadgeText({
    tabId: currentTabId
  }, result => {
    callback(result);
  });
}
function dnrSetBadgeMessageFromMatchedRules(currentTabId) {
  if (compat.dnr.available) {
    Log.warn('[dnr] v3 dnrSetBadgeMessageFromMatchedRules');
    compat.dnr.declarativeNetRequest.getMatchedRules({
      tabId: currentTabId
    }, rulesMatchedDetails => {
      if (rulesMatchedDetails) {
        Log.warn('[dnr] dnrSetBadgeMessageFromMatchedRules: ' + JSON.stringify(rulesMatchedDetails, null, 4));
        let trackersBlocked = 0;
        rulesMatchedDetails.rulesMatchedInfo.forEach(match => {
          switch (tracking.categoryStringToId(match.rule.rulesetId)) {
            case tracking.categories.ADS:
              trackersBlocked++;
              break;
            case tracking.categories.SITE_ANALYTICS:
              trackersBlocked++;
              break;
            case tracking.categories.CUSTOMER_INTERACTION:
              trackersBlocked++;
              break;
            case tracking.categories.SOCIAL_MEDIA:
              trackersBlocked++;
              break;
            case tracking.categories.ESSENTIAL:
              trackersBlocked++;
              break;
            case tracking.categories.COOKIE:
              trackersBlocked++;
              break;
          }
        });
        if (trackersBlocked > 0) {
          setBadgeMessage(currentTabId, trackersBlocked);
        } else {
          clearBadgeMessage(currentTabId);
        }
      }
    });
  }
}
const TAB_INFO_TRANSITION = {
  COMMITED: 1,
  PROVISIONAL: 2
};
function copyTabInfo(inputTabInfo) {
  let outputTabInfo = {
    'transition': TAB_INFO_TRANSITION.COMMITED,
    'url': '',
    'trackersBlocked': 0,
    'pageLoad': 0,
    'pageLoadStartTime': 0,
    'trackersMap': {},
    'trackersUrls': []
  };
  if (inputTabInfo !== undefined) {
    outputTabInfo = {
      'transition': inputTabInfo.transition,
      'url': inputTabInfo.url,
      'trackersBlocked': inputTabInfo.trackersBlocked,
      'pageLoad': inputTabInfo.pageLoad,
      'pageLoadStartTime': inputTabInfo.pageLoadStartTime,
      'trackersMap': inputTabInfo.trackersMap,
      'trackersUrls': inputTabInfo.trackersUrls
    };
  }
  return outputTabInfo;
}
function copyTabStack(inputTabStack) {
  let outputTabStack = [];
  if (inputTabStack !== undefined) {
    for (let i = 0; i < inputTabStack.length; i++) {
      let outputTabInfo = copyTabInfo(inputTabStack[i]);
      outputTabStack[i] = outputTabInfo;
    }
  }
  return outputTabStack;
}
function getTabStackTrackersBlocked(inputTabStack) {
  let trackersBlocked = 0;
  if (inputTabStack !== undefined) {
    for (let i = 0; i < inputTabStack.length; i++) {
      trackersBlocked += inputTabStack[i].trackersBlocked;
    }
  }
  return trackersBlocked;
}

/* updateUiStack
 * @param {*} tabId, inputTabStack, whitelist
 */
function updateUiStack(tabId, inputTabStack, whitelist) {
  chrome.tabs.query({
    active: true,
    currentWindow: true
  }, tabs => {
    if (!tabs || !tabs.length) {
      return;
    }
    if (null != tabs && null != tabs[0]) {
      if (tabId === tabs[0].id && null != inputTabStack) {
        let inputTabInfo = inputTabStack[0];
        if (null != inputTabInfo) {
          let trackersBlocked = getTabStackTrackersBlocked(inputTabStack);
          let objectTabStack = copyTabStack(inputTabStack);
          if (canBlockWebRequest()) {
            setBadgeMessage(tabId, trackersBlocked);
          }
          chrome.runtime.sendMessage({
            type: 'update_tab_stack',
            tabStack: objectTabStack,
            sessionWhitelist: whitelist
          }, () => {
            //need to check lastError to prevent error being displayed in the
            //browser extension page when there is no content script loaded in tab
            chrome.runtime.lastError;
          });
        }
      }
    }
  });
}

/* updateUiLoadTime
 * @param {*} tabId, inputTabStack
 */
function updateUiPageLoad(tabId, inputTabStack) {
  chrome.tabs.query({
    active: true,
    currentWindow: true
  }, tabs => {
    if (!tabs || !tabs.length) {
      return;
    }
    if (null != tabs && null != tabs[0]) {
      if (tabId === tabs[0].id && null != inputTabStack) {
        let inputTabInfo = inputTabStack[0];
        if (null != inputTabInfo) {
          let objectTabStack = copyTabStack(inputTabStack);
          chrome.runtime.sendMessage({
            type: 'update_page_load',
            tabStack: objectTabStack
          }, () => {
            //need to check lastError to prevent error being displayed in the
            //browser extension page when there is no content script loaded in tab
            chrome.runtime.lastError;
          });
        }
      }
    }
  });
}

/* getTelemetryJson
 * @param {*} telemetry_type, telemetry_value
 */
function getTelemetryJson(telemetry_type, telemetry_value) {
  var telemetry_json = {
    'method': 'send_telemetry',
    'browser_context': getBrowserContext()
  };
  var telemetry_info = {
    'type': telemetry_type,
    'value': telemetry_value
  };
  telemetry_json['telemetry_info'] = telemetry_info;
  return telemetry_json;
}

/* isBdTrackingIds
 * @param  tab_url: cirrent tab url
 * @param  scan_url: current scan url
 */
function isBdTrackingIds(tab_url, scan_url) {
  let scan_url_lower = scan_url.toLowerCase();
  if (tab_url.toLowerCase().includes('bitdefender') || scan_url_lower.includes('bitdefender')) {
    return true;
  }
  if (scan_url_lower.includes('assets.adobedtm.com/launch-en6b51aa9552f941f88576315ed8766e3f')) {
    return true;
  }
  if (scan_url_lower.includes('assets.adobedtm.com/4b7ac0a30c6cfe2deb06368f62d41f996c29744e/satelliteLib-3a8d5287cf775324dc6c68719a1ddc96c5a139ba')) {
    return true;
  }
  if (scan_url_lower.includes('gtm-pljjb3') || scan_url_lower.includes('gtm-mq8rtn')) {
    return true;
  }
  if (scan_url_lower.includes('assets.adobedtm.com/launch-ENa82c50bdc4c541bdb7d581931510efc5')) {
    return true;
  }
  if (scan_url_lower.includes('assets.adobedtm.com/8a93f8486ba4/62c1fd5cdcbd/launch-b77a56f2d5f1')) {
    return true;
  }
  if (scan_url_lower.includes('assets.adobedtm.com/8a93f8486ba4/0f17a64d87b7/launch-c3512379eccf')) {
    return true;
  }
  if (scan_url_lower.includes('assets.adobedtm.com/8a93f8486ba4/5492896ad67e/launch-b1f76be4d2ee')) {
    return true;
  }
  if (scan_url_lower.includes('assets.adobedtm.com/extensions/EP308220a2a4c4403f97fc1960100db40f/AppMeasurement')) {
    return true;
  }
  if (scan_url_lower.includes('assets.adobedtm.com/extensions/EP308220a2a4c4403f97fc1960100db40f/AppMeasurement_Module_AudienceManagement')) {
    return true;
  }
  if (scan_url_lower.includes('assets.adobedtm.com/extensions/EPef068a8d6dd34a43866d9a80cc98baab/AppMeasurement')) {
    return true;
  }
  if (scan_url_lower.includes('assets.adobedtm.com/extensions/EPef068a8d6dd34a43866d9a80cc98baab/AppMeasurement_Module_ActivityMap')) {
    return true;
  }
  if (scan_url_lower.includes('assets.adobedtm.com/8a93f8486ba4/df27e7ff35f3/6ad1b33eca05/RC22febb28520c43e3af9acfb4f9bfa34f')) {
    return true;
  }
  return false;
}

/* TabInfo
 * @param null
 */
function TabInfo() {
  this.transition = TAB_INFO_TRANSITION.COMMITED;
  this.url = '';
  this.trackersBlocked = 0;
  this.pageLoad = 0;
  this.pageLoadStartTime = 0;
  this.trackersMap = {};
  this.trackersUrls = [];
}
const SCREEN_UI = {
  MAIN: 1,
  CATEGORY: 2,
  SETTINGS: 4
};
const TELEMETRY_EVENT_TYPE = {
  ENABLED: 0,
  PAUSE: 1,
  ADVERTISING: 2,
  ANALYTICS: 3,
  INTERACTION: 4,
  SOCIAL_MEDIA: 5,
  ESSENTIAL: 6,
  SPECIAL_OFFERS: 7
};
const BROWSER_CONTEXT = {
  BROWSER_CONTEXT_ALL: 0,
  BROWSER_CONTEXT_CHROME: 1,
  BROWSER_CONTEXT_FIREFOX: 2,
  BROWSER_CONTEXT_EDGE_CHROMIUM: 3,
  BROWSER_CONTEXT_IE: 4,
  BROWSER_CONTEXT_IE64: 5,
  BROWSER_CONTEXT_UNKNOWN: 6
};

/* getPathFromUrl
 * @param {String} url
 */
function getPathFromUrl(url) {
  return url.split(/[?#]/)[0];
}
function getTabUrl(url) {
  if (undefined !== url) {
    if (url.startsWith('file:')) {
      return url;
    } else {
      return parseUrl(url).hostname;
    }
  }
  return url;
}
function getBrowserContext() {
  try {
    let browserContextName = "chrome";
    if (browserContextName.toLowerCase() === 'edge') {
      return BROWSER_CONTEXT.BROWSER_CONTEXT_EDGE_CHROMIUM;
    }
    if (browserContextName.toLowerCase() === 'chrome') {
      return BROWSER_CONTEXT.BROWSER_CONTEXT_CHROME;
    }
    if (browserContextName.toLowerCase() === 'firefox') {
      return BROWSER_CONTEXT.BROWSER_CONTEXT_FIREFOX;
    }
  } catch (ex) {}
  try {
    let internalUrl = chrome.runtime.getURL("home.html");
    if (internalUrl.toLowerCase().startsWith('moz-extension')) {
      return BROWSER_CONTEXT.BROWSER_CONTEXT_FIREFOX;
    }
    if (internalUrl.toLowerCase().startsWith('extension://')) {
      return BROWSER_CONTEXT.BROWSER_CONTEXT_EDGE_CHROMIUM;
    }
    if (internalUrl.toLowerCase().startsWith('chrome-extension://')) {
      return BROWSER_CONTEXT.BROWSER_CONTEXT_CHROME;
    }
    return BROWSER_CONTEXT_EDGE_CHROMIUM;
  } catch (ex) {}
  if ('bdtbe@bitdefender.com' === chrome.runtime.id) {
    return BROWSER_CONTEXT.BROWSER_CONTEXT_FIREFOX;
  }
  return BROWSER_CONTEXT.BROWSER_CONTEXT_UNKNOWN;
}
function canBlockWebRequest() {
  const browserContext = getBrowserContext();
  if (browserContext === BROWSER_CONTEXT.BROWSER_CONTEXT_CHROME || browserContext === BROWSER_CONTEXT.BROWSER_CONTEXT_EDGE_CHROMIUM) {
    return false;
  }
  return true;
}

/**
 * 
 * @param {String} host_name 
 */
function getDomain(host_name) {
  var hostname = '';
  try {
    hostname = new URL(host_name).hostname;
  } catch (ex) {}
  if ('' === hostname) {
    //input is usually a bare hostname, without a scheme
    try {
      hostname = new URL('https://' + host_name).hostname;
    } catch (ex) {}
  }
  var domain = getRegistrableDomain(hostname);
  log.info('getDomain: [' + host_name + '] [' + domain + ']');
  return domain;
}

/**
 * 
 * @param {String} request_host 
 * @param {String} tab_host 
 */
function isThirdPartyDomain(request_host, tab_host) {
  var ret = true;
  if (null === request_host || null === tab_host) {
    ret = false;
  } else {
    ret = getDomain(request_host) !== getDomain(tab_host);
  }
  if (ret) {
    if (tracking_default().isThirdPartyDomainException(request_host, tab_host)) {
      log.info('isThirdPartyDomainException: [' + request_host + '] <- [' + tab_host + ']');
      ret = false;
    }
  }
  log.info('isThirdPartyDomain: [' + request_host + '] <- [' + tab_host + '] [' + ret + ']');
  return ret;
}
function replaceStringInObjectProperties(entity, regExp, replacement) {
  for (let property in entity) {
    if (!entity.hasOwnProperty(property)) {
      continue;
    }
    let value = entity[property];
    if (typeof value === "object") {
      value = replaceStringInObjectProperties(value, regExp, replacement);
    } else if (typeof value === "string") {
      value = value.replace(regExp, replacement);
    }
    entity[property] = value;
  }
  return entity;
}
;// ./src/scripts/web_scan.js
/**
 * web_scan callbacks and listeners
 */






class BdWebScan {
  constructor() {}
  startListeners() {
    const HTTP_URL = 'http://*/*';
    const HTTPS_URL = 'https://*/*';
    //url request listener

    if (scripts_compat.dnr.debug.available) {
      log.warn('[dnr] v3 activating dnr debug logging');
      scripts_compat.dnr.declarativeNetRequest.onRuleMatchedDebug.addListener(this.onDnrRuleMatchedDebug);
    }
    let extra_info_spec = [];
    if (canBlockWebRequest()) {
      extra_info_spec.push('blocking');
    }
    chrome.webRequest.onBeforeRequest.addListener(this.onBeforeRequest, {
      urls: [HTTP_URL, HTTPS_URL]
    }, extra_info_spec);

    //header request listener
    extra_info_spec = ['requestHeaders'];
    if (canBlockWebRequest()) {
      extra_info_spec.push('blocking');
    }
    if (chrome.webRequest.OnBeforeSendHeadersOptions.hasOwnProperty('EXTRA_HEADERS')) {
      extra_info_spec.push('extraHeaders');
    }
    chrome.webRequest.onBeforeSendHeaders.addListener(this.onBeforeSendHeaders, {
      urls: [HTTP_URL, HTTPS_URL]
    }, extra_info_spec);

    //header response listener
    extra_info_spec = ['responseHeaders'];
    if (canBlockWebRequest()) {
      extra_info_spec.push('blocking');
    }
    if (chrome.webRequest.OnHeadersReceivedOptions.hasOwnProperty('EXTRA_HEADERS')) {
      extra_info_spec.push('extraHeaders');
    }
    chrome.webRequest.onHeadersReceived.addListener(this.onHeadersReceived, {
      urls: [HTTPS_URL, HTTPS_URL]
    }, extra_info_spec);
  }

  /**
   * Intercept script request and decide if we need to block it.
   *
   * @param {Object} details The event details
   * @returns {Object} Can cancel requests
   * function onBeforeRequest({ url }) { //{url} gets only url parameters
   */
  onBeforeRequest(details) {
    if (!bdAt.isValidRequest(details)) {
      return {
        cancel: false
      };
    }
    if (!bdAt.isScanEnabled(details.tabId, details.url)) {
      return {
        cancel: false
      };
    }
    let request_hostname = parseUrl(details.url).hostname;
    let tab_stack = bdAt.getTabStack(details.tabId);
    let tab_info = tab_stack[0];
    if (!isThirdPartyDomain(request_hostname, tab_info.url)) {
      return {
        cancel: false
      };
    }
    let url_path = getPathFromUrl(details.url);
    let trackerCategory = tracking_default().isTracker(url_path.toLowerCase(), bdAt.state.categories);
    if (trackerCategory === (tracking_default()).categories.NO_FILTER) {
      return {
        cancel: false
      };
    }
    if (!canBlockWebRequest()) {
      log.warn('tabId: ' + details.tabId + ' tab url: ' + tab_info.url + ' v3 cannot block: ' + details.url);
      tab_info.trackersUrls.push(url_path);
      bdAt.tabs_map.set(details.tabId, tab_stack);
      chrome.storage.local.set(bdAt.state);
      return {
        cancel: false
      };
    }
    log.warn('tabId: ' + details.tabId + ' tab url: ' + tab_info.url + ' url blocked: ' + details.url);
    if (undefined === tab_info.trackersMap[trackerCategory] || null === tab_info.trackersMap[trackerCategory]) {
      tab_info.trackersMap[trackerCategory] = []; //empty array
    }
    if (!bdAt.isTrackerExist(tab_info.trackersMap[trackerCategory], url_path)) {
      tab_info.trackersMap[trackerCategory].push(url_path);
      tab_info.trackersBlocked += 1;
      bdAt.updateTabStack(details.tabId, tab_stack);
      updateUiStack(details.tabId, tab_stack, bdAt.session_whitelist);
    }
    return {
      cancel: true
    };
  }
  onDnrRuleMatchedDebug(matchedRuleInfoDebug) {
    log.warn('[dnr] onDnrRuleMatchedDebug: ' + JSON.stringify(matchedRuleInfoDebug, null, 4));
  }

  /**
   * Filters outgoing cookies only and not referer
   * referer header is not blocked and may be used for tracking but may be
   * blocked by the browser with a 'strict-origin-when-cross-origin' policy
   * Injects DNT header
   *
   * @param {Object} details Event details
   * @returns {Object} modified headers
   */
  onBeforeSendHeaders(details) {
    let new_headers = details.requestHeaders;
    let trackerCategory = (tracking_default()).categories.COOKIE;
    do {
      if (undefined === details.url || null === details.url || details.tabId < 0) {
        break;
      }
      if (!bdAt.isScanEnabled(details.tabId, details.url)) {
        break;
      }
      if (!(bdAt.state.categories & trackerCategory)) {
        log.warn('onBeforeSendHeaders, Third party cookie blocking not enabled');
        break;
      }
      new_headers.push({
        name: "dnt",
        value: "1"
      });
      let request_hostname = parseUrl(details.url).hostname;
      if (null === request_hostname || '' === request_hostname) {
        break;
      }
      let tab_stack = bdAt.getTabStack(details.tabId);
      let tab_info = tab_stack[0];
      if (!isThirdPartyDomain(request_hostname, tab_info.url)) {
        break;
      }
      if (tracking_default().blockDomainCookie(request_hostname)) {
        //remove cookie headers
        let old_headers_count = details.requestHeaders.length;
        new_headers = details.requestHeaders.filter(header => {
          return header.name.toLowerCase() !== "cookie";
        });
        let new_headers_count = new_headers.length;
        new_headers.push({
          name: "dnt",
          value: "1"
        });
        if (new_headers_count < old_headers_count) {
          log.warn('onBeforeSendHeaders, Third party cookie blocked: ' + details.url);
          if (undefined === tab_info.trackersMap[trackerCategory] || null === tab_info.trackersMap[trackerCategory]) {
            tab_info.trackersMap[trackerCategory] = []; //empty array
          }
          tab_info.trackersMap[trackerCategory].push(request_hostname);
          tab_info.trackersBlocked += 1;
          bdAt.updateTabStack(details.tabId, tab_stack);
          updateUiStack(details.tabId, tab_stack, bdAt.session_whitelist);
        }
      }
    } while (false);
    return {
      requestHeaders: new_headers
    };
  }

  /**
   * Received incoming headers 
   *
   * @param {Object} details The event details
   * @returns {Object} The new response headers
   */
  onHeadersReceived(details) {
    let new_headers = details.responseHeaders;
    let trackerCategory = (tracking_default()).categories.COOKIE;
    do {
      if (undefined === details.url || null === details.url || details.tabId < 0) {
        break;
      }
      if (!bdAt.isScanEnabled(details.tabId, details.url)) {
        break;
      }
      if (!(bdAt.state.categories & trackerCategory)) {
        log.warn('onHeadersReceived, Third party cookie blocking not enabled');
        break;
      }
      new_headers.push({
        name: "dnt",
        value: "1"
      });
      let request_hostname = parseUrl(details.url).hostname;
      if (null === request_hostname || '' === request_hostname) {
        break;
      }
      let tab_stack = bdAt.getTabStack(details.tabId);
      let tab_info = tab_stack[0];
      if (!isThirdPartyDomain(request_hostname, tab_info.url)) {
        break;
      }
      if (tracking_default().blockDomainCookie(request_hostname)) {
        //remove set-cookie headers value
        let old_headers_count = details.responseHeaders.length;
        new_headers = details.responseHeaders.filter(function (header) {
          return header.name.toLowerCase() !== "set-cookie";
        });
        let new_headers_count = new_headers.length;
        new_headers.push({
          name: "dnt",
          value: "1"
        });
        if (new_headers_count < old_headers_count) {
          log.warn('onHeadersReceived, Third party cookie blocked: ' + details.url);
          if (undefined === tab_info.trackersMap[trackerCategory] || null === tab_info.trackersMap[trackerCategory]) {
            tab_info.trackersMap[trackerCategory] = []; //empty array
          }
          tab_info.trackersMap[trackerCategory].push(request_hostname);
          tab_info.trackersBlocked += 1;
          bdAt.updateTabStack(details.tabId, tab_stack);
          updateUiStack(details.tabId, tab_stack, bdAt.session_whitelist);
        }
      }
    } while (false);
    return {
      responseHeaders: new_headers
    };
  }
}
/* harmony default export */ const web_scan = (new BdWebScan());
;// ./src/scripts/tab_events.js
/**
 * web_scan callbacks and listeners
 */





class BdTabEvents {
  constructor() {}
  startListeners() {
    chrome.webNavigation.onCommitted.addListener(this.onCommitted);
    chrome.webNavigation.onBeforeNavigate.addListener(this.onBeforeNavigate);
    chrome.webNavigation.onCompleted.addListener(this.onCompletedNavigate);
    chrome.tabs.onCreated.addListener(this.onTabCreated);
    chrome.tabs.onActivated.addListener(this.onTabActivated);
    chrome.tabs.onUpdated.addListener(this.onTabUpdated);
    chrome.tabs.onRemoved.addListener(this.onTabRemoved);
    chrome.tabs.onReplaced.addListener(this.onTabReplaced);
  }

  /**** listen tab events ******/
  /**
   * 
   * Fired when a tab is created.
   * 
   * @param {Object} tab 
   */
  onTabCreated(tab) {
    log.info('onTabCreated:' + JSON.stringify(tab));
    if (!bdAt.state.enabled) {
      return;
    }
    if (tab.url) {
      if (null !== bdAt.tabs_map) {
        let tab_info = new TabInfo();
        let tab_url = getTabUrl(tab.url);
        if (undefined !== tab_url) {
          tab_info.url = tab_url;
        }
        bdAt.tabs_map.set(tab.id, [tab_info]);
      }
    }
  }

  /**
   * Fires when the active tab in a window changes. 
   * Note that the tab's URL may not be set at the time this event fired, 
   * but you can listen to onUpdated events so as to be notified when a URL is set. 
   * * @param {Object} active_tab_info 
   */
  onTabActivated(active_tab_info) {
    log.info('onTabActivated: ' + JSON.stringify(active_tab_info));
    if (false === bdAt.state.enabled) {
      return;
    }
    if (null === bdAt.tabs_map) {
      return;
    }
    chrome.tabs.query({
      active: true,
      currentWindow: true
    }, tabs => {
      try {
        if (!tabs || !tabs.length) {
          return;
        }
        if (active_tab_info.tabId !== tabs[0].id) {
          return;
        }
        if (tabs[0].url.startsWith("chrome-extension:")) {
          log.info('onActivated: ignore chrome extension url: ' + tabs[0].url);
          return;
        }
      } catch (error) {
        log.error(`exception: ${error}`);
        return;
      }
      if (!tabs[0].url) {
        return;
      }
      if (!bdAt.tabs_map.has(active_tab_info.tabId)) {
        log.info('onActivated NOT found tabId');
        let tab_info = new TabInfo();
        let tab_url = getTabUrl(tabs[0].url);
        if (undefined !== tab_url) {
          tab_info.url = tab_url;
        }
        bdAt.tabs_map.set(active_tab_info.tabId, [tab_info]);
      }
      let tab_stack = bdAt.tabs_map.get(active_tab_info.tabId);
      let trackersBlocked = getTabStackTrackersBlocked(tab_stack);
      let objectTabStack = copyTabStack(tab_stack);
      updateUiStack(active_tab_info.tabId, objectTabStack, bdAt.session_whitelist);
      log.info('onTabActivated, blocked: ' + trackersBlocked);
    });
  }

  /**
   * 
   * @param {*} tabId 
   * @param {*} changeInfo 
   * @param {*} tab 
   * Fired when a tab is updated. 
   */
  onTabUpdated(tabId, change_info, tab) {
    log.info('onTabUpdated:' + JSON.stringify(tab));
    if (null === bdAt.tabs_map || !bdAt.tabs_map.has(tabId)) {
      log.info('onTabUpdated: tabId not found');
      bdAt.tabs_map.set(tabId, [new TabInfo()]);
      if (canBlockWebRequest()) {
        setBadgeMessage(tabId, 0);
      }
      return;
    }
    let tab_stack = bdAt.tabs_map.get(tabId);
    if (undefined === tab_stack || null === tab_stack) {
      log.info('onTabUpdated: tabStack undefined or null');
      return;
    }
    let tab_info = tab_stack[0];
    if (undefined === tab_info || null === tab_info) {
      log.info('onTabUpdated: tab_info undefined or null');
      return;
    }
    if (!bdAt.state.enabled) {
      log.info("extension disabled");
      if (tab_info.pageLoad > 0) {
        tab_info.trackersBlocked = 0;
        tab_info.pageLoad = 0;
        tab_info.trackersMap = {};
        tab_info.trackersUrls = [];
        bdAt.tabs_map.set(tabId, [tab_info]);
        scripts_compat.action.setIcon({
          path: 'assets/bdlogo_disabled.png'
        });
      }
      return;
    }
    if (undefined === change_info.status) {
      log.info('status tab undefined');
      return;
    }
    if (undefined === tab) {
      log.info('tab undefined');
      return;
    }
    log.info('status tab: ' + change_info.status);
    let trackersBlocked = 0;
    for (let i = 0; i < tab_stack.length; i++) {
      trackersBlocked += tab_stack[i].trackersBlocked;
    }
    if ('loading' === change_info.status) {
      if (canBlockWebRequest()) {
        setBadgeMessage(tabId, trackersBlocked);
      }
    }
  }

  /**
   * Event handler when a tab gets removed
   *
   * @param {Integer} tabId Id of the tab
   */
  onTabRemoved(tabId) {
    log.info('onTabRemoved: ' + tabId);
    if (bdAt.tabs_map.size && bdAt.tabs_map.has(tabId)) {
      bdAt.tabs_map.delete(tabId);
    }
  }

  /**
   * Update internal db on tabs when a tab gets replaced
   *
   * @param {Integer} addedTabId The new tab id that replaces
   * @param {Integer} removedTabId The tab id that gets removed
   */
  onTabReplaced(addedTabId, removedTabId) {
    log.info('onTabReplaced: addedTabId: ' + addedTabId + ' removedTabId: ' + removedTabId);
    if (bdAt.tabs_map.size && bdAt.tabs_map.has(removedTabId)) {
      bdAt.tabs_map.delete(removedTabId);
      bdAt.tabs_map.set(addedTabId, [new TabInfo()]);
    }
  }
  onBeforeNavigate(details) {
    if (0 !== details.frameId) {
      return;
    }
    log.info(`onBeforeNavigate, tabId: ${details.tabId}, frameId: ${details.frameId}, url: [${details.url}]`);
    let tab_stack;
    let tab_info;
    try {
      if (!bdAt.tabs_map.has(details.tabId)) {
        log.info('onBeforeNavigate: tabId not found');
        bdAt.tabs_map.set(details.tabId, [new TabInfo()]);
      }
      tab_stack = bdAt.tabs_map.get(details.tabId);
      tab_info = copyTabInfo(tab_stack[0]);
    } catch (error) {
      log.error(`exception: ${error}`);
      return;
    }
    let tab_url = getTabUrl(details.url);
    if (tab_info.url === tab_url) {
      log.info('same navigation target');
      return;
    }
    if (undefined !== tab_url) {
      tab_info.url = tab_url;
    }
    log.info('tab hostname: ' + tab_info.url);
    tab_info.transition = TAB_INFO_TRANSITION.PROVISIONAL;
    tab_info.pageLoadStartTime = Date.now();
    tab_info.pageLoad = 0;
    tab_info.trackersBlocked = 0;
    tab_info.trackersMap = {};
    tab_info.trackersUrls = [];
    if (tab_stack[0].transition === TAB_INFO_TRANSITION.PROVISIONAL) {
      if (tab_stack[0].trackersBlocked > 0) {
        if (tab_stack[0].pageLoad == 0 && tab_stack[0].pageLoadStartTime > 0) {
          let redirectLoadMillis = tab_info.pageLoadStartTime - tab_stack[0].pageLoadStartTime;
          let redirectSeconds = (redirectLoadMillis / 1000).toFixed(2);
          tab_stack[0].pageLoad = redirectSeconds;
        }
        tab_stack.splice(0, 0, tab_info); //insert as 1st position
      } else {
        tab_stack[0] = tab_info;
      }
    } else {
      tab_stack.splice(0, 0, tab_info); //insert as 1st position
    }
    bdAt.tabs_map.set(details.tabId, tab_stack);
    updateUiStack(details.tabId, tab_stack, bdAt.session_whitelist);
    log.info('onBeforeNavigate, pageLoad: ' + tab_info.pageLoad);
  }
  static isUserInitiatedAction(details) {
    if (details.transitionType === "typed" || details.transitionType === "auto_bookmark" || details.transitionType === "generated" || details.transitionType === "auto_toplevel" || details.transitionType === "reload" || details.transitionType === "keyword" || details.transitionType === "keyword_generated" || details.transitionQualifiers.includes("from_address_bar") || details.transitionQualifiers.includes("forward_back")) {
      return true;
    }
    return false;
  }
  static isAutomaticRedirect(details) {
    if (details.transitionQualifiers.includes("server_redirect") || details.transitionQualifiers.includes("client_redirect")) {
      return true;
    }
    return false;
  }
  static isFirefoxHeuristicRedirect(details, tab_info) {
    //firefox does not correctly set transitionQualifiers
    //https://bugzilla.mozilla.org/show_bug.cgi?id=1595621
    //https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/webNavigation/TransitionQualifier
    //'server_redirect' is limited to top-level frames and 'client_redirect' is not supplied when redirections are created by JavaScript.
    if (getBrowserContext() === BROWSER_CONTEXT.BROWSER_CONTEXT_FIREFOX) {
      if (details.transitionType === "link" && details.transitionQualifiers.length === 0) {
        if (tab_info.pageLoad === 0) {
          let newPageLoadStartTime = Date.now();
          if (newPageLoadStartTime - tab_info.pageLoadStartTime < 2500) {
            return true;
          }
        }
      }
    }
    return false;
  }
  static isCommitRedirect(details, tab_info) {
    let is_redirect = false;
    try {
      do {
        if (BdTabEvents.isUserInitiatedAction(details)) {
          is_redirect = false; //user reset the location
          break;
        }
        if (BdTabEvents.isAutomaticRedirect(details)) {
          is_redirect = true; //automatic redirect
          break;
        }
        if (BdTabEvents.isFirefoxHeuristicRedirect(details, tab_info)) {
          log.warn("Firefox redirect heuristic!");
          is_redirect = true;
          break;
        }
      } while (false);
    } catch (error) {
      log.error('exception: ' + error);
    }
    return is_redirect;
  }

  /**
   * @param {Object} details
   * webNavigation.onCommitted
   */
  onCommitted(details) {
    if (0 !== details.frameId) {
      return;
    }
    log.info(`onCommitted, tabId: ${details.tabId}, frameId: ${details.frameId}, url: [${details.url}]`);
    let tab_stack;
    let tab_info;
    try {
      if (!bdAt.tabs_map.has(details.tabId)) {
        log.info('onCommitted: tabId not found');
        bdAt.tabs_map.set(details.tabId, [new TabInfo()]);
      }
      tab_stack = bdAt.tabs_map.get(details.tabId);
      if (!tab_stack || !tab_stack.length) {
        return;
      }
      tab_info = copyTabInfo(tab_stack[0]);
    } catch (error) {
      log.error(`exception: ${error}`);
      return;
    }
    let tab_url = getTabUrl(details.url);
    if (undefined !== tab_url) {
      tab_info.url = tab_url;
    }
    log.info('tab hostname: ' + tab_info.url);
    let is_redirect = BdTabEvents.isCommitRedirect(details, tab_info);
    tab_info.pageLoadStartTime = Date.now();
    tab_info.pageLoad = 0;
    tab_info.trackersBlocked = 0;
    tab_info.trackersMap = {};
    tab_info.trackersUrls = [];
    if (is_redirect) {
      //only keep stats when trackers have been blocked
      if (tab_stack[0].trackersBlocked > 0) {
        if (tab_stack[0].pageLoad === 0 && tab_stack[0].pageLoadStartTime > 0) {
          let redirectLoadMillis = tab_info.pageLoadStartTime - tab_stack[0].pageLoadStartTime;
          let redirectSeconds = (redirectLoadMillis / 1000).toFixed(2);
          tab_stack[0].pageLoad = redirectSeconds;
        }
        tab_stack.splice(0, 0, tab_info); //insert as 1st position
      } else {
        tab_stack[0] = tab_info;
      }
    } else {
      tab_stack = [tab_info]; //reset whole stack
    }
    bdAt.tabs_map.set(details.tabId, tab_stack);
    updateUiStack(details.tabId, tab_stack, bdAt.session_whitelist);
    log.info('onCommitted, pageLoad: ' + tab_info.pageLoad);
  }

  /**
   * 
   * @param {*} details 
   * webNavigation.onCompleted
   */
  onCompletedNavigate(details) {
    if (0 !== details.frameId) {
      return;
    }
    log.info(`onCompletedNavigate, tabId: ${details.tabId}, frameId: ${details.frameId}, url: [${details.url}]`);
    let tab_stack;
    let tab_info;
    let millis = 0;
    try {
      if (!bdAt.tabs_map.has(details.tabId)) {
        log.info('onCompletedNavigate: tabId not found');
        bdAt.tabs_map.set(details.tabId, [new TabInfo()]);
      }
      tab_stack = bdAt.tabs_map.get(details.tabId);
      tab_info = tab_stack[0];
      if (0 !== tab_info.pageLoadStartTime) {
        millis = Date.now() - tab_info.pageLoadStartTime;
        tab_info.pageLoadStartTime = 0; //reset page loadStartTime
      }
      if (0 === tab_info.pageLoad) {
        let seconds = (millis / 1000).toFixed(2);
        tab_info.pageLoad = seconds;
        bdAt.tabs_map.set(details.tabId, tab_stack);
      }
    } catch (error) {
      log.error(`exception: ${error}`);
      return;
    }
    updateUiPageLoad(details.tabId, tab_stack);
    log.info('onCompletednavigate: pageLoad:' + tab_info.pageLoad);
  }
  /**** listen tab events ******/
}
/* harmony default export */ const tab_events = (new BdTabEvents());
;// ./src/scripts/nmh.js
/**
 * Native Messaging Host
 */



class BdNmh {
  constructor() {
    this.nativeMessageHandler = this.onNativeMessage.bind(this);
    this.disconnectedHandler = this.onDisconnected.bind(this);
    this.native_hostname = 'com.bitdefender.webtrackers.v1';
    this.port = null;
  }
  start() {
    try {
      if (null !== this.port) {
        this.onDisconnected();
      }
      this.port = chrome.runtime.connectNative(this.native_hostname);
      if (null !== this.port) {
        this.port.onMessage.addListener(this.nativeMessageHandler);
        this.port.onDisconnect.addListener(this.disconnectedHandler);
        if (false) // removed by dead control flow
{}
        let get_settings = {
          'method': 'get_settings',
          'browser_context': getBrowserContext()
        };
        this.postNativeMessage(get_settings);
        let get_whitelist = {
          'method': 'get_whitelist'
        };
        this.postNativeMessage(get_whitelist);
      }
    } catch (error) {
      log.error('exception: ' + error);
    }
  }
  postNativeMessage(message) {
    if (null !== this.port) {
      log.info('post native message: ' + JSON.stringify(message));
      this.port.postMessage(message);
    } else {
      log.warn('cannot post native message: not connected');
    }
  }
  onNativeMessage(message) {
    if (undefined === message || null === message) {
      return;
    }
    log.info('Message received from native host: ' + JSON.stringify(message));
    if (!message.hasOwnProperty('method')) {
      return;
    }
    let method = message['method'];
    if (null === method) {
      log.info('Method not found');
      return;
    }
    if ('set_flags' === method) {
      if (message.hasOwnProperty('flags')) {
        let flags = message['flags'];
        let flags_are_ok = Array.isArray(flags);
        if (flags_are_ok) {
          for (let flag of flags) {
            if (!(typeof flag === "string" || flag instanceof String)) {
              flags_are_ok = false;
              break;
            }
          }
        }
        if (flags_are_ok) {
          log.info('received set_flags: ' + flags);
          if (false) // removed by dead control flow
{}
        } else {
          log.error('bad format for set_flags');
        }
      }
    } else if ('add_flag' === method) {
      if (message.hasOwnProperty('flag')) {
        let flag = message['flag'];
        log.info('received add_flag: ' + flag);
        if (false) // removed by dead control flow
{}
      }
    } else if ('set_settings' === method) {
      let feature_status = true;
      if (message.hasOwnProperty('feature_status')) {
        feature_status = message['feature_status'];
        log.info('received feature status: ' + feature_status);
      }
      let settings = message['settings'];
      BdNmh.on_set_settings(feature_status, settings);
    } else if ('set_module_status' === method) {
      let feature_status = true;
      let module_status = true;
      if (message.hasOwnProperty('feature_status')) {
        feature_status = message['feature_status'];
        log.info('received feature status: ' + feature_status);
      }
      if (message.hasOwnProperty('module_status')) {
        module_status = message['module_status'];
        log.info('received module status: ' + module_status);
        bdAt.onModuleStatusChanged(feature_status, module_status);
      }
    } else if ('update' === method) {
      if (message.hasOwnProperty('status')) {
        let b_is_update = message['status'];
        bdAt.onUpdateState(b_is_update);
      }
    } else if ('disconnect' === method) {
      this.onDisconnected();
    } else if ('whitelist_add' === method) {
      if (message.hasOwnProperty('url')) {
        let url = message['url'];
        log.info('received whitelist_add url: ' + url);
        bdAt.onWhitelistAdd(url);
      }
    } else if ('whitelist_remove' === method) {
      if (message.hasOwnProperty('url')) {
        let url = message['url'];
        log.info('received whitelist_remove url: ' + url);
        bdAt.onWhitelistRemove(url);
      }
    } else if ('set_whitelist' === method) {
      if (message.hasOwnProperty('whitelist')) {
        let whitelist = message['whitelist'];
        let whitelist_is_ok = Array.isArray(whitelist);
        if (whitelist_is_ok) {
          for (let url of whitelist) {
            if (!(typeof url === "string" || url instanceof String)) {
              whitelist_is_ok = false;
              break;
            }
          }
        }
        if (whitelist_is_ok) {
          log.info('received set_whitelist: ' + whitelist);
          bdAt.onSetWhitelist(whitelist);
        } else {
          log.error('bad format for set_whitelist');
        }
      }
    }
  }
  onDisconnected() {
    if (undefined !== this.port && null !== this.port) {
      this.port.disconnect();
      this.port = null;
    }
  }
  static on_set_settings(feature_status, settings) {
    if (undefined === settings || null === settings) {
      log.info('Get settings object failed');
      return;
    }
    if (!settings.hasOwnProperty('enable')) {
      log.info('Get enable failed');
      return;
    }
    let setting_enabled = settings['enable'];
    if (!settings.hasOwnProperty('categories')) {
      log.info('Get categories failed');
      return;
    }
    let setting_categories = settings['categories'];
    if (settings.hasOwnProperty('lang')) {
      let lang = extensionLangFromProductLang(settings['lang']);
      log.info('current lang: ' + lang);
      if (undefined !== lang && lang !== chrome.i18n.getUILanguage()) {
        let langRelPath = '_locales/' + lang + '/messages.json';
        bdAt.loadLang(langRelPath);
      }
    }
    log.info("received settings" + " feature_status: " + feature_status + ', enabled: ' + setting_enabled + ', categories: ' + setting_categories);
    bdAt.onSettingsChanged(feature_status, setting_enabled, setting_categories);
  }
}
/* harmony default export */ const nmh = (new BdNmh());
;// ./src/scripts/local_comm.js
/**
 * 
 */




class LocalComm {
  start() {
    try {
      chrome.runtime.onMessage.addListener(this.onMessage);
    } catch (error) {
      log.error('exception: ' + error);
    }
  }
  static onNewState(request) {
    bdAt.setState(request.state);
    let settings_json = {
      'method': 'set_settings',
      'browser_context': getBrowserContext()
    };
    let settings = {
      'enable': request.state.enabled,
      'categories': request.state.categories
    };
    settings_json['settings'] = settings;
    log.info("send msg to nmh: " + JSON.stringify(settings_json));
    nmh.postNativeMessage(settings_json);
  }
  static onGetCurrentTabStack(request) {
    let get_tab_stack = {
      'tabStack': [{
        'transition': TAB_INFO_TRANSITION.COMMITED,
        'url': '',
        'trackersBlocked': 0,
        'pageLoad': 0,
        'trackersMap': {},
        'trackersUrls': []
      }],
      'sessionWhitelist': bdAt.session_whitelist,
      'isUpdate': bdAt.is_update,
      'langMap': null !== bdAt.lang_map ? JSON.stringify([...bdAt.lang_map]) : undefined
    };
    if (bdAt.tabs_map.size && bdAt.tabs_map.has(request.tabId)) {
      let tab_stack = bdAt.tabs_map.get(request.tabId);
      get_tab_stack.tabStack = copyTabStack(tab_stack);
    } else {
      let tab_url = getTabUrl(request.url);
      if (undefined !== tab_url) {
        get_tab_stack.tabStack[0].url = tab_url;
      }
    }
    return get_tab_stack;
  }
  static onWhitelistChanged(request) {
    bdAt.setState({
      ...bdAt.state,
      whitelist: request.whitelist
    });
    if (request.hasOwnProperty('whitelist_add')) {
      let url = request['whitelist_add'];
      log.info('add whitelist url: ' + url);
      nmh.postNativeMessage({
        'method': 'whitelist_add',
        'url': url
      });
    } else if (request.hasOwnProperty('whitelist_remove')) {
      let url = request['whitelist_remove'];
      log.info('remove whitelist url: ' + url);
      nmh.postNativeMessage({
        'method': 'whitelist_remove',
        'url': url
      });
    }
  }
  static onSessionWhitelistChanged(request) {
    bdAt.setSessionWhitelist(request.sessionWhitelist);
    bdAt.setState({
      ...bdAt.state,
      session_whitelist: request.sessionWhitelist
    });
    if (request.disabled) {
      if (request.url.toLowerCase().includes('newtab')) {
        return;
      }
      let telemetry_json = getTelemetryJson(TELEMETRY_EVENT_TYPE.PAUSE, request.url);
      log.info("sending msg to nmh: " + telemetry_json);
      nmh.postNativeMessage(telemetry_json);
    }
  }
  static onSpecialOffers(request) {
    bdAt.setState({
      ...bdAt.state,
      specialOffers: request.specialOffers
    });
    let new_special_offers_state = true === bdAt.state.specialOffers ? '1' : '0';
    let telemetry_json = getTelemetryJson(TELEMETRY_EVENT_TYPE.SPECIAL_OFFERS, new_special_offers_state);
    log.info("sending msg to nmh: " + telemetry_json);
    nmh.postNativeMessage(telemetry_json);
  }

  /****listen internal message ******/
  /**
   * 
   * @param {*} request 
   * @param {*} sender 
   * @param {*} sendResponse 
   */
  onMessage(request, sender, sendResponse) {
    log.info('onMessage: ' + JSON.stringify(request));
    switch (request.type) {
      case 'new_state':
        {
          LocalComm.onNewState(request);
          break;
        }
      case 'get_current_tab_stack':
        {
          let get_tab_stack = LocalComm.onGetCurrentTabStack(request);
          sendResponse(get_tab_stack);
          break;
        }
      case 'whitelist_changed':
        {
          LocalComm.onWhitelistChanged(request);
          break;
        }
      case 'sessionWhitelist_changed':
        {
          LocalComm.onSessionWhitelistChanged(request);
          break;
        }
      case 'special_offers':
        {
          LocalComm.onSpecialOffers(request);
          break;
        }
    }
  }
  /****listen internal message ******/
}
/* harmony default export */ const local_comm = (new LocalComm());
;// ./src/scripts/background.js










if (typeof importScripts !== 'undefined') {}

/**
 * Anti-tracker.
 */
class BdAt {
  constructor() {
    this.is_update = false;
    this.tabs_map = new Map();
    this.lang_map = null;
    this.session_whitelist = [];
    this.state = defaultState;
    this.restoreDnrSessionRules();
  }

  /**
   * start anti-tracker engine
   */
  start(storedState) {
    let initialState = {
      ...defaultState
    };

    //set extension state
    this.setState({
      ...initialState,
      ...storedState
    });
    const trackersUrl = chrome.runtime.getURL('tracking/trackers.json');
    fetch(trackersUrl).then(response => response.json()) //assuming file contains json
    .then(json => tracking_default().loadTrackers(json));

    // start listeners
    web_scan.startListeners();
    nmh.start();
    local_comm.start();
    tab_events.startListeners();
    log.info("Bitdefender Anti-tracker is ready!");
  }
  setSessionWhitelist(new_session_whitelist) {
    log.info('setSessionWhitelist, current: ' + JSON.stringify(this.session_whitelist));
    log.info('setSessionWhitelist, new: ' + JSON.stringify(new_session_whitelist));
    this.session_whitelist = new_session_whitelist;
  }

  /**
   * 
   * @param {*} new_state 
   * update state
   */
  setState(new_state) {
    log.info('setState, current_state: ' + JSON.stringify(this.state));
    log.info('setState, new state: ' + JSON.stringify(new_state));
    if (!this.state || this.state.enabled !== new_state.enabled) {
      scripts_compat.action.setIcon({
        path: true === new_state.enabled ? 'assets/bdlogo.png' : 'assets/bdlogo_disabled.png'
      });
    }
    this.state = new_state;
    chrome.storage.local.set(this.state);
    this.updateDnrRulesets();
    this.updateDnrDynamicRules();
    this.updateDnrSessionRules();
    this.updateDnrSpecialOffers();
  }
  updateDnrRulesets() {
    if (canBlockWebRequest()) {
      return;
    }
    if (!scripts_compat.dnr.rules.rulesets.available) {
      log.error('[dnr] rulesets not available! cannot handle toggling on/off & categories!');
      return;
    }
    let currentCategories = 0;
    if (this.state.enabled) {
      currentCategories = this.state.categories;
    }
    let updateRulesetOptions = tracking_default().categoriesToRulesetOptions(currentCategories);
    if (this.state.enabled) {
      updateRulesetOptions.enableRulesetIds.push((tracking_default()).rulesets.exceptions);
    } else {
      updateRulesetOptions.disableRulesetIds.push((tracking_default()).rulesets.exceptions);
    }
    log.warn('[dnr] updateEnabledRulesets: [' + currentCategories + '] ' + JSON.stringify(updateRulesetOptions, null, 4));
    scripts_compat.dnr.declarativeNetRequest.updateEnabledRulesets(updateRulesetOptions);
  }
  updateDnrDynamicRules() {
    if (canBlockWebRequest()) {
      return;
    }
    if (!scripts_compat.dnr.rules.dynamic.available) {
      log.error('[dnr] dynamic rules not available! cannot handle exceptions!');
      return;
    }
    scripts_compat.dnr.declarativeNetRequest.getDynamicRules(rules => {
      log.warn('[dnr] getDynamicRules: ' + JSON.stringify(rules, null, 4));
      let prevDynamicIds = [];
      rules.forEach(rule => {
        prevDynamicIds.push(rule.id);
      });
      log.warn('[dnr] updateDynamicRules (removeRuleIds): ' + JSON.stringify(prevDynamicIds, null, 4));
      let updateDynamicWhitelist = () => {
        if (this.state.enabled) {
          if (this.state.whitelist.length > 0) {
            let updateDynamicRulesetOptions = tracking_default().urlListToAllowRulesOptions(this.state.whitelist, (tracking_default()).rule_ids.user_exceptions, (tracking_default()).rule_priorities.user_exceptions);
            log.warn('[dnr] updateDynamicRules: ' + JSON.stringify(updateDynamicRulesetOptions, null, 4));
            scripts_compat.dnr.declarativeNetRequest.updateDynamicRules(updateDynamicRulesetOptions);
          }
        }
      };
      if (prevDynamicIds.length > 0) {
        scripts_compat.dnr.declarativeNetRequest.updateDynamicRules({
          removeRuleIds: prevDynamicIds
        }, () => {
          log.warn('[dnr] updateDynamicRules removed rules: ' + JSON.stringify(prevDynamicIds));
          updateDynamicWhitelist();
        });
      } else {
        updateDynamicWhitelist();
      }
    });
  }
  restoreDnrSessionRules() {
    if (!scripts_compat.dnr.rules.session.available) {
      log.warn('[dnr] session rules not available! cannot restore session whitelist!');
      return;
    }
    scripts_compat.dnr.declarativeNetRequest.getSessionRules(rules => {
      log.warn('[dnr] getSessionRules: ' + JSON.stringify(rules, null, 4));
      let prevSessionWhitelist = tracking_default().urlFilterRulesToUrlList(rules);
      log.warn('[dnr] prevSessionWhitelist: ' + JSON.stringify(rules, null, 4));
      this.session_whitelist = prevSessionWhitelist;
    });
  }
  updateDnrSessionRules() {
    if (canBlockWebRequest()) {
      return;
    }
    if (!scripts_compat.dnr.rules.session.available) {
      log.error('[dnr] session rules not available! cannot handle session whitelist!');
      return;
    }
    scripts_compat.dnr.declarativeNetRequest.getSessionRules(rules => {
      log.warn('[dnr] getSessionRules: ' + JSON.stringify(rules, null, 4));
      let prevSessionIds = [];
      rules.forEach(rule => {
        prevSessionIds.push(rule.id);
      });
      log.warn('[dnr] updateSessionRules (removeRuleIds): ' + JSON.stringify(prevSessionIds, null, 4));
      let updateSessionWhitelist = () => {
        if (this.state.enabled) {
          if (this.session_whitelist.length > 0) {
            let updateSessionRulesetOptions = tracking_default().urlListToAllowRulesOptions(this.session_whitelist, (tracking_default()).rule_ids.session_exceptions, (tracking_default()).rule_priorities.session_exceptions);
            log.warn('[dnr] updateSessionRules: ' + JSON.stringify(updateSessionRulesetOptions, null, 4));
            scripts_compat.dnr.declarativeNetRequest.updateSessionRules(updateSessionRulesetOptions);
          }
        }
      };
      if (prevSessionIds.length > 0) {
        scripts_compat.dnr.declarativeNetRequest.updateSessionRules({
          removeRuleIds: prevSessionIds
        }, updateSessionWhitelist);
      } else {
        updateSessionWhitelist();
      }
    });
  }
  updateDnrSpecialOffers() {
    if (canBlockWebRequest()) {
      return;
    }
    if (!scripts_compat.dnr.rules.rulesets.available) {
      log.error('[dnr] rulesets not available! cannot handle toggling on/off special offers!');
      return;
    }
    let updateRulesetOptions = {
      enableRulesetIds: [],
      disableRulesetIds: []
    };
    if (this.state.specialOffers) {
      updateRulesetOptions.enableRulesetIds.push((tracking_default()).rulesets.special_offers);
    } else {
      updateRulesetOptions.disableRulesetIds.push((tracking_default()).rulesets.special_offers);
    }
    log.warn('[dnr] updateDnrSpecialOffers: [' + this.state.specialOffers + '] ' + JSON.stringify(updateRulesetOptions, null, 4));
    scripts_compat.dnr.declarativeNetRequest.updateEnabledRulesets(updateRulesetOptions);
  }

  /**
   * Check if anti-tracler is enabled and
   * check against the whitelist
   *
   * @param {Number} tab_id 
   * @param {String} request_url 
   * @returns {Boolean} true if scan enabled
   */
  isScanEnabled(tab_id, request_url) {
    if (!this.state.enabled) {
      log.info('extension not enabled');
      return false;
    }
    let tab_stack;
    let tab_info;
    try {
      if (!this.tabs_map.has(tab_id)) {
        return false;
      }
      tab_stack = this.tabs_map.get(tab_id);
      tab_info = tab_stack[0];
      if (!tab_info.url) {
        log.info('empty tab url');
        return false;
      }
    } catch (error) {
      log.error(`exception: ${error}`);
      return false;
    }
    if (getBrowserContext() === BROWSER_CONTEXT.BROWSER_CONTEXT_CHROME && 'local-ntp' === tab_info.url) {
      log.info('chrome new tab url');
      return false;
    }
    if (this.state.specialOffers && isBdTrackingIds(tab_info.url, request_url)) {
      log.warn('ignore bd tracking ids: ' + request_url);
      return false;
    }
    if (this.session_whitelist && this.session_whitelist.includes(tab_info.url)) {
      log.warn('ignore url by session whitelist: ' + tab_info.url);
      return false;
    }
    let url_hostname = tab_info.url;
    if (url_hostname.startsWith("www.")) {
      url_hostname = url_hostname.substring(4);
    }
    if (url_hostname === 'newtab' || url_hostname === 'local-ntp') {
      return false;
    }
    if (this.state.whitelist && this.state.whitelist.includes(url_hostname)) {
      log.warn('ignore url by global whitelist: ' + url_hostname);
      return false;
    }
    return true;
  }

  /**
   * 
   * @param {*} langRelPath 
   */
  loadLang(lang_json_path) {
    const lang_json_url = chrome.runtime.getURL(lang_json_path);
    fetch(lang_json_url).then(response => response.json()) //assuming file contains json
    .then(json_lang => {
      this.lang_map = getLangMap(json_lang);
      log.info(this.lang_map);
    });
  }

  /**
   * 
   * @param {Boolean} b_is_update 
   */
  onUpdateState(b_is_update) {
    log.info('onUpdateState: ' + b_is_update);
    this.isUpdate = b_is_update;
  }

  /**
   * 
   * @param {Number} enabled current extension status
   * @param {Number} categories  current extension categories
   */
  onSettingsChanged(feature_status, enabled, categories) {
    log.info("onSettingsChanged" + " feature_status: " + feature_status + ', enabled: ' + enabled + ', categories: ' + categories);
    let new_state = {
      ...this.state
    };
    new_state.featureStatus = feature_status;
    new_state.enabled = enabled;
    new_state.categories = categories;
    this.setState(new_state);
    chrome.runtime.sendMessage({
      type: 'set_settings',
      featureStatus: feature_status,
      enabled: enabled,
      categories: categories
    }, () => {
      //need to check lastError to prevent error being displayed in the
      //browser extension page when there is no content script loaded in tab
      chrome.runtime.lastError;
    });
  }

  /**
   * 
   * @param {*} feature_status  current antitracker feature status
   * @param {*} module_status  current extension status
   */
  onModuleStatusChanged(feature_status, module_status) {
    log.info("onModuleStatusChanged" + " feature: " + feature_status + ', module_status: ' + module_status);
    let new_state = {
      ...this.state
    };
    new_state.featureStatus = feature_status;
    new_state.enabled = module_status;
    this.setState(new_state);
    chrome.runtime.sendMessage({
      type: 'set_module_status',
      featureStatus: feature_status,
      enabled: module_status
    }, () => {
      //need to check lastError to prevent error being displayed in the
      //browser extension page when there is no content script loaded in tab
      chrome.runtime.lastError;
    });
  }
  onWhitelistAdd(url) {
    log.info("onWhitelistAdd" + " url: " + url);
    if (this.state.whitelist) {
      if (!this.state.whitelist.includes(url)) {
        log.info('add url to global whitelist: ' + url);
        let new_state = {
          ...this.state
        };
        new_state.whitelist = this.state.whitelist.concat(url);
        this.setState(new_state);
        chrome.runtime.sendMessage({
          type: 'whitelist_add',
          url: url
        }, () => {
          //need to check lastError to prevent error being displayed in the
          //browser extension page when there is no content script loaded in tab
          chrome.runtime.lastError;
        });
      }
    }
  }
  onWhitelistRemove(url) {
    log.info("onWhitelistRemove" + " url: " + url);
    if (this.state.whitelist) {
      if (this.state.whitelist.includes(url)) {
        log.info('remove url from global whitelist: ' + url);
        let new_state = {
          ...this.state
        };
        new_state.whitelist = this.state.whitelist.filter(site => site !== url);
        this.setState(new_state);
        chrome.runtime.sendMessage({
          type: 'whitelist_remove',
          url: url
        }, () => {
          //need to check lastError to prevent error being displayed in the
          //browser extension page when there is no content script loaded in tab
          chrome.runtime.lastError;
        });
      }
    }
  }
  onSetWhitelist(whitelist) {
    log.info("onSetWhitelist" + " whitelist: " + whitelist);
    let newWhitelist = whitelist.slice(0);
    if (this.state.whitelist) {
      //backwards compatibility with existing whitelist that was not previously synced
      let compatibilityWhitelist = [];
      if (this.state.mustSyncWhitelist) {
        let new_state = {
          ...this.state
        };
        new_state.mustSyncWhitelist = false;
        this.setState(new_state);
        if (this.state.whitelist.length > 0) {
          let existingWhitelist = this.state.whitelist.slice(0);
          existingWhitelist.forEach(url => {
            if (!newWhitelist.includes(url)) {
              compatibilityWhitelist.push(url);
              newWhitelist.push(url);
            }
          });
        }
      }
      let new_state = {
        ...this.state
      };
      new_state.whitelist = newWhitelist.slice(0);
      this.setState(new_state);
      chrome.runtime.sendMessage({
        type: 'set_whitelist',
        whitelist: this.state.whitelist.slice(0)
      }, () => {
        //need to check lastError to prevent error being displayed in the
        //browser extension page when there is no content script loaded in tab
        chrome.runtime.lastError;
      });
      compatibilityWhitelist.forEach(url => {
        nmh.postNativeMessage({
          'method': 'whitelist_add',
          'url': url
        });
      });
    }
  }

  /**
   * 
   * @param {Number} tab_id 
   * @param {Object} tab_stack 
   */
  updateTabStack(tab_id, tab_stack) {
    this.tabs_map.set(tab_id, tab_stack);
    this.state.globalBlocked++;
    chrome.storage.local.set(this.state);
  }

  /**
   * 
   * @param {Number} tab_id 
   * @returns {Object} curent tab info stack
   */
  getTabStack(tab_id) {
    return this.tabs_map.get(tab_id);
  }

  /**
   * 
   * @param {Object} details 
   */
  isValidRequest(details) {
    if (undefined === details.url || null === details.url || details.tabId < 0) {
      return false;
    }
    if (undefined === details.type) {
      return false;
    }
    if ('main_frame' === details.type) {
      log.info('skip main frame');
      return false;
    }
    if ('stylesheet' === details.type || 'font' === details.type || 'media' === details.type) {
      log.info('skip resource type: ' + details.type);
      return false;
    }
    return true;
  }

  /**
   * 
   * @param {List} trackers_list 
   * @param {String} url_path
   */
  isTrackerExist(trackers_list, url_path) {
    let bExist = false;
    for (let item = 0; item < trackers_list.length; item++) {
      let current_tracker = trackers_list[item];
      if (url_path === current_tracker) {
        bExist = true;
        break;
      }
    }
    return bExist;
  }
  reloadExtension() {
    chrome.runtime.reload();
  }
}
;
if (false) // removed by dead control flow
{ var setPolicyNmh, policyNmhSet, policyNmhOnDisconnected, policyNmhOnMessage, postPolicyBrowserFlagsMessage, policyNmhPort, setPolicyLocalComm, policyLocalCommSet, policyOnExtensionMessage, sendPolicyLangChangeMessage, policyLang, setPolicyAction, policyActionSet, openOrFocusPolicyTab, closeInstallTab; }
loadAndInitStoredState(storedState => {
  log.info("background load local storage state: " + JSON.stringify(storedState));
  if (false) // removed by dead control flow
{}
  setBadgeColor();
  if (!canBlockWebRequest()) {
    log.warn('v3 cannot use blocking requests');
    if (scripts_compat.dnr.action.available) {
      log.warn('[dnr] v3 activating dnr action badge');
      scripts_compat.dnr.declarativeNetRequest.setExtensionActionOptions({
        displayActionCountAsBadgeText: true
      });
    }
  }

  //anti-tracker
  var bdAt = self.bdAt = new BdAt();
  if (false) // removed by dead control flow
{}
  bdAt.start(storedState);
});
})();

/******/ })()
;