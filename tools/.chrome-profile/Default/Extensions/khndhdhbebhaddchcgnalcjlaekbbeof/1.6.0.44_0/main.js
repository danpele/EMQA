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

/***/ 287
(__unused_webpack_module, exports) {

"use strict";
/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var l=Symbol.for("react.element"),n=Symbol.for("react.portal"),p=Symbol.for("react.fragment"),q=Symbol.for("react.strict_mode"),r=Symbol.for("react.profiler"),t=Symbol.for("react.provider"),u=Symbol.for("react.context"),v=Symbol.for("react.forward_ref"),w=Symbol.for("react.suspense"),x=Symbol.for("react.memo"),y=Symbol.for("react.lazy"),z=Symbol.iterator;function A(a){if(null===a||"object"!==typeof a)return null;a=z&&a[z]||a["@@iterator"];return"function"===typeof a?a:null}
var B={isMounted:function(){return!1},enqueueForceUpdate:function(){},enqueueReplaceState:function(){},enqueueSetState:function(){}},C=Object.assign,D={};function E(a,b,e){this.props=a;this.context=b;this.refs=D;this.updater=e||B}E.prototype.isReactComponent={};
E.prototype.setState=function(a,b){if("object"!==typeof a&&"function"!==typeof a&&null!=a)throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");this.updater.enqueueSetState(this,a,b,"setState")};E.prototype.forceUpdate=function(a){this.updater.enqueueForceUpdate(this,a,"forceUpdate")};function F(){}F.prototype=E.prototype;function G(a,b,e){this.props=a;this.context=b;this.refs=D;this.updater=e||B}var H=G.prototype=new F;
H.constructor=G;C(H,E.prototype);H.isPureReactComponent=!0;var I=Array.isArray,J=Object.prototype.hasOwnProperty,K={current:null},L={key:!0,ref:!0,__self:!0,__source:!0};
function M(a,b,e){var d,c={},k=null,h=null;if(null!=b)for(d in void 0!==b.ref&&(h=b.ref),void 0!==b.key&&(k=""+b.key),b)J.call(b,d)&&!L.hasOwnProperty(d)&&(c[d]=b[d]);var g=arguments.length-2;if(1===g)c.children=e;else if(1<g){for(var f=Array(g),m=0;m<g;m++)f[m]=arguments[m+2];c.children=f}if(a&&a.defaultProps)for(d in g=a.defaultProps,g)void 0===c[d]&&(c[d]=g[d]);return{$$typeof:l,type:a,key:k,ref:h,props:c,_owner:K.current}}
function N(a,b){return{$$typeof:l,type:a.type,key:b,ref:a.ref,props:a.props,_owner:a._owner}}function O(a){return"object"===typeof a&&null!==a&&a.$$typeof===l}function escape(a){var b={"=":"=0",":":"=2"};return"$"+a.replace(/[=:]/g,function(a){return b[a]})}var P=/\/+/g;function Q(a,b){return"object"===typeof a&&null!==a&&null!=a.key?escape(""+a.key):b.toString(36)}
function R(a,b,e,d,c){var k=typeof a;if("undefined"===k||"boolean"===k)a=null;var h=!1;if(null===a)h=!0;else switch(k){case "string":case "number":h=!0;break;case "object":switch(a.$$typeof){case l:case n:h=!0}}if(h)return h=a,c=c(h),a=""===d?"."+Q(h,0):d,I(c)?(e="",null!=a&&(e=a.replace(P,"$&/")+"/"),R(c,b,e,"",function(a){return a})):null!=c&&(O(c)&&(c=N(c,e+(!c.key||h&&h.key===c.key?"":(""+c.key).replace(P,"$&/")+"/")+a)),b.push(c)),1;h=0;d=""===d?".":d+":";if(I(a))for(var g=0;g<a.length;g++){k=
a[g];var f=d+Q(k,g);h+=R(k,b,e,f,c)}else if(f=A(a),"function"===typeof f)for(a=f.call(a),g=0;!(k=a.next()).done;)k=k.value,f=d+Q(k,g++),h+=R(k,b,e,f,c);else if("object"===k)throw b=String(a),Error("Objects are not valid as a React child (found: "+("[object Object]"===b?"object with keys {"+Object.keys(a).join(", ")+"}":b)+"). If you meant to render a collection of children, use an array instead.");return h}
function S(a,b,e){if(null==a)return a;var d=[],c=0;R(a,d,"","",function(a){return b.call(e,a,c++)});return d}function T(a){if(-1===a._status){var b=a._result;b=b();b.then(function(b){if(0===a._status||-1===a._status)a._status=1,a._result=b},function(b){if(0===a._status||-1===a._status)a._status=2,a._result=b});-1===a._status&&(a._status=0,a._result=b)}if(1===a._status)return a._result.default;throw a._result;}
var U={current:null},V={transition:null},W={ReactCurrentDispatcher:U,ReactCurrentBatchConfig:V,ReactCurrentOwner:K};exports.Children={map:S,forEach:function(a,b,e){S(a,function(){b.apply(this,arguments)},e)},count:function(a){var b=0;S(a,function(){b++});return b},toArray:function(a){return S(a,function(a){return a})||[]},only:function(a){if(!O(a))throw Error("React.Children.only expected to receive a single React element child.");return a}};exports.Component=E;exports.Fragment=p;
exports.Profiler=r;exports.PureComponent=G;exports.StrictMode=q;exports.Suspense=w;exports.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED=W;
exports.cloneElement=function(a,b,e){if(null===a||void 0===a)throw Error("React.cloneElement(...): The argument must be a React element, but you passed "+a+".");var d=C({},a.props),c=a.key,k=a.ref,h=a._owner;if(null!=b){void 0!==b.ref&&(k=b.ref,h=K.current);void 0!==b.key&&(c=""+b.key);if(a.type&&a.type.defaultProps)var g=a.type.defaultProps;for(f in b)J.call(b,f)&&!L.hasOwnProperty(f)&&(d[f]=void 0===b[f]&&void 0!==g?g[f]:b[f])}var f=arguments.length-2;if(1===f)d.children=e;else if(1<f){g=Array(f);
for(var m=0;m<f;m++)g[m]=arguments[m+2];d.children=g}return{$$typeof:l,type:a.type,key:c,ref:k,props:d,_owner:h}};exports.createContext=function(a){a={$$typeof:u,_currentValue:a,_currentValue2:a,_threadCount:0,Provider:null,Consumer:null,_defaultValue:null,_globalName:null};a.Provider={$$typeof:t,_context:a};return a.Consumer=a};exports.createElement=M;exports.createFactory=function(a){var b=M.bind(null,a);b.type=a;return b};exports.createRef=function(){return{current:null}};
exports.forwardRef=function(a){return{$$typeof:v,render:a}};exports.isValidElement=O;exports.lazy=function(a){return{$$typeof:y,_payload:{_status:-1,_result:a},_init:T}};exports.memo=function(a,b){return{$$typeof:x,type:a,compare:void 0===b?null:b}};exports.startTransition=function(a){var b=V.transition;V.transition={};try{a()}finally{V.transition=b}};exports.unstable_act=function(){throw Error("act(...) is not supported in production builds of React.");};
exports.useCallback=function(a,b){return U.current.useCallback(a,b)};exports.useContext=function(a){return U.current.useContext(a)};exports.useDebugValue=function(){};exports.useDeferredValue=function(a){return U.current.useDeferredValue(a)};exports.useEffect=function(a,b){return U.current.useEffect(a,b)};exports.useId=function(){return U.current.useId()};exports.useImperativeHandle=function(a,b,e){return U.current.useImperativeHandle(a,b,e)};
exports.useInsertionEffect=function(a,b){return U.current.useInsertionEffect(a,b)};exports.useLayoutEffect=function(a,b){return U.current.useLayoutEffect(a,b)};exports.useMemo=function(a,b){return U.current.useMemo(a,b)};exports.useReducer=function(a,b,e){return U.current.useReducer(a,b,e)};exports.useRef=function(a){return U.current.useRef(a)};exports.useState=function(a){return U.current.useState(a)};exports.useSyncExternalStore=function(a,b,e){return U.current.useSyncExternalStore(a,b,e)};
exports.useTransition=function(){return U.current.useTransition()};exports.version="18.2.0";


/***/ },

/***/ 338
(__unused_webpack_module, exports, __webpack_require__) {

"use strict";
var __webpack_unused_export__;


var m = __webpack_require__(961);
if (true) {
  exports.H = m.createRoot;
  __webpack_unused_export__ = m.hydrateRoot;
} else // removed by dead control flow
{ var i; }


/***/ },

/***/ 372
(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = isIP;
var _assertString = _interopRequireDefault(__webpack_require__(399));
function _interopRequireDefault(e) { return e && e.__esModule ? e : { default: e }; }
function _typeof(o) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (o) { return typeof o; } : function (o) { return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o; }, _typeof(o); }
/**
11.3.  Examples

   The following addresses

             fe80::1234 (on the 1st link of the node)
             ff02::5678 (on the 5th link of the node)
             ff08::9abc (on the 10th organization of the node)

   would be represented as follows:

             fe80::1234%1
             ff02::5678%5
             ff08::9abc%10

   (Here we assume a natural translation from a zone index to the
   <zone_id> part, where the Nth zone of any scope is translated into
   "N".)

   If we use interface names as <zone_id>, those addresses could also be
   represented as follows:

            fe80::1234%ne0
            ff02::5678%pvc1.3
            ff08::9abc%interface10

   where the interface "ne0" belongs to the 1st link, "pvc1.3" belongs
   to the 5th link, and "interface10" belongs to the 10th organization.
 * * */
var IPv4SegmentFormat = '(?:[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])';
var IPv4AddressFormat = "(".concat(IPv4SegmentFormat, "[.]){3}").concat(IPv4SegmentFormat);
var IPv4AddressRegExp = new RegExp("^".concat(IPv4AddressFormat, "$"));
var IPv6SegmentFormat = '(?:[0-9a-fA-F]{1,4})';
var IPv6AddressRegExp = new RegExp('^(' + "(?:".concat(IPv6SegmentFormat, ":){7}(?:").concat(IPv6SegmentFormat, "|:)|") + "(?:".concat(IPv6SegmentFormat, ":){6}(?:").concat(IPv4AddressFormat, "|:").concat(IPv6SegmentFormat, "|:)|") + "(?:".concat(IPv6SegmentFormat, ":){5}(?::").concat(IPv4AddressFormat, "|(:").concat(IPv6SegmentFormat, "){1,2}|:)|") + "(?:".concat(IPv6SegmentFormat, ":){4}(?:(:").concat(IPv6SegmentFormat, "){0,1}:").concat(IPv4AddressFormat, "|(:").concat(IPv6SegmentFormat, "){1,3}|:)|") + "(?:".concat(IPv6SegmentFormat, ":){3}(?:(:").concat(IPv6SegmentFormat, "){0,2}:").concat(IPv4AddressFormat, "|(:").concat(IPv6SegmentFormat, "){1,4}|:)|") + "(?:".concat(IPv6SegmentFormat, ":){2}(?:(:").concat(IPv6SegmentFormat, "){0,3}:").concat(IPv4AddressFormat, "|(:").concat(IPv6SegmentFormat, "){1,5}|:)|") + "(?:".concat(IPv6SegmentFormat, ":){1}(?:(:").concat(IPv6SegmentFormat, "){0,4}:").concat(IPv4AddressFormat, "|(:").concat(IPv6SegmentFormat, "){1,6}|:)|") + "(?::((?::".concat(IPv6SegmentFormat, "){0,5}:").concat(IPv4AddressFormat, "|(?::").concat(IPv6SegmentFormat, "){1,7}|:))") + ')(%[0-9a-zA-Z.]{1,})?$');
function isIP(ipAddress) {
  var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
  (0, _assertString.default)(ipAddress);

  // accessing 'arguments' for backwards compatibility: isIP(ipAddress [, version])
  // eslint-disable-next-line prefer-rest-params
  var version = (_typeof(options) === 'object' ? options.version : arguments[1]) || '';
  if (!version) {
    return isIP(ipAddress, {
      version: 4
    }) || isIP(ipAddress, {
      version: 6
    });
  }
  if (version.toString() === '4') {
    return IPv4AddressRegExp.test(ipAddress);
  }
  if (version.toString() === '6') {
    return IPv6AddressRegExp.test(ipAddress);
  }
  return false;
}
module.exports = exports.default;
module.exports["default"] = exports.default;

/***/ },

/***/ 399
(module, exports) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = assertString;
function assertString(input) {
  if (input === undefined || input === null) throw new TypeError("Expected a string but received a ".concat(input));
  if (input.constructor.name !== 'String') throw new TypeError("Expected a string but received a ".concat(input.constructor.name));
}
module.exports = exports.default;
module.exports["default"] = exports.default;

/***/ },

/***/ 463
(__unused_webpack_module, exports) {

"use strict";
/**
 * @license React
 * scheduler.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
function f(a,b){var c=a.length;a.push(b);a:for(;0<c;){var d=c-1>>>1,e=a[d];if(0<g(e,b))a[d]=b,a[c]=e,c=d;else break a}}function h(a){return 0===a.length?null:a[0]}function k(a){if(0===a.length)return null;var b=a[0],c=a.pop();if(c!==b){a[0]=c;a:for(var d=0,e=a.length,w=e>>>1;d<w;){var m=2*(d+1)-1,C=a[m],n=m+1,x=a[n];if(0>g(C,c))n<e&&0>g(x,C)?(a[d]=x,a[n]=c,d=n):(a[d]=C,a[m]=c,d=m);else if(n<e&&0>g(x,c))a[d]=x,a[n]=c,d=n;else break a}}return b}
function g(a,b){var c=a.sortIndex-b.sortIndex;return 0!==c?c:a.id-b.id}if("object"===typeof performance&&"function"===typeof performance.now){var l=performance;exports.unstable_now=function(){return l.now()}}else{var p=Date,q=p.now();exports.unstable_now=function(){return p.now()-q}}var r=[],t=[],u=1,v=null,y=3,z=!1,A=!1,B=!1,D="function"===typeof setTimeout?setTimeout:null,E="function"===typeof clearTimeout?clearTimeout:null,F="undefined"!==typeof setImmediate?setImmediate:null;
"undefined"!==typeof navigator&&void 0!==navigator.scheduling&&void 0!==navigator.scheduling.isInputPending&&navigator.scheduling.isInputPending.bind(navigator.scheduling);function G(a){for(var b=h(t);null!==b;){if(null===b.callback)k(t);else if(b.startTime<=a)k(t),b.sortIndex=b.expirationTime,f(r,b);else break;b=h(t)}}function H(a){B=!1;G(a);if(!A)if(null!==h(r))A=!0,I(J);else{var b=h(t);null!==b&&K(H,b.startTime-a)}}
function J(a,b){A=!1;B&&(B=!1,E(L),L=-1);z=!0;var c=y;try{G(b);for(v=h(r);null!==v&&(!(v.expirationTime>b)||a&&!M());){var d=v.callback;if("function"===typeof d){v.callback=null;y=v.priorityLevel;var e=d(v.expirationTime<=b);b=exports.unstable_now();"function"===typeof e?v.callback=e:v===h(r)&&k(r);G(b)}else k(r);v=h(r)}if(null!==v)var w=!0;else{var m=h(t);null!==m&&K(H,m.startTime-b);w=!1}return w}finally{v=null,y=c,z=!1}}var N=!1,O=null,L=-1,P=5,Q=-1;
function M(){return exports.unstable_now()-Q<P?!1:!0}function R(){if(null!==O){var a=exports.unstable_now();Q=a;var b=!0;try{b=O(!0,a)}finally{b?S():(N=!1,O=null)}}else N=!1}var S;if("function"===typeof F)S=function(){F(R)};else if("undefined"!==typeof MessageChannel){var T=new MessageChannel,U=T.port2;T.port1.onmessage=R;S=function(){U.postMessage(null)}}else S=function(){D(R,0)};function I(a){O=a;N||(N=!0,S())}function K(a,b){L=D(function(){a(exports.unstable_now())},b)}
exports.unstable_IdlePriority=5;exports.unstable_ImmediatePriority=1;exports.unstable_LowPriority=4;exports.unstable_NormalPriority=3;exports.unstable_Profiling=null;exports.unstable_UserBlockingPriority=2;exports.unstable_cancelCallback=function(a){a.callback=null};exports.unstable_continueExecution=function(){A||z||(A=!0,I(J))};
exports.unstable_forceFrameRate=function(a){0>a||125<a?console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported"):P=0<a?Math.floor(1E3/a):5};exports.unstable_getCurrentPriorityLevel=function(){return y};exports.unstable_getFirstCallbackNode=function(){return h(r)};exports.unstable_next=function(a){switch(y){case 1:case 2:case 3:var b=3;break;default:b=y}var c=y;y=b;try{return a()}finally{y=c}};exports.unstable_pauseExecution=function(){};
exports.unstable_requestPaint=function(){};exports.unstable_runWithPriority=function(a,b){switch(a){case 1:case 2:case 3:case 4:case 5:break;default:a=3}var c=y;y=a;try{return b()}finally{y=c}};
exports.unstable_scheduleCallback=function(a,b,c){var d=exports.unstable_now();"object"===typeof c&&null!==c?(c=c.delay,c="number"===typeof c&&0<c?d+c:d):c=d;switch(a){case 1:var e=-1;break;case 2:e=250;break;case 5:e=1073741823;break;case 4:e=1E4;break;default:e=5E3}e=c+e;a={id:u++,callback:b,priorityLevel:a,startTime:c,expirationTime:e,sortIndex:-1};c>d?(a.sortIndex=c,f(t,a),null===h(r)&&a===h(t)&&(B?(E(L),L=-1):B=!0,K(H,c-d))):(a.sortIndex=e,f(r,a),A||z||(A=!0,I(J)));return a};
exports.unstable_shouldYield=M;exports.unstable_wrapCallback=function(a){var b=y;return function(){var c=y;y=b;try{return a.apply(this,arguments)}finally{y=c}}};


/***/ },

/***/ 540
(module, __unused_webpack_exports, __webpack_require__) {

"use strict";


if (true) {
  module.exports = __webpack_require__(287);
} else // removed by dead control flow
{}


/***/ },

/***/ 551
(__unused_webpack_module, exports, __webpack_require__) {

"use strict";
/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
/*
 Modernizr 3.0.0pre (Custom Build) | MIT
*/
var aa=__webpack_require__(540),ca=__webpack_require__(982);function p(a){for(var b="https://reactjs.org/docs/error-decoder.html?invariant="+a,c=1;c<arguments.length;c++)b+="&args[]="+encodeURIComponent(arguments[c]);return"Minified React error #"+a+"; visit "+b+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}var da=new Set,ea={};function fa(a,b){ha(a,b);ha(a+"Capture",b)}
function ha(a,b){ea[a]=b;for(a=0;a<b.length;a++)da.add(b[a])}
var ia=!("undefined"===typeof window||"undefined"===typeof window.document||"undefined"===typeof window.document.createElement),ja=Object.prototype.hasOwnProperty,ka=/^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/,la=
{},ma={};function oa(a){if(ja.call(ma,a))return!0;if(ja.call(la,a))return!1;if(ka.test(a))return ma[a]=!0;la[a]=!0;return!1}function pa(a,b,c,d){if(null!==c&&0===c.type)return!1;switch(typeof b){case "function":case "symbol":return!0;case "boolean":if(d)return!1;if(null!==c)return!c.acceptsBooleans;a=a.toLowerCase().slice(0,5);return"data-"!==a&&"aria-"!==a;default:return!1}}
function qa(a,b,c,d){if(null===b||"undefined"===typeof b||pa(a,b,c,d))return!0;if(d)return!1;if(null!==c)switch(c.type){case 3:return!b;case 4:return!1===b;case 5:return isNaN(b);case 6:return isNaN(b)||1>b}return!1}function v(a,b,c,d,e,f,g){this.acceptsBooleans=2===b||3===b||4===b;this.attributeName=d;this.attributeNamespace=e;this.mustUseProperty=c;this.propertyName=a;this.type=b;this.sanitizeURL=f;this.removeEmptyString=g}var z={};
"children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(a){z[a]=new v(a,0,!1,a,null,!1,!1)});[["acceptCharset","accept-charset"],["className","class"],["htmlFor","for"],["httpEquiv","http-equiv"]].forEach(function(a){var b=a[0];z[b]=new v(b,1,!1,a[1],null,!1,!1)});["contentEditable","draggable","spellCheck","value"].forEach(function(a){z[a]=new v(a,2,!1,a.toLowerCase(),null,!1,!1)});
["autoReverse","externalResourcesRequired","focusable","preserveAlpha"].forEach(function(a){z[a]=new v(a,2,!1,a,null,!1,!1)});"allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(a){z[a]=new v(a,3,!1,a.toLowerCase(),null,!1,!1)});
["checked","multiple","muted","selected"].forEach(function(a){z[a]=new v(a,3,!0,a,null,!1,!1)});["capture","download"].forEach(function(a){z[a]=new v(a,4,!1,a,null,!1,!1)});["cols","rows","size","span"].forEach(function(a){z[a]=new v(a,6,!1,a,null,!1,!1)});["rowSpan","start"].forEach(function(a){z[a]=new v(a,5,!1,a.toLowerCase(),null,!1,!1)});var ra=/[\-:]([a-z])/g;function sa(a){return a[1].toUpperCase()}
"accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(a){var b=a.replace(ra,
sa);z[b]=new v(b,1,!1,a,null,!1,!1)});"xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(a){var b=a.replace(ra,sa);z[b]=new v(b,1,!1,a,"http://www.w3.org/1999/xlink",!1,!1)});["xml:base","xml:lang","xml:space"].forEach(function(a){var b=a.replace(ra,sa);z[b]=new v(b,1,!1,a,"http://www.w3.org/XML/1998/namespace",!1,!1)});["tabIndex","crossOrigin"].forEach(function(a){z[a]=new v(a,1,!1,a.toLowerCase(),null,!1,!1)});
z.xlinkHref=new v("xlinkHref",1,!1,"xlink:href","http://www.w3.org/1999/xlink",!0,!1);["src","href","action","formAction"].forEach(function(a){z[a]=new v(a,1,!1,a.toLowerCase(),null,!0,!0)});
function ta(a,b,c,d){var e=z.hasOwnProperty(b)?z[b]:null;if(null!==e?0!==e.type:d||!(2<b.length)||"o"!==b[0]&&"O"!==b[0]||"n"!==b[1]&&"N"!==b[1])qa(b,c,e,d)&&(c=null),d||null===e?oa(b)&&(null===c?a.removeAttribute(b):a.setAttribute(b,""+c)):e.mustUseProperty?a[e.propertyName]=null===c?3===e.type?!1:"":c:(b=e.attributeName,d=e.attributeNamespace,null===c?a.removeAttribute(b):(e=e.type,c=3===e||4===e&&!0===c?"":""+c,d?a.setAttributeNS(d,b,c):a.setAttribute(b,c)))}
var ua=aa.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED,va=Symbol.for("react.element"),wa=Symbol.for("react.portal"),ya=Symbol.for("react.fragment"),za=Symbol.for("react.strict_mode"),Aa=Symbol.for("react.profiler"),Ba=Symbol.for("react.provider"),Ca=Symbol.for("react.context"),Da=Symbol.for("react.forward_ref"),Ea=Symbol.for("react.suspense"),Fa=Symbol.for("react.suspense_list"),Ga=Symbol.for("react.memo"),Ha=Symbol.for("react.lazy");Symbol.for("react.scope");Symbol.for("react.debug_trace_mode");
var Ia=Symbol.for("react.offscreen");Symbol.for("react.legacy_hidden");Symbol.for("react.cache");Symbol.for("react.tracing_marker");var Ja=Symbol.iterator;function Ka(a){if(null===a||"object"!==typeof a)return null;a=Ja&&a[Ja]||a["@@iterator"];return"function"===typeof a?a:null}var A=Object.assign,La;function Ma(a){if(void 0===La)try{throw Error();}catch(c){var b=c.stack.trim().match(/\n( *(at )?)/);La=b&&b[1]||""}return"\n"+La+a}var Na=!1;
function Oa(a,b){if(!a||Na)return"";Na=!0;var c=Error.prepareStackTrace;Error.prepareStackTrace=void 0;try{if(b)if(b=function(){throw Error();},Object.defineProperty(b.prototype,"props",{set:function(){throw Error();}}),"object"===typeof Reflect&&Reflect.construct){try{Reflect.construct(b,[])}catch(l){var d=l}Reflect.construct(a,[],b)}else{try{b.call()}catch(l){d=l}a.call(b.prototype)}else{try{throw Error();}catch(l){d=l}a()}}catch(l){if(l&&d&&"string"===typeof l.stack){for(var e=l.stack.split("\n"),
f=d.stack.split("\n"),g=e.length-1,h=f.length-1;1<=g&&0<=h&&e[g]!==f[h];)h--;for(;1<=g&&0<=h;g--,h--)if(e[g]!==f[h]){if(1!==g||1!==h){do if(g--,h--,0>h||e[g]!==f[h]){var k="\n"+e[g].replace(" at new "," at ");a.displayName&&k.includes("<anonymous>")&&(k=k.replace("<anonymous>",a.displayName));return k}while(1<=g&&0<=h)}break}}}finally{Na=!1,Error.prepareStackTrace=c}return(a=a?a.displayName||a.name:"")?Ma(a):""}
function Pa(a){switch(a.tag){case 5:return Ma(a.type);case 16:return Ma("Lazy");case 13:return Ma("Suspense");case 19:return Ma("SuspenseList");case 0:case 2:case 15:return a=Oa(a.type,!1),a;case 11:return a=Oa(a.type.render,!1),a;case 1:return a=Oa(a.type,!0),a;default:return""}}
function Qa(a){if(null==a)return null;if("function"===typeof a)return a.displayName||a.name||null;if("string"===typeof a)return a;switch(a){case ya:return"Fragment";case wa:return"Portal";case Aa:return"Profiler";case za:return"StrictMode";case Ea:return"Suspense";case Fa:return"SuspenseList"}if("object"===typeof a)switch(a.$$typeof){case Ca:return(a.displayName||"Context")+".Consumer";case Ba:return(a._context.displayName||"Context")+".Provider";case Da:var b=a.render;a=a.displayName;a||(a=b.displayName||
b.name||"",a=""!==a?"ForwardRef("+a+")":"ForwardRef");return a;case Ga:return b=a.displayName||null,null!==b?b:Qa(a.type)||"Memo";case Ha:b=a._payload;a=a._init;try{return Qa(a(b))}catch(c){}}return null}
function Ra(a){var b=a.type;switch(a.tag){case 24:return"Cache";case 9:return(b.displayName||"Context")+".Consumer";case 10:return(b._context.displayName||"Context")+".Provider";case 18:return"DehydratedFragment";case 11:return a=b.render,a=a.displayName||a.name||"",b.displayName||(""!==a?"ForwardRef("+a+")":"ForwardRef");case 7:return"Fragment";case 5:return b;case 4:return"Portal";case 3:return"Root";case 6:return"Text";case 16:return Qa(b);case 8:return b===za?"StrictMode":"Mode";case 22:return"Offscreen";
case 12:return"Profiler";case 21:return"Scope";case 13:return"Suspense";case 19:return"SuspenseList";case 25:return"TracingMarker";case 1:case 0:case 17:case 2:case 14:case 15:if("function"===typeof b)return b.displayName||b.name||null;if("string"===typeof b)return b}return null}function Sa(a){switch(typeof a){case "boolean":case "number":case "string":case "undefined":return a;case "object":return a;default:return""}}
function Ta(a){var b=a.type;return(a=a.nodeName)&&"input"===a.toLowerCase()&&("checkbox"===b||"radio"===b)}
function Ua(a){var b=Ta(a)?"checked":"value",c=Object.getOwnPropertyDescriptor(a.constructor.prototype,b),d=""+a[b];if(!a.hasOwnProperty(b)&&"undefined"!==typeof c&&"function"===typeof c.get&&"function"===typeof c.set){var e=c.get,f=c.set;Object.defineProperty(a,b,{configurable:!0,get:function(){return e.call(this)},set:function(a){d=""+a;f.call(this,a)}});Object.defineProperty(a,b,{enumerable:c.enumerable});return{getValue:function(){return d},setValue:function(a){d=""+a},stopTracking:function(){a._valueTracker=
null;delete a[b]}}}}function Va(a){a._valueTracker||(a._valueTracker=Ua(a))}function Wa(a){if(!a)return!1;var b=a._valueTracker;if(!b)return!0;var c=b.getValue();var d="";a&&(d=Ta(a)?a.checked?"true":"false":a.value);a=d;return a!==c?(b.setValue(a),!0):!1}function Xa(a){a=a||("undefined"!==typeof document?document:void 0);if("undefined"===typeof a)return null;try{return a.activeElement||a.body}catch(b){return a.body}}
function Ya(a,b){var c=b.checked;return A({},b,{defaultChecked:void 0,defaultValue:void 0,value:void 0,checked:null!=c?c:a._wrapperState.initialChecked})}function Za(a,b){var c=null==b.defaultValue?"":b.defaultValue,d=null!=b.checked?b.checked:b.defaultChecked;c=Sa(null!=b.value?b.value:c);a._wrapperState={initialChecked:d,initialValue:c,controlled:"checkbox"===b.type||"radio"===b.type?null!=b.checked:null!=b.value}}function ab(a,b){b=b.checked;null!=b&&ta(a,"checked",b,!1)}
function bb(a,b){ab(a,b);var c=Sa(b.value),d=b.type;if(null!=c)if("number"===d){if(0===c&&""===a.value||a.value!=c)a.value=""+c}else a.value!==""+c&&(a.value=""+c);else if("submit"===d||"reset"===d){a.removeAttribute("value");return}b.hasOwnProperty("value")?cb(a,b.type,c):b.hasOwnProperty("defaultValue")&&cb(a,b.type,Sa(b.defaultValue));null==b.checked&&null!=b.defaultChecked&&(a.defaultChecked=!!b.defaultChecked)}
function db(a,b,c){if(b.hasOwnProperty("value")||b.hasOwnProperty("defaultValue")){var d=b.type;if(!("submit"!==d&&"reset"!==d||void 0!==b.value&&null!==b.value))return;b=""+a._wrapperState.initialValue;c||b===a.value||(a.value=b);a.defaultValue=b}c=a.name;""!==c&&(a.name="");a.defaultChecked=!!a._wrapperState.initialChecked;""!==c&&(a.name=c)}
function cb(a,b,c){if("number"!==b||Xa(a.ownerDocument)!==a)null==c?a.defaultValue=""+a._wrapperState.initialValue:a.defaultValue!==""+c&&(a.defaultValue=""+c)}var eb=Array.isArray;
function fb(a,b,c,d){a=a.options;if(b){b={};for(var e=0;e<c.length;e++)b["$"+c[e]]=!0;for(c=0;c<a.length;c++)e=b.hasOwnProperty("$"+a[c].value),a[c].selected!==e&&(a[c].selected=e),e&&d&&(a[c].defaultSelected=!0)}else{c=""+Sa(c);b=null;for(e=0;e<a.length;e++){if(a[e].value===c){a[e].selected=!0;d&&(a[e].defaultSelected=!0);return}null!==b||a[e].disabled||(b=a[e])}null!==b&&(b.selected=!0)}}
function gb(a,b){if(null!=b.dangerouslySetInnerHTML)throw Error(p(91));return A({},b,{value:void 0,defaultValue:void 0,children:""+a._wrapperState.initialValue})}function hb(a,b){var c=b.value;if(null==c){c=b.children;b=b.defaultValue;if(null!=c){if(null!=b)throw Error(p(92));if(eb(c)){if(1<c.length)throw Error(p(93));c=c[0]}b=c}null==b&&(b="");c=b}a._wrapperState={initialValue:Sa(c)}}
function ib(a,b){var c=Sa(b.value),d=Sa(b.defaultValue);null!=c&&(c=""+c,c!==a.value&&(a.value=c),null==b.defaultValue&&a.defaultValue!==c&&(a.defaultValue=c));null!=d&&(a.defaultValue=""+d)}function jb(a){var b=a.textContent;b===a._wrapperState.initialValue&&""!==b&&null!==b&&(a.value=b)}function kb(a){switch(a){case "svg":return"http://www.w3.org/2000/svg";case "math":return"http://www.w3.org/1998/Math/MathML";default:return"http://www.w3.org/1999/xhtml"}}
function lb(a,b){return null==a||"http://www.w3.org/1999/xhtml"===a?kb(b):"http://www.w3.org/2000/svg"===a&&"foreignObject"===b?"http://www.w3.org/1999/xhtml":a}
var mb,nb=function(a){return"undefined"!==typeof MSApp&&MSApp.execUnsafeLocalFunction?function(b,c,d,e){MSApp.execUnsafeLocalFunction(function(){return a(b,c,d,e)})}:a}(function(a,b){if("http://www.w3.org/2000/svg"!==a.namespaceURI||"innerHTML"in a)a.innerHTML=b;else{mb=mb||document.createElement("div");mb.innerHTML="<svg>"+b.valueOf().toString()+"</svg>";for(b=mb.firstChild;a.firstChild;)a.removeChild(a.firstChild);for(;b.firstChild;)a.appendChild(b.firstChild)}});
function ob(a,b){if(b){var c=a.firstChild;if(c&&c===a.lastChild&&3===c.nodeType){c.nodeValue=b;return}}a.textContent=b}
var pb={animationIterationCount:!0,aspectRatio:!0,borderImageOutset:!0,borderImageSlice:!0,borderImageWidth:!0,boxFlex:!0,boxFlexGroup:!0,boxOrdinalGroup:!0,columnCount:!0,columns:!0,flex:!0,flexGrow:!0,flexPositive:!0,flexShrink:!0,flexNegative:!0,flexOrder:!0,gridArea:!0,gridRow:!0,gridRowEnd:!0,gridRowSpan:!0,gridRowStart:!0,gridColumn:!0,gridColumnEnd:!0,gridColumnSpan:!0,gridColumnStart:!0,fontWeight:!0,lineClamp:!0,lineHeight:!0,opacity:!0,order:!0,orphans:!0,tabSize:!0,widows:!0,zIndex:!0,
zoom:!0,fillOpacity:!0,floodOpacity:!0,stopOpacity:!0,strokeDasharray:!0,strokeDashoffset:!0,strokeMiterlimit:!0,strokeOpacity:!0,strokeWidth:!0},qb=["Webkit","ms","Moz","O"];Object.keys(pb).forEach(function(a){qb.forEach(function(b){b=b+a.charAt(0).toUpperCase()+a.substring(1);pb[b]=pb[a]})});function rb(a,b,c){return null==b||"boolean"===typeof b||""===b?"":c||"number"!==typeof b||0===b||pb.hasOwnProperty(a)&&pb[a]?(""+b).trim():b+"px"}
function sb(a,b){a=a.style;for(var c in b)if(b.hasOwnProperty(c)){var d=0===c.indexOf("--"),e=rb(c,b[c],d);"float"===c&&(c="cssFloat");d?a.setProperty(c,e):a[c]=e}}var tb=A({menuitem:!0},{area:!0,base:!0,br:!0,col:!0,embed:!0,hr:!0,img:!0,input:!0,keygen:!0,link:!0,meta:!0,param:!0,source:!0,track:!0,wbr:!0});
function ub(a,b){if(b){if(tb[a]&&(null!=b.children||null!=b.dangerouslySetInnerHTML))throw Error(p(137,a));if(null!=b.dangerouslySetInnerHTML){if(null!=b.children)throw Error(p(60));if("object"!==typeof b.dangerouslySetInnerHTML||!("__html"in b.dangerouslySetInnerHTML))throw Error(p(61));}if(null!=b.style&&"object"!==typeof b.style)throw Error(p(62));}}
function vb(a,b){if(-1===a.indexOf("-"))return"string"===typeof b.is;switch(a){case "annotation-xml":case "color-profile":case "font-face":case "font-face-src":case "font-face-uri":case "font-face-format":case "font-face-name":case "missing-glyph":return!1;default:return!0}}var wb=null;function xb(a){a=a.target||a.srcElement||window;a.correspondingUseElement&&(a=a.correspondingUseElement);return 3===a.nodeType?a.parentNode:a}var yb=null,zb=null,Ab=null;
function Bb(a){if(a=Cb(a)){if("function"!==typeof yb)throw Error(p(280));var b=a.stateNode;b&&(b=Db(b),yb(a.stateNode,a.type,b))}}function Eb(a){zb?Ab?Ab.push(a):Ab=[a]:zb=a}function Fb(){if(zb){var a=zb,b=Ab;Ab=zb=null;Bb(a);if(b)for(a=0;a<b.length;a++)Bb(b[a])}}function Gb(a,b){return a(b)}function Hb(){}var Ib=!1;function Jb(a,b,c){if(Ib)return a(b,c);Ib=!0;try{return Gb(a,b,c)}finally{if(Ib=!1,null!==zb||null!==Ab)Hb(),Fb()}}
function Kb(a,b){var c=a.stateNode;if(null===c)return null;var d=Db(c);if(null===d)return null;c=d[b];a:switch(b){case "onClick":case "onClickCapture":case "onDoubleClick":case "onDoubleClickCapture":case "onMouseDown":case "onMouseDownCapture":case "onMouseMove":case "onMouseMoveCapture":case "onMouseUp":case "onMouseUpCapture":case "onMouseEnter":(d=!d.disabled)||(a=a.type,d=!("button"===a||"input"===a||"select"===a||"textarea"===a));a=!d;break a;default:a=!1}if(a)return null;if(c&&"function"!==
typeof c)throw Error(p(231,b,typeof c));return c}var Lb=!1;if(ia)try{var Mb={};Object.defineProperty(Mb,"passive",{get:function(){Lb=!0}});window.addEventListener("test",Mb,Mb);window.removeEventListener("test",Mb,Mb)}catch(a){Lb=!1}function Nb(a,b,c,d,e,f,g,h,k){var l=Array.prototype.slice.call(arguments,3);try{b.apply(c,l)}catch(m){this.onError(m)}}var Ob=!1,Pb=null,Qb=!1,Rb=null,Sb={onError:function(a){Ob=!0;Pb=a}};function Tb(a,b,c,d,e,f,g,h,k){Ob=!1;Pb=null;Nb.apply(Sb,arguments)}
function Ub(a,b,c,d,e,f,g,h,k){Tb.apply(this,arguments);if(Ob){if(Ob){var l=Pb;Ob=!1;Pb=null}else throw Error(p(198));Qb||(Qb=!0,Rb=l)}}function Vb(a){var b=a,c=a;if(a.alternate)for(;b.return;)b=b.return;else{a=b;do b=a,0!==(b.flags&4098)&&(c=b.return),a=b.return;while(a)}return 3===b.tag?c:null}function Wb(a){if(13===a.tag){var b=a.memoizedState;null===b&&(a=a.alternate,null!==a&&(b=a.memoizedState));if(null!==b)return b.dehydrated}return null}function Xb(a){if(Vb(a)!==a)throw Error(p(188));}
function Yb(a){var b=a.alternate;if(!b){b=Vb(a);if(null===b)throw Error(p(188));return b!==a?null:a}for(var c=a,d=b;;){var e=c.return;if(null===e)break;var f=e.alternate;if(null===f){d=e.return;if(null!==d){c=d;continue}break}if(e.child===f.child){for(f=e.child;f;){if(f===c)return Xb(e),a;if(f===d)return Xb(e),b;f=f.sibling}throw Error(p(188));}if(c.return!==d.return)c=e,d=f;else{for(var g=!1,h=e.child;h;){if(h===c){g=!0;c=e;d=f;break}if(h===d){g=!0;d=e;c=f;break}h=h.sibling}if(!g){for(h=f.child;h;){if(h===
c){g=!0;c=f;d=e;break}if(h===d){g=!0;d=f;c=e;break}h=h.sibling}if(!g)throw Error(p(189));}}if(c.alternate!==d)throw Error(p(190));}if(3!==c.tag)throw Error(p(188));return c.stateNode.current===c?a:b}function Zb(a){a=Yb(a);return null!==a?$b(a):null}function $b(a){if(5===a.tag||6===a.tag)return a;for(a=a.child;null!==a;){var b=$b(a);if(null!==b)return b;a=a.sibling}return null}
var ac=ca.unstable_scheduleCallback,bc=ca.unstable_cancelCallback,cc=ca.unstable_shouldYield,dc=ca.unstable_requestPaint,B=ca.unstable_now,ec=ca.unstable_getCurrentPriorityLevel,fc=ca.unstable_ImmediatePriority,gc=ca.unstable_UserBlockingPriority,hc=ca.unstable_NormalPriority,ic=ca.unstable_LowPriority,jc=ca.unstable_IdlePriority,kc=null,lc=null;function mc(a){if(lc&&"function"===typeof lc.onCommitFiberRoot)try{lc.onCommitFiberRoot(kc,a,void 0,128===(a.current.flags&128))}catch(b){}}
var oc=Math.clz32?Math.clz32:nc,pc=Math.log,qc=Math.LN2;function nc(a){a>>>=0;return 0===a?32:31-(pc(a)/qc|0)|0}var rc=64,sc=4194304;
function tc(a){switch(a&-a){case 1:return 1;case 2:return 2;case 4:return 4;case 8:return 8;case 16:return 16;case 32:return 32;case 64:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return a&4194240;case 4194304:case 8388608:case 16777216:case 33554432:case 67108864:return a&130023424;case 134217728:return 134217728;case 268435456:return 268435456;case 536870912:return 536870912;case 1073741824:return 1073741824;
default:return a}}function uc(a,b){var c=a.pendingLanes;if(0===c)return 0;var d=0,e=a.suspendedLanes,f=a.pingedLanes,g=c&268435455;if(0!==g){var h=g&~e;0!==h?d=tc(h):(f&=g,0!==f&&(d=tc(f)))}else g=c&~e,0!==g?d=tc(g):0!==f&&(d=tc(f));if(0===d)return 0;if(0!==b&&b!==d&&0===(b&e)&&(e=d&-d,f=b&-b,e>=f||16===e&&0!==(f&4194240)))return b;0!==(d&4)&&(d|=c&16);b=a.entangledLanes;if(0!==b)for(a=a.entanglements,b&=d;0<b;)c=31-oc(b),e=1<<c,d|=a[c],b&=~e;return d}
function vc(a,b){switch(a){case 1:case 2:case 4:return b+250;case 8:case 16:case 32:case 64:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return b+5E3;case 4194304:case 8388608:case 16777216:case 33554432:case 67108864:return-1;case 134217728:case 268435456:case 536870912:case 1073741824:return-1;default:return-1}}
function wc(a,b){for(var c=a.suspendedLanes,d=a.pingedLanes,e=a.expirationTimes,f=a.pendingLanes;0<f;){var g=31-oc(f),h=1<<g,k=e[g];if(-1===k){if(0===(h&c)||0!==(h&d))e[g]=vc(h,b)}else k<=b&&(a.expiredLanes|=h);f&=~h}}function xc(a){a=a.pendingLanes&-1073741825;return 0!==a?a:a&1073741824?1073741824:0}function yc(){var a=rc;rc<<=1;0===(rc&4194240)&&(rc=64);return a}function zc(a){for(var b=[],c=0;31>c;c++)b.push(a);return b}
function Ac(a,b,c){a.pendingLanes|=b;536870912!==b&&(a.suspendedLanes=0,a.pingedLanes=0);a=a.eventTimes;b=31-oc(b);a[b]=c}function Bc(a,b){var c=a.pendingLanes&~b;a.pendingLanes=b;a.suspendedLanes=0;a.pingedLanes=0;a.expiredLanes&=b;a.mutableReadLanes&=b;a.entangledLanes&=b;b=a.entanglements;var d=a.eventTimes;for(a=a.expirationTimes;0<c;){var e=31-oc(c),f=1<<e;b[e]=0;d[e]=-1;a[e]=-1;c&=~f}}
function Cc(a,b){var c=a.entangledLanes|=b;for(a=a.entanglements;c;){var d=31-oc(c),e=1<<d;e&b|a[d]&b&&(a[d]|=b);c&=~e}}var C=0;function Dc(a){a&=-a;return 1<a?4<a?0!==(a&268435455)?16:536870912:4:1}var Ec,Fc,Gc,Hc,Ic,Jc=!1,Kc=[],Lc=null,Mc=null,Nc=null,Oc=new Map,Pc=new Map,Qc=[],Rc="mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
function Sc(a,b){switch(a){case "focusin":case "focusout":Lc=null;break;case "dragenter":case "dragleave":Mc=null;break;case "mouseover":case "mouseout":Nc=null;break;case "pointerover":case "pointerout":Oc.delete(b.pointerId);break;case "gotpointercapture":case "lostpointercapture":Pc.delete(b.pointerId)}}
function Tc(a,b,c,d,e,f){if(null===a||a.nativeEvent!==f)return a={blockedOn:b,domEventName:c,eventSystemFlags:d,nativeEvent:f,targetContainers:[e]},null!==b&&(b=Cb(b),null!==b&&Fc(b)),a;a.eventSystemFlags|=d;b=a.targetContainers;null!==e&&-1===b.indexOf(e)&&b.push(e);return a}
function Uc(a,b,c,d,e){switch(b){case "focusin":return Lc=Tc(Lc,a,b,c,d,e),!0;case "dragenter":return Mc=Tc(Mc,a,b,c,d,e),!0;case "mouseover":return Nc=Tc(Nc,a,b,c,d,e),!0;case "pointerover":var f=e.pointerId;Oc.set(f,Tc(Oc.get(f)||null,a,b,c,d,e));return!0;case "gotpointercapture":return f=e.pointerId,Pc.set(f,Tc(Pc.get(f)||null,a,b,c,d,e)),!0}return!1}
function Vc(a){var b=Wc(a.target);if(null!==b){var c=Vb(b);if(null!==c)if(b=c.tag,13===b){if(b=Wb(c),null!==b){a.blockedOn=b;Ic(a.priority,function(){Gc(c)});return}}else if(3===b&&c.stateNode.current.memoizedState.isDehydrated){a.blockedOn=3===c.tag?c.stateNode.containerInfo:null;return}}a.blockedOn=null}
function Xc(a){if(null!==a.blockedOn)return!1;for(var b=a.targetContainers;0<b.length;){var c=Yc(a.domEventName,a.eventSystemFlags,b[0],a.nativeEvent);if(null===c){c=a.nativeEvent;var d=new c.constructor(c.type,c);wb=d;c.target.dispatchEvent(d);wb=null}else return b=Cb(c),null!==b&&Fc(b),a.blockedOn=c,!1;b.shift()}return!0}function Zc(a,b,c){Xc(a)&&c.delete(b)}function $c(){Jc=!1;null!==Lc&&Xc(Lc)&&(Lc=null);null!==Mc&&Xc(Mc)&&(Mc=null);null!==Nc&&Xc(Nc)&&(Nc=null);Oc.forEach(Zc);Pc.forEach(Zc)}
function ad(a,b){a.blockedOn===b&&(a.blockedOn=null,Jc||(Jc=!0,ca.unstable_scheduleCallback(ca.unstable_NormalPriority,$c)))}
function bd(a){function b(b){return ad(b,a)}if(0<Kc.length){ad(Kc[0],a);for(var c=1;c<Kc.length;c++){var d=Kc[c];d.blockedOn===a&&(d.blockedOn=null)}}null!==Lc&&ad(Lc,a);null!==Mc&&ad(Mc,a);null!==Nc&&ad(Nc,a);Oc.forEach(b);Pc.forEach(b);for(c=0;c<Qc.length;c++)d=Qc[c],d.blockedOn===a&&(d.blockedOn=null);for(;0<Qc.length&&(c=Qc[0],null===c.blockedOn);)Vc(c),null===c.blockedOn&&Qc.shift()}var cd=ua.ReactCurrentBatchConfig,dd=!0;
function ed(a,b,c,d){var e=C,f=cd.transition;cd.transition=null;try{C=1,fd(a,b,c,d)}finally{C=e,cd.transition=f}}function gd(a,b,c,d){var e=C,f=cd.transition;cd.transition=null;try{C=4,fd(a,b,c,d)}finally{C=e,cd.transition=f}}
function fd(a,b,c,d){if(dd){var e=Yc(a,b,c,d);if(null===e)hd(a,b,d,id,c),Sc(a,d);else if(Uc(e,a,b,c,d))d.stopPropagation();else if(Sc(a,d),b&4&&-1<Rc.indexOf(a)){for(;null!==e;){var f=Cb(e);null!==f&&Ec(f);f=Yc(a,b,c,d);null===f&&hd(a,b,d,id,c);if(f===e)break;e=f}null!==e&&d.stopPropagation()}else hd(a,b,d,null,c)}}var id=null;
function Yc(a,b,c,d){id=null;a=xb(d);a=Wc(a);if(null!==a)if(b=Vb(a),null===b)a=null;else if(c=b.tag,13===c){a=Wb(b);if(null!==a)return a;a=null}else if(3===c){if(b.stateNode.current.memoizedState.isDehydrated)return 3===b.tag?b.stateNode.containerInfo:null;a=null}else b!==a&&(a=null);id=a;return null}
function jd(a){switch(a){case "cancel":case "click":case "close":case "contextmenu":case "copy":case "cut":case "auxclick":case "dblclick":case "dragend":case "dragstart":case "drop":case "focusin":case "focusout":case "input":case "invalid":case "keydown":case "keypress":case "keyup":case "mousedown":case "mouseup":case "paste":case "pause":case "play":case "pointercancel":case "pointerdown":case "pointerup":case "ratechange":case "reset":case "resize":case "seeked":case "submit":case "touchcancel":case "touchend":case "touchstart":case "volumechange":case "change":case "selectionchange":case "textInput":case "compositionstart":case "compositionend":case "compositionupdate":case "beforeblur":case "afterblur":case "beforeinput":case "blur":case "fullscreenchange":case "focus":case "hashchange":case "popstate":case "select":case "selectstart":return 1;case "drag":case "dragenter":case "dragexit":case "dragleave":case "dragover":case "mousemove":case "mouseout":case "mouseover":case "pointermove":case "pointerout":case "pointerover":case "scroll":case "toggle":case "touchmove":case "wheel":case "mouseenter":case "mouseleave":case "pointerenter":case "pointerleave":return 4;
case "message":switch(ec()){case fc:return 1;case gc:return 4;case hc:case ic:return 16;case jc:return 536870912;default:return 16}default:return 16}}var kd=null,ld=null,md=null;function nd(){if(md)return md;var a,b=ld,c=b.length,d,e="value"in kd?kd.value:kd.textContent,f=e.length;for(a=0;a<c&&b[a]===e[a];a++);var g=c-a;for(d=1;d<=g&&b[c-d]===e[f-d];d++);return md=e.slice(a,1<d?1-d:void 0)}
function od(a){var b=a.keyCode;"charCode"in a?(a=a.charCode,0===a&&13===b&&(a=13)):a=b;10===a&&(a=13);return 32<=a||13===a?a:0}function pd(){return!0}function qd(){return!1}
function rd(a){function b(b,d,e,f,g){this._reactName=b;this._targetInst=e;this.type=d;this.nativeEvent=f;this.target=g;this.currentTarget=null;for(var c in a)a.hasOwnProperty(c)&&(b=a[c],this[c]=b?b(f):f[c]);this.isDefaultPrevented=(null!=f.defaultPrevented?f.defaultPrevented:!1===f.returnValue)?pd:qd;this.isPropagationStopped=qd;return this}A(b.prototype,{preventDefault:function(){this.defaultPrevented=!0;var a=this.nativeEvent;a&&(a.preventDefault?a.preventDefault():"unknown"!==typeof a.returnValue&&
(a.returnValue=!1),this.isDefaultPrevented=pd)},stopPropagation:function(){var a=this.nativeEvent;a&&(a.stopPropagation?a.stopPropagation():"unknown"!==typeof a.cancelBubble&&(a.cancelBubble=!0),this.isPropagationStopped=pd)},persist:function(){},isPersistent:pd});return b}
var sd={eventPhase:0,bubbles:0,cancelable:0,timeStamp:function(a){return a.timeStamp||Date.now()},defaultPrevented:0,isTrusted:0},td=rd(sd),ud=A({},sd,{view:0,detail:0}),vd=rd(ud),wd,xd,yd,Ad=A({},ud,{screenX:0,screenY:0,clientX:0,clientY:0,pageX:0,pageY:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,getModifierState:zd,button:0,buttons:0,relatedTarget:function(a){return void 0===a.relatedTarget?a.fromElement===a.srcElement?a.toElement:a.fromElement:a.relatedTarget},movementX:function(a){if("movementX"in
a)return a.movementX;a!==yd&&(yd&&"mousemove"===a.type?(wd=a.screenX-yd.screenX,xd=a.screenY-yd.screenY):xd=wd=0,yd=a);return wd},movementY:function(a){return"movementY"in a?a.movementY:xd}}),Bd=rd(Ad),Cd=A({},Ad,{dataTransfer:0}),Dd=rd(Cd),Ed=A({},ud,{relatedTarget:0}),Fd=rd(Ed),Gd=A({},sd,{animationName:0,elapsedTime:0,pseudoElement:0}),Hd=rd(Gd),Id=A({},sd,{clipboardData:function(a){return"clipboardData"in a?a.clipboardData:window.clipboardData}}),Jd=rd(Id),Kd=A({},sd,{data:0}),Ld=rd(Kd),Md={Esc:"Escape",
Spacebar:" ",Left:"ArrowLeft",Up:"ArrowUp",Right:"ArrowRight",Down:"ArrowDown",Del:"Delete",Win:"OS",Menu:"ContextMenu",Apps:"ContextMenu",Scroll:"ScrollLock",MozPrintableKey:"Unidentified"},Nd={8:"Backspace",9:"Tab",12:"Clear",13:"Enter",16:"Shift",17:"Control",18:"Alt",19:"Pause",20:"CapsLock",27:"Escape",32:" ",33:"PageUp",34:"PageDown",35:"End",36:"Home",37:"ArrowLeft",38:"ArrowUp",39:"ArrowRight",40:"ArrowDown",45:"Insert",46:"Delete",112:"F1",113:"F2",114:"F3",115:"F4",116:"F5",117:"F6",118:"F7",
119:"F8",120:"F9",121:"F10",122:"F11",123:"F12",144:"NumLock",145:"ScrollLock",224:"Meta"},Od={Alt:"altKey",Control:"ctrlKey",Meta:"metaKey",Shift:"shiftKey"};function Pd(a){var b=this.nativeEvent;return b.getModifierState?b.getModifierState(a):(a=Od[a])?!!b[a]:!1}function zd(){return Pd}
var Qd=A({},ud,{key:function(a){if(a.key){var b=Md[a.key]||a.key;if("Unidentified"!==b)return b}return"keypress"===a.type?(a=od(a),13===a?"Enter":String.fromCharCode(a)):"keydown"===a.type||"keyup"===a.type?Nd[a.keyCode]||"Unidentified":""},code:0,location:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,repeat:0,locale:0,getModifierState:zd,charCode:function(a){return"keypress"===a.type?od(a):0},keyCode:function(a){return"keydown"===a.type||"keyup"===a.type?a.keyCode:0},which:function(a){return"keypress"===
a.type?od(a):"keydown"===a.type||"keyup"===a.type?a.keyCode:0}}),Rd=rd(Qd),Sd=A({},Ad,{pointerId:0,width:0,height:0,pressure:0,tangentialPressure:0,tiltX:0,tiltY:0,twist:0,pointerType:0,isPrimary:0}),Td=rd(Sd),Ud=A({},ud,{touches:0,targetTouches:0,changedTouches:0,altKey:0,metaKey:0,ctrlKey:0,shiftKey:0,getModifierState:zd}),Vd=rd(Ud),Wd=A({},sd,{propertyName:0,elapsedTime:0,pseudoElement:0}),Xd=rd(Wd),Yd=A({},Ad,{deltaX:function(a){return"deltaX"in a?a.deltaX:"wheelDeltaX"in a?-a.wheelDeltaX:0},
deltaY:function(a){return"deltaY"in a?a.deltaY:"wheelDeltaY"in a?-a.wheelDeltaY:"wheelDelta"in a?-a.wheelDelta:0},deltaZ:0,deltaMode:0}),Zd=rd(Yd),$d=[9,13,27,32],ae=ia&&"CompositionEvent"in window,be=null;ia&&"documentMode"in document&&(be=document.documentMode);var ce=ia&&"TextEvent"in window&&!be,de=ia&&(!ae||be&&8<be&&11>=be),ee=String.fromCharCode(32),fe=!1;
function ge(a,b){switch(a){case "keyup":return-1!==$d.indexOf(b.keyCode);case "keydown":return 229!==b.keyCode;case "keypress":case "mousedown":case "focusout":return!0;default:return!1}}function he(a){a=a.detail;return"object"===typeof a&&"data"in a?a.data:null}var ie=!1;function je(a,b){switch(a){case "compositionend":return he(b);case "keypress":if(32!==b.which)return null;fe=!0;return ee;case "textInput":return a=b.data,a===ee&&fe?null:a;default:return null}}
function ke(a,b){if(ie)return"compositionend"===a||!ae&&ge(a,b)?(a=nd(),md=ld=kd=null,ie=!1,a):null;switch(a){case "paste":return null;case "keypress":if(!(b.ctrlKey||b.altKey||b.metaKey)||b.ctrlKey&&b.altKey){if(b.char&&1<b.char.length)return b.char;if(b.which)return String.fromCharCode(b.which)}return null;case "compositionend":return de&&"ko"!==b.locale?null:b.data;default:return null}}
var le={color:!0,date:!0,datetime:!0,"datetime-local":!0,email:!0,month:!0,number:!0,password:!0,range:!0,search:!0,tel:!0,text:!0,time:!0,url:!0,week:!0};function me(a){var b=a&&a.nodeName&&a.nodeName.toLowerCase();return"input"===b?!!le[a.type]:"textarea"===b?!0:!1}function ne(a,b,c,d){Eb(d);b=oe(b,"onChange");0<b.length&&(c=new td("onChange","change",null,c,d),a.push({event:c,listeners:b}))}var pe=null,qe=null;function re(a){se(a,0)}function te(a){var b=ue(a);if(Wa(b))return a}
function ve(a,b){if("change"===a)return b}var we=!1;if(ia){var xe;if(ia){var ye="oninput"in document;if(!ye){var ze=document.createElement("div");ze.setAttribute("oninput","return;");ye="function"===typeof ze.oninput}xe=ye}else xe=!1;we=xe&&(!document.documentMode||9<document.documentMode)}function Ae(){pe&&(pe.detachEvent("onpropertychange",Be),qe=pe=null)}function Be(a){if("value"===a.propertyName&&te(qe)){var b=[];ne(b,qe,a,xb(a));Jb(re,b)}}
function Ce(a,b,c){"focusin"===a?(Ae(),pe=b,qe=c,pe.attachEvent("onpropertychange",Be)):"focusout"===a&&Ae()}function De(a){if("selectionchange"===a||"keyup"===a||"keydown"===a)return te(qe)}function Ee(a,b){if("click"===a)return te(b)}function Fe(a,b){if("input"===a||"change"===a)return te(b)}function Ge(a,b){return a===b&&(0!==a||1/a===1/b)||a!==a&&b!==b}var He="function"===typeof Object.is?Object.is:Ge;
function Ie(a,b){if(He(a,b))return!0;if("object"!==typeof a||null===a||"object"!==typeof b||null===b)return!1;var c=Object.keys(a),d=Object.keys(b);if(c.length!==d.length)return!1;for(d=0;d<c.length;d++){var e=c[d];if(!ja.call(b,e)||!He(a[e],b[e]))return!1}return!0}function Je(a){for(;a&&a.firstChild;)a=a.firstChild;return a}
function Ke(a,b){var c=Je(a);a=0;for(var d;c;){if(3===c.nodeType){d=a+c.textContent.length;if(a<=b&&d>=b)return{node:c,offset:b-a};a=d}a:{for(;c;){if(c.nextSibling){c=c.nextSibling;break a}c=c.parentNode}c=void 0}c=Je(c)}}function Le(a,b){return a&&b?a===b?!0:a&&3===a.nodeType?!1:b&&3===b.nodeType?Le(a,b.parentNode):"contains"in a?a.contains(b):a.compareDocumentPosition?!!(a.compareDocumentPosition(b)&16):!1:!1}
function Me(){for(var a=window,b=Xa();b instanceof a.HTMLIFrameElement;){try{var c="string"===typeof b.contentWindow.location.href}catch(d){c=!1}if(c)a=b.contentWindow;else break;b=Xa(a.document)}return b}function Ne(a){var b=a&&a.nodeName&&a.nodeName.toLowerCase();return b&&("input"===b&&("text"===a.type||"search"===a.type||"tel"===a.type||"url"===a.type||"password"===a.type)||"textarea"===b||"true"===a.contentEditable)}
function Oe(a){var b=Me(),c=a.focusedElem,d=a.selectionRange;if(b!==c&&c&&c.ownerDocument&&Le(c.ownerDocument.documentElement,c)){if(null!==d&&Ne(c))if(b=d.start,a=d.end,void 0===a&&(a=b),"selectionStart"in c)c.selectionStart=b,c.selectionEnd=Math.min(a,c.value.length);else if(a=(b=c.ownerDocument||document)&&b.defaultView||window,a.getSelection){a=a.getSelection();var e=c.textContent.length,f=Math.min(d.start,e);d=void 0===d.end?f:Math.min(d.end,e);!a.extend&&f>d&&(e=d,d=f,f=e);e=Ke(c,f);var g=Ke(c,
d);e&&g&&(1!==a.rangeCount||a.anchorNode!==e.node||a.anchorOffset!==e.offset||a.focusNode!==g.node||a.focusOffset!==g.offset)&&(b=b.createRange(),b.setStart(e.node,e.offset),a.removeAllRanges(),f>d?(a.addRange(b),a.extend(g.node,g.offset)):(b.setEnd(g.node,g.offset),a.addRange(b)))}b=[];for(a=c;a=a.parentNode;)1===a.nodeType&&b.push({element:a,left:a.scrollLeft,top:a.scrollTop});"function"===typeof c.focus&&c.focus();for(c=0;c<b.length;c++)a=b[c],a.element.scrollLeft=a.left,a.element.scrollTop=a.top}}
var Pe=ia&&"documentMode"in document&&11>=document.documentMode,Qe=null,Re=null,Se=null,Te=!1;
function Ue(a,b,c){var d=c.window===c?c.document:9===c.nodeType?c:c.ownerDocument;Te||null==Qe||Qe!==Xa(d)||(d=Qe,"selectionStart"in d&&Ne(d)?d={start:d.selectionStart,end:d.selectionEnd}:(d=(d.ownerDocument&&d.ownerDocument.defaultView||window).getSelection(),d={anchorNode:d.anchorNode,anchorOffset:d.anchorOffset,focusNode:d.focusNode,focusOffset:d.focusOffset}),Se&&Ie(Se,d)||(Se=d,d=oe(Re,"onSelect"),0<d.length&&(b=new td("onSelect","select",null,b,c),a.push({event:b,listeners:d}),b.target=Qe)))}
function Ve(a,b){var c={};c[a.toLowerCase()]=b.toLowerCase();c["Webkit"+a]="webkit"+b;c["Moz"+a]="moz"+b;return c}var We={animationend:Ve("Animation","AnimationEnd"),animationiteration:Ve("Animation","AnimationIteration"),animationstart:Ve("Animation","AnimationStart"),transitionend:Ve("Transition","TransitionEnd")},Xe={},Ye={};
ia&&(Ye=document.createElement("div").style,"AnimationEvent"in window||(delete We.animationend.animation,delete We.animationiteration.animation,delete We.animationstart.animation),"TransitionEvent"in window||delete We.transitionend.transition);function Ze(a){if(Xe[a])return Xe[a];if(!We[a])return a;var b=We[a],c;for(c in b)if(b.hasOwnProperty(c)&&c in Ye)return Xe[a]=b[c];return a}var $e=Ze("animationend"),af=Ze("animationiteration"),bf=Ze("animationstart"),cf=Ze("transitionend"),df=new Map,ef="abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
function ff(a,b){df.set(a,b);fa(b,[a])}for(var gf=0;gf<ef.length;gf++){var hf=ef[gf],jf=hf.toLowerCase(),kf=hf[0].toUpperCase()+hf.slice(1);ff(jf,"on"+kf)}ff($e,"onAnimationEnd");ff(af,"onAnimationIteration");ff(bf,"onAnimationStart");ff("dblclick","onDoubleClick");ff("focusin","onFocus");ff("focusout","onBlur");ff(cf,"onTransitionEnd");ha("onMouseEnter",["mouseout","mouseover"]);ha("onMouseLeave",["mouseout","mouseover"]);ha("onPointerEnter",["pointerout","pointerover"]);
ha("onPointerLeave",["pointerout","pointerover"]);fa("onChange","change click focusin focusout input keydown keyup selectionchange".split(" "));fa("onSelect","focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));fa("onBeforeInput",["compositionend","keypress","textInput","paste"]);fa("onCompositionEnd","compositionend focusout keydown keypress keyup mousedown".split(" "));fa("onCompositionStart","compositionstart focusout keydown keypress keyup mousedown".split(" "));
fa("onCompositionUpdate","compositionupdate focusout keydown keypress keyup mousedown".split(" "));var lf="abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "),mf=new Set("cancel close invalid load scroll toggle".split(" ").concat(lf));
function nf(a,b,c){var d=a.type||"unknown-event";a.currentTarget=c;Ub(d,b,void 0,a);a.currentTarget=null}
function se(a,b){b=0!==(b&4);for(var c=0;c<a.length;c++){var d=a[c],e=d.event;d=d.listeners;a:{var f=void 0;if(b)for(var g=d.length-1;0<=g;g--){var h=d[g],k=h.instance,l=h.currentTarget;h=h.listener;if(k!==f&&e.isPropagationStopped())break a;nf(e,h,l);f=k}else for(g=0;g<d.length;g++){h=d[g];k=h.instance;l=h.currentTarget;h=h.listener;if(k!==f&&e.isPropagationStopped())break a;nf(e,h,l);f=k}}}if(Qb)throw a=Rb,Qb=!1,Rb=null,a;}
function D(a,b){var c=b[of];void 0===c&&(c=b[of]=new Set);var d=a+"__bubble";c.has(d)||(pf(b,a,2,!1),c.add(d))}function qf(a,b,c){var d=0;b&&(d|=4);pf(c,a,d,b)}var rf="_reactListening"+Math.random().toString(36).slice(2);function sf(a){if(!a[rf]){a[rf]=!0;da.forEach(function(b){"selectionchange"!==b&&(mf.has(b)||qf(b,!1,a),qf(b,!0,a))});var b=9===a.nodeType?a:a.ownerDocument;null===b||b[rf]||(b[rf]=!0,qf("selectionchange",!1,b))}}
function pf(a,b,c,d){switch(jd(b)){case 1:var e=ed;break;case 4:e=gd;break;default:e=fd}c=e.bind(null,b,c,a);e=void 0;!Lb||"touchstart"!==b&&"touchmove"!==b&&"wheel"!==b||(e=!0);d?void 0!==e?a.addEventListener(b,c,{capture:!0,passive:e}):a.addEventListener(b,c,!0):void 0!==e?a.addEventListener(b,c,{passive:e}):a.addEventListener(b,c,!1)}
function hd(a,b,c,d,e){var f=d;if(0===(b&1)&&0===(b&2)&&null!==d)a:for(;;){if(null===d)return;var g=d.tag;if(3===g||4===g){var h=d.stateNode.containerInfo;if(h===e||8===h.nodeType&&h.parentNode===e)break;if(4===g)for(g=d.return;null!==g;){var k=g.tag;if(3===k||4===k)if(k=g.stateNode.containerInfo,k===e||8===k.nodeType&&k.parentNode===e)return;g=g.return}for(;null!==h;){g=Wc(h);if(null===g)return;k=g.tag;if(5===k||6===k){d=f=g;continue a}h=h.parentNode}}d=d.return}Jb(function(){var d=f,e=xb(c),g=[];
a:{var h=df.get(a);if(void 0!==h){var k=td,n=a;switch(a){case "keypress":if(0===od(c))break a;case "keydown":case "keyup":k=Rd;break;case "focusin":n="focus";k=Fd;break;case "focusout":n="blur";k=Fd;break;case "beforeblur":case "afterblur":k=Fd;break;case "click":if(2===c.button)break a;case "auxclick":case "dblclick":case "mousedown":case "mousemove":case "mouseup":case "mouseout":case "mouseover":case "contextmenu":k=Bd;break;case "drag":case "dragend":case "dragenter":case "dragexit":case "dragleave":case "dragover":case "dragstart":case "drop":k=
Dd;break;case "touchcancel":case "touchend":case "touchmove":case "touchstart":k=Vd;break;case $e:case af:case bf:k=Hd;break;case cf:k=Xd;break;case "scroll":k=vd;break;case "wheel":k=Zd;break;case "copy":case "cut":case "paste":k=Jd;break;case "gotpointercapture":case "lostpointercapture":case "pointercancel":case "pointerdown":case "pointermove":case "pointerout":case "pointerover":case "pointerup":k=Td}var t=0!==(b&4),J=!t&&"scroll"===a,x=t?null!==h?h+"Capture":null:h;t=[];for(var w=d,u;null!==
w;){u=w;var F=u.stateNode;5===u.tag&&null!==F&&(u=F,null!==x&&(F=Kb(w,x),null!=F&&t.push(tf(w,F,u))));if(J)break;w=w.return}0<t.length&&(h=new k(h,n,null,c,e),g.push({event:h,listeners:t}))}}if(0===(b&7)){a:{h="mouseover"===a||"pointerover"===a;k="mouseout"===a||"pointerout"===a;if(h&&c!==wb&&(n=c.relatedTarget||c.fromElement)&&(Wc(n)||n[uf]))break a;if(k||h){h=e.window===e?e:(h=e.ownerDocument)?h.defaultView||h.parentWindow:window;if(k){if(n=c.relatedTarget||c.toElement,k=d,n=n?Wc(n):null,null!==
n&&(J=Vb(n),n!==J||5!==n.tag&&6!==n.tag))n=null}else k=null,n=d;if(k!==n){t=Bd;F="onMouseLeave";x="onMouseEnter";w="mouse";if("pointerout"===a||"pointerover"===a)t=Td,F="onPointerLeave",x="onPointerEnter",w="pointer";J=null==k?h:ue(k);u=null==n?h:ue(n);h=new t(F,w+"leave",k,c,e);h.target=J;h.relatedTarget=u;F=null;Wc(e)===d&&(t=new t(x,w+"enter",n,c,e),t.target=u,t.relatedTarget=J,F=t);J=F;if(k&&n)b:{t=k;x=n;w=0;for(u=t;u;u=vf(u))w++;u=0;for(F=x;F;F=vf(F))u++;for(;0<w-u;)t=vf(t),w--;for(;0<u-w;)x=
vf(x),u--;for(;w--;){if(t===x||null!==x&&t===x.alternate)break b;t=vf(t);x=vf(x)}t=null}else t=null;null!==k&&wf(g,h,k,t,!1);null!==n&&null!==J&&wf(g,J,n,t,!0)}}}a:{h=d?ue(d):window;k=h.nodeName&&h.nodeName.toLowerCase();if("select"===k||"input"===k&&"file"===h.type)var na=ve;else if(me(h))if(we)na=Fe;else{na=De;var xa=Ce}else(k=h.nodeName)&&"input"===k.toLowerCase()&&("checkbox"===h.type||"radio"===h.type)&&(na=Ee);if(na&&(na=na(a,d))){ne(g,na,c,e);break a}xa&&xa(a,h,d);"focusout"===a&&(xa=h._wrapperState)&&
xa.controlled&&"number"===h.type&&cb(h,"number",h.value)}xa=d?ue(d):window;switch(a){case "focusin":if(me(xa)||"true"===xa.contentEditable)Qe=xa,Re=d,Se=null;break;case "focusout":Se=Re=Qe=null;break;case "mousedown":Te=!0;break;case "contextmenu":case "mouseup":case "dragend":Te=!1;Ue(g,c,e);break;case "selectionchange":if(Pe)break;case "keydown":case "keyup":Ue(g,c,e)}var $a;if(ae)b:{switch(a){case "compositionstart":var ba="onCompositionStart";break b;case "compositionend":ba="onCompositionEnd";
break b;case "compositionupdate":ba="onCompositionUpdate";break b}ba=void 0}else ie?ge(a,c)&&(ba="onCompositionEnd"):"keydown"===a&&229===c.keyCode&&(ba="onCompositionStart");ba&&(de&&"ko"!==c.locale&&(ie||"onCompositionStart"!==ba?"onCompositionEnd"===ba&&ie&&($a=nd()):(kd=e,ld="value"in kd?kd.value:kd.textContent,ie=!0)),xa=oe(d,ba),0<xa.length&&(ba=new Ld(ba,a,null,c,e),g.push({event:ba,listeners:xa}),$a?ba.data=$a:($a=he(c),null!==$a&&(ba.data=$a))));if($a=ce?je(a,c):ke(a,c))d=oe(d,"onBeforeInput"),
0<d.length&&(e=new Ld("onBeforeInput","beforeinput",null,c,e),g.push({event:e,listeners:d}),e.data=$a)}se(g,b)})}function tf(a,b,c){return{instance:a,listener:b,currentTarget:c}}function oe(a,b){for(var c=b+"Capture",d=[];null!==a;){var e=a,f=e.stateNode;5===e.tag&&null!==f&&(e=f,f=Kb(a,c),null!=f&&d.unshift(tf(a,f,e)),f=Kb(a,b),null!=f&&d.push(tf(a,f,e)));a=a.return}return d}function vf(a){if(null===a)return null;do a=a.return;while(a&&5!==a.tag);return a?a:null}
function wf(a,b,c,d,e){for(var f=b._reactName,g=[];null!==c&&c!==d;){var h=c,k=h.alternate,l=h.stateNode;if(null!==k&&k===d)break;5===h.tag&&null!==l&&(h=l,e?(k=Kb(c,f),null!=k&&g.unshift(tf(c,k,h))):e||(k=Kb(c,f),null!=k&&g.push(tf(c,k,h))));c=c.return}0!==g.length&&a.push({event:b,listeners:g})}var xf=/\r\n?/g,yf=/\u0000|\uFFFD/g;function zf(a){return("string"===typeof a?a:""+a).replace(xf,"\n").replace(yf,"")}function Af(a,b,c){b=zf(b);if(zf(a)!==b&&c)throw Error(p(425));}function Bf(){}
var Cf=null,Df=null;function Ef(a,b){return"textarea"===a||"noscript"===a||"string"===typeof b.children||"number"===typeof b.children||"object"===typeof b.dangerouslySetInnerHTML&&null!==b.dangerouslySetInnerHTML&&null!=b.dangerouslySetInnerHTML.__html}
var Ff="function"===typeof setTimeout?setTimeout:void 0,Gf="function"===typeof clearTimeout?clearTimeout:void 0,Hf="function"===typeof Promise?Promise:void 0,Jf="function"===typeof queueMicrotask?queueMicrotask:"undefined"!==typeof Hf?function(a){return Hf.resolve(null).then(a).catch(If)}:Ff;function If(a){setTimeout(function(){throw a;})}
function Kf(a,b){var c=b,d=0;do{var e=c.nextSibling;a.removeChild(c);if(e&&8===e.nodeType)if(c=e.data,"/$"===c){if(0===d){a.removeChild(e);bd(b);return}d--}else"$"!==c&&"$?"!==c&&"$!"!==c||d++;c=e}while(c);bd(b)}function Lf(a){for(;null!=a;a=a.nextSibling){var b=a.nodeType;if(1===b||3===b)break;if(8===b){b=a.data;if("$"===b||"$!"===b||"$?"===b)break;if("/$"===b)return null}}return a}
function Mf(a){a=a.previousSibling;for(var b=0;a;){if(8===a.nodeType){var c=a.data;if("$"===c||"$!"===c||"$?"===c){if(0===b)return a;b--}else"/$"===c&&b++}a=a.previousSibling}return null}var Nf=Math.random().toString(36).slice(2),Of="__reactFiber$"+Nf,Pf="__reactProps$"+Nf,uf="__reactContainer$"+Nf,of="__reactEvents$"+Nf,Qf="__reactListeners$"+Nf,Rf="__reactHandles$"+Nf;
function Wc(a){var b=a[Of];if(b)return b;for(var c=a.parentNode;c;){if(b=c[uf]||c[Of]){c=b.alternate;if(null!==b.child||null!==c&&null!==c.child)for(a=Mf(a);null!==a;){if(c=a[Of])return c;a=Mf(a)}return b}a=c;c=a.parentNode}return null}function Cb(a){a=a[Of]||a[uf];return!a||5!==a.tag&&6!==a.tag&&13!==a.tag&&3!==a.tag?null:a}function ue(a){if(5===a.tag||6===a.tag)return a.stateNode;throw Error(p(33));}function Db(a){return a[Pf]||null}var Sf=[],Tf=-1;function Uf(a){return{current:a}}
function E(a){0>Tf||(a.current=Sf[Tf],Sf[Tf]=null,Tf--)}function G(a,b){Tf++;Sf[Tf]=a.current;a.current=b}var Vf={},H=Uf(Vf),Wf=Uf(!1),Xf=Vf;function Yf(a,b){var c=a.type.contextTypes;if(!c)return Vf;var d=a.stateNode;if(d&&d.__reactInternalMemoizedUnmaskedChildContext===b)return d.__reactInternalMemoizedMaskedChildContext;var e={},f;for(f in c)e[f]=b[f];d&&(a=a.stateNode,a.__reactInternalMemoizedUnmaskedChildContext=b,a.__reactInternalMemoizedMaskedChildContext=e);return e}
function Zf(a){a=a.childContextTypes;return null!==a&&void 0!==a}function $f(){E(Wf);E(H)}function ag(a,b,c){if(H.current!==Vf)throw Error(p(168));G(H,b);G(Wf,c)}function bg(a,b,c){var d=a.stateNode;b=b.childContextTypes;if("function"!==typeof d.getChildContext)return c;d=d.getChildContext();for(var e in d)if(!(e in b))throw Error(p(108,Ra(a)||"Unknown",e));return A({},c,d)}
function cg(a){a=(a=a.stateNode)&&a.__reactInternalMemoizedMergedChildContext||Vf;Xf=H.current;G(H,a);G(Wf,Wf.current);return!0}function dg(a,b,c){var d=a.stateNode;if(!d)throw Error(p(169));c?(a=bg(a,b,Xf),d.__reactInternalMemoizedMergedChildContext=a,E(Wf),E(H),G(H,a)):E(Wf);G(Wf,c)}var eg=null,fg=!1,gg=!1;function hg(a){null===eg?eg=[a]:eg.push(a)}function ig(a){fg=!0;hg(a)}
function jg(){if(!gg&&null!==eg){gg=!0;var a=0,b=C;try{var c=eg;for(C=1;a<c.length;a++){var d=c[a];do d=d(!0);while(null!==d)}eg=null;fg=!1}catch(e){throw null!==eg&&(eg=eg.slice(a+1)),ac(fc,jg),e;}finally{C=b,gg=!1}}return null}var kg=[],lg=0,mg=null,ng=0,og=[],pg=0,qg=null,rg=1,sg="";function tg(a,b){kg[lg++]=ng;kg[lg++]=mg;mg=a;ng=b}
function ug(a,b,c){og[pg++]=rg;og[pg++]=sg;og[pg++]=qg;qg=a;var d=rg;a=sg;var e=32-oc(d)-1;d&=~(1<<e);c+=1;var f=32-oc(b)+e;if(30<f){var g=e-e%5;f=(d&(1<<g)-1).toString(32);d>>=g;e-=g;rg=1<<32-oc(b)+e|c<<e|d;sg=f+a}else rg=1<<f|c<<e|d,sg=a}function vg(a){null!==a.return&&(tg(a,1),ug(a,1,0))}function wg(a){for(;a===mg;)mg=kg[--lg],kg[lg]=null,ng=kg[--lg],kg[lg]=null;for(;a===qg;)qg=og[--pg],og[pg]=null,sg=og[--pg],og[pg]=null,rg=og[--pg],og[pg]=null}var xg=null,yg=null,I=!1,zg=null;
function Ag(a,b){var c=Bg(5,null,null,0);c.elementType="DELETED";c.stateNode=b;c.return=a;b=a.deletions;null===b?(a.deletions=[c],a.flags|=16):b.push(c)}
function Cg(a,b){switch(a.tag){case 5:var c=a.type;b=1!==b.nodeType||c.toLowerCase()!==b.nodeName.toLowerCase()?null:b;return null!==b?(a.stateNode=b,xg=a,yg=Lf(b.firstChild),!0):!1;case 6:return b=""===a.pendingProps||3!==b.nodeType?null:b,null!==b?(a.stateNode=b,xg=a,yg=null,!0):!1;case 13:return b=8!==b.nodeType?null:b,null!==b?(c=null!==qg?{id:rg,overflow:sg}:null,a.memoizedState={dehydrated:b,treeContext:c,retryLane:1073741824},c=Bg(18,null,null,0),c.stateNode=b,c.return=a,a.child=c,xg=a,yg=
null,!0):!1;default:return!1}}function Dg(a){return 0!==(a.mode&1)&&0===(a.flags&128)}function Eg(a){if(I){var b=yg;if(b){var c=b;if(!Cg(a,b)){if(Dg(a))throw Error(p(418));b=Lf(c.nextSibling);var d=xg;b&&Cg(a,b)?Ag(d,c):(a.flags=a.flags&-4097|2,I=!1,xg=a)}}else{if(Dg(a))throw Error(p(418));a.flags=a.flags&-4097|2;I=!1;xg=a}}}function Fg(a){for(a=a.return;null!==a&&5!==a.tag&&3!==a.tag&&13!==a.tag;)a=a.return;xg=a}
function Gg(a){if(a!==xg)return!1;if(!I)return Fg(a),I=!0,!1;var b;(b=3!==a.tag)&&!(b=5!==a.tag)&&(b=a.type,b="head"!==b&&"body"!==b&&!Ef(a.type,a.memoizedProps));if(b&&(b=yg)){if(Dg(a))throw Hg(),Error(p(418));for(;b;)Ag(a,b),b=Lf(b.nextSibling)}Fg(a);if(13===a.tag){a=a.memoizedState;a=null!==a?a.dehydrated:null;if(!a)throw Error(p(317));a:{a=a.nextSibling;for(b=0;a;){if(8===a.nodeType){var c=a.data;if("/$"===c){if(0===b){yg=Lf(a.nextSibling);break a}b--}else"$"!==c&&"$!"!==c&&"$?"!==c||b++}a=a.nextSibling}yg=
null}}else yg=xg?Lf(a.stateNode.nextSibling):null;return!0}function Hg(){for(var a=yg;a;)a=Lf(a.nextSibling)}function Ig(){yg=xg=null;I=!1}function Jg(a){null===zg?zg=[a]:zg.push(a)}var Kg=ua.ReactCurrentBatchConfig;function Lg(a,b){if(a&&a.defaultProps){b=A({},b);a=a.defaultProps;for(var c in a)void 0===b[c]&&(b[c]=a[c]);return b}return b}var Mg=Uf(null),Ng=null,Og=null,Pg=null;function Qg(){Pg=Og=Ng=null}function Rg(a){var b=Mg.current;E(Mg);a._currentValue=b}
function Sg(a,b,c){for(;null!==a;){var d=a.alternate;(a.childLanes&b)!==b?(a.childLanes|=b,null!==d&&(d.childLanes|=b)):null!==d&&(d.childLanes&b)!==b&&(d.childLanes|=b);if(a===c)break;a=a.return}}function Tg(a,b){Ng=a;Pg=Og=null;a=a.dependencies;null!==a&&null!==a.firstContext&&(0!==(a.lanes&b)&&(Ug=!0),a.firstContext=null)}
function Vg(a){var b=a._currentValue;if(Pg!==a)if(a={context:a,memoizedValue:b,next:null},null===Og){if(null===Ng)throw Error(p(308));Og=a;Ng.dependencies={lanes:0,firstContext:a}}else Og=Og.next=a;return b}var Wg=null;function Xg(a){null===Wg?Wg=[a]:Wg.push(a)}function Yg(a,b,c,d){var e=b.interleaved;null===e?(c.next=c,Xg(b)):(c.next=e.next,e.next=c);b.interleaved=c;return Zg(a,d)}
function Zg(a,b){a.lanes|=b;var c=a.alternate;null!==c&&(c.lanes|=b);c=a;for(a=a.return;null!==a;)a.childLanes|=b,c=a.alternate,null!==c&&(c.childLanes|=b),c=a,a=a.return;return 3===c.tag?c.stateNode:null}var $g=!1;function ah(a){a.updateQueue={baseState:a.memoizedState,firstBaseUpdate:null,lastBaseUpdate:null,shared:{pending:null,interleaved:null,lanes:0},effects:null}}
function bh(a,b){a=a.updateQueue;b.updateQueue===a&&(b.updateQueue={baseState:a.baseState,firstBaseUpdate:a.firstBaseUpdate,lastBaseUpdate:a.lastBaseUpdate,shared:a.shared,effects:a.effects})}function ch(a,b){return{eventTime:a,lane:b,tag:0,payload:null,callback:null,next:null}}
function dh(a,b,c){var d=a.updateQueue;if(null===d)return null;d=d.shared;if(0!==(K&2)){var e=d.pending;null===e?b.next=b:(b.next=e.next,e.next=b);d.pending=b;return Zg(a,c)}e=d.interleaved;null===e?(b.next=b,Xg(d)):(b.next=e.next,e.next=b);d.interleaved=b;return Zg(a,c)}function eh(a,b,c){b=b.updateQueue;if(null!==b&&(b=b.shared,0!==(c&4194240))){var d=b.lanes;d&=a.pendingLanes;c|=d;b.lanes=c;Cc(a,c)}}
function fh(a,b){var c=a.updateQueue,d=a.alternate;if(null!==d&&(d=d.updateQueue,c===d)){var e=null,f=null;c=c.firstBaseUpdate;if(null!==c){do{var g={eventTime:c.eventTime,lane:c.lane,tag:c.tag,payload:c.payload,callback:c.callback,next:null};null===f?e=f=g:f=f.next=g;c=c.next}while(null!==c);null===f?e=f=b:f=f.next=b}else e=f=b;c={baseState:d.baseState,firstBaseUpdate:e,lastBaseUpdate:f,shared:d.shared,effects:d.effects};a.updateQueue=c;return}a=c.lastBaseUpdate;null===a?c.firstBaseUpdate=b:a.next=
b;c.lastBaseUpdate=b}
function gh(a,b,c,d){var e=a.updateQueue;$g=!1;var f=e.firstBaseUpdate,g=e.lastBaseUpdate,h=e.shared.pending;if(null!==h){e.shared.pending=null;var k=h,l=k.next;k.next=null;null===g?f=l:g.next=l;g=k;var m=a.alternate;null!==m&&(m=m.updateQueue,h=m.lastBaseUpdate,h!==g&&(null===h?m.firstBaseUpdate=l:h.next=l,m.lastBaseUpdate=k))}if(null!==f){var q=e.baseState;g=0;m=l=k=null;h=f;do{var r=h.lane,y=h.eventTime;if((d&r)===r){null!==m&&(m=m.next={eventTime:y,lane:0,tag:h.tag,payload:h.payload,callback:h.callback,
next:null});a:{var n=a,t=h;r=b;y=c;switch(t.tag){case 1:n=t.payload;if("function"===typeof n){q=n.call(y,q,r);break a}q=n;break a;case 3:n.flags=n.flags&-65537|128;case 0:n=t.payload;r="function"===typeof n?n.call(y,q,r):n;if(null===r||void 0===r)break a;q=A({},q,r);break a;case 2:$g=!0}}null!==h.callback&&0!==h.lane&&(a.flags|=64,r=e.effects,null===r?e.effects=[h]:r.push(h))}else y={eventTime:y,lane:r,tag:h.tag,payload:h.payload,callback:h.callback,next:null},null===m?(l=m=y,k=q):m=m.next=y,g|=r;
h=h.next;if(null===h)if(h=e.shared.pending,null===h)break;else r=h,h=r.next,r.next=null,e.lastBaseUpdate=r,e.shared.pending=null}while(1);null===m&&(k=q);e.baseState=k;e.firstBaseUpdate=l;e.lastBaseUpdate=m;b=e.shared.interleaved;if(null!==b){e=b;do g|=e.lane,e=e.next;while(e!==b)}else null===f&&(e.shared.lanes=0);hh|=g;a.lanes=g;a.memoizedState=q}}
function ih(a,b,c){a=b.effects;b.effects=null;if(null!==a)for(b=0;b<a.length;b++){var d=a[b],e=d.callback;if(null!==e){d.callback=null;d=c;if("function"!==typeof e)throw Error(p(191,e));e.call(d)}}}var jh=(new aa.Component).refs;function kh(a,b,c,d){b=a.memoizedState;c=c(d,b);c=null===c||void 0===c?b:A({},b,c);a.memoizedState=c;0===a.lanes&&(a.updateQueue.baseState=c)}
var nh={isMounted:function(a){return(a=a._reactInternals)?Vb(a)===a:!1},enqueueSetState:function(a,b,c){a=a._reactInternals;var d=L(),e=lh(a),f=ch(d,e);f.payload=b;void 0!==c&&null!==c&&(f.callback=c);b=dh(a,f,e);null!==b&&(mh(b,a,e,d),eh(b,a,e))},enqueueReplaceState:function(a,b,c){a=a._reactInternals;var d=L(),e=lh(a),f=ch(d,e);f.tag=1;f.payload=b;void 0!==c&&null!==c&&(f.callback=c);b=dh(a,f,e);null!==b&&(mh(b,a,e,d),eh(b,a,e))},enqueueForceUpdate:function(a,b){a=a._reactInternals;var c=L(),d=
lh(a),e=ch(c,d);e.tag=2;void 0!==b&&null!==b&&(e.callback=b);b=dh(a,e,d);null!==b&&(mh(b,a,d,c),eh(b,a,d))}};function oh(a,b,c,d,e,f,g){a=a.stateNode;return"function"===typeof a.shouldComponentUpdate?a.shouldComponentUpdate(d,f,g):b.prototype&&b.prototype.isPureReactComponent?!Ie(c,d)||!Ie(e,f):!0}
function ph(a,b,c){var d=!1,e=Vf;var f=b.contextType;"object"===typeof f&&null!==f?f=Vg(f):(e=Zf(b)?Xf:H.current,d=b.contextTypes,f=(d=null!==d&&void 0!==d)?Yf(a,e):Vf);b=new b(c,f);a.memoizedState=null!==b.state&&void 0!==b.state?b.state:null;b.updater=nh;a.stateNode=b;b._reactInternals=a;d&&(a=a.stateNode,a.__reactInternalMemoizedUnmaskedChildContext=e,a.__reactInternalMemoizedMaskedChildContext=f);return b}
function qh(a,b,c,d){a=b.state;"function"===typeof b.componentWillReceiveProps&&b.componentWillReceiveProps(c,d);"function"===typeof b.UNSAFE_componentWillReceiveProps&&b.UNSAFE_componentWillReceiveProps(c,d);b.state!==a&&nh.enqueueReplaceState(b,b.state,null)}
function rh(a,b,c,d){var e=a.stateNode;e.props=c;e.state=a.memoizedState;e.refs=jh;ah(a);var f=b.contextType;"object"===typeof f&&null!==f?e.context=Vg(f):(f=Zf(b)?Xf:H.current,e.context=Yf(a,f));e.state=a.memoizedState;f=b.getDerivedStateFromProps;"function"===typeof f&&(kh(a,b,f,c),e.state=a.memoizedState);"function"===typeof b.getDerivedStateFromProps||"function"===typeof e.getSnapshotBeforeUpdate||"function"!==typeof e.UNSAFE_componentWillMount&&"function"!==typeof e.componentWillMount||(b=e.state,
"function"===typeof e.componentWillMount&&e.componentWillMount(),"function"===typeof e.UNSAFE_componentWillMount&&e.UNSAFE_componentWillMount(),b!==e.state&&nh.enqueueReplaceState(e,e.state,null),gh(a,c,e,d),e.state=a.memoizedState);"function"===typeof e.componentDidMount&&(a.flags|=4194308)}
function sh(a,b,c){a=c.ref;if(null!==a&&"function"!==typeof a&&"object"!==typeof a){if(c._owner){c=c._owner;if(c){if(1!==c.tag)throw Error(p(309));var d=c.stateNode}if(!d)throw Error(p(147,a));var e=d,f=""+a;if(null!==b&&null!==b.ref&&"function"===typeof b.ref&&b.ref._stringRef===f)return b.ref;b=function(a){var b=e.refs;b===jh&&(b=e.refs={});null===a?delete b[f]:b[f]=a};b._stringRef=f;return b}if("string"!==typeof a)throw Error(p(284));if(!c._owner)throw Error(p(290,a));}return a}
function th(a,b){a=Object.prototype.toString.call(b);throw Error(p(31,"[object Object]"===a?"object with keys {"+Object.keys(b).join(", ")+"}":a));}function uh(a){var b=a._init;return b(a._payload)}
function vh(a){function b(b,c){if(a){var d=b.deletions;null===d?(b.deletions=[c],b.flags|=16):d.push(c)}}function c(c,d){if(!a)return null;for(;null!==d;)b(c,d),d=d.sibling;return null}function d(a,b){for(a=new Map;null!==b;)null!==b.key?a.set(b.key,b):a.set(b.index,b),b=b.sibling;return a}function e(a,b){a=wh(a,b);a.index=0;a.sibling=null;return a}function f(b,c,d){b.index=d;if(!a)return b.flags|=1048576,c;d=b.alternate;if(null!==d)return d=d.index,d<c?(b.flags|=2,c):d;b.flags|=2;return c}function g(b){a&&
null===b.alternate&&(b.flags|=2);return b}function h(a,b,c,d){if(null===b||6!==b.tag)return b=xh(c,a.mode,d),b.return=a,b;b=e(b,c);b.return=a;return b}function k(a,b,c,d){var f=c.type;if(f===ya)return m(a,b,c.props.children,d,c.key);if(null!==b&&(b.elementType===f||"object"===typeof f&&null!==f&&f.$$typeof===Ha&&uh(f)===b.type))return d=e(b,c.props),d.ref=sh(a,b,c),d.return=a,d;d=yh(c.type,c.key,c.props,null,a.mode,d);d.ref=sh(a,b,c);d.return=a;return d}function l(a,b,c,d){if(null===b||4!==b.tag||
b.stateNode.containerInfo!==c.containerInfo||b.stateNode.implementation!==c.implementation)return b=zh(c,a.mode,d),b.return=a,b;b=e(b,c.children||[]);b.return=a;return b}function m(a,b,c,d,f){if(null===b||7!==b.tag)return b=Ah(c,a.mode,d,f),b.return=a,b;b=e(b,c);b.return=a;return b}function q(a,b,c){if("string"===typeof b&&""!==b||"number"===typeof b)return b=xh(""+b,a.mode,c),b.return=a,b;if("object"===typeof b&&null!==b){switch(b.$$typeof){case va:return c=yh(b.type,b.key,b.props,null,a.mode,c),
c.ref=sh(a,null,b),c.return=a,c;case wa:return b=zh(b,a.mode,c),b.return=a,b;case Ha:var d=b._init;return q(a,d(b._payload),c)}if(eb(b)||Ka(b))return b=Ah(b,a.mode,c,null),b.return=a,b;th(a,b)}return null}function r(a,b,c,d){var e=null!==b?b.key:null;if("string"===typeof c&&""!==c||"number"===typeof c)return null!==e?null:h(a,b,""+c,d);if("object"===typeof c&&null!==c){switch(c.$$typeof){case va:return c.key===e?k(a,b,c,d):null;case wa:return c.key===e?l(a,b,c,d):null;case Ha:return e=c._init,r(a,
b,e(c._payload),d)}if(eb(c)||Ka(c))return null!==e?null:m(a,b,c,d,null);th(a,c)}return null}function y(a,b,c,d,e){if("string"===typeof d&&""!==d||"number"===typeof d)return a=a.get(c)||null,h(b,a,""+d,e);if("object"===typeof d&&null!==d){switch(d.$$typeof){case va:return a=a.get(null===d.key?c:d.key)||null,k(b,a,d,e);case wa:return a=a.get(null===d.key?c:d.key)||null,l(b,a,d,e);case Ha:var f=d._init;return y(a,b,c,f(d._payload),e)}if(eb(d)||Ka(d))return a=a.get(c)||null,m(b,a,d,e,null);th(b,d)}return null}
function n(e,g,h,k){for(var l=null,m=null,u=g,w=g=0,x=null;null!==u&&w<h.length;w++){u.index>w?(x=u,u=null):x=u.sibling;var n=r(e,u,h[w],k);if(null===n){null===u&&(u=x);break}a&&u&&null===n.alternate&&b(e,u);g=f(n,g,w);null===m?l=n:m.sibling=n;m=n;u=x}if(w===h.length)return c(e,u),I&&tg(e,w),l;if(null===u){for(;w<h.length;w++)u=q(e,h[w],k),null!==u&&(g=f(u,g,w),null===m?l=u:m.sibling=u,m=u);I&&tg(e,w);return l}for(u=d(e,u);w<h.length;w++)x=y(u,e,w,h[w],k),null!==x&&(a&&null!==x.alternate&&u.delete(null===
x.key?w:x.key),g=f(x,g,w),null===m?l=x:m.sibling=x,m=x);a&&u.forEach(function(a){return b(e,a)});I&&tg(e,w);return l}function t(e,g,h,k){var l=Ka(h);if("function"!==typeof l)throw Error(p(150));h=l.call(h);if(null==h)throw Error(p(151));for(var u=l=null,m=g,w=g=0,x=null,n=h.next();null!==m&&!n.done;w++,n=h.next()){m.index>w?(x=m,m=null):x=m.sibling;var t=r(e,m,n.value,k);if(null===t){null===m&&(m=x);break}a&&m&&null===t.alternate&&b(e,m);g=f(t,g,w);null===u?l=t:u.sibling=t;u=t;m=x}if(n.done)return c(e,
m),I&&tg(e,w),l;if(null===m){for(;!n.done;w++,n=h.next())n=q(e,n.value,k),null!==n&&(g=f(n,g,w),null===u?l=n:u.sibling=n,u=n);I&&tg(e,w);return l}for(m=d(e,m);!n.done;w++,n=h.next())n=y(m,e,w,n.value,k),null!==n&&(a&&null!==n.alternate&&m.delete(null===n.key?w:n.key),g=f(n,g,w),null===u?l=n:u.sibling=n,u=n);a&&m.forEach(function(a){return b(e,a)});I&&tg(e,w);return l}function J(a,d,f,h){"object"===typeof f&&null!==f&&f.type===ya&&null===f.key&&(f=f.props.children);if("object"===typeof f&&null!==f){switch(f.$$typeof){case va:a:{for(var k=
f.key,l=d;null!==l;){if(l.key===k){k=f.type;if(k===ya){if(7===l.tag){c(a,l.sibling);d=e(l,f.props.children);d.return=a;a=d;break a}}else if(l.elementType===k||"object"===typeof k&&null!==k&&k.$$typeof===Ha&&uh(k)===l.type){c(a,l.sibling);d=e(l,f.props);d.ref=sh(a,l,f);d.return=a;a=d;break a}c(a,l);break}else b(a,l);l=l.sibling}f.type===ya?(d=Ah(f.props.children,a.mode,h,f.key),d.return=a,a=d):(h=yh(f.type,f.key,f.props,null,a.mode,h),h.ref=sh(a,d,f),h.return=a,a=h)}return g(a);case wa:a:{for(l=f.key;null!==
d;){if(d.key===l)if(4===d.tag&&d.stateNode.containerInfo===f.containerInfo&&d.stateNode.implementation===f.implementation){c(a,d.sibling);d=e(d,f.children||[]);d.return=a;a=d;break a}else{c(a,d);break}else b(a,d);d=d.sibling}d=zh(f,a.mode,h);d.return=a;a=d}return g(a);case Ha:return l=f._init,J(a,d,l(f._payload),h)}if(eb(f))return n(a,d,f,h);if(Ka(f))return t(a,d,f,h);th(a,f)}return"string"===typeof f&&""!==f||"number"===typeof f?(f=""+f,null!==d&&6===d.tag?(c(a,d.sibling),d=e(d,f),d.return=a,a=d):
(c(a,d),d=xh(f,a.mode,h),d.return=a,a=d),g(a)):c(a,d)}return J}var Bh=vh(!0),Ch=vh(!1),Dh={},Eh=Uf(Dh),Fh=Uf(Dh),Gh=Uf(Dh);function Hh(a){if(a===Dh)throw Error(p(174));return a}function Ih(a,b){G(Gh,b);G(Fh,a);G(Eh,Dh);a=b.nodeType;switch(a){case 9:case 11:b=(b=b.documentElement)?b.namespaceURI:lb(null,"");break;default:a=8===a?b.parentNode:b,b=a.namespaceURI||null,a=a.tagName,b=lb(b,a)}E(Eh);G(Eh,b)}function Jh(){E(Eh);E(Fh);E(Gh)}
function Kh(a){Hh(Gh.current);var b=Hh(Eh.current);var c=lb(b,a.type);b!==c&&(G(Fh,a),G(Eh,c))}function Lh(a){Fh.current===a&&(E(Eh),E(Fh))}var M=Uf(0);
function Mh(a){for(var b=a;null!==b;){if(13===b.tag){var c=b.memoizedState;if(null!==c&&(c=c.dehydrated,null===c||"$?"===c.data||"$!"===c.data))return b}else if(19===b.tag&&void 0!==b.memoizedProps.revealOrder){if(0!==(b.flags&128))return b}else if(null!==b.child){b.child.return=b;b=b.child;continue}if(b===a)break;for(;null===b.sibling;){if(null===b.return||b.return===a)return null;b=b.return}b.sibling.return=b.return;b=b.sibling}return null}var Nh=[];
function Oh(){for(var a=0;a<Nh.length;a++)Nh[a]._workInProgressVersionPrimary=null;Nh.length=0}var Ph=ua.ReactCurrentDispatcher,Qh=ua.ReactCurrentBatchConfig,Rh=0,N=null,O=null,P=null,Sh=!1,Th=!1,Uh=0,Vh=0;function Q(){throw Error(p(321));}function Wh(a,b){if(null===b)return!1;for(var c=0;c<b.length&&c<a.length;c++)if(!He(a[c],b[c]))return!1;return!0}
function Xh(a,b,c,d,e,f){Rh=f;N=b;b.memoizedState=null;b.updateQueue=null;b.lanes=0;Ph.current=null===a||null===a.memoizedState?Yh:Zh;a=c(d,e);if(Th){f=0;do{Th=!1;Uh=0;if(25<=f)throw Error(p(301));f+=1;P=O=null;b.updateQueue=null;Ph.current=$h;a=c(d,e)}while(Th)}Ph.current=ai;b=null!==O&&null!==O.next;Rh=0;P=O=N=null;Sh=!1;if(b)throw Error(p(300));return a}function bi(){var a=0!==Uh;Uh=0;return a}
function ci(){var a={memoizedState:null,baseState:null,baseQueue:null,queue:null,next:null};null===P?N.memoizedState=P=a:P=P.next=a;return P}function di(){if(null===O){var a=N.alternate;a=null!==a?a.memoizedState:null}else a=O.next;var b=null===P?N.memoizedState:P.next;if(null!==b)P=b,O=a;else{if(null===a)throw Error(p(310));O=a;a={memoizedState:O.memoizedState,baseState:O.baseState,baseQueue:O.baseQueue,queue:O.queue,next:null};null===P?N.memoizedState=P=a:P=P.next=a}return P}
function ei(a,b){return"function"===typeof b?b(a):b}
function fi(a){var b=di(),c=b.queue;if(null===c)throw Error(p(311));c.lastRenderedReducer=a;var d=O,e=d.baseQueue,f=c.pending;if(null!==f){if(null!==e){var g=e.next;e.next=f.next;f.next=g}d.baseQueue=e=f;c.pending=null}if(null!==e){f=e.next;d=d.baseState;var h=g=null,k=null,l=f;do{var m=l.lane;if((Rh&m)===m)null!==k&&(k=k.next={lane:0,action:l.action,hasEagerState:l.hasEagerState,eagerState:l.eagerState,next:null}),d=l.hasEagerState?l.eagerState:a(d,l.action);else{var q={lane:m,action:l.action,hasEagerState:l.hasEagerState,
eagerState:l.eagerState,next:null};null===k?(h=k=q,g=d):k=k.next=q;N.lanes|=m;hh|=m}l=l.next}while(null!==l&&l!==f);null===k?g=d:k.next=h;He(d,b.memoizedState)||(Ug=!0);b.memoizedState=d;b.baseState=g;b.baseQueue=k;c.lastRenderedState=d}a=c.interleaved;if(null!==a){e=a;do f=e.lane,N.lanes|=f,hh|=f,e=e.next;while(e!==a)}else null===e&&(c.lanes=0);return[b.memoizedState,c.dispatch]}
function gi(a){var b=di(),c=b.queue;if(null===c)throw Error(p(311));c.lastRenderedReducer=a;var d=c.dispatch,e=c.pending,f=b.memoizedState;if(null!==e){c.pending=null;var g=e=e.next;do f=a(f,g.action),g=g.next;while(g!==e);He(f,b.memoizedState)||(Ug=!0);b.memoizedState=f;null===b.baseQueue&&(b.baseState=f);c.lastRenderedState=f}return[f,d]}function hi(){}
function ii(a,b){var c=N,d=di(),e=b(),f=!He(d.memoizedState,e);f&&(d.memoizedState=e,Ug=!0);d=d.queue;ji(ki.bind(null,c,d,a),[a]);if(d.getSnapshot!==b||f||null!==P&&P.memoizedState.tag&1){c.flags|=2048;li(9,mi.bind(null,c,d,e,b),void 0,null);if(null===R)throw Error(p(349));0!==(Rh&30)||ni(c,b,e)}return e}function ni(a,b,c){a.flags|=16384;a={getSnapshot:b,value:c};b=N.updateQueue;null===b?(b={lastEffect:null,stores:null},N.updateQueue=b,b.stores=[a]):(c=b.stores,null===c?b.stores=[a]:c.push(a))}
function mi(a,b,c,d){b.value=c;b.getSnapshot=d;oi(b)&&pi(a)}function ki(a,b,c){return c(function(){oi(b)&&pi(a)})}function oi(a){var b=a.getSnapshot;a=a.value;try{var c=b();return!He(a,c)}catch(d){return!0}}function pi(a){var b=Zg(a,1);null!==b&&mh(b,a,1,-1)}
function qi(a){var b=ci();"function"===typeof a&&(a=a());b.memoizedState=b.baseState=a;a={pending:null,interleaved:null,lanes:0,dispatch:null,lastRenderedReducer:ei,lastRenderedState:a};b.queue=a;a=a.dispatch=ri.bind(null,N,a);return[b.memoizedState,a]}
function li(a,b,c,d){a={tag:a,create:b,destroy:c,deps:d,next:null};b=N.updateQueue;null===b?(b={lastEffect:null,stores:null},N.updateQueue=b,b.lastEffect=a.next=a):(c=b.lastEffect,null===c?b.lastEffect=a.next=a:(d=c.next,c.next=a,a.next=d,b.lastEffect=a));return a}function si(){return di().memoizedState}function ti(a,b,c,d){var e=ci();N.flags|=a;e.memoizedState=li(1|b,c,void 0,void 0===d?null:d)}
function ui(a,b,c,d){var e=di();d=void 0===d?null:d;var f=void 0;if(null!==O){var g=O.memoizedState;f=g.destroy;if(null!==d&&Wh(d,g.deps)){e.memoizedState=li(b,c,f,d);return}}N.flags|=a;e.memoizedState=li(1|b,c,f,d)}function vi(a,b){return ti(8390656,8,a,b)}function ji(a,b){return ui(2048,8,a,b)}function wi(a,b){return ui(4,2,a,b)}function xi(a,b){return ui(4,4,a,b)}
function yi(a,b){if("function"===typeof b)return a=a(),b(a),function(){b(null)};if(null!==b&&void 0!==b)return a=a(),b.current=a,function(){b.current=null}}function zi(a,b,c){c=null!==c&&void 0!==c?c.concat([a]):null;return ui(4,4,yi.bind(null,b,a),c)}function Ai(){}function Bi(a,b){var c=di();b=void 0===b?null:b;var d=c.memoizedState;if(null!==d&&null!==b&&Wh(b,d[1]))return d[0];c.memoizedState=[a,b];return a}
function Ci(a,b){var c=di();b=void 0===b?null:b;var d=c.memoizedState;if(null!==d&&null!==b&&Wh(b,d[1]))return d[0];a=a();c.memoizedState=[a,b];return a}function Di(a,b,c){if(0===(Rh&21))return a.baseState&&(a.baseState=!1,Ug=!0),a.memoizedState=c;He(c,b)||(c=yc(),N.lanes|=c,hh|=c,a.baseState=!0);return b}function Ei(a,b){var c=C;C=0!==c&&4>c?c:4;a(!0);var d=Qh.transition;Qh.transition={};try{a(!1),b()}finally{C=c,Qh.transition=d}}function Fi(){return di().memoizedState}
function Gi(a,b,c){var d=lh(a);c={lane:d,action:c,hasEagerState:!1,eagerState:null,next:null};if(Hi(a))Ii(b,c);else if(c=Yg(a,b,c,d),null!==c){var e=L();mh(c,a,d,e);Ji(c,b,d)}}
function ri(a,b,c){var d=lh(a),e={lane:d,action:c,hasEagerState:!1,eagerState:null,next:null};if(Hi(a))Ii(b,e);else{var f=a.alternate;if(0===a.lanes&&(null===f||0===f.lanes)&&(f=b.lastRenderedReducer,null!==f))try{var g=b.lastRenderedState,h=f(g,c);e.hasEagerState=!0;e.eagerState=h;if(He(h,g)){var k=b.interleaved;null===k?(e.next=e,Xg(b)):(e.next=k.next,k.next=e);b.interleaved=e;return}}catch(l){}finally{}c=Yg(a,b,e,d);null!==c&&(e=L(),mh(c,a,d,e),Ji(c,b,d))}}
function Hi(a){var b=a.alternate;return a===N||null!==b&&b===N}function Ii(a,b){Th=Sh=!0;var c=a.pending;null===c?b.next=b:(b.next=c.next,c.next=b);a.pending=b}function Ji(a,b,c){if(0!==(c&4194240)){var d=b.lanes;d&=a.pendingLanes;c|=d;b.lanes=c;Cc(a,c)}}
var ai={readContext:Vg,useCallback:Q,useContext:Q,useEffect:Q,useImperativeHandle:Q,useInsertionEffect:Q,useLayoutEffect:Q,useMemo:Q,useReducer:Q,useRef:Q,useState:Q,useDebugValue:Q,useDeferredValue:Q,useTransition:Q,useMutableSource:Q,useSyncExternalStore:Q,useId:Q,unstable_isNewReconciler:!1},Yh={readContext:Vg,useCallback:function(a,b){ci().memoizedState=[a,void 0===b?null:b];return a},useContext:Vg,useEffect:vi,useImperativeHandle:function(a,b,c){c=null!==c&&void 0!==c?c.concat([a]):null;return ti(4194308,
4,yi.bind(null,b,a),c)},useLayoutEffect:function(a,b){return ti(4194308,4,a,b)},useInsertionEffect:function(a,b){return ti(4,2,a,b)},useMemo:function(a,b){var c=ci();b=void 0===b?null:b;a=a();c.memoizedState=[a,b];return a},useReducer:function(a,b,c){var d=ci();b=void 0!==c?c(b):b;d.memoizedState=d.baseState=b;a={pending:null,interleaved:null,lanes:0,dispatch:null,lastRenderedReducer:a,lastRenderedState:b};d.queue=a;a=a.dispatch=Gi.bind(null,N,a);return[d.memoizedState,a]},useRef:function(a){var b=
ci();a={current:a};return b.memoizedState=a},useState:qi,useDebugValue:Ai,useDeferredValue:function(a){return ci().memoizedState=a},useTransition:function(){var a=qi(!1),b=a[0];a=Ei.bind(null,a[1]);ci().memoizedState=a;return[b,a]},useMutableSource:function(){},useSyncExternalStore:function(a,b,c){var d=N,e=ci();if(I){if(void 0===c)throw Error(p(407));c=c()}else{c=b();if(null===R)throw Error(p(349));0!==(Rh&30)||ni(d,b,c)}e.memoizedState=c;var f={value:c,getSnapshot:b};e.queue=f;vi(ki.bind(null,d,
f,a),[a]);d.flags|=2048;li(9,mi.bind(null,d,f,c,b),void 0,null);return c},useId:function(){var a=ci(),b=R.identifierPrefix;if(I){var c=sg;var d=rg;c=(d&~(1<<32-oc(d)-1)).toString(32)+c;b=":"+b+"R"+c;c=Uh++;0<c&&(b+="H"+c.toString(32));b+=":"}else c=Vh++,b=":"+b+"r"+c.toString(32)+":";return a.memoizedState=b},unstable_isNewReconciler:!1},Zh={readContext:Vg,useCallback:Bi,useContext:Vg,useEffect:ji,useImperativeHandle:zi,useInsertionEffect:wi,useLayoutEffect:xi,useMemo:Ci,useReducer:fi,useRef:si,useState:function(){return fi(ei)},
useDebugValue:Ai,useDeferredValue:function(a){var b=di();return Di(b,O.memoizedState,a)},useTransition:function(){var a=fi(ei)[0],b=di().memoizedState;return[a,b]},useMutableSource:hi,useSyncExternalStore:ii,useId:Fi,unstable_isNewReconciler:!1},$h={readContext:Vg,useCallback:Bi,useContext:Vg,useEffect:ji,useImperativeHandle:zi,useInsertionEffect:wi,useLayoutEffect:xi,useMemo:Ci,useReducer:gi,useRef:si,useState:function(){return gi(ei)},useDebugValue:Ai,useDeferredValue:function(a){var b=di();return null===
O?b.memoizedState=a:Di(b,O.memoizedState,a)},useTransition:function(){var a=gi(ei)[0],b=di().memoizedState;return[a,b]},useMutableSource:hi,useSyncExternalStore:ii,useId:Fi,unstable_isNewReconciler:!1};function Ki(a,b){try{var c="",d=b;do c+=Pa(d),d=d.return;while(d);var e=c}catch(f){e="\nError generating stack: "+f.message+"\n"+f.stack}return{value:a,source:b,stack:e,digest:null}}function Li(a,b,c){return{value:a,source:null,stack:null!=c?c:null,digest:null!=b?b:null}}
function Mi(a,b){try{console.error(b.value)}catch(c){setTimeout(function(){throw c;})}}var Ni="function"===typeof WeakMap?WeakMap:Map;function Oi(a,b,c){c=ch(-1,c);c.tag=3;c.payload={element:null};var d=b.value;c.callback=function(){Pi||(Pi=!0,Qi=d);Mi(a,b)};return c}
function Ri(a,b,c){c=ch(-1,c);c.tag=3;var d=a.type.getDerivedStateFromError;if("function"===typeof d){var e=b.value;c.payload=function(){return d(e)};c.callback=function(){Mi(a,b)}}var f=a.stateNode;null!==f&&"function"===typeof f.componentDidCatch&&(c.callback=function(){Mi(a,b);"function"!==typeof d&&(null===Si?Si=new Set([this]):Si.add(this));var c=b.stack;this.componentDidCatch(b.value,{componentStack:null!==c?c:""})});return c}
function Ti(a,b,c){var d=a.pingCache;if(null===d){d=a.pingCache=new Ni;var e=new Set;d.set(b,e)}else e=d.get(b),void 0===e&&(e=new Set,d.set(b,e));e.has(c)||(e.add(c),a=Ui.bind(null,a,b,c),b.then(a,a))}function Vi(a){do{var b;if(b=13===a.tag)b=a.memoizedState,b=null!==b?null!==b.dehydrated?!0:!1:!0;if(b)return a;a=a.return}while(null!==a);return null}
function Wi(a,b,c,d,e){if(0===(a.mode&1))return a===b?a.flags|=65536:(a.flags|=128,c.flags|=131072,c.flags&=-52805,1===c.tag&&(null===c.alternate?c.tag=17:(b=ch(-1,1),b.tag=2,dh(c,b,1))),c.lanes|=1),a;a.flags|=65536;a.lanes=e;return a}var Xi=ua.ReactCurrentOwner,Ug=!1;function Yi(a,b,c,d){b.child=null===a?Ch(b,null,c,d):Bh(b,a.child,c,d)}
function Zi(a,b,c,d,e){c=c.render;var f=b.ref;Tg(b,e);d=Xh(a,b,c,d,f,e);c=bi();if(null!==a&&!Ug)return b.updateQueue=a.updateQueue,b.flags&=-2053,a.lanes&=~e,$i(a,b,e);I&&c&&vg(b);b.flags|=1;Yi(a,b,d,e);return b.child}
function aj(a,b,c,d,e){if(null===a){var f=c.type;if("function"===typeof f&&!bj(f)&&void 0===f.defaultProps&&null===c.compare&&void 0===c.defaultProps)return b.tag=15,b.type=f,cj(a,b,f,d,e);a=yh(c.type,null,d,b,b.mode,e);a.ref=b.ref;a.return=b;return b.child=a}f=a.child;if(0===(a.lanes&e)){var g=f.memoizedProps;c=c.compare;c=null!==c?c:Ie;if(c(g,d)&&a.ref===b.ref)return $i(a,b,e)}b.flags|=1;a=wh(f,d);a.ref=b.ref;a.return=b;return b.child=a}
function cj(a,b,c,d,e){if(null!==a){var f=a.memoizedProps;if(Ie(f,d)&&a.ref===b.ref)if(Ug=!1,b.pendingProps=d=f,0!==(a.lanes&e))0!==(a.flags&131072)&&(Ug=!0);else return b.lanes=a.lanes,$i(a,b,e)}return dj(a,b,c,d,e)}
function ej(a,b,c){var d=b.pendingProps,e=d.children,f=null!==a?a.memoizedState:null;if("hidden"===d.mode)if(0===(b.mode&1))b.memoizedState={baseLanes:0,cachePool:null,transitions:null},G(fj,gj),gj|=c;else{if(0===(c&1073741824))return a=null!==f?f.baseLanes|c:c,b.lanes=b.childLanes=1073741824,b.memoizedState={baseLanes:a,cachePool:null,transitions:null},b.updateQueue=null,G(fj,gj),gj|=a,null;b.memoizedState={baseLanes:0,cachePool:null,transitions:null};d=null!==f?f.baseLanes:c;G(fj,gj);gj|=d}else null!==
f?(d=f.baseLanes|c,b.memoizedState=null):d=c,G(fj,gj),gj|=d;Yi(a,b,e,c);return b.child}function hj(a,b){var c=b.ref;if(null===a&&null!==c||null!==a&&a.ref!==c)b.flags|=512,b.flags|=2097152}function dj(a,b,c,d,e){var f=Zf(c)?Xf:H.current;f=Yf(b,f);Tg(b,e);c=Xh(a,b,c,d,f,e);d=bi();if(null!==a&&!Ug)return b.updateQueue=a.updateQueue,b.flags&=-2053,a.lanes&=~e,$i(a,b,e);I&&d&&vg(b);b.flags|=1;Yi(a,b,c,e);return b.child}
function ij(a,b,c,d,e){if(Zf(c)){var f=!0;cg(b)}else f=!1;Tg(b,e);if(null===b.stateNode)jj(a,b),ph(b,c,d),rh(b,c,d,e),d=!0;else if(null===a){var g=b.stateNode,h=b.memoizedProps;g.props=h;var k=g.context,l=c.contextType;"object"===typeof l&&null!==l?l=Vg(l):(l=Zf(c)?Xf:H.current,l=Yf(b,l));var m=c.getDerivedStateFromProps,q="function"===typeof m||"function"===typeof g.getSnapshotBeforeUpdate;q||"function"!==typeof g.UNSAFE_componentWillReceiveProps&&"function"!==typeof g.componentWillReceiveProps||
(h!==d||k!==l)&&qh(b,g,d,l);$g=!1;var r=b.memoizedState;g.state=r;gh(b,d,g,e);k=b.memoizedState;h!==d||r!==k||Wf.current||$g?("function"===typeof m&&(kh(b,c,m,d),k=b.memoizedState),(h=$g||oh(b,c,h,d,r,k,l))?(q||"function"!==typeof g.UNSAFE_componentWillMount&&"function"!==typeof g.componentWillMount||("function"===typeof g.componentWillMount&&g.componentWillMount(),"function"===typeof g.UNSAFE_componentWillMount&&g.UNSAFE_componentWillMount()),"function"===typeof g.componentDidMount&&(b.flags|=4194308)):
("function"===typeof g.componentDidMount&&(b.flags|=4194308),b.memoizedProps=d,b.memoizedState=k),g.props=d,g.state=k,g.context=l,d=h):("function"===typeof g.componentDidMount&&(b.flags|=4194308),d=!1)}else{g=b.stateNode;bh(a,b);h=b.memoizedProps;l=b.type===b.elementType?h:Lg(b.type,h);g.props=l;q=b.pendingProps;r=g.context;k=c.contextType;"object"===typeof k&&null!==k?k=Vg(k):(k=Zf(c)?Xf:H.current,k=Yf(b,k));var y=c.getDerivedStateFromProps;(m="function"===typeof y||"function"===typeof g.getSnapshotBeforeUpdate)||
"function"!==typeof g.UNSAFE_componentWillReceiveProps&&"function"!==typeof g.componentWillReceiveProps||(h!==q||r!==k)&&qh(b,g,d,k);$g=!1;r=b.memoizedState;g.state=r;gh(b,d,g,e);var n=b.memoizedState;h!==q||r!==n||Wf.current||$g?("function"===typeof y&&(kh(b,c,y,d),n=b.memoizedState),(l=$g||oh(b,c,l,d,r,n,k)||!1)?(m||"function"!==typeof g.UNSAFE_componentWillUpdate&&"function"!==typeof g.componentWillUpdate||("function"===typeof g.componentWillUpdate&&g.componentWillUpdate(d,n,k),"function"===typeof g.UNSAFE_componentWillUpdate&&
g.UNSAFE_componentWillUpdate(d,n,k)),"function"===typeof g.componentDidUpdate&&(b.flags|=4),"function"===typeof g.getSnapshotBeforeUpdate&&(b.flags|=1024)):("function"!==typeof g.componentDidUpdate||h===a.memoizedProps&&r===a.memoizedState||(b.flags|=4),"function"!==typeof g.getSnapshotBeforeUpdate||h===a.memoizedProps&&r===a.memoizedState||(b.flags|=1024),b.memoizedProps=d,b.memoizedState=n),g.props=d,g.state=n,g.context=k,d=l):("function"!==typeof g.componentDidUpdate||h===a.memoizedProps&&r===
a.memoizedState||(b.flags|=4),"function"!==typeof g.getSnapshotBeforeUpdate||h===a.memoizedProps&&r===a.memoizedState||(b.flags|=1024),d=!1)}return kj(a,b,c,d,f,e)}
function kj(a,b,c,d,e,f){hj(a,b);var g=0!==(b.flags&128);if(!d&&!g)return e&&dg(b,c,!1),$i(a,b,f);d=b.stateNode;Xi.current=b;var h=g&&"function"!==typeof c.getDerivedStateFromError?null:d.render();b.flags|=1;null!==a&&g?(b.child=Bh(b,a.child,null,f),b.child=Bh(b,null,h,f)):Yi(a,b,h,f);b.memoizedState=d.state;e&&dg(b,c,!0);return b.child}function lj(a){var b=a.stateNode;b.pendingContext?ag(a,b.pendingContext,b.pendingContext!==b.context):b.context&&ag(a,b.context,!1);Ih(a,b.containerInfo)}
function mj(a,b,c,d,e){Ig();Jg(e);b.flags|=256;Yi(a,b,c,d);return b.child}var nj={dehydrated:null,treeContext:null,retryLane:0};function oj(a){return{baseLanes:a,cachePool:null,transitions:null}}
function pj(a,b,c){var d=b.pendingProps,e=M.current,f=!1,g=0!==(b.flags&128),h;(h=g)||(h=null!==a&&null===a.memoizedState?!1:0!==(e&2));if(h)f=!0,b.flags&=-129;else if(null===a||null!==a.memoizedState)e|=1;G(M,e&1);if(null===a){Eg(b);a=b.memoizedState;if(null!==a&&(a=a.dehydrated,null!==a))return 0===(b.mode&1)?b.lanes=1:"$!"===a.data?b.lanes=8:b.lanes=1073741824,null;g=d.children;a=d.fallback;return f?(d=b.mode,f=b.child,g={mode:"hidden",children:g},0===(d&1)&&null!==f?(f.childLanes=0,f.pendingProps=
g):f=qj(g,d,0,null),a=Ah(a,d,c,null),f.return=b,a.return=b,f.sibling=a,b.child=f,b.child.memoizedState=oj(c),b.memoizedState=nj,a):rj(b,g)}e=a.memoizedState;if(null!==e&&(h=e.dehydrated,null!==h))return sj(a,b,g,d,h,e,c);if(f){f=d.fallback;g=b.mode;e=a.child;h=e.sibling;var k={mode:"hidden",children:d.children};0===(g&1)&&b.child!==e?(d=b.child,d.childLanes=0,d.pendingProps=k,b.deletions=null):(d=wh(e,k),d.subtreeFlags=e.subtreeFlags&14680064);null!==h?f=wh(h,f):(f=Ah(f,g,c,null),f.flags|=2);f.return=
b;d.return=b;d.sibling=f;b.child=d;d=f;f=b.child;g=a.child.memoizedState;g=null===g?oj(c):{baseLanes:g.baseLanes|c,cachePool:null,transitions:g.transitions};f.memoizedState=g;f.childLanes=a.childLanes&~c;b.memoizedState=nj;return d}f=a.child;a=f.sibling;d=wh(f,{mode:"visible",children:d.children});0===(b.mode&1)&&(d.lanes=c);d.return=b;d.sibling=null;null!==a&&(c=b.deletions,null===c?(b.deletions=[a],b.flags|=16):c.push(a));b.child=d;b.memoizedState=null;return d}
function rj(a,b){b=qj({mode:"visible",children:b},a.mode,0,null);b.return=a;return a.child=b}function tj(a,b,c,d){null!==d&&Jg(d);Bh(b,a.child,null,c);a=rj(b,b.pendingProps.children);a.flags|=2;b.memoizedState=null;return a}
function sj(a,b,c,d,e,f,g){if(c){if(b.flags&256)return b.flags&=-257,d=Li(Error(p(422))),tj(a,b,g,d);if(null!==b.memoizedState)return b.child=a.child,b.flags|=128,null;f=d.fallback;e=b.mode;d=qj({mode:"visible",children:d.children},e,0,null);f=Ah(f,e,g,null);f.flags|=2;d.return=b;f.return=b;d.sibling=f;b.child=d;0!==(b.mode&1)&&Bh(b,a.child,null,g);b.child.memoizedState=oj(g);b.memoizedState=nj;return f}if(0===(b.mode&1))return tj(a,b,g,null);if("$!"===e.data){d=e.nextSibling&&e.nextSibling.dataset;
if(d)var h=d.dgst;d=h;f=Error(p(419));d=Li(f,d,void 0);return tj(a,b,g,d)}h=0!==(g&a.childLanes);if(Ug||h){d=R;if(null!==d){switch(g&-g){case 4:e=2;break;case 16:e=8;break;case 64:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:case 4194304:case 8388608:case 16777216:case 33554432:case 67108864:e=32;break;case 536870912:e=268435456;break;default:e=0}e=0!==(e&(d.suspendedLanes|g))?0:e;
0!==e&&e!==f.retryLane&&(f.retryLane=e,Zg(a,e),mh(d,a,e,-1))}uj();d=Li(Error(p(421)));return tj(a,b,g,d)}if("$?"===e.data)return b.flags|=128,b.child=a.child,b=vj.bind(null,a),e._reactRetry=b,null;a=f.treeContext;yg=Lf(e.nextSibling);xg=b;I=!0;zg=null;null!==a&&(og[pg++]=rg,og[pg++]=sg,og[pg++]=qg,rg=a.id,sg=a.overflow,qg=b);b=rj(b,d.children);b.flags|=4096;return b}function wj(a,b,c){a.lanes|=b;var d=a.alternate;null!==d&&(d.lanes|=b);Sg(a.return,b,c)}
function xj(a,b,c,d,e){var f=a.memoizedState;null===f?a.memoizedState={isBackwards:b,rendering:null,renderingStartTime:0,last:d,tail:c,tailMode:e}:(f.isBackwards=b,f.rendering=null,f.renderingStartTime=0,f.last=d,f.tail=c,f.tailMode=e)}
function yj(a,b,c){var d=b.pendingProps,e=d.revealOrder,f=d.tail;Yi(a,b,d.children,c);d=M.current;if(0!==(d&2))d=d&1|2,b.flags|=128;else{if(null!==a&&0!==(a.flags&128))a:for(a=b.child;null!==a;){if(13===a.tag)null!==a.memoizedState&&wj(a,c,b);else if(19===a.tag)wj(a,c,b);else if(null!==a.child){a.child.return=a;a=a.child;continue}if(a===b)break a;for(;null===a.sibling;){if(null===a.return||a.return===b)break a;a=a.return}a.sibling.return=a.return;a=a.sibling}d&=1}G(M,d);if(0===(b.mode&1))b.memoizedState=
null;else switch(e){case "forwards":c=b.child;for(e=null;null!==c;)a=c.alternate,null!==a&&null===Mh(a)&&(e=c),c=c.sibling;c=e;null===c?(e=b.child,b.child=null):(e=c.sibling,c.sibling=null);xj(b,!1,e,c,f);break;case "backwards":c=null;e=b.child;for(b.child=null;null!==e;){a=e.alternate;if(null!==a&&null===Mh(a)){b.child=e;break}a=e.sibling;e.sibling=c;c=e;e=a}xj(b,!0,c,null,f);break;case "together":xj(b,!1,null,null,void 0);break;default:b.memoizedState=null}return b.child}
function jj(a,b){0===(b.mode&1)&&null!==a&&(a.alternate=null,b.alternate=null,b.flags|=2)}function $i(a,b,c){null!==a&&(b.dependencies=a.dependencies);hh|=b.lanes;if(0===(c&b.childLanes))return null;if(null!==a&&b.child!==a.child)throw Error(p(153));if(null!==b.child){a=b.child;c=wh(a,a.pendingProps);b.child=c;for(c.return=b;null!==a.sibling;)a=a.sibling,c=c.sibling=wh(a,a.pendingProps),c.return=b;c.sibling=null}return b.child}
function zj(a,b,c){switch(b.tag){case 3:lj(b);Ig();break;case 5:Kh(b);break;case 1:Zf(b.type)&&cg(b);break;case 4:Ih(b,b.stateNode.containerInfo);break;case 10:var d=b.type._context,e=b.memoizedProps.value;G(Mg,d._currentValue);d._currentValue=e;break;case 13:d=b.memoizedState;if(null!==d){if(null!==d.dehydrated)return G(M,M.current&1),b.flags|=128,null;if(0!==(c&b.child.childLanes))return pj(a,b,c);G(M,M.current&1);a=$i(a,b,c);return null!==a?a.sibling:null}G(M,M.current&1);break;case 19:d=0!==(c&
b.childLanes);if(0!==(a.flags&128)){if(d)return yj(a,b,c);b.flags|=128}e=b.memoizedState;null!==e&&(e.rendering=null,e.tail=null,e.lastEffect=null);G(M,M.current);if(d)break;else return null;case 22:case 23:return b.lanes=0,ej(a,b,c)}return $i(a,b,c)}var Aj,Bj,Cj,Dj;
Aj=function(a,b){for(var c=b.child;null!==c;){if(5===c.tag||6===c.tag)a.appendChild(c.stateNode);else if(4!==c.tag&&null!==c.child){c.child.return=c;c=c.child;continue}if(c===b)break;for(;null===c.sibling;){if(null===c.return||c.return===b)return;c=c.return}c.sibling.return=c.return;c=c.sibling}};Bj=function(){};
Cj=function(a,b,c,d){var e=a.memoizedProps;if(e!==d){a=b.stateNode;Hh(Eh.current);var f=null;switch(c){case "input":e=Ya(a,e);d=Ya(a,d);f=[];break;case "select":e=A({},e,{value:void 0});d=A({},d,{value:void 0});f=[];break;case "textarea":e=gb(a,e);d=gb(a,d);f=[];break;default:"function"!==typeof e.onClick&&"function"===typeof d.onClick&&(a.onclick=Bf)}ub(c,d);var g;c=null;for(l in e)if(!d.hasOwnProperty(l)&&e.hasOwnProperty(l)&&null!=e[l])if("style"===l){var h=e[l];for(g in h)h.hasOwnProperty(g)&&
(c||(c={}),c[g]="")}else"dangerouslySetInnerHTML"!==l&&"children"!==l&&"suppressContentEditableWarning"!==l&&"suppressHydrationWarning"!==l&&"autoFocus"!==l&&(ea.hasOwnProperty(l)?f||(f=[]):(f=f||[]).push(l,null));for(l in d){var k=d[l];h=null!=e?e[l]:void 0;if(d.hasOwnProperty(l)&&k!==h&&(null!=k||null!=h))if("style"===l)if(h){for(g in h)!h.hasOwnProperty(g)||k&&k.hasOwnProperty(g)||(c||(c={}),c[g]="");for(g in k)k.hasOwnProperty(g)&&h[g]!==k[g]&&(c||(c={}),c[g]=k[g])}else c||(f||(f=[]),f.push(l,
c)),c=k;else"dangerouslySetInnerHTML"===l?(k=k?k.__html:void 0,h=h?h.__html:void 0,null!=k&&h!==k&&(f=f||[]).push(l,k)):"children"===l?"string"!==typeof k&&"number"!==typeof k||(f=f||[]).push(l,""+k):"suppressContentEditableWarning"!==l&&"suppressHydrationWarning"!==l&&(ea.hasOwnProperty(l)?(null!=k&&"onScroll"===l&&D("scroll",a),f||h===k||(f=[])):(f=f||[]).push(l,k))}c&&(f=f||[]).push("style",c);var l=f;if(b.updateQueue=l)b.flags|=4}};Dj=function(a,b,c,d){c!==d&&(b.flags|=4)};
function Ej(a,b){if(!I)switch(a.tailMode){case "hidden":b=a.tail;for(var c=null;null!==b;)null!==b.alternate&&(c=b),b=b.sibling;null===c?a.tail=null:c.sibling=null;break;case "collapsed":c=a.tail;for(var d=null;null!==c;)null!==c.alternate&&(d=c),c=c.sibling;null===d?b||null===a.tail?a.tail=null:a.tail.sibling=null:d.sibling=null}}
function S(a){var b=null!==a.alternate&&a.alternate.child===a.child,c=0,d=0;if(b)for(var e=a.child;null!==e;)c|=e.lanes|e.childLanes,d|=e.subtreeFlags&14680064,d|=e.flags&14680064,e.return=a,e=e.sibling;else for(e=a.child;null!==e;)c|=e.lanes|e.childLanes,d|=e.subtreeFlags,d|=e.flags,e.return=a,e=e.sibling;a.subtreeFlags|=d;a.childLanes=c;return b}
function Fj(a,b,c){var d=b.pendingProps;wg(b);switch(b.tag){case 2:case 16:case 15:case 0:case 11:case 7:case 8:case 12:case 9:case 14:return S(b),null;case 1:return Zf(b.type)&&$f(),S(b),null;case 3:d=b.stateNode;Jh();E(Wf);E(H);Oh();d.pendingContext&&(d.context=d.pendingContext,d.pendingContext=null);if(null===a||null===a.child)Gg(b)?b.flags|=4:null===a||a.memoizedState.isDehydrated&&0===(b.flags&256)||(b.flags|=1024,null!==zg&&(Gj(zg),zg=null));Bj(a,b);S(b);return null;case 5:Lh(b);var e=Hh(Gh.current);
c=b.type;if(null!==a&&null!=b.stateNode)Cj(a,b,c,d,e),a.ref!==b.ref&&(b.flags|=512,b.flags|=2097152);else{if(!d){if(null===b.stateNode)throw Error(p(166));S(b);return null}a=Hh(Eh.current);if(Gg(b)){d=b.stateNode;c=b.type;var f=b.memoizedProps;d[Of]=b;d[Pf]=f;a=0!==(b.mode&1);switch(c){case "dialog":D("cancel",d);D("close",d);break;case "iframe":case "object":case "embed":D("load",d);break;case "video":case "audio":for(e=0;e<lf.length;e++)D(lf[e],d);break;case "source":D("error",d);break;case "img":case "image":case "link":D("error",
d);D("load",d);break;case "details":D("toggle",d);break;case "input":Za(d,f);D("invalid",d);break;case "select":d._wrapperState={wasMultiple:!!f.multiple};D("invalid",d);break;case "textarea":hb(d,f),D("invalid",d)}ub(c,f);e=null;for(var g in f)if(f.hasOwnProperty(g)){var h=f[g];"children"===g?"string"===typeof h?d.textContent!==h&&(!0!==f.suppressHydrationWarning&&Af(d.textContent,h,a),e=["children",h]):"number"===typeof h&&d.textContent!==""+h&&(!0!==f.suppressHydrationWarning&&Af(d.textContent,
h,a),e=["children",""+h]):ea.hasOwnProperty(g)&&null!=h&&"onScroll"===g&&D("scroll",d)}switch(c){case "input":Va(d);db(d,f,!0);break;case "textarea":Va(d);jb(d);break;case "select":case "option":break;default:"function"===typeof f.onClick&&(d.onclick=Bf)}d=e;b.updateQueue=d;null!==d&&(b.flags|=4)}else{g=9===e.nodeType?e:e.ownerDocument;"http://www.w3.org/1999/xhtml"===a&&(a=kb(c));"http://www.w3.org/1999/xhtml"===a?"script"===c?(a=g.createElement("div"),a.innerHTML="<script>\x3c/script>",a=a.removeChild(a.firstChild)):
"string"===typeof d.is?a=g.createElement(c,{is:d.is}):(a=g.createElement(c),"select"===c&&(g=a,d.multiple?g.multiple=!0:d.size&&(g.size=d.size))):a=g.createElementNS(a,c);a[Of]=b;a[Pf]=d;Aj(a,b,!1,!1);b.stateNode=a;a:{g=vb(c,d);switch(c){case "dialog":D("cancel",a);D("close",a);e=d;break;case "iframe":case "object":case "embed":D("load",a);e=d;break;case "video":case "audio":for(e=0;e<lf.length;e++)D(lf[e],a);e=d;break;case "source":D("error",a);e=d;break;case "img":case "image":case "link":D("error",
a);D("load",a);e=d;break;case "details":D("toggle",a);e=d;break;case "input":Za(a,d);e=Ya(a,d);D("invalid",a);break;case "option":e=d;break;case "select":a._wrapperState={wasMultiple:!!d.multiple};e=A({},d,{value:void 0});D("invalid",a);break;case "textarea":hb(a,d);e=gb(a,d);D("invalid",a);break;default:e=d}ub(c,e);h=e;for(f in h)if(h.hasOwnProperty(f)){var k=h[f];"style"===f?sb(a,k):"dangerouslySetInnerHTML"===f?(k=k?k.__html:void 0,null!=k&&nb(a,k)):"children"===f?"string"===typeof k?("textarea"!==
c||""!==k)&&ob(a,k):"number"===typeof k&&ob(a,""+k):"suppressContentEditableWarning"!==f&&"suppressHydrationWarning"!==f&&"autoFocus"!==f&&(ea.hasOwnProperty(f)?null!=k&&"onScroll"===f&&D("scroll",a):null!=k&&ta(a,f,k,g))}switch(c){case "input":Va(a);db(a,d,!1);break;case "textarea":Va(a);jb(a);break;case "option":null!=d.value&&a.setAttribute("value",""+Sa(d.value));break;case "select":a.multiple=!!d.multiple;f=d.value;null!=f?fb(a,!!d.multiple,f,!1):null!=d.defaultValue&&fb(a,!!d.multiple,d.defaultValue,
!0);break;default:"function"===typeof e.onClick&&(a.onclick=Bf)}switch(c){case "button":case "input":case "select":case "textarea":d=!!d.autoFocus;break a;case "img":d=!0;break a;default:d=!1}}d&&(b.flags|=4)}null!==b.ref&&(b.flags|=512,b.flags|=2097152)}S(b);return null;case 6:if(a&&null!=b.stateNode)Dj(a,b,a.memoizedProps,d);else{if("string"!==typeof d&&null===b.stateNode)throw Error(p(166));c=Hh(Gh.current);Hh(Eh.current);if(Gg(b)){d=b.stateNode;c=b.memoizedProps;d[Of]=b;if(f=d.nodeValue!==c)if(a=
xg,null!==a)switch(a.tag){case 3:Af(d.nodeValue,c,0!==(a.mode&1));break;case 5:!0!==a.memoizedProps.suppressHydrationWarning&&Af(d.nodeValue,c,0!==(a.mode&1))}f&&(b.flags|=4)}else d=(9===c.nodeType?c:c.ownerDocument).createTextNode(d),d[Of]=b,b.stateNode=d}S(b);return null;case 13:E(M);d=b.memoizedState;if(null===a||null!==a.memoizedState&&null!==a.memoizedState.dehydrated){if(I&&null!==yg&&0!==(b.mode&1)&&0===(b.flags&128))Hg(),Ig(),b.flags|=98560,f=!1;else if(f=Gg(b),null!==d&&null!==d.dehydrated){if(null===
a){if(!f)throw Error(p(318));f=b.memoizedState;f=null!==f?f.dehydrated:null;if(!f)throw Error(p(317));f[Of]=b}else Ig(),0===(b.flags&128)&&(b.memoizedState=null),b.flags|=4;S(b);f=!1}else null!==zg&&(Gj(zg),zg=null),f=!0;if(!f)return b.flags&65536?b:null}if(0!==(b.flags&128))return b.lanes=c,b;d=null!==d;d!==(null!==a&&null!==a.memoizedState)&&d&&(b.child.flags|=8192,0!==(b.mode&1)&&(null===a||0!==(M.current&1)?0===T&&(T=3):uj()));null!==b.updateQueue&&(b.flags|=4);S(b);return null;case 4:return Jh(),
Bj(a,b),null===a&&sf(b.stateNode.containerInfo),S(b),null;case 10:return Rg(b.type._context),S(b),null;case 17:return Zf(b.type)&&$f(),S(b),null;case 19:E(M);f=b.memoizedState;if(null===f)return S(b),null;d=0!==(b.flags&128);g=f.rendering;if(null===g)if(d)Ej(f,!1);else{if(0!==T||null!==a&&0!==(a.flags&128))for(a=b.child;null!==a;){g=Mh(a);if(null!==g){b.flags|=128;Ej(f,!1);d=g.updateQueue;null!==d&&(b.updateQueue=d,b.flags|=4);b.subtreeFlags=0;d=c;for(c=b.child;null!==c;)f=c,a=d,f.flags&=14680066,
g=f.alternate,null===g?(f.childLanes=0,f.lanes=a,f.child=null,f.subtreeFlags=0,f.memoizedProps=null,f.memoizedState=null,f.updateQueue=null,f.dependencies=null,f.stateNode=null):(f.childLanes=g.childLanes,f.lanes=g.lanes,f.child=g.child,f.subtreeFlags=0,f.deletions=null,f.memoizedProps=g.memoizedProps,f.memoizedState=g.memoizedState,f.updateQueue=g.updateQueue,f.type=g.type,a=g.dependencies,f.dependencies=null===a?null:{lanes:a.lanes,firstContext:a.firstContext}),c=c.sibling;G(M,M.current&1|2);return b.child}a=
a.sibling}null!==f.tail&&B()>Hj&&(b.flags|=128,d=!0,Ej(f,!1),b.lanes=4194304)}else{if(!d)if(a=Mh(g),null!==a){if(b.flags|=128,d=!0,c=a.updateQueue,null!==c&&(b.updateQueue=c,b.flags|=4),Ej(f,!0),null===f.tail&&"hidden"===f.tailMode&&!g.alternate&&!I)return S(b),null}else 2*B()-f.renderingStartTime>Hj&&1073741824!==c&&(b.flags|=128,d=!0,Ej(f,!1),b.lanes=4194304);f.isBackwards?(g.sibling=b.child,b.child=g):(c=f.last,null!==c?c.sibling=g:b.child=g,f.last=g)}if(null!==f.tail)return b=f.tail,f.rendering=
b,f.tail=b.sibling,f.renderingStartTime=B(),b.sibling=null,c=M.current,G(M,d?c&1|2:c&1),b;S(b);return null;case 22:case 23:return Ij(),d=null!==b.memoizedState,null!==a&&null!==a.memoizedState!==d&&(b.flags|=8192),d&&0!==(b.mode&1)?0!==(gj&1073741824)&&(S(b),b.subtreeFlags&6&&(b.flags|=8192)):S(b),null;case 24:return null;case 25:return null}throw Error(p(156,b.tag));}
function Jj(a,b){wg(b);switch(b.tag){case 1:return Zf(b.type)&&$f(),a=b.flags,a&65536?(b.flags=a&-65537|128,b):null;case 3:return Jh(),E(Wf),E(H),Oh(),a=b.flags,0!==(a&65536)&&0===(a&128)?(b.flags=a&-65537|128,b):null;case 5:return Lh(b),null;case 13:E(M);a=b.memoizedState;if(null!==a&&null!==a.dehydrated){if(null===b.alternate)throw Error(p(340));Ig()}a=b.flags;return a&65536?(b.flags=a&-65537|128,b):null;case 19:return E(M),null;case 4:return Jh(),null;case 10:return Rg(b.type._context),null;case 22:case 23:return Ij(),
null;case 24:return null;default:return null}}var Kj=!1,U=!1,Lj="function"===typeof WeakSet?WeakSet:Set,V=null;function Mj(a,b){var c=a.ref;if(null!==c)if("function"===typeof c)try{c(null)}catch(d){W(a,b,d)}else c.current=null}function Nj(a,b,c){try{c()}catch(d){W(a,b,d)}}var Oj=!1;
function Pj(a,b){Cf=dd;a=Me();if(Ne(a)){if("selectionStart"in a)var c={start:a.selectionStart,end:a.selectionEnd};else a:{c=(c=a.ownerDocument)&&c.defaultView||window;var d=c.getSelection&&c.getSelection();if(d&&0!==d.rangeCount){c=d.anchorNode;var e=d.anchorOffset,f=d.focusNode;d=d.focusOffset;try{c.nodeType,f.nodeType}catch(F){c=null;break a}var g=0,h=-1,k=-1,l=0,m=0,q=a,r=null;b:for(;;){for(var y;;){q!==c||0!==e&&3!==q.nodeType||(h=g+e);q!==f||0!==d&&3!==q.nodeType||(k=g+d);3===q.nodeType&&(g+=
q.nodeValue.length);if(null===(y=q.firstChild))break;r=q;q=y}for(;;){if(q===a)break b;r===c&&++l===e&&(h=g);r===f&&++m===d&&(k=g);if(null!==(y=q.nextSibling))break;q=r;r=q.parentNode}q=y}c=-1===h||-1===k?null:{start:h,end:k}}else c=null}c=c||{start:0,end:0}}else c=null;Df={focusedElem:a,selectionRange:c};dd=!1;for(V=b;null!==V;)if(b=V,a=b.child,0!==(b.subtreeFlags&1028)&&null!==a)a.return=b,V=a;else for(;null!==V;){b=V;try{var n=b.alternate;if(0!==(b.flags&1024))switch(b.tag){case 0:case 11:case 15:break;
case 1:if(null!==n){var t=n.memoizedProps,J=n.memoizedState,x=b.stateNode,w=x.getSnapshotBeforeUpdate(b.elementType===b.type?t:Lg(b.type,t),J);x.__reactInternalSnapshotBeforeUpdate=w}break;case 3:var u=b.stateNode.containerInfo;1===u.nodeType?u.textContent="":9===u.nodeType&&u.documentElement&&u.removeChild(u.documentElement);break;case 5:case 6:case 4:case 17:break;default:throw Error(p(163));}}catch(F){W(b,b.return,F)}a=b.sibling;if(null!==a){a.return=b.return;V=a;break}V=b.return}n=Oj;Oj=!1;return n}
function Qj(a,b,c){var d=b.updateQueue;d=null!==d?d.lastEffect:null;if(null!==d){var e=d=d.next;do{if((e.tag&a)===a){var f=e.destroy;e.destroy=void 0;void 0!==f&&Nj(b,c,f)}e=e.next}while(e!==d)}}function Rj(a,b){b=b.updateQueue;b=null!==b?b.lastEffect:null;if(null!==b){var c=b=b.next;do{if((c.tag&a)===a){var d=c.create;c.destroy=d()}c=c.next}while(c!==b)}}function Sj(a){var b=a.ref;if(null!==b){var c=a.stateNode;switch(a.tag){case 5:a=c;break;default:a=c}"function"===typeof b?b(a):b.current=a}}
function Tj(a){var b=a.alternate;null!==b&&(a.alternate=null,Tj(b));a.child=null;a.deletions=null;a.sibling=null;5===a.tag&&(b=a.stateNode,null!==b&&(delete b[Of],delete b[Pf],delete b[of],delete b[Qf],delete b[Rf]));a.stateNode=null;a.return=null;a.dependencies=null;a.memoizedProps=null;a.memoizedState=null;a.pendingProps=null;a.stateNode=null;a.updateQueue=null}function Uj(a){return 5===a.tag||3===a.tag||4===a.tag}
function Vj(a){a:for(;;){for(;null===a.sibling;){if(null===a.return||Uj(a.return))return null;a=a.return}a.sibling.return=a.return;for(a=a.sibling;5!==a.tag&&6!==a.tag&&18!==a.tag;){if(a.flags&2)continue a;if(null===a.child||4===a.tag)continue a;else a.child.return=a,a=a.child}if(!(a.flags&2))return a.stateNode}}
function Wj(a,b,c){var d=a.tag;if(5===d||6===d)a=a.stateNode,b?8===c.nodeType?c.parentNode.insertBefore(a,b):c.insertBefore(a,b):(8===c.nodeType?(b=c.parentNode,b.insertBefore(a,c)):(b=c,b.appendChild(a)),c=c._reactRootContainer,null!==c&&void 0!==c||null!==b.onclick||(b.onclick=Bf));else if(4!==d&&(a=a.child,null!==a))for(Wj(a,b,c),a=a.sibling;null!==a;)Wj(a,b,c),a=a.sibling}
function Xj(a,b,c){var d=a.tag;if(5===d||6===d)a=a.stateNode,b?c.insertBefore(a,b):c.appendChild(a);else if(4!==d&&(a=a.child,null!==a))for(Xj(a,b,c),a=a.sibling;null!==a;)Xj(a,b,c),a=a.sibling}var X=null,Yj=!1;function Zj(a,b,c){for(c=c.child;null!==c;)ak(a,b,c),c=c.sibling}
function ak(a,b,c){if(lc&&"function"===typeof lc.onCommitFiberUnmount)try{lc.onCommitFiberUnmount(kc,c)}catch(h){}switch(c.tag){case 5:U||Mj(c,b);case 6:var d=X,e=Yj;X=null;Zj(a,b,c);X=d;Yj=e;null!==X&&(Yj?(a=X,c=c.stateNode,8===a.nodeType?a.parentNode.removeChild(c):a.removeChild(c)):X.removeChild(c.stateNode));break;case 18:null!==X&&(Yj?(a=X,c=c.stateNode,8===a.nodeType?Kf(a.parentNode,c):1===a.nodeType&&Kf(a,c),bd(a)):Kf(X,c.stateNode));break;case 4:d=X;e=Yj;X=c.stateNode.containerInfo;Yj=!0;
Zj(a,b,c);X=d;Yj=e;break;case 0:case 11:case 14:case 15:if(!U&&(d=c.updateQueue,null!==d&&(d=d.lastEffect,null!==d))){e=d=d.next;do{var f=e,g=f.destroy;f=f.tag;void 0!==g&&(0!==(f&2)?Nj(c,b,g):0!==(f&4)&&Nj(c,b,g));e=e.next}while(e!==d)}Zj(a,b,c);break;case 1:if(!U&&(Mj(c,b),d=c.stateNode,"function"===typeof d.componentWillUnmount))try{d.props=c.memoizedProps,d.state=c.memoizedState,d.componentWillUnmount()}catch(h){W(c,b,h)}Zj(a,b,c);break;case 21:Zj(a,b,c);break;case 22:c.mode&1?(U=(d=U)||null!==
c.memoizedState,Zj(a,b,c),U=d):Zj(a,b,c);break;default:Zj(a,b,c)}}function bk(a){var b=a.updateQueue;if(null!==b){a.updateQueue=null;var c=a.stateNode;null===c&&(c=a.stateNode=new Lj);b.forEach(function(b){var d=ck.bind(null,a,b);c.has(b)||(c.add(b),b.then(d,d))})}}
function dk(a,b){var c=b.deletions;if(null!==c)for(var d=0;d<c.length;d++){var e=c[d];try{var f=a,g=b,h=g;a:for(;null!==h;){switch(h.tag){case 5:X=h.stateNode;Yj=!1;break a;case 3:X=h.stateNode.containerInfo;Yj=!0;break a;case 4:X=h.stateNode.containerInfo;Yj=!0;break a}h=h.return}if(null===X)throw Error(p(160));ak(f,g,e);X=null;Yj=!1;var k=e.alternate;null!==k&&(k.return=null);e.return=null}catch(l){W(e,b,l)}}if(b.subtreeFlags&12854)for(b=b.child;null!==b;)ek(b,a),b=b.sibling}
function ek(a,b){var c=a.alternate,d=a.flags;switch(a.tag){case 0:case 11:case 14:case 15:dk(b,a);fk(a);if(d&4){try{Qj(3,a,a.return),Rj(3,a)}catch(t){W(a,a.return,t)}try{Qj(5,a,a.return)}catch(t){W(a,a.return,t)}}break;case 1:dk(b,a);fk(a);d&512&&null!==c&&Mj(c,c.return);break;case 5:dk(b,a);fk(a);d&512&&null!==c&&Mj(c,c.return);if(a.flags&32){var e=a.stateNode;try{ob(e,"")}catch(t){W(a,a.return,t)}}if(d&4&&(e=a.stateNode,null!=e)){var f=a.memoizedProps,g=null!==c?c.memoizedProps:f,h=a.type,k=a.updateQueue;
a.updateQueue=null;if(null!==k)try{"input"===h&&"radio"===f.type&&null!=f.name&&ab(e,f);vb(h,g);var l=vb(h,f);for(g=0;g<k.length;g+=2){var m=k[g],q=k[g+1];"style"===m?sb(e,q):"dangerouslySetInnerHTML"===m?nb(e,q):"children"===m?ob(e,q):ta(e,m,q,l)}switch(h){case "input":bb(e,f);break;case "textarea":ib(e,f);break;case "select":var r=e._wrapperState.wasMultiple;e._wrapperState.wasMultiple=!!f.multiple;var y=f.value;null!=y?fb(e,!!f.multiple,y,!1):r!==!!f.multiple&&(null!=f.defaultValue?fb(e,!!f.multiple,
f.defaultValue,!0):fb(e,!!f.multiple,f.multiple?[]:"",!1))}e[Pf]=f}catch(t){W(a,a.return,t)}}break;case 6:dk(b,a);fk(a);if(d&4){if(null===a.stateNode)throw Error(p(162));e=a.stateNode;f=a.memoizedProps;try{e.nodeValue=f}catch(t){W(a,a.return,t)}}break;case 3:dk(b,a);fk(a);if(d&4&&null!==c&&c.memoizedState.isDehydrated)try{bd(b.containerInfo)}catch(t){W(a,a.return,t)}break;case 4:dk(b,a);fk(a);break;case 13:dk(b,a);fk(a);e=a.child;e.flags&8192&&(f=null!==e.memoizedState,e.stateNode.isHidden=f,!f||
null!==e.alternate&&null!==e.alternate.memoizedState||(gk=B()));d&4&&bk(a);break;case 22:m=null!==c&&null!==c.memoizedState;a.mode&1?(U=(l=U)||m,dk(b,a),U=l):dk(b,a);fk(a);if(d&8192){l=null!==a.memoizedState;if((a.stateNode.isHidden=l)&&!m&&0!==(a.mode&1))for(V=a,m=a.child;null!==m;){for(q=V=m;null!==V;){r=V;y=r.child;switch(r.tag){case 0:case 11:case 14:case 15:Qj(4,r,r.return);break;case 1:Mj(r,r.return);var n=r.stateNode;if("function"===typeof n.componentWillUnmount){d=r;c=r.return;try{b=d,n.props=
b.memoizedProps,n.state=b.memoizedState,n.componentWillUnmount()}catch(t){W(d,c,t)}}break;case 5:Mj(r,r.return);break;case 22:if(null!==r.memoizedState){hk(q);continue}}null!==y?(y.return=r,V=y):hk(q)}m=m.sibling}a:for(m=null,q=a;;){if(5===q.tag){if(null===m){m=q;try{e=q.stateNode,l?(f=e.style,"function"===typeof f.setProperty?f.setProperty("display","none","important"):f.display="none"):(h=q.stateNode,k=q.memoizedProps.style,g=void 0!==k&&null!==k&&k.hasOwnProperty("display")?k.display:null,h.style.display=
rb("display",g))}catch(t){W(a,a.return,t)}}}else if(6===q.tag){if(null===m)try{q.stateNode.nodeValue=l?"":q.memoizedProps}catch(t){W(a,a.return,t)}}else if((22!==q.tag&&23!==q.tag||null===q.memoizedState||q===a)&&null!==q.child){q.child.return=q;q=q.child;continue}if(q===a)break a;for(;null===q.sibling;){if(null===q.return||q.return===a)break a;m===q&&(m=null);q=q.return}m===q&&(m=null);q.sibling.return=q.return;q=q.sibling}}break;case 19:dk(b,a);fk(a);d&4&&bk(a);break;case 21:break;default:dk(b,
a),fk(a)}}function fk(a){var b=a.flags;if(b&2){try{a:{for(var c=a.return;null!==c;){if(Uj(c)){var d=c;break a}c=c.return}throw Error(p(160));}switch(d.tag){case 5:var e=d.stateNode;d.flags&32&&(ob(e,""),d.flags&=-33);var f=Vj(a);Xj(a,f,e);break;case 3:case 4:var g=d.stateNode.containerInfo,h=Vj(a);Wj(a,h,g);break;default:throw Error(p(161));}}catch(k){W(a,a.return,k)}a.flags&=-3}b&4096&&(a.flags&=-4097)}function ik(a,b,c){V=a;jk(a,b,c)}
function jk(a,b,c){for(var d=0!==(a.mode&1);null!==V;){var e=V,f=e.child;if(22===e.tag&&d){var g=null!==e.memoizedState||Kj;if(!g){var h=e.alternate,k=null!==h&&null!==h.memoizedState||U;h=Kj;var l=U;Kj=g;if((U=k)&&!l)for(V=e;null!==V;)g=V,k=g.child,22===g.tag&&null!==g.memoizedState?kk(e):null!==k?(k.return=g,V=k):kk(e);for(;null!==f;)V=f,jk(f,b,c),f=f.sibling;V=e;Kj=h;U=l}lk(a,b,c)}else 0!==(e.subtreeFlags&8772)&&null!==f?(f.return=e,V=f):lk(a,b,c)}}
function lk(a){for(;null!==V;){var b=V;if(0!==(b.flags&8772)){var c=b.alternate;try{if(0!==(b.flags&8772))switch(b.tag){case 0:case 11:case 15:U||Rj(5,b);break;case 1:var d=b.stateNode;if(b.flags&4&&!U)if(null===c)d.componentDidMount();else{var e=b.elementType===b.type?c.memoizedProps:Lg(b.type,c.memoizedProps);d.componentDidUpdate(e,c.memoizedState,d.__reactInternalSnapshotBeforeUpdate)}var f=b.updateQueue;null!==f&&ih(b,f,d);break;case 3:var g=b.updateQueue;if(null!==g){c=null;if(null!==b.child)switch(b.child.tag){case 5:c=
b.child.stateNode;break;case 1:c=b.child.stateNode}ih(b,g,c)}break;case 5:var h=b.stateNode;if(null===c&&b.flags&4){c=h;var k=b.memoizedProps;switch(b.type){case "button":case "input":case "select":case "textarea":k.autoFocus&&c.focus();break;case "img":k.src&&(c.src=k.src)}}break;case 6:break;case 4:break;case 12:break;case 13:if(null===b.memoizedState){var l=b.alternate;if(null!==l){var m=l.memoizedState;if(null!==m){var q=m.dehydrated;null!==q&&bd(q)}}}break;case 19:case 17:case 21:case 22:case 23:case 25:break;
default:throw Error(p(163));}U||b.flags&512&&Sj(b)}catch(r){W(b,b.return,r)}}if(b===a){V=null;break}c=b.sibling;if(null!==c){c.return=b.return;V=c;break}V=b.return}}function hk(a){for(;null!==V;){var b=V;if(b===a){V=null;break}var c=b.sibling;if(null!==c){c.return=b.return;V=c;break}V=b.return}}
function kk(a){for(;null!==V;){var b=V;try{switch(b.tag){case 0:case 11:case 15:var c=b.return;try{Rj(4,b)}catch(k){W(b,c,k)}break;case 1:var d=b.stateNode;if("function"===typeof d.componentDidMount){var e=b.return;try{d.componentDidMount()}catch(k){W(b,e,k)}}var f=b.return;try{Sj(b)}catch(k){W(b,f,k)}break;case 5:var g=b.return;try{Sj(b)}catch(k){W(b,g,k)}}}catch(k){W(b,b.return,k)}if(b===a){V=null;break}var h=b.sibling;if(null!==h){h.return=b.return;V=h;break}V=b.return}}
var mk=Math.ceil,nk=ua.ReactCurrentDispatcher,ok=ua.ReactCurrentOwner,pk=ua.ReactCurrentBatchConfig,K=0,R=null,Y=null,Z=0,gj=0,fj=Uf(0),T=0,qk=null,hh=0,rk=0,sk=0,tk=null,uk=null,gk=0,Hj=Infinity,vk=null,Pi=!1,Qi=null,Si=null,wk=!1,xk=null,yk=0,zk=0,Ak=null,Bk=-1,Ck=0;function L(){return 0!==(K&6)?B():-1!==Bk?Bk:Bk=B()}
function lh(a){if(0===(a.mode&1))return 1;if(0!==(K&2)&&0!==Z)return Z&-Z;if(null!==Kg.transition)return 0===Ck&&(Ck=yc()),Ck;a=C;if(0!==a)return a;a=window.event;a=void 0===a?16:jd(a.type);return a}function mh(a,b,c,d){if(50<zk)throw zk=0,Ak=null,Error(p(185));Ac(a,c,d);if(0===(K&2)||a!==R)a===R&&(0===(K&2)&&(rk|=c),4===T&&Dk(a,Z)),Ek(a,d),1===c&&0===K&&0===(b.mode&1)&&(Hj=B()+500,fg&&jg())}
function Ek(a,b){var c=a.callbackNode;wc(a,b);var d=uc(a,a===R?Z:0);if(0===d)null!==c&&bc(c),a.callbackNode=null,a.callbackPriority=0;else if(b=d&-d,a.callbackPriority!==b){null!=c&&bc(c);if(1===b)0===a.tag?ig(Fk.bind(null,a)):hg(Fk.bind(null,a)),Jf(function(){0===(K&6)&&jg()}),c=null;else{switch(Dc(d)){case 1:c=fc;break;case 4:c=gc;break;case 16:c=hc;break;case 536870912:c=jc;break;default:c=hc}c=Gk(c,Hk.bind(null,a))}a.callbackPriority=b;a.callbackNode=c}}
function Hk(a,b){Bk=-1;Ck=0;if(0!==(K&6))throw Error(p(327));var c=a.callbackNode;if(Ik()&&a.callbackNode!==c)return null;var d=uc(a,a===R?Z:0);if(0===d)return null;if(0!==(d&30)||0!==(d&a.expiredLanes)||b)b=Jk(a,d);else{b=d;var e=K;K|=2;var f=Kk();if(R!==a||Z!==b)vk=null,Hj=B()+500,Lk(a,b);do try{Mk();break}catch(h){Nk(a,h)}while(1);Qg();nk.current=f;K=e;null!==Y?b=0:(R=null,Z=0,b=T)}if(0!==b){2===b&&(e=xc(a),0!==e&&(d=e,b=Ok(a,e)));if(1===b)throw c=qk,Lk(a,0),Dk(a,d),Ek(a,B()),c;if(6===b)Dk(a,d);
else{e=a.current.alternate;if(0===(d&30)&&!Pk(e)&&(b=Jk(a,d),2===b&&(f=xc(a),0!==f&&(d=f,b=Ok(a,f))),1===b))throw c=qk,Lk(a,0),Dk(a,d),Ek(a,B()),c;a.finishedWork=e;a.finishedLanes=d;switch(b){case 0:case 1:throw Error(p(345));case 2:Qk(a,uk,vk);break;case 3:Dk(a,d);if((d&130023424)===d&&(b=gk+500-B(),10<b)){if(0!==uc(a,0))break;e=a.suspendedLanes;if((e&d)!==d){L();a.pingedLanes|=a.suspendedLanes&e;break}a.timeoutHandle=Ff(Qk.bind(null,a,uk,vk),b);break}Qk(a,uk,vk);break;case 4:Dk(a,d);if((d&4194240)===
d)break;b=a.eventTimes;for(e=-1;0<d;){var g=31-oc(d);f=1<<g;g=b[g];g>e&&(e=g);d&=~f}d=e;d=B()-d;d=(120>d?120:480>d?480:1080>d?1080:1920>d?1920:3E3>d?3E3:4320>d?4320:1960*mk(d/1960))-d;if(10<d){a.timeoutHandle=Ff(Qk.bind(null,a,uk,vk),d);break}Qk(a,uk,vk);break;case 5:Qk(a,uk,vk);break;default:throw Error(p(329));}}}Ek(a,B());return a.callbackNode===c?Hk.bind(null,a):null}
function Ok(a,b){var c=tk;a.current.memoizedState.isDehydrated&&(Lk(a,b).flags|=256);a=Jk(a,b);2!==a&&(b=uk,uk=c,null!==b&&Gj(b));return a}function Gj(a){null===uk?uk=a:uk.push.apply(uk,a)}
function Pk(a){for(var b=a;;){if(b.flags&16384){var c=b.updateQueue;if(null!==c&&(c=c.stores,null!==c))for(var d=0;d<c.length;d++){var e=c[d],f=e.getSnapshot;e=e.value;try{if(!He(f(),e))return!1}catch(g){return!1}}}c=b.child;if(b.subtreeFlags&16384&&null!==c)c.return=b,b=c;else{if(b===a)break;for(;null===b.sibling;){if(null===b.return||b.return===a)return!0;b=b.return}b.sibling.return=b.return;b=b.sibling}}return!0}
function Dk(a,b){b&=~sk;b&=~rk;a.suspendedLanes|=b;a.pingedLanes&=~b;for(a=a.expirationTimes;0<b;){var c=31-oc(b),d=1<<c;a[c]=-1;b&=~d}}function Fk(a){if(0!==(K&6))throw Error(p(327));Ik();var b=uc(a,0);if(0===(b&1))return Ek(a,B()),null;var c=Jk(a,b);if(0!==a.tag&&2===c){var d=xc(a);0!==d&&(b=d,c=Ok(a,d))}if(1===c)throw c=qk,Lk(a,0),Dk(a,b),Ek(a,B()),c;if(6===c)throw Error(p(345));a.finishedWork=a.current.alternate;a.finishedLanes=b;Qk(a,uk,vk);Ek(a,B());return null}
function Rk(a,b){var c=K;K|=1;try{return a(b)}finally{K=c,0===K&&(Hj=B()+500,fg&&jg())}}function Sk(a){null!==xk&&0===xk.tag&&0===(K&6)&&Ik();var b=K;K|=1;var c=pk.transition,d=C;try{if(pk.transition=null,C=1,a)return a()}finally{C=d,pk.transition=c,K=b,0===(K&6)&&jg()}}function Ij(){gj=fj.current;E(fj)}
function Lk(a,b){a.finishedWork=null;a.finishedLanes=0;var c=a.timeoutHandle;-1!==c&&(a.timeoutHandle=-1,Gf(c));if(null!==Y)for(c=Y.return;null!==c;){var d=c;wg(d);switch(d.tag){case 1:d=d.type.childContextTypes;null!==d&&void 0!==d&&$f();break;case 3:Jh();E(Wf);E(H);Oh();break;case 5:Lh(d);break;case 4:Jh();break;case 13:E(M);break;case 19:E(M);break;case 10:Rg(d.type._context);break;case 22:case 23:Ij()}c=c.return}R=a;Y=a=wh(a.current,null);Z=gj=b;T=0;qk=null;sk=rk=hh=0;uk=tk=null;if(null!==Wg){for(b=
0;b<Wg.length;b++)if(c=Wg[b],d=c.interleaved,null!==d){c.interleaved=null;var e=d.next,f=c.pending;if(null!==f){var g=f.next;f.next=e;d.next=g}c.pending=d}Wg=null}return a}
function Nk(a,b){do{var c=Y;try{Qg();Ph.current=ai;if(Sh){for(var d=N.memoizedState;null!==d;){var e=d.queue;null!==e&&(e.pending=null);d=d.next}Sh=!1}Rh=0;P=O=N=null;Th=!1;Uh=0;ok.current=null;if(null===c||null===c.return){T=1;qk=b;Y=null;break}a:{var f=a,g=c.return,h=c,k=b;b=Z;h.flags|=32768;if(null!==k&&"object"===typeof k&&"function"===typeof k.then){var l=k,m=h,q=m.tag;if(0===(m.mode&1)&&(0===q||11===q||15===q)){var r=m.alternate;r?(m.updateQueue=r.updateQueue,m.memoizedState=r.memoizedState,
m.lanes=r.lanes):(m.updateQueue=null,m.memoizedState=null)}var y=Vi(g);if(null!==y){y.flags&=-257;Wi(y,g,h,f,b);y.mode&1&&Ti(f,l,b);b=y;k=l;var n=b.updateQueue;if(null===n){var t=new Set;t.add(k);b.updateQueue=t}else n.add(k);break a}else{if(0===(b&1)){Ti(f,l,b);uj();break a}k=Error(p(426))}}else if(I&&h.mode&1){var J=Vi(g);if(null!==J){0===(J.flags&65536)&&(J.flags|=256);Wi(J,g,h,f,b);Jg(Ki(k,h));break a}}f=k=Ki(k,h);4!==T&&(T=2);null===tk?tk=[f]:tk.push(f);f=g;do{switch(f.tag){case 3:f.flags|=65536;
b&=-b;f.lanes|=b;var x=Oi(f,k,b);fh(f,x);break a;case 1:h=k;var w=f.type,u=f.stateNode;if(0===(f.flags&128)&&("function"===typeof w.getDerivedStateFromError||null!==u&&"function"===typeof u.componentDidCatch&&(null===Si||!Si.has(u)))){f.flags|=65536;b&=-b;f.lanes|=b;var F=Ri(f,h,b);fh(f,F);break a}}f=f.return}while(null!==f)}Tk(c)}catch(na){b=na;Y===c&&null!==c&&(Y=c=c.return);continue}break}while(1)}function Kk(){var a=nk.current;nk.current=ai;return null===a?ai:a}
function uj(){if(0===T||3===T||2===T)T=4;null===R||0===(hh&268435455)&&0===(rk&268435455)||Dk(R,Z)}function Jk(a,b){var c=K;K|=2;var d=Kk();if(R!==a||Z!==b)vk=null,Lk(a,b);do try{Uk();break}catch(e){Nk(a,e)}while(1);Qg();K=c;nk.current=d;if(null!==Y)throw Error(p(261));R=null;Z=0;return T}function Uk(){for(;null!==Y;)Vk(Y)}function Mk(){for(;null!==Y&&!cc();)Vk(Y)}function Vk(a){var b=Wk(a.alternate,a,gj);a.memoizedProps=a.pendingProps;null===b?Tk(a):Y=b;ok.current=null}
function Tk(a){var b=a;do{var c=b.alternate;a=b.return;if(0===(b.flags&32768)){if(c=Fj(c,b,gj),null!==c){Y=c;return}}else{c=Jj(c,b);if(null!==c){c.flags&=32767;Y=c;return}if(null!==a)a.flags|=32768,a.subtreeFlags=0,a.deletions=null;else{T=6;Y=null;return}}b=b.sibling;if(null!==b){Y=b;return}Y=b=a}while(null!==b);0===T&&(T=5)}function Qk(a,b,c){var d=C,e=pk.transition;try{pk.transition=null,C=1,Xk(a,b,c,d)}finally{pk.transition=e,C=d}return null}
function Xk(a,b,c,d){do Ik();while(null!==xk);if(0!==(K&6))throw Error(p(327));c=a.finishedWork;var e=a.finishedLanes;if(null===c)return null;a.finishedWork=null;a.finishedLanes=0;if(c===a.current)throw Error(p(177));a.callbackNode=null;a.callbackPriority=0;var f=c.lanes|c.childLanes;Bc(a,f);a===R&&(Y=R=null,Z=0);0===(c.subtreeFlags&2064)&&0===(c.flags&2064)||wk||(wk=!0,Gk(hc,function(){Ik();return null}));f=0!==(c.flags&15990);if(0!==(c.subtreeFlags&15990)||f){f=pk.transition;pk.transition=null;
var g=C;C=1;var h=K;K|=4;ok.current=null;Pj(a,c);ek(c,a);Oe(Df);dd=!!Cf;Df=Cf=null;a.current=c;ik(c,a,e);dc();K=h;C=g;pk.transition=f}else a.current=c;wk&&(wk=!1,xk=a,yk=e);f=a.pendingLanes;0===f&&(Si=null);mc(c.stateNode,d);Ek(a,B());if(null!==b)for(d=a.onRecoverableError,c=0;c<b.length;c++)e=b[c],d(e.value,{componentStack:e.stack,digest:e.digest});if(Pi)throw Pi=!1,a=Qi,Qi=null,a;0!==(yk&1)&&0!==a.tag&&Ik();f=a.pendingLanes;0!==(f&1)?a===Ak?zk++:(zk=0,Ak=a):zk=0;jg();return null}
function Ik(){if(null!==xk){var a=Dc(yk),b=pk.transition,c=C;try{pk.transition=null;C=16>a?16:a;if(null===xk)var d=!1;else{a=xk;xk=null;yk=0;if(0!==(K&6))throw Error(p(331));var e=K;K|=4;for(V=a.current;null!==V;){var f=V,g=f.child;if(0!==(V.flags&16)){var h=f.deletions;if(null!==h){for(var k=0;k<h.length;k++){var l=h[k];for(V=l;null!==V;){var m=V;switch(m.tag){case 0:case 11:case 15:Qj(8,m,f)}var q=m.child;if(null!==q)q.return=m,V=q;else for(;null!==V;){m=V;var r=m.sibling,y=m.return;Tj(m);if(m===
l){V=null;break}if(null!==r){r.return=y;V=r;break}V=y}}}var n=f.alternate;if(null!==n){var t=n.child;if(null!==t){n.child=null;do{var J=t.sibling;t.sibling=null;t=J}while(null!==t)}}V=f}}if(0!==(f.subtreeFlags&2064)&&null!==g)g.return=f,V=g;else b:for(;null!==V;){f=V;if(0!==(f.flags&2048))switch(f.tag){case 0:case 11:case 15:Qj(9,f,f.return)}var x=f.sibling;if(null!==x){x.return=f.return;V=x;break b}V=f.return}}var w=a.current;for(V=w;null!==V;){g=V;var u=g.child;if(0!==(g.subtreeFlags&2064)&&null!==
u)u.return=g,V=u;else b:for(g=w;null!==V;){h=V;if(0!==(h.flags&2048))try{switch(h.tag){case 0:case 11:case 15:Rj(9,h)}}catch(na){W(h,h.return,na)}if(h===g){V=null;break b}var F=h.sibling;if(null!==F){F.return=h.return;V=F;break b}V=h.return}}K=e;jg();if(lc&&"function"===typeof lc.onPostCommitFiberRoot)try{lc.onPostCommitFiberRoot(kc,a)}catch(na){}d=!0}return d}finally{C=c,pk.transition=b}}return!1}function Yk(a,b,c){b=Ki(c,b);b=Oi(a,b,1);a=dh(a,b,1);b=L();null!==a&&(Ac(a,1,b),Ek(a,b))}
function W(a,b,c){if(3===a.tag)Yk(a,a,c);else for(;null!==b;){if(3===b.tag){Yk(b,a,c);break}else if(1===b.tag){var d=b.stateNode;if("function"===typeof b.type.getDerivedStateFromError||"function"===typeof d.componentDidCatch&&(null===Si||!Si.has(d))){a=Ki(c,a);a=Ri(b,a,1);b=dh(b,a,1);a=L();null!==b&&(Ac(b,1,a),Ek(b,a));break}}b=b.return}}
function Ui(a,b,c){var d=a.pingCache;null!==d&&d.delete(b);b=L();a.pingedLanes|=a.suspendedLanes&c;R===a&&(Z&c)===c&&(4===T||3===T&&(Z&130023424)===Z&&500>B()-gk?Lk(a,0):sk|=c);Ek(a,b)}function Zk(a,b){0===b&&(0===(a.mode&1)?b=1:(b=sc,sc<<=1,0===(sc&130023424)&&(sc=4194304)));var c=L();a=Zg(a,b);null!==a&&(Ac(a,b,c),Ek(a,c))}function vj(a){var b=a.memoizedState,c=0;null!==b&&(c=b.retryLane);Zk(a,c)}
function ck(a,b){var c=0;switch(a.tag){case 13:var d=a.stateNode;var e=a.memoizedState;null!==e&&(c=e.retryLane);break;case 19:d=a.stateNode;break;default:throw Error(p(314));}null!==d&&d.delete(b);Zk(a,c)}var Wk;
Wk=function(a,b,c){if(null!==a)if(a.memoizedProps!==b.pendingProps||Wf.current)Ug=!0;else{if(0===(a.lanes&c)&&0===(b.flags&128))return Ug=!1,zj(a,b,c);Ug=0!==(a.flags&131072)?!0:!1}else Ug=!1,I&&0!==(b.flags&1048576)&&ug(b,ng,b.index);b.lanes=0;switch(b.tag){case 2:var d=b.type;jj(a,b);a=b.pendingProps;var e=Yf(b,H.current);Tg(b,c);e=Xh(null,b,d,a,e,c);var f=bi();b.flags|=1;"object"===typeof e&&null!==e&&"function"===typeof e.render&&void 0===e.$$typeof?(b.tag=1,b.memoizedState=null,b.updateQueue=
null,Zf(d)?(f=!0,cg(b)):f=!1,b.memoizedState=null!==e.state&&void 0!==e.state?e.state:null,ah(b),e.updater=nh,b.stateNode=e,e._reactInternals=b,rh(b,d,a,c),b=kj(null,b,d,!0,f,c)):(b.tag=0,I&&f&&vg(b),Yi(null,b,e,c),b=b.child);return b;case 16:d=b.elementType;a:{jj(a,b);a=b.pendingProps;e=d._init;d=e(d._payload);b.type=d;e=b.tag=$k(d);a=Lg(d,a);switch(e){case 0:b=dj(null,b,d,a,c);break a;case 1:b=ij(null,b,d,a,c);break a;case 11:b=Zi(null,b,d,a,c);break a;case 14:b=aj(null,b,d,Lg(d.type,a),c);break a}throw Error(p(306,
d,""));}return b;case 0:return d=b.type,e=b.pendingProps,e=b.elementType===d?e:Lg(d,e),dj(a,b,d,e,c);case 1:return d=b.type,e=b.pendingProps,e=b.elementType===d?e:Lg(d,e),ij(a,b,d,e,c);case 3:a:{lj(b);if(null===a)throw Error(p(387));d=b.pendingProps;f=b.memoizedState;e=f.element;bh(a,b);gh(b,d,null,c);var g=b.memoizedState;d=g.element;if(f.isDehydrated)if(f={element:d,isDehydrated:!1,cache:g.cache,pendingSuspenseBoundaries:g.pendingSuspenseBoundaries,transitions:g.transitions},b.updateQueue.baseState=
f,b.memoizedState=f,b.flags&256){e=Ki(Error(p(423)),b);b=mj(a,b,d,c,e);break a}else if(d!==e){e=Ki(Error(p(424)),b);b=mj(a,b,d,c,e);break a}else for(yg=Lf(b.stateNode.containerInfo.firstChild),xg=b,I=!0,zg=null,c=Ch(b,null,d,c),b.child=c;c;)c.flags=c.flags&-3|4096,c=c.sibling;else{Ig();if(d===e){b=$i(a,b,c);break a}Yi(a,b,d,c)}b=b.child}return b;case 5:return Kh(b),null===a&&Eg(b),d=b.type,e=b.pendingProps,f=null!==a?a.memoizedProps:null,g=e.children,Ef(d,e)?g=null:null!==f&&Ef(d,f)&&(b.flags|=32),
hj(a,b),Yi(a,b,g,c),b.child;case 6:return null===a&&Eg(b),null;case 13:return pj(a,b,c);case 4:return Ih(b,b.stateNode.containerInfo),d=b.pendingProps,null===a?b.child=Bh(b,null,d,c):Yi(a,b,d,c),b.child;case 11:return d=b.type,e=b.pendingProps,e=b.elementType===d?e:Lg(d,e),Zi(a,b,d,e,c);case 7:return Yi(a,b,b.pendingProps,c),b.child;case 8:return Yi(a,b,b.pendingProps.children,c),b.child;case 12:return Yi(a,b,b.pendingProps.children,c),b.child;case 10:a:{d=b.type._context;e=b.pendingProps;f=b.memoizedProps;
g=e.value;G(Mg,d._currentValue);d._currentValue=g;if(null!==f)if(He(f.value,g)){if(f.children===e.children&&!Wf.current){b=$i(a,b,c);break a}}else for(f=b.child,null!==f&&(f.return=b);null!==f;){var h=f.dependencies;if(null!==h){g=f.child;for(var k=h.firstContext;null!==k;){if(k.context===d){if(1===f.tag){k=ch(-1,c&-c);k.tag=2;var l=f.updateQueue;if(null!==l){l=l.shared;var m=l.pending;null===m?k.next=k:(k.next=m.next,m.next=k);l.pending=k}}f.lanes|=c;k=f.alternate;null!==k&&(k.lanes|=c);Sg(f.return,
c,b);h.lanes|=c;break}k=k.next}}else if(10===f.tag)g=f.type===b.type?null:f.child;else if(18===f.tag){g=f.return;if(null===g)throw Error(p(341));g.lanes|=c;h=g.alternate;null!==h&&(h.lanes|=c);Sg(g,c,b);g=f.sibling}else g=f.child;if(null!==g)g.return=f;else for(g=f;null!==g;){if(g===b){g=null;break}f=g.sibling;if(null!==f){f.return=g.return;g=f;break}g=g.return}f=g}Yi(a,b,e.children,c);b=b.child}return b;case 9:return e=b.type,d=b.pendingProps.children,Tg(b,c),e=Vg(e),d=d(e),b.flags|=1,Yi(a,b,d,c),
b.child;case 14:return d=b.type,e=Lg(d,b.pendingProps),e=Lg(d.type,e),aj(a,b,d,e,c);case 15:return cj(a,b,b.type,b.pendingProps,c);case 17:return d=b.type,e=b.pendingProps,e=b.elementType===d?e:Lg(d,e),jj(a,b),b.tag=1,Zf(d)?(a=!0,cg(b)):a=!1,Tg(b,c),ph(b,d,e),rh(b,d,e,c),kj(null,b,d,!0,a,c);case 19:return yj(a,b,c);case 22:return ej(a,b,c)}throw Error(p(156,b.tag));};function Gk(a,b){return ac(a,b)}
function al(a,b,c,d){this.tag=a;this.key=c;this.sibling=this.child=this.return=this.stateNode=this.type=this.elementType=null;this.index=0;this.ref=null;this.pendingProps=b;this.dependencies=this.memoizedState=this.updateQueue=this.memoizedProps=null;this.mode=d;this.subtreeFlags=this.flags=0;this.deletions=null;this.childLanes=this.lanes=0;this.alternate=null}function Bg(a,b,c,d){return new al(a,b,c,d)}function bj(a){a=a.prototype;return!(!a||!a.isReactComponent)}
function $k(a){if("function"===typeof a)return bj(a)?1:0;if(void 0!==a&&null!==a){a=a.$$typeof;if(a===Da)return 11;if(a===Ga)return 14}return 2}
function wh(a,b){var c=a.alternate;null===c?(c=Bg(a.tag,b,a.key,a.mode),c.elementType=a.elementType,c.type=a.type,c.stateNode=a.stateNode,c.alternate=a,a.alternate=c):(c.pendingProps=b,c.type=a.type,c.flags=0,c.subtreeFlags=0,c.deletions=null);c.flags=a.flags&14680064;c.childLanes=a.childLanes;c.lanes=a.lanes;c.child=a.child;c.memoizedProps=a.memoizedProps;c.memoizedState=a.memoizedState;c.updateQueue=a.updateQueue;b=a.dependencies;c.dependencies=null===b?null:{lanes:b.lanes,firstContext:b.firstContext};
c.sibling=a.sibling;c.index=a.index;c.ref=a.ref;return c}
function yh(a,b,c,d,e,f){var g=2;d=a;if("function"===typeof a)bj(a)&&(g=1);else if("string"===typeof a)g=5;else a:switch(a){case ya:return Ah(c.children,e,f,b);case za:g=8;e|=8;break;case Aa:return a=Bg(12,c,b,e|2),a.elementType=Aa,a.lanes=f,a;case Ea:return a=Bg(13,c,b,e),a.elementType=Ea,a.lanes=f,a;case Fa:return a=Bg(19,c,b,e),a.elementType=Fa,a.lanes=f,a;case Ia:return qj(c,e,f,b);default:if("object"===typeof a&&null!==a)switch(a.$$typeof){case Ba:g=10;break a;case Ca:g=9;break a;case Da:g=11;
break a;case Ga:g=14;break a;case Ha:g=16;d=null;break a}throw Error(p(130,null==a?a:typeof a,""));}b=Bg(g,c,b,e);b.elementType=a;b.type=d;b.lanes=f;return b}function Ah(a,b,c,d){a=Bg(7,a,d,b);a.lanes=c;return a}function qj(a,b,c,d){a=Bg(22,a,d,b);a.elementType=Ia;a.lanes=c;a.stateNode={isHidden:!1};return a}function xh(a,b,c){a=Bg(6,a,null,b);a.lanes=c;return a}
function zh(a,b,c){b=Bg(4,null!==a.children?a.children:[],a.key,b);b.lanes=c;b.stateNode={containerInfo:a.containerInfo,pendingChildren:null,implementation:a.implementation};return b}
function bl(a,b,c,d,e){this.tag=b;this.containerInfo=a;this.finishedWork=this.pingCache=this.current=this.pendingChildren=null;this.timeoutHandle=-1;this.callbackNode=this.pendingContext=this.context=null;this.callbackPriority=0;this.eventTimes=zc(0);this.expirationTimes=zc(-1);this.entangledLanes=this.finishedLanes=this.mutableReadLanes=this.expiredLanes=this.pingedLanes=this.suspendedLanes=this.pendingLanes=0;this.entanglements=zc(0);this.identifierPrefix=d;this.onRecoverableError=e;this.mutableSourceEagerHydrationData=
null}function cl(a,b,c,d,e,f,g,h,k){a=new bl(a,b,c,h,k);1===b?(b=1,!0===f&&(b|=8)):b=0;f=Bg(3,null,null,b);a.current=f;f.stateNode=a;f.memoizedState={element:d,isDehydrated:c,cache:null,transitions:null,pendingSuspenseBoundaries:null};ah(f);return a}function dl(a,b,c){var d=3<arguments.length&&void 0!==arguments[3]?arguments[3]:null;return{$$typeof:wa,key:null==d?null:""+d,children:a,containerInfo:b,implementation:c}}
function el(a){if(!a)return Vf;a=a._reactInternals;a:{if(Vb(a)!==a||1!==a.tag)throw Error(p(170));var b=a;do{switch(b.tag){case 3:b=b.stateNode.context;break a;case 1:if(Zf(b.type)){b=b.stateNode.__reactInternalMemoizedMergedChildContext;break a}}b=b.return}while(null!==b);throw Error(p(171));}if(1===a.tag){var c=a.type;if(Zf(c))return bg(a,c,b)}return b}
function fl(a,b,c,d,e,f,g,h,k){a=cl(c,d,!0,a,e,f,g,h,k);a.context=el(null);c=a.current;d=L();e=lh(c);f=ch(d,e);f.callback=void 0!==b&&null!==b?b:null;dh(c,f,e);a.current.lanes=e;Ac(a,e,d);Ek(a,d);return a}function gl(a,b,c,d){var e=b.current,f=L(),g=lh(e);c=el(c);null===b.context?b.context=c:b.pendingContext=c;b=ch(f,g);b.payload={element:a};d=void 0===d?null:d;null!==d&&(b.callback=d);a=dh(e,b,g);null!==a&&(mh(a,e,g,f),eh(a,e,g));return g}
function hl(a){a=a.current;if(!a.child)return null;switch(a.child.tag){case 5:return a.child.stateNode;default:return a.child.stateNode}}function il(a,b){a=a.memoizedState;if(null!==a&&null!==a.dehydrated){var c=a.retryLane;a.retryLane=0!==c&&c<b?c:b}}function jl(a,b){il(a,b);(a=a.alternate)&&il(a,b)}function kl(){return null}var ll="function"===typeof reportError?reportError:function(a){console.error(a)};function ml(a){this._internalRoot=a}
nl.prototype.render=ml.prototype.render=function(a){var b=this._internalRoot;if(null===b)throw Error(p(409));gl(a,b,null,null)};nl.prototype.unmount=ml.prototype.unmount=function(){var a=this._internalRoot;if(null!==a){this._internalRoot=null;var b=a.containerInfo;Sk(function(){gl(null,a,null,null)});b[uf]=null}};function nl(a){this._internalRoot=a}
nl.prototype.unstable_scheduleHydration=function(a){if(a){var b=Hc();a={blockedOn:null,target:a,priority:b};for(var c=0;c<Qc.length&&0!==b&&b<Qc[c].priority;c++);Qc.splice(c,0,a);0===c&&Vc(a)}};function ol(a){return!(!a||1!==a.nodeType&&9!==a.nodeType&&11!==a.nodeType)}function pl(a){return!(!a||1!==a.nodeType&&9!==a.nodeType&&11!==a.nodeType&&(8!==a.nodeType||" react-mount-point-unstable "!==a.nodeValue))}function ql(){}
function rl(a,b,c,d,e){if(e){if("function"===typeof d){var f=d;d=function(){var a=hl(g);f.call(a)}}var g=fl(b,d,a,0,null,!1,!1,"",ql);a._reactRootContainer=g;a[uf]=g.current;sf(8===a.nodeType?a.parentNode:a);Sk();return g}for(;e=a.lastChild;)a.removeChild(e);if("function"===typeof d){var h=d;d=function(){var a=hl(k);h.call(a)}}var k=cl(a,0,!1,null,null,!1,!1,"",ql);a._reactRootContainer=k;a[uf]=k.current;sf(8===a.nodeType?a.parentNode:a);Sk(function(){gl(b,k,c,d)});return k}
function sl(a,b,c,d,e){var f=c._reactRootContainer;if(f){var g=f;if("function"===typeof e){var h=e;e=function(){var a=hl(g);h.call(a)}}gl(b,g,a,e)}else g=rl(c,b,a,e,d);return hl(g)}Ec=function(a){switch(a.tag){case 3:var b=a.stateNode;if(b.current.memoizedState.isDehydrated){var c=tc(b.pendingLanes);0!==c&&(Cc(b,c|1),Ek(b,B()),0===(K&6)&&(Hj=B()+500,jg()))}break;case 13:Sk(function(){var b=Zg(a,1);if(null!==b){var c=L();mh(b,a,1,c)}}),jl(a,1)}};
Fc=function(a){if(13===a.tag){var b=Zg(a,134217728);if(null!==b){var c=L();mh(b,a,134217728,c)}jl(a,134217728)}};Gc=function(a){if(13===a.tag){var b=lh(a),c=Zg(a,b);if(null!==c){var d=L();mh(c,a,b,d)}jl(a,b)}};Hc=function(){return C};Ic=function(a,b){var c=C;try{return C=a,b()}finally{C=c}};
yb=function(a,b,c){switch(b){case "input":bb(a,c);b=c.name;if("radio"===c.type&&null!=b){for(c=a;c.parentNode;)c=c.parentNode;c=c.querySelectorAll("input[name="+JSON.stringify(""+b)+'][type="radio"]');for(b=0;b<c.length;b++){var d=c[b];if(d!==a&&d.form===a.form){var e=Db(d);if(!e)throw Error(p(90));Wa(d);bb(d,e)}}}break;case "textarea":ib(a,c);break;case "select":b=c.value,null!=b&&fb(a,!!c.multiple,b,!1)}};Gb=Rk;Hb=Sk;
var tl={usingClientEntryPoint:!1,Events:[Cb,ue,Db,Eb,Fb,Rk]},ul={findFiberByHostInstance:Wc,bundleType:0,version:"18.2.0",rendererPackageName:"react-dom"};
var vl={bundleType:ul.bundleType,version:ul.version,rendererPackageName:ul.rendererPackageName,rendererConfig:ul.rendererConfig,overrideHookState:null,overrideHookStateDeletePath:null,overrideHookStateRenamePath:null,overrideProps:null,overridePropsDeletePath:null,overridePropsRenamePath:null,setErrorHandler:null,setSuspenseHandler:null,scheduleUpdate:null,currentDispatcherRef:ua.ReactCurrentDispatcher,findHostInstanceByFiber:function(a){a=Zb(a);return null===a?null:a.stateNode},findFiberByHostInstance:ul.findFiberByHostInstance||
kl,findHostInstancesForRefresh:null,scheduleRefresh:null,scheduleRoot:null,setRefreshHandler:null,getCurrentFiber:null,reconcilerVersion:"18.2.0-next-9e3b772b8-20220608"};if("undefined"!==typeof __REACT_DEVTOOLS_GLOBAL_HOOK__){var wl=__REACT_DEVTOOLS_GLOBAL_HOOK__;if(!wl.isDisabled&&wl.supportsFiber)try{kc=wl.inject(vl),lc=wl}catch(a){}}exports.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED=tl;
exports.createPortal=function(a,b){var c=2<arguments.length&&void 0!==arguments[2]?arguments[2]:null;if(!ol(b))throw Error(p(200));return dl(a,b,null,c)};exports.createRoot=function(a,b){if(!ol(a))throw Error(p(299));var c=!1,d="",e=ll;null!==b&&void 0!==b&&(!0===b.unstable_strictMode&&(c=!0),void 0!==b.identifierPrefix&&(d=b.identifierPrefix),void 0!==b.onRecoverableError&&(e=b.onRecoverableError));b=cl(a,1,!1,null,null,c,!1,d,e);a[uf]=b.current;sf(8===a.nodeType?a.parentNode:a);return new ml(b)};
exports.findDOMNode=function(a){if(null==a)return null;if(1===a.nodeType)return a;var b=a._reactInternals;if(void 0===b){if("function"===typeof a.render)throw Error(p(188));a=Object.keys(a).join(",");throw Error(p(268,a));}a=Zb(b);a=null===a?null:a.stateNode;return a};exports.flushSync=function(a){return Sk(a)};exports.hydrate=function(a,b,c){if(!pl(b))throw Error(p(200));return sl(null,a,b,!0,c)};
exports.hydrateRoot=function(a,b,c){if(!ol(a))throw Error(p(405));var d=null!=c&&c.hydratedSources||null,e=!1,f="",g=ll;null!==c&&void 0!==c&&(!0===c.unstable_strictMode&&(e=!0),void 0!==c.identifierPrefix&&(f=c.identifierPrefix),void 0!==c.onRecoverableError&&(g=c.onRecoverableError));b=fl(b,null,a,1,null!=c?c:null,e,!1,f,g);a[uf]=b.current;sf(a);if(d)for(a=0;a<d.length;a++)c=d[a],e=c._getVersion,e=e(c._source),null==b.mutableSourceEagerHydrationData?b.mutableSourceEagerHydrationData=[c,e]:b.mutableSourceEagerHydrationData.push(c,
e);return new nl(b)};exports.render=function(a,b,c){if(!pl(b))throw Error(p(200));return sl(null,a,b,!1,c)};exports.unmountComponentAtNode=function(a){if(!pl(a))throw Error(p(40));return a._reactRootContainer?(Sk(function(){sl(null,null,a,!1,function(){a._reactRootContainer=null;a[uf]=null})}),!0):!1};exports.unstable_batchedUpdates=Rk;
exports.unstable_renderSubtreeIntoContainer=function(a,b,c,d){if(!pl(c))throw Error(p(200));if(null==a||void 0===a._reactInternals)throw Error(p(38));return sl(a,b,c,!1,d)};exports.version="18.2.0-next-9e3b772b8-20220608";


/***/ },

/***/ 572
(module, exports) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = checkHost;
function isRegExp(obj) {
  return Object.prototype.toString.call(obj) === '[object RegExp]';
}
function checkHost(host, matches) {
  for (var i = 0; i < matches.length; i++) {
    var match = matches[i];
    if (host === match || isRegExp(match) && match.test(host)) {
      return true;
    }
  }
  return false;
}
module.exports = exports.default;
module.exports["default"] = exports.default;

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

/***/ 610
(module, exports) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = merge;
function merge() {
  var obj = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
  var defaults = arguments.length > 1 ? arguments[1] : undefined;
  for (var key in defaults) {
    if (typeof obj[key] === 'undefined') {
      obj[key] = defaults[key];
    }
  }
  return obj;
}
module.exports = exports.default;
module.exports["default"] = exports.default;

/***/ },

/***/ 636
(module, exports) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;
var includes = function includes(str, val) {
  return str.indexOf(val) !== -1;
};
var _default = exports["default"] = includes;
module.exports = exports.default;
module.exports["default"] = exports.default;

/***/ },

/***/ 658
(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = isFQDN;
var _assertString = _interopRequireDefault(__webpack_require__(399));
var _merge = _interopRequireDefault(__webpack_require__(610));
function _interopRequireDefault(e) { return e && e.__esModule ? e : { default: e }; }
var default_fqdn_options = {
  require_tld: true,
  allow_underscores: false,
  allow_trailing_dot: false,
  allow_numeric_tld: false,
  allow_wildcard: false,
  ignore_max_length: false
};
function isFQDN(str, options) {
  (0, _assertString.default)(str);
  options = (0, _merge.default)(options, default_fqdn_options);

  /* Remove the optional trailing dot before checking validity */
  if (options.allow_trailing_dot && str[str.length - 1] === '.') {
    str = str.substring(0, str.length - 1);
  }

  /* Remove the optional wildcard before checking validity */
  if (options.allow_wildcard === true && str.indexOf('*.') === 0) {
    str = str.substring(2);
  }
  var parts = str.split('.');
  var tld = parts[parts.length - 1];
  if (options.require_tld) {
    // disallow fqdns without tld
    if (parts.length < 2) {
      return false;
    }
    if (!options.allow_numeric_tld && !/^([a-z\u00A1-\u00A8\u00AA-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]{2,}|xn[a-z0-9-]{2,})$/i.test(tld)) {
      return false;
    }

    // disallow spaces
    if (/\s/.test(tld)) {
      return false;
    }
  }

  // reject numeric TLDs
  if (!options.allow_numeric_tld && /^\d+$/.test(tld)) {
    return false;
  }
  return parts.every(function (part) {
    if (part.length > 63 && !options.ignore_max_length) {
      return false;
    }
    if (!/^[a-z_\u00a1-\uffff0-9-]+$/i.test(part)) {
      return false;
    }

    // disallow full-width chars
    if (/[\uff01-\uff5e]/.test(part)) {
      return false;
    }

    // disallow parts starting or ending with hyphen
    if (/^-|-$/.test(part)) {
      return false;
    }
    if (!options.allow_underscores && /_/.test(part)) {
      return false;
    }
    return true;
  });
}
module.exports = exports.default;
module.exports["default"] = exports.default;

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


/***/ },

/***/ 844
(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = isURL;
var _assertString = _interopRequireDefault(__webpack_require__(399));
var _checkHost = _interopRequireDefault(__webpack_require__(572));
var _includesString = _interopRequireDefault(__webpack_require__(636));
var _isFQDN = _interopRequireDefault(__webpack_require__(658));
var _isIP = _interopRequireDefault(__webpack_require__(372));
var _merge = _interopRequireDefault(__webpack_require__(610));
function _interopRequireDefault(e) { return e && e.__esModule ? e : { default: e }; }
function _slicedToArray(r, e) { return _arrayWithHoles(r) || _iterableToArrayLimit(r, e) || _unsupportedIterableToArray(r, e) || _nonIterableRest(); }
function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }
function _unsupportedIterableToArray(r, a) { if (r) { if ("string" == typeof r) return _arrayLikeToArray(r, a); var t = {}.toString.call(r).slice(8, -1); return "Object" === t && r.constructor && (t = r.constructor.name), "Map" === t || "Set" === t ? Array.from(r) : "Arguments" === t || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t) ? _arrayLikeToArray(r, a) : void 0; } }
function _arrayLikeToArray(r, a) { (null == a || a > r.length) && (a = r.length); for (var e = 0, n = Array(a); e < a; e++) n[e] = r[e]; return n; }
function _iterableToArrayLimit(r, l) { var t = null == r ? null : "undefined" != typeof Symbol && r[Symbol.iterator] || r["@@iterator"]; if (null != t) { var e, n, i, u, a = [], f = !0, o = !1; try { if (i = (t = t.call(r)).next, 0 === l) { if (Object(t) !== t) return; f = !1; } else for (; !(f = (e = i.call(t)).done) && (a.push(e.value), a.length !== l); f = !0); } catch (r) { o = !0, n = r; } finally { try { if (!f && null != t.return && (u = t.return(), Object(u) !== u)) return; } finally { if (o) throw n; } } return a; } }
function _arrayWithHoles(r) { if (Array.isArray(r)) return r; }
/*
options for isURL method

protocols - valid protocols can be modified with this option.
require_tld - If set to false isURL will not check if the URL's host includes a top-level domain.
require_protocol - if set to true isURL will return false if protocol is not present in the URL.
require_host - if set to false isURL will not check if host is present in the URL.
require_port - if set to true isURL will check if port is present in the URL.
require_valid_protocol - isURL will check if the URL's protocol is present in the protocols option.
allow_underscores - if set to true, the validator will allow underscores in the URL.
host_whitelist - if set to an array of strings or regexp, and the domain matches none of the strings
                 defined in it, the validation fails.
host_blacklist - if set to an array of strings or regexp, and the domain matches any of the strings
                 defined in it, the validation fails.
allow_trailing_dot - if set to true, the validator will allow the domain to end with
                     a `.` character.
allow_protocol_relative_urls - if set to true protocol relative URLs will be allowed.
allow_fragments - if set to false isURL will return false if fragments are present.
allow_query_components - if set to false isURL will return false if query components are present.
disallow_auth - if set to true, the validator will fail if the URL contains an authentication
                component, e.g. `http://username:password@example.com`
validate_length - if set to false isURL will skip string length validation. `max_allowed_length`
                  will be ignored if this is set as `false`.
max_allowed_length - if set, isURL will not allow URLs longer than the specified value (default is
                     2084 that IE maximum URL length).

*/

var default_url_options = {
  protocols: ['http', 'https', 'ftp'],
  require_tld: true,
  require_protocol: false,
  require_host: true,
  require_port: false,
  require_valid_protocol: true,
  allow_underscores: false,
  allow_trailing_dot: false,
  allow_protocol_relative_urls: false,
  allow_fragments: true,
  allow_query_components: true,
  validate_length: true,
  max_allowed_length: 2084
};
var wrapped_ipv6 = /^\[([^\]]+)\](?::([0-9]+))?$/;
function isURL(url, options) {
  (0, _assertString.default)(url);
  if (!url || /[\s<>]/.test(url)) {
    return false;
  }
  if (url.indexOf('mailto:') === 0) {
    return false;
  }
  options = (0, _merge.default)(options, default_url_options);
  if (options.validate_length && url.length > options.max_allowed_length) {
    return false;
  }
  if (!options.allow_fragments && (0, _includesString.default)(url, '#')) {
    return false;
  }
  if (!options.allow_query_components && ((0, _includesString.default)(url, '?') || (0, _includesString.default)(url, '&'))) {
    return false;
  }
  var protocol, auth, host, hostname, port, port_str, split, ipv6;
  split = url.split('#');
  url = split.shift();
  split = url.split('?');
  url = split.shift();

  // Replaced the 'split("://")' logic with a regex to match the protocol.
  // This correctly identifies schemes like `javascript:` which don't use `//`.
  // However, we need to be careful not to confuse authentication credentials (user:password@host)
  // with protocols. A colon before an @ symbol might be part of auth, not a protocol separator.
  var protocol_match = url.match(/^([a-z][a-z0-9+\-.]*):/i);
  var had_explicit_protocol = false;
  var cleanUpProtocol = function cleanUpProtocol(potential_protocol) {
    had_explicit_protocol = true;
    protocol = potential_protocol.toLowerCase();
    if (options.require_valid_protocol && options.protocols.indexOf(protocol) === -1) {
      // The identified protocol is not in the allowed list.
      return false;
    }

    // Remove the protocol from the URL string.
    return url.substring(protocol_match[0].length);
  };
  if (protocol_match) {
    var potential_protocol = protocol_match[1];
    var after_colon = url.substring(protocol_match[0].length);

    // Check if what follows looks like authentication credentials (user:password@host)
    // rather than a protocol. This happens when:
    // 1. There's no `//` after the colon (protocols like `http://` have this)
    // 2. There's an `@` symbol before any `/`
    // 3. The part before `@` contains only valid auth characters (alphanumeric, -, _, ., %, :)
    var starts_with_slashes = after_colon.slice(0, 2) === '//';
    if (!starts_with_slashes) {
      var first_slash_position = after_colon.indexOf('/');
      var before_slash = first_slash_position === -1 ? after_colon : after_colon.substring(0, first_slash_position);
      var at_position = before_slash.indexOf('@');
      if (at_position !== -1) {
        var before_at = before_slash.substring(0, at_position);
        var valid_auth_regex = /^[a-zA-Z0-9\-_.%:]*$/;
        var is_valid_auth = valid_auth_regex.test(before_at);

        // Check if this contains URL-encoded content that could be malicious
        // For example: javascript:%61%6c%65%72%74%28%31%29@example.com
        // The encoded part decodes to: alert(1)
        var has_encoded_content = /%[0-9a-fA-F]{2}/.test(before_at);
        if (is_valid_auth && !has_encoded_content) {
          // This looks like authentication (e.g., user:password@host), not a protocol
          if (options.require_protocol) {
            return false;
          }

          // Don't consume the colon; let the auth parsing handle it later
        } else {
          // This looks like a malicious protocol (e.g., javascript:alert();@host)
          // or URL-encoded protocol handler (e.g., javascript:%61%6c%65%72%74%28%31%29@host)
          url = cleanUpProtocol(potential_protocol);
          if (url === false) {
            return false;
          }
        }
      } else {
        // No @ symbol found. Check if this could be a port number instead of a protocol.
        // If what's after the colon is numeric (or starts with a digit and contains only
        // valid port characters until a path separator), it's likely hostname:port, not a protocol.
        var looks_like_port = /^[0-9]/.test(after_colon);
        if (looks_like_port) {
          // This looks like hostname:port, not a protocol
          if (options.require_protocol) {
            return false;
          }
          // Don't consume anything; let it be parsed as hostname:port
        } else {
          // This is definitely a protocol
          url = cleanUpProtocol(potential_protocol);
          if (url === false) {
            return false;
          }
        }
      }
    } else {
      // Starts with '//', this is definitely a protocol like http://
      url = cleanUpProtocol(potential_protocol);
      if (url === false) {
        return false;
      }
    }
  } else if (options.require_protocol) {
    return false;
  }

  // Handle leading '//' only as protocol-relative when there was NO explicit protocol.
  // If there was an explicit protocol, '//' is the normal separator
  // and should be stripped unconditionally.
  if (url.slice(0, 2) === '//') {
    if (!had_explicit_protocol && !options.allow_protocol_relative_urls) {
      return false;
    }
    url = url.slice(2);
  }
  if (url === '') {
    return false;
  }
  split = url.split('/');
  url = split.shift();
  if (url === '' && !options.require_host) {
    return true;
  }
  split = url.split('@');
  if (split.length > 1) {
    if (options.disallow_auth) {
      return false;
    }
    if (split[0] === '') {
      return false;
    }
    auth = split.shift();
    if (auth.indexOf(':') >= 0 && auth.split(':').length > 2) {
      return false;
    }
    var _auth$split = auth.split(':'),
      _auth$split2 = _slicedToArray(_auth$split, 2),
      user = _auth$split2[0],
      password = _auth$split2[1];
    if (user === '' && password === '') {
      return false;
    }
  }
  hostname = split.join('@');
  port_str = null;
  ipv6 = null;
  var ipv6_match = hostname.match(wrapped_ipv6);
  if (ipv6_match) {
    host = '';
    ipv6 = ipv6_match[1];
    port_str = ipv6_match[2] || null;
  } else {
    split = hostname.split(':');
    host = split.shift();
    if (split.length) {
      port_str = split.join(':');
    }
  }
  if (port_str !== null && port_str.length > 0) {
    port = parseInt(port_str, 10);
    if (!/^[0-9]+$/.test(port_str) || port <= 0 || port > 65535) {
      return false;
    }
  } else if (options.require_port) {
    return false;
  }
  if (options.host_whitelist) {
    return (0, _checkHost.default)(host, options.host_whitelist);
  }
  if (host === '' && !options.require_host) {
    return true;
  }
  if (!(0, _isIP.default)(host) && !(0, _isFQDN.default)(host, options) && (!ipv6 || !(0, _isIP.default)(ipv6, 6))) {
    return false;
  }
  host = host || ipv6;
  if (options.host_blacklist && (0, _checkHost.default)(host, options.host_blacklist)) {
    return false;
  }
  return true;
}
module.exports = exports.default;
module.exports["default"] = exports.default;

/***/ },

/***/ 961
(module, __unused_webpack_exports, __webpack_require__) {

"use strict";


function checkDCE() {
  /* global __REACT_DEVTOOLS_GLOBAL_HOOK__ */
  if (
    typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ === 'undefined' ||
    typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE !== 'function'
  ) {
    return;
  }
  if (false) // removed by dead control flow
{}
  try {
    // Verify that the code above has been dead code eliminated (DCE'd).
    __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(checkDCE);
  } catch (err) {
    // DevTools shouldn't crash React, no matter what.
    // We should still report in case we break this code.
    console.error(err);
  }
}

if (true) {
  // DCE check should happen before ReactDOM bundle executes so that
  // DevTools can report bad minification during injection.
  checkDCE();
  module.exports = __webpack_require__(551);
} else // removed by dead control flow
{}


/***/ },

/***/ 982
(module, __unused_webpack_exports, __webpack_require__) {

"use strict";


if (true) {
  module.exports = __webpack_require__(463);
} else // removed by dead control flow
{}


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
/******/ 	/* webpack/runtime/global */
/******/ 	(() => {
/******/ 		__webpack_require__.g = (function() {
/******/ 			if (typeof globalThis === 'object') return globalThis;
/******/ 			try {
/******/ 				return this || new Function('return this')();
/******/ 			} catch (e) {
/******/ 				if (typeof window === 'object') return window;
/******/ 			}
/******/ 		})();
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

// EXTERNAL MODULE: ./node_modules/react/index.js
var react = __webpack_require__(540);
;// ./src/components/DebuggingUtils.js

class DebuggingUtils_Home extends react.Component {
  triggerCrash = () => {
    if (false) // removed by dead control flow
{}
  };
  render() {
    if (false) // removed by dead control flow
{}
    return null;
  }
}
;// ./src/components/DisableButton.js

/* harmony default export */ const DisableButton = (({
  sessionWhitelist,
  currentUrl,
  onSiteDisable,
  onSiteEnable,
  bdLang
}) => {
  let currentState = true;
  let currentCallback = onSiteDisable;
  if (undefined != sessionWhitelist && sessionWhitelist.includes(currentUrl)) {
    currentState = false;
    currentCallback = onSiteEnable;
  }
  return /*#__PURE__*/react.createElement("div", null, /*#__PURE__*/react.createElement("label", {
    className: "play-pause"
  }, /*#__PURE__*/react.createElement("input", {
    type: "checkbox",
    checked: currentState,
    onChange: currentCallback
  }), /*#__PURE__*/react.createElement("div", null, /*#__PURE__*/react.createElement("span", null, bdLang.getString("pause_protection")), /*#__PURE__*/react.createElement("span", null, bdLang.getString("enable_protection")))), /*#__PURE__*/react.createElement("div", {
    className: "enable-shadow"
  }, bdLang.getString("enable_app")));
});
// EXTERNAL MODULE: ./node_modules/debug/src/browser.js
var src_browser = __webpack_require__(833);
var browser_default = /*#__PURE__*/__webpack_require__.n(src_browser);
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
;// ./src/utils/parseUrl.js

const emptyUrlParts = () => ({
  schema: '',
  hostname: '',
  port: '',
  pathname: '',
  search: '',
  hash: ''
});
/* harmony default export */ const utils_parseUrl = (url => {
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
function domain_getRegistrableDomain(hostname) {
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
// EXTERNAL MODULE: ./src/tracking/tracking.js
var tracking_tracking = __webpack_require__(177);
var tracking_default = /*#__PURE__*/__webpack_require__.n(tracking_tracking);
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
  compat.action.setBadgeBackgroundColor({
    color: "rgb(0,0,255)"
  });
}

/* setBadgeMessage
 * @param {*} currentTabId, nrTrackers
 */
function setBadgeMessage(currentTabId, nrTrackers) {
  compat.action.setBadgeText({
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
  scripts_compat.action.getBadgeText({
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
  Log.info('getDomain: [' + host_name + '] [' + domain + ']');
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
    if (tracking.isThirdPartyDomainException(request_host, tab_host)) {
      Log.info('isThirdPartyDomainException: [' + request_host + '] <- [' + tab_host + ']');
      ret = false;
    }
  }
  Log.info('isThirdPartyDomain: [' + request_host + '] <- [' + tab_host + '] [' + ret + ']');
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
;// ./src/components/TrackersCategory.js




function getTrackerUrlHostname(url, trackersUrls) {
  let hostName = url;
  if (canBlockWebRequest()) {
    hostName = utils_parseUrl(url).hostname;
    return hostName;
  }
  if (trackersUrls.length > 0) {
    let urlRegex = new RegExp(url);
    for (let tIndex = 0; tIndex < trackersUrls.length; ++tIndex) {
      let tUrl = trackersUrls[tIndex];
      if (urlRegex.test(tUrl)) {
        hostName = utils_parseUrl(tUrl).hostname;
        return hostName;
      }
    }
  }
  let pos = hostName.indexOf('/');
  if (pos > 0) {
    hostName = hostName.substring(0, pos);
  }
  return hostName;
}
function displayTrackersUrls(trackersMap, trackersUrls, currentCategoryKey) {
  let listItems = [];
  if (undefined === trackersMap || undefined === trackersMap[currentCategoryKey] || null === trackersMap[currentCategoryKey]) {
    return listItems;
  }
  log.warn('displayTrackersUrls trackersMap: ' + JSON.stringify(trackersMap, null, 4));
  log.warn('displayTrackersUrls trackersUrls: ' + JSON.stringify(trackersUrls, null, 4));
  function CatInfo(_url, _urlCount) {
    this.url = _url;
    this.urlCount = _urlCount;
  }
  let trackersUrlList = trackersMap[currentCategoryKey];
  let trackersCatMap = new Map();
  for (let index = 0; index < trackersUrlList.length; ++index) {
    let url = trackersUrlList[index];
    let hostName = getTrackerUrlHostname(url, trackersUrls);
    if (hostName.length === 0) {
      hostName = url;
    }
    if (trackersCatMap.has(hostName)) {
      let catInfo = trackersCatMap.get(hostName);
      catInfo.urlCount = catInfo.urlCount + 1;
      trackersCatMap.set(hostName, catInfo);
    } else {
      let catInfo = new CatInfo(url, 1);
      trackersCatMap.set(hostName, catInfo);
    }
  }
  let indexKey = 0;
  for (let [key, value] of trackersCatMap) {
    listItems.push(/*#__PURE__*/react.createElement("li", {
      key: indexKey
    }, /*#__PURE__*/react.createElement("div", {
      className: "name"
    }, /*#__PURE__*/react.createElement("span", null, key), /*#__PURE__*/react.createElement("span", {
      className: "count"
    }, value.urlCount)), /*#__PURE__*/react.createElement("div", {
      className: "url",
      title: value.url
    }, value.url)));
    indexKey++;
  }
  return listItems;
}
/* harmony default export */ const TrackersCategory = (({
  currentScreen,
  currentCategoryKey,
  categoryExpandRef,
  categories,
  trackersMap,
  trackersUrls,
  categoryStatusChanged,
  onClickCategoryLink,
  onClickBack,
  bdLang
}) => {
  if (currentScreen & SCREEN_UI.CATEGORY) {
    log.info('current screen: ' + currentScreen + ' current category key: ' + currentCategoryKey);
    let currentStatus = true;
    if (categories & currentCategoryKey) {
      currentStatus = false;
    }
    let categoryInfo = getTrackerCategoryName(bdLang, currentCategoryKey);
    let nrTrackers = 0;
    if (undefined !== trackersMap && undefined !== trackersMap[currentCategoryKey] && null !== trackersMap[currentCategoryKey]) {
      nrTrackers = trackersMap[currentCategoryKey].length;
    }
    let categoryTitle = categoryInfo.blocked.replace("%d", nrTrackers);
    let categoryButtonStatus = getTrackerCategoryStatus(bdLang, currentCategoryKey, currentStatus);
    let linkDescriptionDisplay = false;
    let catDescriptionText = getTrackerCategoryDescription(bdLang, currentCategoryKey);
    log.info('desc size: ' + catDescriptionText.length);
    if (catDescriptionText.length < 118) {
      linkDescriptionDisplay = true;
    }
    return /*#__PURE__*/react.createElement("div", {
      className: "category-screen show"
    }, /*#__PURE__*/react.createElement("div", {
      className: "dashboard _expand",
      ref: categoryExpandRef
    }, /*#__PURE__*/react.createElement("button", {
      className: "back",
      onClick: onClickBack
    }), /*#__PURE__*/react.createElement("img", {
      className: categoryInfo.icon
    }), /*#__PURE__*/react.createElement("div", {
      className: "category-title"
    }, categoryTitle), /*#__PURE__*/react.createElement("div", {
      className: "description"
    }, catDescriptionText), /*#__PURE__*/react.createElement("div", {
      hidden: linkDescriptionDisplay
    }, /*#__PURE__*/react.createElement("a", {
      onClick: onClickCategoryLink
    }, /*#__PURE__*/react.createElement("span", null, bdLang.getString("show_more_details")), /*#__PURE__*/react.createElement("span", null, bdLang.getString("hide_more_details")))), /*#__PURE__*/react.createElement("br", null), /*#__PURE__*/react.createElement("label", {
      className: "block-all"
    }, /*#__PURE__*/react.createElement("input", {
      type: "checkbox",
      checked: currentStatus,
      onChange: categoryStatusChanged
    }), /*#__PURE__*/react.createElement("div", null, /*#__PURE__*/react.createElement("span", null, categoryButtonStatus), /*#__PURE__*/react.createElement("span", null, categoryButtonStatus)))), /*#__PURE__*/react.createElement("ul", {
      className: categoryInfo.className
    }, displayTrackersUrls(trackersMap, trackersUrls, currentCategoryKey)));
  } else {
    return null;
  }
});
;// ./src/components/TrackersSettings.js


/* harmony default export */ const TrackersSettings = (({
  currentScreen,
  featureStatus,
  extensionEnabled,
  enableSwitchWasChanged,
  extensionSpecialOffers,
  specialOffersSwitchWasChanged,
  whitelist,
  inputWhitelistUrlRef,
  whitelistUrlErrorRef,
  onClickBack,
  addUrlToWhitelist,
  deleteUrlFromWhitelist,
  bdLang
}) => {
  let statusString = bdLang.getString("extension_status_on");
  if (!extensionEnabled) {
    statusString = bdLang.getString("extension_status_off");
  }
  let specialOffersString = bdLang.getString("special_offers");
  let specialOffersTooltipString = bdLang.getString("special_offers_tooltip");
  const displayTrackersWhiteList = () => {
    let listItems = [];
    if (undefined === whitelist) {
      return listItems;
    }
    for (let i = 0; i < whitelist.length; ++i) {
      listItems.push(/*#__PURE__*/react.createElement("li", {
        key: i
      }, /*#__PURE__*/react.createElement("div", {
        className: "url"
      }, whitelist[i]), /*#__PURE__*/react.createElement("button", {
        className: "remove",
        onClick: e => {
          deleteUrlFromWhitelist(e, whitelist[i]);
        }
      })));
    }
    return listItems;
  };
  if (currentScreen & SCREEN_UI.SETTINGS) {
    return /*#__PURE__*/react.createElement("div", {
      className: "whitelist-screen show"
    }, /*#__PURE__*/react.createElement("div", null, /*#__PURE__*/react.createElement("button", {
      className: "back",
      onClick: onClickBack
    }), /*#__PURE__*/react.createElement("div", {
      className: "page-title"
    }, bdLang.getString("settings_title")), /*#__PURE__*/react.createElement("div", {
      className: "switch-wrap"
    }, /*#__PURE__*/react.createElement("div", null, /*#__PURE__*/react.createElement("div", {
      className: "lbl"
    }, statusString), /*#__PURE__*/react.createElement("div", {
      className: "feat-description"
    }, bdLang.getString("extension_status_desc"))), /*#__PURE__*/react.createElement("label", {
      className: "switch"
    }, /*#__PURE__*/react.createElement("input", {
      type: "checkbox",
      disabled: !featureStatus,
      checked: extensionEnabled,
      onChange: enableSwitchWasChanged
    }), /*#__PURE__*/react.createElement("div", null))), /*#__PURE__*/react.createElement("div", {
      className: "switch-wrap sm"
    }, /*#__PURE__*/react.createElement("div", null, /*#__PURE__*/react.createElement("div", {
      className: "lbl"
    }, specialOffersString), /*#__PURE__*/react.createElement("div", {
      className: "tooltip-target"
    }, /*#__PURE__*/react.createElement("div", {
      className: "info-tooltip"
    }, /*#__PURE__*/react.createElement("div", null, specialOffersTooltipString)))), /*#__PURE__*/react.createElement("label", {
      className: "switch"
    }, /*#__PURE__*/react.createElement("input", {
      id: "start_stop_button",
      type: "checkbox",
      checked: extensionSpecialOffers,
      onChange: specialOffersSwitchWasChanged
    }), /*#__PURE__*/react.createElement("div", null))), /*#__PURE__*/react.createElement("div", {
      className: "section-title"
    }, bdLang.getString("exceptions_title")), /*#__PURE__*/react.createElement("div", {
      className: "page-description"
    }, bdLang.getString("exceptions_desc")), /*#__PURE__*/react.createElement("a", {
      onClick: e => {
        addUrlToWhitelist(e, true);
      }
    }, bdLang.getString("add_curr_website")), /*#__PURE__*/react.createElement("br", null), /*#__PURE__*/react.createElement("div", {
      className: "added",
      hidden: true
    }, bdLang.getString("website_added_list")), /*#__PURE__*/react.createElement("div", {
      className: "field-label"
    }, bdLang.getString("exception_action_desc")), /*#__PURE__*/react.createElement("div", {
      className: "field"
    }, /*#__PURE__*/react.createElement("div", null, /*#__PURE__*/react.createElement("input", {
      type: "text",
      className: "text-field",
      placeholder: bdLang.getString("website_url_enter"),
      ref: inputWhitelistUrlRef
    }), /*#__PURE__*/react.createElement("div", {
      className: "error-text",
      ref: whitelistUrlErrorRef
    }, bdLang.getString("url_not_valid"))), /*#__PURE__*/react.createElement("button", {
      className: "add",
      onClick: e => {
        addUrlToWhitelist(e, false);
      }
    }))), /*#__PURE__*/react.createElement("ul", {
      className: "url-list"
    }, displayTrackersWhiteList()), /*#__PURE__*/react.createElement("div", {
      className: "ad",
      hidden: true
    }, /*#__PURE__*/react.createElement("div", null, "Try the lastest version of"), /*#__PURE__*/react.createElement("div", {
      className: "product-name"
    }, "Bitdefender Antivirus Plus"), /*#__PURE__*/react.createElement("button", {
      className: "get-free"
    }, "Get 3 months free")));
  } else {
    return null;
  }
});
;// ./src/components/StackNavigation.js

/* harmony default export */ const StackNavigation = (({
  hostname,
  tabStack,
  stackIndex,
  onStackGoIndex
}) => {
  const navigationButtonsTop = 13;
  const websiteExtendedWidth = 350;
  const websiteReducedWidth = 230;
  let stackHasIndex = index => {
    return index >= 0 && index <= tabStack.length - 1;
  };
  let stackCanGoBack = () => {
    return stackHasIndex(stackIndex + 1);
  };
  let stackCanGoForward = () => {
    return stackHasIndex(stackIndex - 1);
  };
  let stackTrackersBlockedAtIndex = index => {
    if (stackHasIndex(index)) {
      let tabInfo = tabStack[index];
      return tabInfo.trackersBlocked;
    }
    return 0;
  };
  let stackTrackersBlockedBack = () => {
    return stackTrackersBlockedAtIndex(stackIndex + 1);
  };
  let stackTrackersBlockedForward = () => {
    return stackTrackersBlockedAtIndex(stackIndex - 1);
  };
  let onStackGoBack = () => {
    onStackGoIndex(stackIndex + 1);
  };
  let onStackGoForward = () => {
    onStackGoIndex(stackIndex - 1);
  };
  let stackBackButton = '';
  if (stackCanGoBack()) {
    let backText = '';
    if (stackTrackersBlockedBack() > 0) {
      backText = /*#__PURE__*/react.createElement("div", {
        className: "backTrackers"
      }, stackTrackersBlockedBack());
    }
    stackBackButton = /*#__PURE__*/react.createElement("label", {
      style: {
        float: 'left'
      }
    }, /*#__PURE__*/react.createElement("button", {
      id: "stackBack",
      className: "back",
      style: {
        top: navigationButtonsTop
      },
      onClick: onStackGoBack
    }), backText);
  }
  let stackForwardButton = '';
  if (stackCanGoForward()) {
    let forwardText = '';
    if (stackTrackersBlockedForward() > 0) {
      forwardText = /*#__PURE__*/react.createElement("div", {
        className: "forwardTrackers"
      }, stackTrackersBlockedForward());
    }
    stackForwardButton = /*#__PURE__*/react.createElement("label", {
      style: {
        float: 'right'
      }
    }, forwardText, /*#__PURE__*/react.createElement("button", {
      id: "stackForward",
      className: "forward",
      style: {
        top: navigationButtonsTop
      },
      onClick: onStackGoForward
    }));
  }
  let websiteMaxWidth = websiteExtendedWidth;
  if (stackCanGoBack() || stackCanGoForward()) {
    websiteMaxWidth = websiteReducedWidth;
  }
  return /*#__PURE__*/react.createElement("div", {
    className: "website-navigation"
  }, stackBackButton, /*#__PURE__*/react.createElement("div", {
    className: "website",
    title: hostname,
    style: {
      maxWidth: websiteMaxWidth
    }
  }, hostname), stackForwardButton);
});
// EXTERNAL MODULE: ./node_modules/validator/lib/isURL.js
var isURL = __webpack_require__(844);
var isURL_default = /*#__PURE__*/__webpack_require__.n(isURL);
;// ./src/utils/anims.js

class Pie {
  constructor() {
    this.canvas = null;
    this.tooltip = null;
    this.ctx = null;
    this.colors = ["#815dc4", "#1cb2a4", "#269ac8", "#b35ca1", "#60aec5", "#e67e17"];
    this.x = 0;
    this.y = 0;
    this.r = 0;
    this.lw = 10;
    this.angles = [];
    this.nrBlockedTrackers = 0;
  }
  init() {
    this.canvas = document.getElementById("pie");
    this.tooltip = document.getElementById("pie-tooltip");
    this.ctx = this.canvas.getContext("2d");
    this.ctx.lineWidth = this.lw;
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.x = this.canvas.width / 2;
    this.y = this.x;
    this.r = this.x - this.lw / 2 - 0.1;
    this.setMouse();
  }
  clear() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
  }
  update(trackers) {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    var totalTrackers = trackers.reduce((a, b) => a + b);
    this.nrBlockedTrackers = totalTrackers;
    var parts = trackers.length;
    var start = 0;
    var grad = 0;
    document.getElementById("pieCount").firstChild.nodeValue = getTrackerPieCountText(totalTrackers);
    for (var i = 0; i < parts; i++) {
      this.ctx.beginPath();
      this.ctx.strokeStyle = this.colors[i];
      grad = Math.PI * 2 * trackers[i] / totalTrackers;
      this.ctx.arc(this.x, this.y, this.r, start, start + grad);
      this.ctx.stroke();
      this.angles.push([start, start + grad, i]);
      start += grad;
    }
  }
  mouseEnterEvent() {
    this.showTooltip();
  }
  mouseLeaveEvent() {
    this.hideTooltip();
  }
  mouseMoveEvent(evt) {
    var distance = 0;
    var angle = 0;
    var dx = evt.offsetX - this.x;
    var dy = -(evt.offsetY - this.x);
    this.tooltip.style.left = evt.offsetX - 40 + "px";
    this.tooltip.style.top = evt.offsetY + 10 + "px";
    if (0 === this.angles.length) {
      return;
    }
    angle = Math.atan2(dy, dx);
    if (angle < 0) {
      angle += Math.PI * 2;
    }
    angle = 2 * Math.PI - angle;
    let current = this.angles.filter(function (item) {
      if (item[0] <= angle && angle <= item[1]) {
        return true;
      }
      return false;
    });
    if (null != current && current.length > 0) {
      current = current[0][2];
      let label = document.querySelectorAll(".tooltip-labels div.show")[0];
      if (label) {
        label.classList.remove("show");
      }
      label = document.querySelectorAll(".tooltip-labels div").item(current);
      label.classList.add("show");
      distance = Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2));
      if (distance < this.x - this.lw || distance > this.x + this.lw) {
        this.hideTooltip();
      } else {
        this.showTooltip();
      }
    }
  }
  setMouse() {
    this.canvas.addEventListener("mouseenter", this.mouseEnterEvent.bind(this));
    this.canvas.addEventListener("mouseleave", this.mouseLeaveEvent.bind(this));
    this.canvas.addEventListener("mousemove", this.mouseMoveEvent.bind(this));
  }
  hideTooltip() {
    this.tooltip.style.display = "none";
  }
  showTooltip() {
    if (this.nrBlockedTrackers > 0) {
      this.tooltip.style.display = "block";
    }
  }
}
;
class PageLoad {
  constructor() {
    this.canvas = null;
    this.ctx = null;
    this.lw = 8;
    this.x = 0;
    this.y = 0;
    this.r = 0;
  }
  init() {
    this.canvas = document.getElementById("pageSpeed");
    this.ctx = this.canvas.getContext("2d");
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.x = this.canvas.width / 2;
    this.r = this.x - this.lw / 2 - 0.1;
  }
  clear() {
    indicator.style.transform = "rotate(0deg)";
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
  }
  update(val) {
    var gradient;
    var grad;
    var offset = 0.08;
    var start = Math.PI;
    var rotation = val / 100 * 182 - 91;
    var indicator = document.getElementById("indicator");
    indicator.style.transform = "rotate(" + rotation + "deg)";
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.ctx.beginPath();
    this.ctx.lineWidth = this.lw;
    grad = Math.PI * 2 * val / 100.0 / 2 - start;
    if (val < 35) {
      gradient = this.ctx.createLinearGradient(0, 40, 20, 0);
      gradient.addColorStop(0, "#d90016");
      gradient.addColorStop(1, "#e15765");
      this.ctx.strokeStyle = gradient;
    } else if (val >= 35 && val < 55) {
      gradient = this.ctx.createLinearGradient(0, 40, 50, 0);
      gradient.addColorStop(0, "#ff9933");
      gradient.addColorStop(1, "#f7d360");
      this.ctx.strokeStyle = gradient;
    } else {
      gradient = this.ctx.createLinearGradient(0, 40, 80, 40);
      gradient.addColorStop(0, "#1f991f");
      gradient.addColorStop(1, "#42c942");
      this.ctx.strokeStyle = gradient;
    }
    this.ctx.arc(this.x, this.x, this.r, start - offset, grad);
    this.ctx.stroke();
    this.ctx.beginPath();
    this.ctx.strokeStyle = "#cccccc";
    this.ctx.arc(this.x, this.x, this.r, grad, 0 + offset);
    this.ctx.stroke();
  }
}
;
class PageTooltip {
  constructor() {}
  init() {
    var targets = document.querySelectorAll(".tooltip-target");
    targets.forEach(function (elem) {
      var tooltip = elem.querySelector(".info-tooltip");
      if (null != tooltip) {
        elem.addEventListener("mouseover", function () {
          var br = elem.getBoundingClientRect();
          if (br.left > 240) {
            tooltip.classList.add("left");
          } else {
            tooltip.classList.remove("left");
          }
        });
      }
    });
  }
}
;

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
;// ./src/ui/home.js














class Home extends react.Component {
  constructor(props) {
    super(props);
    this.state = {
      tabId: props.currentTab.id,
      hostname: utils_parseUrl(props.currentTab.url).hostname,
      featureStatus: props.featureStatus,
      enabled: props.enabled,
      categories: props.categories,
      specialOffers: props.specialOffers,
      stackIndex: 0,
      tabStack: [],
      pageLoad: 0,
      trackersBlocked: 0,
      trackersMap: {},
      trackersUrls: [],
      whitelist: props.whitelist,
      isUpdate: false
    };
    this.currentScreen = SCREEN_UI.MAIN;
    this.pie = new Pie();
    this.pageLoad = new PageLoad();
    this.pageTooltip = new PageTooltip();
    this.sessionWhitelist = [];
    this.categoryKey = 0;
    this.featureStatus = this.state.featureStatus;
    this.extensionEnabled = this.state.enabled;
    this.extensionSpecialOffers = this.state.specialOffers;
    this.inputWhitelistUrlRef = /*#__PURE__*/react.createRef();
    this.whitelistUrlErrorRef = /*#__PURE__*/react.createRef();
    this.categoryExpandRef = /*#__PURE__*/react.createRef();
    this.dnrBadgeMessage = '';
    log.init('popup');
    if (props.rulesMatchedDetails) {
      this.onDnrMatchedRules(props.rulesMatchedDetails);
    }
    chrome.runtime.onMessage.addListener(this.onBackgroundMessage);
    chrome.runtime.sendMessage({
      type: 'get_current_tab_stack',
      tabId: this.props.currentTab.id,
      tabUrl: props.currentTab.url
    }, response => {
      if (response) {
        this.sessionWhitelist = response.sessionWhitelist;
        if (undefined !== response.langMap && null != response.langMap) {
          locale_lang.init(new Map(JSON.parse(response.langMap)));
        }
        let tabInfo = response.tabStack[0];
        if (canBlockWebRequest()) {
          this.setState({
            hostname: tabInfo.url,
            stackIndex: 0,
            tabStack: response.tabStack,
            pageLoad: tabInfo.pageLoad,
            trackersBlocked: tabInfo.trackersBlocked,
            trackersMap: tabInfo.trackersMap,
            trackersUrls: tabInfo.trackersUrls,
            isUpdate: tabInfo.isUpdate
          });
        } else {
          this.setState({
            pageLoad: tabInfo.pageLoad,
            trackersUrls: tabInfo.trackersUrls,
            isUpdate: tabInfo.isUpdate
          });
        }
      }
    });
    log.trace('ctor');
  }
  componentDidMount() {
    log.trace('componentDidMount');
    if (null != this.pie) {
      this.pie.init();
    }
    if (null != this.pageLoad) {
      this.pageLoad.init();
    }
    if (null != this.pageTooltip) {
      this.pageTooltip.init();
    }
  }
  componentDidUpdate() {
    log.trace('componentDidUpdate');
    if (this.state.trackersBlocked === 0) {
      if (null != this.pie) {
        this.pie.clear();
      }
    }
    if (this.state.pageLoad === 0) {
      if (null != this.pageLoad) {
        this.pageLoad.clear();
      }
    }
  }
  getProtectionStatusClassName = () => {
    if (this.extensionEnabled) {
      if (undefined !== this.sessionWhitelist && this.sessionWhitelist.includes(this.state.hostname)) {
        return 'main-screen disabled-protection';
      } else {
        return 'main-screen';
      }
    } else {
      return 'main-screen disabled-shadow';
    }
  };
  trackersMapIsEmpty = () => {
    if (undefined === this.state.trackersMap || 0 === this.state.trackersMap.size) {
      return true;
    }
    if (0 === Object.keys(this.state.trackersMap).length) {
      return true;
    }
    return false;
  };
  updatePageLoad = () => {
    if (null != this.pageLoad && this.state.pageLoad > 0) {
      if (this.state.pageLoad <= 1) {
        this.pageLoad.update(100); // val 0 - 100
      } else if (this.state.pageLoad <= 2) {
        this.pageLoad.update(90);
      } else if (this.state.pageLoad <= 3) {
        this.pageLoad.update(70);
      } else if (this.state.pageLoad <= 4) {
        this.pageLoad.update(50);
      } else if (this.state.pageLoad <= 5) {
        this.pageLoad.update(40);
      } else if (this.state.pageLoad <= 6) {
        this.pageLoad.update(30);
      } else if (this.state.pageLoad <= 7) {
        this.pageLoad.update(20);
      } else if (this.state.pageLoad <= 8) {
        this.pageLoad.update(10);
      } else if (this.state.pageLoad <= 9) {
        this.pageLoad.update(5);
      } else if (this.state.pageLoad <= 10) {
        this.pageLoad.update(2.5);
      } else {
        this.pageLoad.update(0);
      }
    }
  };
  updatePieTooltips = () => {
    this.updatePageLoad();
    if (!this.trackersMapIsEmpty()) {
      let categoriesNrTrackers = [0, 0, 0, 0, 0, 0];
      const keys = Object.keys(this.state.trackersMap);
      for (const key of keys) {
        let index = -1;
        switch (key) {
          case '1':
            //ads
            {
              index = 0;
              break;
            }
          case '2':
            //analytics
            {
              index = 3;
              break;
            }
          case '4':
            //customer interaction
            {
              index = 1;
              break;
            }
          case '8':
            //social media
            {
              index = 4;
              break;
            }
          case '16':
            //essentials
            {
              index = 2;
              break;
            }
          case '32':
            //cookies
            {
              index = 5;
              break;
            }
        }
        if (-1 != index) {
          categoriesNrTrackers[index] = this.state.trackersMap[key].length;
        }
      }
      if (null != this.pie) {
        this.pie.update(categoriesNrTrackers);
      }
    }
    return null;
  };
  onCategoryListItemClick = event => {
    this.categoryKey = event.currentTarget.dataset.id;
    this.currentScreen = SCREEN_UI.CATEGORY;
    this.setState({
      state: this.state
    });
  };
  onClickSettings = event => {
    this.currentScreen = SCREEN_UI.SETTINGS;
    this.setState({
      state: this.state
    });
  };
  onClickBack = () => {
    this.currentScreen = SCREEN_UI.MAIN;
    this.setState({
      state: this.state
    });
  };
  onClickCategoryLink = () => {
    if ('dashboard expand' === this.categoryExpandRef.current.className) {
      this.categoryExpandRef.current.className = 'dashboard';
    } else {
      this.categoryExpandRef.current.className = 'dashboard expand';
    }
  };
  showTrackersList = () => {
    let listItems = [];
    const keys = ['1', '2', '4', '8', '16', '32'];
    for (const key of keys) {
      let categoryInfo = getTrackerCategoryName(locale_lang, key);
      let nrTracks = 0;
      if (undefined !== this.state.trackersMap && 0 !== Object.keys(this.state.trackersMap).length) {
        if (null != this.state.trackersMap[key]) {
          nrTracks = this.state.trackersMap[key].length;
        }
      }
      let nrTrackersBlocked = nrTracks + ' ' + locale_lang.getString("str");
      listItems.push(/*#__PURE__*/react.createElement("li", {
        className: categoryInfo.icon,
        key: key,
        "data-id": key,
        onClick: this.onCategoryListItemClick
      }, /*#__PURE__*/react.createElement("div", {
        className: "title with-tooltip"
      }, /*#__PURE__*/react.createElement("span", null, categoryInfo.name), /*#__PURE__*/react.createElement("div", {
        className: "tooltip-target"
      }, /*#__PURE__*/react.createElement("div", {
        className: "info-tooltip up"
      }, /*#__PURE__*/react.createElement("div", null, getTrackerCategoryTooltip(locale_lang, key))))), /*#__PURE__*/react.createElement("div", {
        className: "trackers"
      }, nrTrackersBlocked)));
    }
    return listItems;
  };
  enableSwitchWasChanged = () => {
    this.extensionEnabled = !this.state.enabled;
    this.setState(prevState => ({
      enabled: !prevState.enabled
    }), this.stateWasUpdatedFromUI);
  };
  specialOffersSwitchWasChanged = () => {
    this.extensionSpecialOffers = !this.state.specialOffers;
    this.setState({
      specialOffers: this.extensionSpecialOffers
    }, () => {
      chrome.storage.local.set(this.state);
      chrome.runtime.sendMessage({
        type: 'special_offers',
        specialOffers: this.state.specialOffers
      });
    });
  };
  categoryStatusChanged = event => {
    log.info('categoryStatusChanged: ' + event.target.checked);
    let newCategories = 0;
    if (true === event.target.checked) {
      newCategories = this.state.categories & ~this.categoryKey;
    } else {
      newCategories = this.state.categories | this.categoryKey;
    }
    this.setState({
      categories: newCategories
    }, this.stateWasUpdatedFromUI);
    log.info("categories: " + newCategories);
  };
  addUrlToWhitelist = (event, isCurrentUrl) => {
    log.info('addWhiteListUrl: ' + isCurrentUrl);
    const textFieldError = 'text-field error';
    let whitelistUrl = null;
    if (isCurrentUrl) {
      whitelistUrl = this.state.hostname;
    } else {
      whitelistUrl = this.inputWhitelistUrlRef.current.value;
    }
    log.info('url: ' + whitelistUrl);
    if (null === whitelistUrl || 0 === whitelistUrl.length) {
      this.whitelistUrlErrorRef.current.textContent = locale_lang.getString('url_is_empty');
      this.inputWhitelistUrlRef.current.className = textFieldError;
      return;
    }
    let currentUrl = whitelistUrl;
    if (!/^https?:/i.test(whitelistUrl)) {
      currentUrl = 'https://' + whitelistUrl;
    }
    if (!isURL_default()(currentUrl)) {
      this.whitelistUrlErrorRef.current.textContent = locale_lang.getString('url_not_valid');
      this.inputWhitelistUrlRef.current.className = textFieldError;
      return;
    }
    whitelistUrl = utils_parseUrl(currentUrl).hostname;
    log.info("url: " + currentUrl);
    log.info("whitelistUrl: " + whitelistUrl);
    if (whitelistUrl.startsWith("www.")) {
      whitelistUrl = whitelistUrl.substring(4);
    }
    let reg = new RegExp('[\.]([^$.?#]+)');
    if (!reg.test(whitelistUrl)) {
      this.whitelistUrlErrorRef.current.textContent = locale_lang.getString('url_not_valid');
      this.inputWhitelistUrlRef.current.className = textFieldError;
      return;
    }
    if (this.state.whitelist.includes(whitelistUrl)) {
      this.whitelistUrlErrorRef.current.textContent = locale_lang.getString('url_already_exists');
      this.inputWhitelistUrlRef.current.className = textFieldError;
      return;
    }
    this.setState({
      whitelist: this.state.whitelist.concat(whitelistUrl)
    }, () => {
      chrome.storage.local.set(this.state);
      chrome.runtime.sendMessage({
        type: 'whitelist_changed',
        whitelist: this.state.whitelist,
        whitelist_add: whitelistUrl
      });
      log.info('whitelist (add):' + this.state.whitelist);
    });
    this.inputWhitelistUrlRef.current.value = '';
    this.inputWhitelistUrlRef.current.className = 'text-field';
  };
  deleteUrlFromWhitelist = (event, url) => {
    log.info('deleteUrlFromWhitelist: ' + url);
    if (null === url || 0 === url.length) {
      return;
    }
    this.setState({
      whitelist: this.state.whitelist.filter(site => site !== url)
    }, () => {
      chrome.storage.local.set(this.state);
      chrome.runtime.sendMessage({
        type: 'whitelist_changed',
        whitelist: this.state.whitelist,
        whitelist_remove: url
      });
      log.info('whitelist (delete):' + this.state.whitelist);
    });
  };
  siteWasDisabled = () => {
    log.info('siteWasDisabled');
    if (!this.sessionWhitelist.includes(this.state.hostname)) {
      this.sessionWhitelist = this.sessionWhitelist.concat(this.state.hostname);
    }
    chrome.runtime.sendMessage({
      type: 'sessionWhitelist_changed',
      sessionWhitelist: this.sessionWhitelist,
      disabled: true,
      url: this.state.hostname
    });
    this.setState({
      state: this.state.enabled
    });
  };
  siteWasEnabled = () => {
    log.info('siteWasEnabled');
    this.sessionWhitelist = this.sessionWhitelist.filter(site => site !== this.state.hostname);
    chrome.runtime.sendMessage({
      type: 'sessionWhitelist_changed',
      sessionWhitelist: this.sessionWhitelist,
      disabled: false
    });
    this.setState({
      state: this.state.enabled
    });
  };

  /**
   * Sync every UI state change with local storage and background process.
   */
  stateWasUpdatedFromUI = () => {
    chrome.storage.local.set(this.state);
    chrome.runtime.sendMessage({
      type: 'new_state',
      state: this.state
    });
  };
  dnrUpdateMatchedRules = () => {
    if (scripts_compat.dnr.available) {
      getBadgeMessage(this.props.currentTab.id, text => {
        if (text !== this.dnrBadgeMessage) {
          this.dnrBadgeMessage = text;
          log.warn('[dnr] v3 query dnr rule matching data for new stats: ' + this.dnrBadgeMessage);
          scripts_compat.dnr.declarativeNetRequest.getMatchedRules({
            tabId: this.props.currentTab.id
          }, this.onDnrMatchedRules.bind(this));
        } else {
          log.warn('[dnr] v3 skip dnr rule matching query due to same badge action count');
        }
      });
    }
  };
  onDnrMatchedRules = rulesMatchedDetails => {
    if (!rulesMatchedDetails) {
      return;
    }
    log.warn('[dnr] onDnrMatchedRules: ' + JSON.stringify(rulesMatchedDetails, null, 4));
    if (!canBlockWebRequest()) {
      if (rulesMatchedDetails.rulesMatchedInfo.length > 0) {
        const trackersUrl = chrome.runtime.getURL('tracking/trackers.json');
        fetch(trackersUrl).then(response => response.json()) //assuming file contains json
        .then(json => {
          let trackersBlocked = 0;
          let trackersMap = {};
          trackersMap[(tracking_default()).categories.ADS] = [];
          trackersMap[(tracking_default()).categories.SITE_ANALYTICS] = [];
          trackersMap[(tracking_default()).categories.CUSTOMER_INTERACTION] = [];
          trackersMap[(tracking_default()).categories.SOCIAL_MEDIA] = [];
          trackersMap[(tracking_default()).categories.ESSENTIAL] = [];
          trackersMap[(tracking_default()).categories.COOKIE] = [];
          let domainCookies = tracking_default().getDomainCookies();
          rulesMatchedDetails.rulesMatchedInfo.forEach(match => {
            if (match.tabId !== this.state.tabId) {
              return;
            }
            let rule = match.rule;
            if (json.hasOwnProperty(rule.rulesetId)) {
              let rulesetTrackers = json[rule.rulesetId];
              let rulesetInnerId = rule.ruleId % 10000;
              if (rulesetInnerId > 0 && rulesetTrackers.length > rulesetInnerId) {
                let ruleExpr = rulesetTrackers[rulesetInnerId - 1];
                log.warn('[dnr] onDnrMatchedRules match: ' + '[' + rule.rulesetId + '][' + rulesetInnerId + '][' + ruleExpr + ']' + JSON.stringify(rule, null, 4));
                let rulesetCategId = tracking_default().categoryStringToId(rule.rulesetId);
                if (rulesetCategId != (tracking_default()).categories.UNKNOWN) {
                  trackersBlocked++;
                  trackersMap[rulesetCategId].push(ruleExpr);
                }
              }
            } else {
              if (rule.rulesetId === (tracking_default()).rulesets.domain_cookies) {
                let rulesetInnerId = rule.ruleId % 10000;
                if (rulesetInnerId > 0 && domainCookies.length > rulesetInnerId) {
                  let ruleDomain = domainCookies[rulesetInnerId - 1];
                  log.warn('[dnr] onDnrMatchedRules match: ' + '[' + rule.rulesetId + '][' + rulesetInnerId + '][' + ruleDomain + ']' + JSON.stringify(rule, null, 4));
                  trackersBlocked++;
                  trackersMap[(tracking_default()).categories.COOKIE].push(ruleDomain);
                }
              }
            }
          });
          log.warn('[dnr] onDnrMatchedRules trackersMap: ' + JSON.stringify(trackersMap, null, 4));
          if (trackersBlocked > 0) {
            let newState = {
              trackersBlocked: trackersBlocked,
              trackersMap: trackersMap
            };
            getBadgeMessage(this.props.currentTab.id, text => {
              if (text !== this.dnrBadgeMessage) {
                this.dnrBadgeMessage = text;
                log.warn('[dnr] v3 update dnr rule matching data with new stats: ' + this.dnrBadgeMessage);
              }
            });
            log.warn('[dnr] onDnrMatchedRules newState: ' + JSON.stringify(newState, null, 4));
            this.setState(newState);
          }
        });
      }
    }
  };

  /**
  * Receive messages from background process and update UI.
  */
  onBackgroundMessage = (request, sender, sendResponse) => {
    log.info('onBackgroundMessage: ' + request.type);
    switch (request.type) {
      case 'update_tab_stack':
        {
          this.sessionWhitelist = request.sessionWhitelist;
          if (undefined !== request.tabStack) {
            let tabInfo = request.tabStack[0];
            if (undefined !== tabInfo) {
              this.setState({
                hostname: tabInfo.url,
                stackIndex: 0,
                tabStack: request.tabStack,
                pageLoad: tabInfo.pageLoad,
                trackersBlocked: tabInfo.trackersBlocked,
                trackersMap: tabInfo.trackersMap,
                trackersUrls: tabInfo.trackersUrls
              });
            }
          }
          break;
        }
      case 'update_page_load':
        {
          if (undefined !== request.tabStack) {
            let tabInfo = request.tabStack[0];
            if (undefined !== tabInfo) {
              this.setState({
                pageLoad: tabInfo.pageLoad
              }, () => {
                this.dnrUpdateMatchedRules();
              });
            }
          }
          break;
        }
      case 'new_state':
        {
          this.extensionEnabled = request.state;
          this.setState({
            enabled: request.state
          });
          break;
        }
      case 'set_settings':
        {
          this.extensionEnabled = request.enabled;
          this.setState({
            featureStatus: request.featureStatus,
            enabled: request.enabled,
            categories: request.categories
          });
          break;
        }
      case 'set_module_status':
        {
          this.extensionEnabled = request.enabled;
          this.setState({
            featureStatus: request.featureStatus,
            enabled: request.enabled
          });
          break;
        }
      case 'whitelist_add':
        {
          let url = request.url;
          if (!this.state.whitelist.includes(url)) {
            log.info('add url to whitelist: ' + url);
            this.setState({
              whitelist: this.state.whitelist.concat(url)
            });
          }
          break;
        }
      case 'whitelist_remove':
        {
          let url = request.url;
          if (this.state.whitelist.includes(url)) {
            log.info('remove url from whitelist: ' + url);
            this.setState({
              whitelist: this.state.whitelist.filter(site => site !== url)
            });
          }
          break;
        }
      case 'set_whitelist':
        {
          let whitelist = request.whitelist;
          if (Array.isArray(whitelist)) {
            log.info('set new whitelist: ' + whitelist);
            this.setState({
              whitelist: whitelist.slice(0)
            });
          }
          break;
        }
      default:
        {
          break;
        }
    }
  };
  onStackGoIndex = index => {
    if (index >= 0 && index <= this.state.tabStack.length - 1) {
      let tabInfo = this.state.tabStack[index];
      this.setState({
        hostname: tabInfo.url,
        stackIndex: index,
        pageLoad: tabInfo.pageLoad,
        trackersBlocked: tabInfo.trackersBlocked,
        trackersMap: tabInfo.trackersMap,
        trackersUrls: tabInfo.trackersUrls
      });
    }
  };
  render() {
    if (this.state.isUpdate) {
      return /*#__PURE__*/react.createElement("div", {
        className: "main-ui"
      }, /*#__PURE__*/react.createElement("header", null, /*#__PURE__*/react.createElement("div", {
        className: "title"
      }, locale_lang.getString("app_name"))), /*#__PURE__*/react.createElement("div", {
        className: "center"
      }, /*#__PURE__*/react.createElement("h2", null, locale_lang.getString("update_in_progress"))));
    }
    return /*#__PURE__*/react.createElement("div", {
      className: "main-ui"
    }, /*#__PURE__*/react.createElement("header", null, /*#__PURE__*/react.createElement("div", {
      className: "title"
    }, locale_lang.getString("app_name")), /*#__PURE__*/react.createElement(DebuggingUtils_Home, null), /*#__PURE__*/react.createElement("button", {
      className: "settings",
      onClick: this.onClickSettings
    })), /*#__PURE__*/react.createElement("div", {
      className: this.getProtectionStatusClassName()
    }, /*#__PURE__*/react.createElement("div", {
      className: "dashboard"
    }, /*#__PURE__*/react.createElement("div", {
      className: "total-trackers",
      hidden: true
    }, /*#__PURE__*/react.createElement("strong", null, "252"), " ", /*#__PURE__*/react.createElement("span", null, locale_lang.getString("browser_session_blocked"))), /*#__PURE__*/react.createElement(StackNavigation, {
      hostname: this.state.hostname,
      tabStack: this.state.tabStack,
      stackIndex: this.state.stackIndex,
      onStackGoIndex: this.onStackGoIndex
    }), /*#__PURE__*/react.createElement("div", {
      className: "gauges-container"
    }, /*#__PURE__*/react.createElement("div", {
      className: "pie-wprap"
    }, /*#__PURE__*/react.createElement("canvas", {
      className: "trackers-pie",
      id: "pie",
      width: "110",
      height: "110"
    }), /*#__PURE__*/react.createElement("div", {
      className: "count",
      id: "pieCount"
    }, getTrackerPieCountText(this.state.trackersBlocked)), /*#__PURE__*/react.createElement("div", {
      className: "label"
    }, locale_lang.getString("trackers_blocked")), /*#__PURE__*/react.createElement("div", {
      className: "info-tooltip",
      id: "pie-tooltip"
    }, /*#__PURE__*/react.createElement("div", {
      className: "tooltip-labels"
    }, this.updatePieTooltips(), /*#__PURE__*/react.createElement("div", null, locale_lang.getString("advertising_trackers_tooltip")), /*#__PURE__*/react.createElement("div", null, locale_lang.getString("interaction_trackers_tooltip")), /*#__PURE__*/react.createElement("div", null, locale_lang.getString("essentials_trackers_tooltip")), /*#__PURE__*/react.createElement("div", null, locale_lang.getString("analytics_trackers_tooltip")), /*#__PURE__*/react.createElement("div", null, locale_lang.getString("social_trackers_tooltip")), /*#__PURE__*/react.createElement("div", null, locale_lang.getString("cookies_trackers_tooltip"))))), /*#__PURE__*/react.createElement("div", null, /*#__PURE__*/react.createElement("div", {
      className: "load-gauge"
    }, /*#__PURE__*/react.createElement("canvas", {
      id: "pageSpeed",
      width: "88",
      height: "88"
    }), /*#__PURE__*/react.createElement("div", {
      className: "indicator",
      id: "indicator"
    }), /*#__PURE__*/react.createElement("div", {
      className: "speed"
    }, /*#__PURE__*/react.createElement("span", null, this.state.pageLoad), /*#__PURE__*/react.createElement("span", null, locale_lang.getString("seconds")))), /*#__PURE__*/react.createElement("div", {
      className: "label"
    }, locale_lang.getString("page_load")))), /*#__PURE__*/react.createElement(DisableButton, {
      sessionWhitelist: this.sessionWhitelist,
      currentUrl: this.state.hostname,
      onSiteDisable: this.siteWasDisabled,
      onSiteEnable: this.siteWasEnabled,
      bdLang: locale_lang
    })), /*#__PURE__*/react.createElement("ul", {
      className: "trackers-list"
    }, this.showTrackersList())), /*#__PURE__*/react.createElement(TrackersCategory, {
      currentScreen: this.currentScreen,
      currentCategoryKey: this.categoryKey,
      categoryExpandRef: this.categoryExpandRef,
      categories: this.state.categories,
      trackersMap: this.state.trackersMap,
      trackersUrls: this.state.trackersUrls,
      categoryStatusChanged: this.categoryStatusChanged,
      onClickCategoryLink: this.onClickCategoryLink,
      onClickBack: this.onClickBack,
      bdLang: locale_lang
    }), /*#__PURE__*/react.createElement(TrackersSettings, {
      currentScreen: this.currentScreen,
      featureStatus: this.featureStatus,
      extensionEnabled: this.extensionEnabled,
      enableSwitchWasChanged: this.enableSwitchWasChanged,
      extensionSpecialOffers: this.extensionSpecialOffers,
      specialOffersSwitchWasChanged: this.specialOffersSwitchWasChanged,
      whitelist: this.state.whitelist,
      inputWhitelistUrlRef: this.inputWhitelistUrlRef,
      whitelistUrlErrorRef: this.whitelistUrlErrorRef,
      onClickBack: this.onClickBack,
      addUrlToWhitelist: this.addUrlToWhitelist,
      deleteUrlFromWhitelist: this.deleteUrlFromWhitelist,
      bdLang: locale_lang
    }));
  }
}
// EXTERNAL MODULE: ./node_modules/react-dom/client.js
var client = __webpack_require__(338);
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
;// ./node_modules/@sentry/core/build/esm/debug-build.js
const debug_build_DEBUG_BUILD = (typeof __SENTRY_DEBUG__ === 'undefined' || __SENTRY_DEBUG__);


//# sourceMappingURL=debug-build.js.map

;// ./node_modules/@sentry/core/build/esm/utils/version.js
const SDK_VERSION = "10.70.0" ;


//# sourceMappingURL=version.js.map

;// ./node_modules/@sentry/core/build/esm/utils/worldwide.js
const worldwide_GLOBAL_OBJ = globalThis;


//# sourceMappingURL=worldwide.js.map

;// ./node_modules/@sentry/core/build/esm/carrier.js



function carrier_getMainCarrier() {
  carrier_getSentryCarrier(worldwide_GLOBAL_OBJ);
  return worldwide_GLOBAL_OBJ;
}
function carrier_getSentryCarrier(carrier) {
  const __SENTRY__ = carrier.__SENTRY__ = carrier.__SENTRY__ || {};
  __SENTRY__.version = __SENTRY__.version || SDK_VERSION;
  return __SENTRY__[SDK_VERSION] = __SENTRY__[SDK_VERSION] || {};
}
function getGlobalSingleton(name, creator, obj = worldwide_GLOBAL_OBJ) {
  const __SENTRY__ = obj.__SENTRY__ = obj.__SENTRY__ || {};
  const carrier = __SENTRY__[SDK_VERSION] = __SENTRY__[SDK_VERSION] || {};
  return carrier[name] || (carrier[name] = creator());
}


//# sourceMappingURL=carrier.js.map

;// ./node_modules/@sentry/core/build/esm/utils/debug-logger.js




const CONSOLE_LEVELS = [
  "debug",
  "info",
  "warn",
  "error",
  "log",
  "assert",
  "trace"
];
const PREFIX = "Sentry Logger ";
const originalConsoleMethods = {};
function debug_logger_consoleSandbox(callback) {
  if (!("console" in worldwide_GLOBAL_OBJ)) {
    return callback();
  }
  const console = worldwide_GLOBAL_OBJ.console;
  const wrappedFuncs = {};
  const wrappedLevels = Object.keys(originalConsoleMethods);
  wrappedLevels.forEach((level) => {
    const originalConsoleMethod = originalConsoleMethods[level];
    wrappedFuncs[level] = console[level];
    console[level] = originalConsoleMethod;
  });
  try {
    return callback();
  } finally {
    wrappedLevels.forEach((level) => {
      console[level] = wrappedFuncs[level];
    });
  }
}
function enable() {
  _getLoggerSettings().enabled = true;
}
function disable() {
  _getLoggerSettings().enabled = false;
}
function isEnabled() {
  return _getLoggerSettings().enabled;
}
function debug_logger_log(...args) {
  _maybeLog("log", ...args);
}
function warn(...args) {
  _maybeLog("warn", ...args);
}
function error(...args) {
  _maybeLog("error", ...args);
}
function _maybeLog(level, ...args) {
  if (!debug_build_DEBUG_BUILD) {
    return;
  }
  if (isEnabled()) {
    debug_logger_consoleSandbox(() => {
      worldwide_GLOBAL_OBJ.console[level](`${PREFIX}[${level}]:`, ...args);
    });
  }
}
function _getLoggerSettings() {
  if (!debug_build_DEBUG_BUILD) {
    return { enabled: false };
  }
  return getGlobalSingleton("loggerSettings", () => ({ enabled: false }));
}
const debug_logger_debug = {
  /** Enable logging. */
  enable,
  /** Disable logging. */
  disable,
  /** Check if logging is enabled. */
  isEnabled,
  /** Log a message. */
  log: debug_logger_log,
  /** Log a warning. */
  warn,
  /** Log an error. */
  error
};


//# sourceMappingURL=debug-logger.js.map

;// ./node_modules/@sentry/core/build/esm/integration.js




const installedIntegrations = [];
function filterDuplicates(integrations) {
  const integrationsByName = {};
  integrations.forEach((currentInstance) => {
    const { name } = currentInstance;
    const existingInstance = integrationsByName[name];
    if (existingInstance && !existingInstance.isDefaultInstance && currentInstance.isDefaultInstance) {
      return;
    }
    integrationsByName[name] = currentInstance;
  });
  return Object.values(integrationsByName);
}
function getIntegrationsToSetup(options) {
  const defaultIntegrations = options.defaultIntegrations || [];
  const userIntegrations = options.integrations;
  defaultIntegrations.forEach((integration) => {
    integration.isDefaultInstance = true;
  });
  let integrations;
  if (Array.isArray(userIntegrations)) {
    integrations = [...defaultIntegrations, ...userIntegrations];
  } else if (typeof userIntegrations === "function") {
    const resolvedUserIntegrations = userIntegrations(defaultIntegrations);
    integrations = Array.isArray(resolvedUserIntegrations) ? resolvedUserIntegrations : [resolvedUserIntegrations];
  } else {
    integrations = defaultIntegrations;
  }
  return filterDuplicates(integrations);
}
function setupIntegrations(client, integrations) {
  const integrationIndex = {};
  integrations.forEach((integration) => {
    if (integration?.beforeSetup) {
      integration.beforeSetup(client);
    }
  });
  integrations.forEach((integration) => {
    if (integration) {
      setupIntegration(client, integration, integrationIndex);
    }
  });
  return integrationIndex;
}
function afterSetupIntegrations(client, integrations) {
  for (const integration of integrations) {
    if (integration?.afterAllSetup) {
      integration.afterAllSetup(client);
    }
  }
}
function setupIntegration(client, integration, integrationIndex) {
  if (integrationIndex[integration.name]) {
    debug_build_DEBUG_BUILD && debug_logger_debug.log(`Integration skipped because it was already installed: ${integration.name}`);
    return;
  }
  integrationIndex[integration.name] = integration;
  if (!installedIntegrations.includes(integration.name) && typeof integration.setupOnce === "function") {
    integration.setupOnce();
    installedIntegrations.push(integration.name);
  }
  if (integration.setup && typeof integration.setup === "function") {
    integration.setup(client);
  }
  if (typeof integration.preprocessEvent === "function") {
    const callback = integration.preprocessEvent.bind(integration);
    client.on("preprocessEvent", (event, hint) => callback(event, hint, client));
  }
  if (typeof integration.processEvent === "function") {
    const callback = integration.processEvent.bind(integration);
    const processor = Object.assign((event, hint) => callback(event, hint, client), {
      id: integration.name
    });
    client.addEventProcessor(processor);
  }
  ["processSpan", "processSegmentSpan"].forEach((hook) => {
    const callback = integration[hook];
    if (typeof callback === "function") {
      client.on(hook, (span) => callback.call(integration, span, client));
    }
  });
  debug_build_DEBUG_BUILD && debug_logger_debug.log(`Integration installed: ${integration.name}`);
}
function addIntegration(integration) {
  const client = getClient();
  if (!client) {
    DEBUG_BUILD && debug.warn(`Cannot add integration "${integration.name}" because no SDK Client is available.`);
    return;
  }
  client.addIntegration(integration);
}
function defineIntegration(fn) {
  return fn;
}
function extendIntegration(integration, extendedIntegration) {
  const wrappedIntegration = {
    ...integration,
    ...extendedIntegration
  };
  for (const key in extendedIntegration) {
    const baseValue = integration[key];
    const extendedValue = extendedIntegration[key];
    if (typeof baseValue === "function" && typeof extendedValue === "function") {
      const wrappedFunction = new Proxy(baseValue, {
        apply: (target, thisArg, args) => {
          Reflect.apply(target, thisArg, args);
          return Reflect.apply(extendedValue, thisArg, args);
        }
      });
      wrappedIntegration[key] = wrappedFunction;
    }
  }
  return wrappedIntegration;
}


//# sourceMappingURL=integration.js.map

;// ./node_modules/@sentry/core/build/esm/utils/eventUtils.js
function getPossibleEventMessages(event) {
  const possibleMessages = [];
  if (event.message) {
    possibleMessages.push(event.message);
  }
  try {
    const lastException = event.exception.values[event.exception.values.length - 1];
    if (lastException?.value) {
      possibleMessages.push(lastException.value);
      if (lastException.type) {
        possibleMessages.push(`${lastException.type}: ${lastException.value}`);
      }
    }
  } catch {
  }
  return possibleMessages;
}


//# sourceMappingURL=eventUtils.js.map

;// ./node_modules/@sentry/core/build/esm/utils/is.js
const objectToString = Object.prototype.toString;
function is_isError(wat) {
  switch (objectToString.call(wat)) {
    case "[object Error]":
    case "[object Exception]":
    case "[object DOMException]":
    case "[object WebAssembly.Exception]":
      return true;
    default:
      return isInstanceOf(wat, Error);
  }
}
function isBuiltin(wat, className) {
  return objectToString.call(wat) === `[object ${className}]`;
}
function is_isErrorEvent(wat) {
  return isBuiltin(wat, "ErrorEvent");
}
function isDOMError(wat) {
  return isBuiltin(wat, "DOMError");
}
function isDOMException(wat) {
  return isBuiltin(wat, "DOMException");
}
function is_isString(wat) {
  return isBuiltin(wat, "String");
}
function is_isParameterizedString(wat) {
  return typeof wat === "object" && wat !== null && "__sentry_template_string__" in wat && "__sentry_template_values__" in wat;
}
function is_isPrimitive(wat) {
  return wat === null || is_isParameterizedString(wat) || typeof wat !== "object" && typeof wat !== "function";
}
function is_isPlainObject(wat) {
  return isBuiltin(wat, "Object");
}
function isObjectLike(wat) {
  return typeof wat === "object" && wat !== null;
}
function isEvent(wat) {
  return typeof Event !== "undefined" && isInstanceOf(wat, Event);
}
function isElement(wat) {
  return typeof Element !== "undefined" && isInstanceOf(wat, Element);
}
function isRegExp(wat) {
  return isBuiltin(wat, "RegExp");
}
function is_isThenable(wat) {
  return Boolean(wat?.then && typeof wat.then === "function");
}
function isSyntheticEvent(wat) {
  return is_isPlainObject(wat) && "nativeEvent" in wat && "preventDefault" in wat && "stopPropagation" in wat;
}
function isInstanceOf(wat, base) {
  try {
    return wat instanceof base;
  } catch {
    return false;
  }
}
function isVueViewModel(wat) {
  return !!(typeof wat === "object" && wat !== null && (wat.__isVue || wat._isVue || wat.__v_isVNode));
}
function isRequest(request) {
  return typeof Request !== "undefined" && isInstanceOf(request, Request);
}


//# sourceMappingURL=is.js.map

;// ./node_modules/@sentry/core/build/esm/utils/object.js




function fill(source, name, replacementFactory) {
  if (!(name in source)) {
    return;
  }
  const original = source[name];
  if (typeof original !== "function") {
    return;
  }
  const wrapped = replacementFactory(original);
  if (typeof wrapped === "function") {
    markFunctionWrapped(wrapped, original);
  }
  try {
    source[name] = wrapped;
  } catch {
    debug_build_DEBUG_BUILD && debug_logger_debug.log(`Failed to replace method "${name}" in object`, source);
  }
}
function object_addNonEnumerableProperty(obj, name, value) {
  try {
    Object.defineProperty(obj, name, {
      // enumerable: false, // the default, so we can save on bundle size by not explicitly setting it
      value,
      writable: true,
      configurable: true
    });
  } catch {
    debug_build_DEBUG_BUILD && debug_logger_debug.log(`Failed to add non-enumerable property "${String(name)}" to object`, obj);
  }
}
function markFunctionWrapped(wrapped, original) {
  try {
    const proto = original.prototype || {};
    wrapped.prototype = original.prototype = proto;
    object_addNonEnumerableProperty(wrapped, "__sentry_original__", original);
  } catch {
  }
}
function wrapMethod(obj, field, wrapped, enumerable = true) {
  const original = obj[field];
  if (typeof original !== "function") {
    throw new Error(`Cannot wrap method: ${field} is not a function`);
  }
  if (getOriginalFunction(original)) {
    throw new Error(`Attempting to wrap method ${field} multiple times`);
  }
  markFunctionWrapped(wrapped, original);
  Object.defineProperty(obj, field, {
    writable: true,
    configurable: true,
    enumerable,
    value: wrapped
  });
}
function getOriginalFunction(func) {
  return func.__sentry_original__;
}
function convertToPlainObject(value) {
  if (is_isError(value)) {
    return {
      message: value.message,
      name: value.name,
      stack: value.stack,
      ...getOwnProperties(value)
    };
  }
  if (isEvent(value)) {
    const { type, target, currentTarget, detail } = value;
    return {
      type,
      target,
      currentTarget,
      ...detail ? { detail } : {},
      ...getOwnProperties(value)
    };
  }
  return value;
}
function getOwnProperties(obj) {
  if (isObjectLike(obj)) {
    return Object.fromEntries(Object.entries(obj));
  }
  return {};
}
function object_extractExceptionKeysForMessage(exception) {
  const keys = Object.keys(convertToPlainObject(exception));
  keys.sort();
  return !keys[0] ? "[object has no keys]" : keys.join(", ");
}
function dropUndefinedKeys(inputValue) {
  const memoizationMap = /* @__PURE__ */ new Map();
  return _dropUndefinedKeys(inputValue, memoizationMap);
}
function _dropUndefinedKeys(inputValue, memoizationMap) {
  if (inputValue === null || typeof inputValue !== "object") {
    return inputValue;
  }
  const memoVal = memoizationMap.get(inputValue);
  if (memoVal !== void 0) {
    return memoVal;
  }
  if (Array.isArray(inputValue)) {
    const returnValue = [];
    memoizationMap.set(inputValue, returnValue);
    inputValue.forEach((value) => {
      returnValue.push(_dropUndefinedKeys(value, memoizationMap));
    });
    return returnValue;
  }
  if (isPojo(inputValue)) {
    const returnValue = {};
    memoizationMap.set(inputValue, returnValue);
    const keys = Object.keys(inputValue);
    keys.forEach((key) => {
      const val = inputValue[key];
      if (val !== void 0) {
        returnValue[key] = _dropUndefinedKeys(val, memoizationMap);
      }
    });
    return returnValue;
  }
  return inputValue;
}
function isPojo(input) {
  const constructor = input.constructor;
  return constructor === Object || constructor === void 0;
}
function objectify(wat) {
  let objectified;
  switch (true) {
    // this will catch both undefined and null
    case wat == void 0:
      objectified = new String(wat);
      break;
    // Though symbols and bigints do have wrapper classes (`Symbol` and `BigInt`, respectively), for whatever reason
    // those classes don't have constructors which can be used with the `new` keyword. We therefore need to cast each as
    // an object in order to wrap it.
    case (typeof wat === "symbol" || typeof wat === "bigint"):
      objectified = Object(wat);
      break;
    // this will catch the remaining primitives: `String`, `Number`, and `Boolean`
    case isPrimitive(wat):
      objectified = new wat.constructor(wat);
      break;
    // by process of elimination, at this point we know that `wat` must already be an object
    default:
      objectified = wat;
      break;
  }
  return objectified;
}


//# sourceMappingURL=object.js.map

;// ./node_modules/@sentry/core/build/esm/utils/randomSafeContext.js


let RESOLVED_RUNNER;
function randomSafeContext_withRandomSafeContext(cb) {
  if (RESOLVED_RUNNER !== void 0) {
    return RESOLVED_RUNNER ? RESOLVED_RUNNER(cb) : cb();
  }
  const sym = /* @__PURE__ */ Symbol.for("__SENTRY_SAFE_RANDOM_ID_WRAPPER__");
  const globalWithSymbol = worldwide_GLOBAL_OBJ;
  if (sym in globalWithSymbol && typeof globalWithSymbol[sym] === "function") {
    RESOLVED_RUNNER = globalWithSymbol[sym];
    return RESOLVED_RUNNER(cb);
  }
  RESOLVED_RUNNER = null;
  return cb();
}
function safeMathRandom() {
  return randomSafeContext_withRandomSafeContext(() => Math.random());
}
function randomSafeContext_safeDateNow() {
  return randomSafeContext_withRandomSafeContext(() => Date.now());
}


//# sourceMappingURL=randomSafeContext.js.map

;// ./node_modules/@sentry/core/build/esm/utils/misc.js





function getCrypto() {
  const gbl = worldwide_GLOBAL_OBJ;
  return gbl.crypto || gbl.msCrypto;
}
let emptyUuid;
function getRandomByte() {
  return safeMathRandom() * 16;
}
function misc_uuid4(crypto = getCrypto()) {
  try {
    if (crypto?.randomUUID) {
      return randomSafeContext_withRandomSafeContext(() => crypto.randomUUID()).replace(/-/g, "");
    }
  } catch {
  }
  if (!emptyUuid) {
    emptyUuid = "10000000100040008000" + 1e11;
  }
  return emptyUuid.replace(
    /[018]/g,
    (c) => (
      // eslint-disable-next-line no-bitwise
      (c ^ (getRandomByte() & 15) >> c / 4).toString(16)
    )
  );
}
function getFirstException(event) {
  return event.exception?.values?.[0];
}
function getEventDescription(event) {
  const { message, event_id: eventId } = event;
  if (message) {
    return message;
  }
  const firstException = getFirstException(event);
  if (firstException) {
    if (firstException.type && firstException.value) {
      return `${firstException.type}: ${firstException.value}`;
    }
    return firstException.type || firstException.value || eventId || "<unknown>";
  }
  return eventId || "<unknown>";
}
function misc_addExceptionTypeValue(event, value, type) {
  const exception = event.exception = event.exception || {};
  const values = exception.values = exception.values || [];
  const firstException = values[0] = values[0] || {};
  if (!firstException.value) {
    firstException.value = value || "";
  }
  if (!firstException.type) {
    firstException.type = type || "Error";
  }
}
function misc_addExceptionMechanism(event, newMechanism) {
  const firstException = getFirstException(event);
  if (!firstException) {
    return;
  }
  const defaultMechanism = { type: "generic", handled: true };
  const currentMechanism = firstException.mechanism;
  firstException.mechanism = { ...defaultMechanism, ...currentMechanism, ...newMechanism };
  if (newMechanism && "data" in newMechanism) {
    const mergedData = { ...currentMechanism?.data, ...newMechanism.data };
    firstException.mechanism.data = mergedData;
  }
}
const SEMVER_REGEXP = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$/;
function _parseInt(input) {
  return parseInt(input || "", 10);
}
function parseSemver(input) {
  const match = input.match(SEMVER_REGEXP) || [];
  const major = _parseInt(match[1]);
  const minor = _parseInt(match[2]);
  const patch = _parseInt(match[3]);
  return {
    buildmetadata: match[5],
    major: isNaN(major) ? void 0 : major,
    minor: isNaN(minor) ? void 0 : minor,
    patch: isNaN(patch) ? void 0 : patch,
    prerelease: match[4]
  };
}
function addContextToFrame(lines, frame, linesOfContext = 5) {
  if (frame.lineno === void 0) {
    return;
  }
  const maxLines = lines.length;
  const sourceLine = Math.max(Math.min(maxLines - 1, frame.lineno - 1), 0);
  frame.pre_context = lines.slice(Math.max(0, sourceLine - linesOfContext), sourceLine).map((line) => snipLine(line, 0));
  const lineIndex = Math.min(maxLines - 1, sourceLine);
  frame.context_line = snipLine(lines[lineIndex], frame.colno || 0);
  frame.post_context = lines.slice(Math.min(sourceLine + 1, maxLines), sourceLine + 1 + linesOfContext).map((line) => snipLine(line, 0));
}
function checkOrSetAlreadyCaught(exception) {
  if (isAlreadyCaptured(exception)) {
    return true;
  }
  try {
    object_addNonEnumerableProperty(exception, "__sentry_captured__", true);
  } catch {
  }
  return false;
}
function isAlreadyCaptured(exception) {
  try {
    return exception.__sentry_captured__;
  } catch {
  }
}


//# sourceMappingURL=misc.js.map

;// ./node_modules/@sentry/core/build/esm/utils/normalizationHints.js


const SENTRY_SKIP_NORMALIZATION = /* @__PURE__ */ Symbol.for("sentry.skipNormalization");
const SENTRY_OVERRIDE_NORMALIZATION_DEPTH = /* @__PURE__ */ Symbol.for("sentry.overrideNormalizationDepth");
function setSkipNormalizationHint(obj) {
  addNonEnumerableProperty(obj, SENTRY_SKIP_NORMALIZATION, true);
}
function setNormalizationDepthOverrideHint(obj, depth) {
  addNonEnumerableProperty(obj, SENTRY_OVERRIDE_NORMALIZATION_DEPTH, depth);
}
function hasSkipNormalizationHint(value) {
  return Boolean(value[SENTRY_SKIP_NORMALIZATION]);
}
function getNormalizationDepthOverrideHint(value) {
  const v = value[SENTRY_OVERRIDE_NORMALIZATION_DEPTH];
  return typeof v === "number" ? v : void 0;
}


//# sourceMappingURL=normalizationHints.js.map

;// ./node_modules/@sentry/core/build/esm/utils/stacktrace.js
const STACKTRACE_FRAME_LIMIT = 50;
const UNKNOWN_FUNCTION = "?";
const WEBPACK_ERROR_REGEXP = /\(error: (.*)\)/;
const STRIP_FRAME_REGEXP = /captureMessage|captureException/;
function createStackParser(...parsers) {
  const sortedParsers = parsers.sort((a, b) => a[0] - b[0]).map((p) => p[1]);
  return (stack, skipFirstLines = 0, framesToPop = 0) => {
    const frames = [];
    const lines = stack.split("\n");
    for (let i = skipFirstLines; i < lines.length; i++) {
      let line = lines[i];
      if (line.length > 1024) {
        line = line.slice(0, 1024);
      }
      const cleanedLine = WEBPACK_ERROR_REGEXP.test(line) ? line.replace(WEBPACK_ERROR_REGEXP, "$1") : line;
      if (cleanedLine.includes("Error: ")) {
        continue;
      }
      for (const parser of sortedParsers) {
        const frame = parser(cleanedLine);
        if (frame) {
          frames.push(frame);
          break;
        }
      }
      if (frames.length >= STACKTRACE_FRAME_LIMIT + framesToPop) {
        break;
      }
    }
    return stripSentryFramesAndReverse(frames.slice(framesToPop));
  };
}
function stackParserFromStackParserOptions(stackParser) {
  if (Array.isArray(stackParser)) {
    return createStackParser(...stackParser);
  }
  return stackParser;
}
function stripSentryFramesAndReverse(stack) {
  if (!stack.length) {
    return [];
  }
  const localStack = Array.from(stack);
  if (/sentryWrapped/.test(getLastStackFrame(localStack).function || "")) {
    localStack.pop();
  }
  localStack.reverse();
  if (STRIP_FRAME_REGEXP.test(getLastStackFrame(localStack).function || "")) {
    localStack.pop();
    if (STRIP_FRAME_REGEXP.test(getLastStackFrame(localStack).function || "")) {
      localStack.pop();
    }
  }
  return localStack.slice(0, STACKTRACE_FRAME_LIMIT).map((frame) => ({
    ...frame,
    filename: frame.filename || getLastStackFrame(localStack).filename,
    function: frame.function || UNKNOWN_FUNCTION
  }));
}
function getLastStackFrame(arr) {
  return arr[arr.length - 1] || {};
}
const defaultFunctionName = "<anonymous>";
function getFunctionName(fn) {
  try {
    if (!fn || typeof fn !== "function") {
      return defaultFunctionName;
    }
    return fn.name || defaultFunctionName;
  } catch {
    return defaultFunctionName;
  }
}
function getFramesFromEvent(event) {
  const exception = event.exception;
  if (exception) {
    const frames = [];
    try {
      exception.values.forEach((value) => {
        if (value.stacktrace.frames) {
          frames.push(...value.stacktrace.frames);
        }
      });
      return frames;
    } catch {
      return void 0;
    }
  }
  return void 0;
}
function stacktrace_normalizeStackTracePath(path) {
  let filename = path?.startsWith("file://") ? path.slice(7) : path;
  if (filename?.match(/\/[A-Z]:/)) {
    filename = filename.slice(1);
  }
  return filename;
}


//# sourceMappingURL=stacktrace.js.map

;// ./node_modules/@sentry/core/build/esm/utils/normalize.js




let stringifier;
function setNormalizeStringifier(newStringifier) {
  stringifier = newStringifier;
}
function normalize(input, depth = 100, maxProperties = Infinity) {
  try {
    return visit("", input, depth, maxProperties);
  } catch (err) {
    return { ERROR: `**non-serializable** (${err})` };
  }
}
function normalize_normalizeToSize(object, depth = 3, maxSize = 100 * 1024) {
  const normalized = normalize(object, depth);
  if (jsonSize(normalized) > maxSize) {
    return normalize_normalizeToSize(object, depth - 1, maxSize);
  }
  return normalized;
}
function visit(key, value, depth = Infinity, maxProperties = Infinity, memo = memoBuilder()) {
  const [memoize, unmemoize] = memo;
  if (value == null || // this matches null and undefined -> eqeq not eqeqeq
  ["boolean", "string"].includes(typeof value) || typeof value === "number" && Number.isFinite(value)) {
    return value;
  }
  const stringified = stringifyValue(key, value);
  if (!stringified.startsWith("[object ")) {
    return stringified;
  }
  if (hasSkipNormalizationHint(value)) {
    return value;
  }
  const overrideDepth = getNormalizationDepthOverrideHint(value);
  const remainingDepth = overrideDepth !== void 0 ? overrideDepth : depth;
  if (remainingDepth === 0) {
    return stringified.replace("object ", "");
  }
  if (memoize(value)) {
    return "[Circular ~]";
  }
  const valueWithToJSON = value;
  if (valueWithToJSON && typeof valueWithToJSON.toJSON === "function") {
    try {
      const jsonValue = valueWithToJSON.toJSON();
      return visit("", jsonValue, remainingDepth - 1, maxProperties, memo);
    } catch {
    }
  }
  const normalized = Array.isArray(value) ? [] : {};
  let numAdded = 0;
  const visitable = convertToPlainObject(value);
  for (const visitKey in visitable) {
    if (!Object.prototype.hasOwnProperty.call(visitable, visitKey)) {
      continue;
    }
    if (numAdded >= maxProperties) {
      normalized[visitKey] = "[MaxProperties ~]";
      break;
    }
    const visitValue = visitable[visitKey];
    normalized[visitKey] = visit(visitKey, visitValue, remainingDepth - 1, maxProperties, memo);
    numAdded++;
  }
  unmemoize(value);
  return normalized;
}
function stringifyValue(key, value) {
  try {
    if (stringifier) {
      const stringified = stringifier(value);
      if (stringified) {
        return stringified;
      }
    }
    if (typeof __webpack_require__.g !== "undefined" && value === __webpack_require__.g) {
      return "[Global]";
    }
    if (typeof value === "number" && !Number.isFinite(value)) {
      return `[${value}]`;
    }
    if (typeof value === "function") {
      return `[Function: ${getFunctionName(value)}]`;
    }
    if (typeof value === "symbol") {
      return `[${String(value)}]`;
    }
    if (typeof value === "bigint") {
      return `[BigInt: ${String(value)}]`;
    }
    const objName = getConstructorName(value);
    return `[object ${objName}]`;
  } catch (err) {
    return `**non-serializable** (${err})`;
  }
}
function getConstructorName(value) {
  const prototype = Object.getPrototypeOf(value);
  return prototype?.constructor ? prototype.constructor.name : "null prototype";
}
function utf8Length(value) {
  return ~-encodeURI(value).split(/%..|./).length;
}
function jsonSize(value) {
  return utf8Length(JSON.stringify(value));
}
function normalizeUrlToBase(url, basePath) {
  const escapedBase = basePath.replace(/\\/g, "/").replace(/[|\\{}()[\]^$+*?.]/g, "\\$&");
  let newUrl = url;
  try {
    newUrl = decodeURI(url);
  } catch {
  }
  return newUrl.replace(/\\/g, "/").replace(/webpack:\/?/g, "").replace(new RegExp(`(file://)?/*${escapedBase}/*`, "ig"), "app:///");
}
function memoBuilder() {
  const inner = /* @__PURE__ */ new WeakSet();
  function memoize(obj) {
    if (inner.has(obj)) {
      return true;
    }
    inner.add(obj);
    return false;
  }
  function unmemoize(obj) {
    inner.delete(obj);
  }
  return [memoize, unmemoize];
}


//# sourceMappingURL=normalize.js.map

;// ./node_modules/@sentry/core/build/esm/utils/string.js



function stringify(value, fallback = "[unserializable]") {
  if (typeof value === "string") {
    return value;
  }
  try {
    return JSON.stringify(value);
  } catch {
    return typeof fallback === "function" ? fallback(value) : fallback;
  }
}
function truncate(str, max = 0) {
  if (typeof str !== "string" || max === 0) {
    return str;
  }
  return str.length <= max ? str : `${str.slice(0, max)}...`;
}
function string_snipLine(line, colno) {
  let newLine = line;
  const lineLength = newLine.length;
  if (lineLength <= 150) {
    return newLine;
  }
  if (colno > lineLength) {
    colno = lineLength;
  }
  let start = Math.max(colno - 60, 0);
  if (start < 5) {
    start = 0;
  }
  let end = Math.min(start + 140, lineLength);
  if (end > lineLength - 5) {
    end = lineLength;
  }
  if (end === lineLength) {
    start = Math.max(end - 140, 0);
  }
  newLine = newLine.slice(start, end);
  if (start > 0) {
    newLine = `'{snip} ${newLine}`;
  }
  if (end < lineLength) {
    newLine += " {snip}";
  }
  return newLine;
}
function safeJoin(input, delimiter) {
  if (!Array.isArray(input)) {
    return "";
  }
  const output = [];
  for (let i = 0; i < input.length; i++) {
    const value = input[i];
    if (is_isPrimitive(value)) {
      output.push(String(value));
    } else if (value instanceof Error) {
      output.push(value.message ? `${value.name}: ${value.message}` : value.name);
    } else {
      output.push(stringifyValue(void 0, value));
    }
  }
  return output.join(delimiter);
}
function isMatchingPattern(value, pattern, requireExactStringMatch = false) {
  if (!is_isString(value)) {
    return false;
  }
  if (isRegExp(pattern)) {
    return pattern.test(value);
  }
  if (is_isString(pattern)) {
    return requireExactStringMatch ? value === pattern : value.includes(pattern);
  }
  if (typeof pattern === "function") {
    return pattern(value);
  }
  return false;
}
function stringMatchesSomePattern(testString, patterns = [], requireExactStringMatch = false) {
  for (const pattern of patterns) {
    if (isMatchingPattern(testString, pattern, requireExactStringMatch)) {
      return true;
    }
  }
  return false;
}


//# sourceMappingURL=string.js.map

;// ./node_modules/@sentry/core/build/esm/integrations/eventFilters.js







const DEFAULT_IGNORE_ERRORS = [
  /^Script error\.?$/,
  /^Javascript error: Script error\.? on line 0$/,
  /^ResizeObserver loop completed with undelivered notifications.$/,
  // The browser logs this when a ResizeObserver handler takes a bit longer. Usually this is not an actual issue though. It indicates slowness.
  /^Cannot redefine property: googletag$/,
  // This is thrown when google tag manager is used in combination with an ad blocker
  /^Can't find variable: gmo$/,
  // Error from Google Search App https://issuetracker.google.com/issues/396043331
  /^undefined is not an object \(evaluating 'a\.[A-Z]'\)$/,
  // Random error that happens but not actionable or noticeable to end-users.
  /can't redefine non-configurable property "solana"/,
  // Probably a browser extension or custom browser (Brave) throwing this error
  /vv\(\)\.getRestrictions is not a function/,
  // Error thrown by GTM, seemingly not affecting end-users
  /Can't find variable: _AutofillCallbackHandler/,
  // Unactionable error in instagram webview https://developers.facebook.com/community/threads/320013549791141/
  /Object Not Found Matching Id:\d+, MethodName:simulateEvent/,
  // unactionable error from CEFSharp, a .NET library that embeds chromium in .NET apps
  /^Java exception was raised during method invocation$/
  // error from Facebook Mobile browser (https://github.com/getsentry/sentry-javascript/issues/15065)
];
const INTEGRATION_NAME = "EventFilters";
const eventFiltersIntegration = defineIntegration((options = {}) => {
  let mergedOptions;
  return {
    name: INTEGRATION_NAME,
    setup(client) {
      const clientOptions = client.getOptions();
      mergedOptions = _mergeOptions(options, clientOptions);
    },
    processEvent(event, _hint, client) {
      if (!mergedOptions) {
        const clientOptions = client.getOptions();
        mergedOptions = _mergeOptions(options, clientOptions);
      }
      return _shouldDropEvent(event, mergedOptions) ? null : event;
    }
  };
});
const inboundFiltersIntegration = defineIntegration(((options = {}) => {
  return {
    ...eventFiltersIntegration(options),
    name: "InboundFilters"
  };
}));
function _mergeOptions(internalOptions = {}, clientOptions = {}) {
  return {
    allowUrls: [...internalOptions.allowUrls || [], ...clientOptions.allowUrls || []],
    denyUrls: [...internalOptions.denyUrls || [], ...clientOptions.denyUrls || []],
    ignoreErrors: [
      ...internalOptions.ignoreErrors || [],
      ...clientOptions.ignoreErrors || [],
      ...internalOptions.disableErrorDefaults ? [] : DEFAULT_IGNORE_ERRORS
    ],
    ignoreTransactions: [...internalOptions.ignoreTransactions || [], ...clientOptions.ignoreTransactions || []]
  };
}
function _shouldDropEvent(event, options) {
  if (!event.type) {
    if (_isIgnoredError(event, options.ignoreErrors)) {
      debug_build_DEBUG_BUILD && debug_logger_debug.warn(
        `Event dropped due to being matched by \`ignoreErrors\` option.
Event: ${getEventDescription(event)}`
      );
      return true;
    }
    if (_isUselessError(event)) {
      debug_build_DEBUG_BUILD && debug_logger_debug.warn(
        `Event dropped due to not having an error message, error type or stacktrace.
Event: ${getEventDescription(
          event
        )}`
      );
      return true;
    }
    if (_isDeniedUrl(event, options.denyUrls)) {
      debug_build_DEBUG_BUILD && debug_logger_debug.warn(
        `Event dropped due to being matched by \`denyUrls\` option.
Event: ${getEventDescription(
          event
        )}.
Url: ${_getEventFilterUrl(event)}`
      );
      return true;
    }
    if (!_isAllowedUrl(event, options.allowUrls)) {
      debug_build_DEBUG_BUILD && debug_logger_debug.warn(
        `Event dropped due to not being matched by \`allowUrls\` option.
Event: ${getEventDescription(
          event
        )}.
Url: ${_getEventFilterUrl(event)}`
      );
      return true;
    }
  } else if (event.type === "transaction") {
    if (_isIgnoredTransaction(event, options.ignoreTransactions)) {
      debug_build_DEBUG_BUILD && debug_logger_debug.warn(
        `Event dropped due to being matched by \`ignoreTransactions\` option.
Event: ${getEventDescription(event)}`
      );
      return true;
    }
  }
  return false;
}
function _isIgnoredError(event, ignoreErrors) {
  if (!ignoreErrors?.length) {
    return false;
  }
  return getPossibleEventMessages(event).some((message) => stringMatchesSomePattern(message, ignoreErrors));
}
function _isIgnoredTransaction(event, ignoreTransactions) {
  if (!ignoreTransactions?.length) {
    return false;
  }
  const name = event.transaction;
  return name ? stringMatchesSomePattern(name, ignoreTransactions) : false;
}
function _isDeniedUrl(event, denyUrls) {
  if (!denyUrls?.length) {
    return false;
  }
  const url = _getEventFilterUrl(event);
  return !url ? false : stringMatchesSomePattern(url, denyUrls);
}
function _isAllowedUrl(event, allowUrls) {
  if (!allowUrls?.length) {
    return true;
  }
  const url = _getEventFilterUrl(event);
  return !url ? true : stringMatchesSomePattern(url, allowUrls);
}
function _getLastValidUrl(frames = []) {
  for (let i = frames.length - 1; i >= 0; i--) {
    const frame = frames[i];
    if (frame && frame.filename !== "<anonymous>" && frame.filename !== "[native code]") {
      return frame.filename || null;
    }
  }
  return null;
}
function _getEventFilterUrl(event) {
  try {
    const rootException = [...event.exception?.values ?? []].reverse().find((value) => value.mechanism?.parent_id === void 0 && value.stacktrace?.frames?.length);
    const frames = rootException?.stacktrace?.frames;
    return frames ? _getLastValidUrl(frames) : null;
  } catch {
    debug_build_DEBUG_BUILD && debug_logger_debug.error(`Cannot extract url for event ${getEventDescription(event)}`);
    return null;
  }
}
function _isUselessError(event) {
  if (!event.exception?.values?.length) {
    return false;
  }
  return (
    // No top-level message
    !event.message && // There are no exception values that have a stacktrace, a non-generic-Error type or value
    !event.exception.values.some((value) => value.stacktrace || value.type && value.type !== "Error" || value.value)
  );
}


//# sourceMappingURL=eventFilters.js.map

;// ./node_modules/@sentry/core/build/esm/utils/time.js



const ONE_SECOND_IN_MS = 1e3;
function dateTimestampInSeconds() {
  return randomSafeContext_safeDateNow() / ONE_SECOND_IN_MS;
}
function createUnixTimestampInSecondsFunc() {
  const { performance } = worldwide_GLOBAL_OBJ;
  if (!performance?.now || !performance.timeOrigin) {
    return dateTimestampInSeconds;
  }
  const timeOrigin = performance.timeOrigin;
  return () => {
    return (timeOrigin + randomSafeContext_withRandomSafeContext(() => performance.now())) / ONE_SECOND_IN_MS;
  };
}
let _cachedTimestampInSeconds;
function time_timestampInSeconds() {
  const func = _cachedTimestampInSeconds ?? (_cachedTimestampInSeconds = createUnixTimestampInSecondsFunc());
  return func();
}
let cachedTimeOrigin = null;
function getBrowserTimeOrigin() {
  const { performance } = GLOBAL_OBJ;
  if (!performance?.now) {
    return void 0;
  }
  const threshold = 3e5;
  const performanceNow = withRandomSafeContext(() => performance.now());
  const dateNow = safeDateNow();
  const timeOrigin = performance.timeOrigin;
  if (typeof timeOrigin === "number") {
    const timeOriginDelta = Math.abs(timeOrigin + performanceNow - dateNow);
    if (timeOriginDelta < threshold) {
      return timeOrigin;
    }
  }
  const navigationStart = performance.timing?.navigationStart;
  if (typeof navigationStart === "number") {
    const navigationStartDelta = Math.abs(navigationStart + performanceNow - dateNow);
    if (navigationStartDelta < threshold) {
      return navigationStart;
    }
  }
  return dateNow - performanceNow;
}
function browserPerformanceTimeOrigin() {
  if (cachedTimeOrigin === null) {
    cachedTimeOrigin = getBrowserTimeOrigin();
  }
  return cachedTimeOrigin;
}


//# sourceMappingURL=time.js.map

;// ./node_modules/@sentry/core/build/esm/session.js



function makeSession(context) {
  const startingTime = time_timestampInSeconds();
  const session = {
    sid: misc_uuid4(),
    init: true,
    timestamp: startingTime,
    started: startingTime,
    duration: 0,
    status: "ok",
    errors: 0,
    ignoreDuration: false,
    toJSON: () => sessionToJSON(session)
  };
  if (context) {
    updateSession(session, context);
  }
  return session;
}
function updateSession(session, context = {}) {
  if (context.user) {
    if (!session.ipAddress && context.user.ip_address) {
      session.ipAddress = context.user.ip_address;
    }
    if (!session.did && !context.did) {
      session.did = context.user.id || context.user.email || context.user.username;
    }
  }
  session.timestamp = context.timestamp || time_timestampInSeconds();
  if (context.abnormal_mechanism) {
    session.abnormal_mechanism = context.abnormal_mechanism;
  }
  if (context.ignoreDuration) {
    session.ignoreDuration = context.ignoreDuration;
  }
  if (context.sid) {
    session.sid = context.sid.length === 32 ? context.sid : misc_uuid4();
  }
  if (context.init !== void 0) {
    session.init = context.init;
  }
  if (!session.did && context.did) {
    session.did = `${context.did}`;
  }
  if (typeof context.started === "number") {
    session.started = context.started;
  }
  if (session.ignoreDuration) {
    session.duration = void 0;
  } else if (typeof context.duration === "number") {
    session.duration = context.duration;
  } else {
    const duration = session.timestamp - session.started;
    session.duration = duration >= 0 ? duration : 0;
  }
  if (context.release) {
    session.release = context.release;
  }
  if (context.environment) {
    session.environment = context.environment;
  }
  if (!session.ipAddress && context.ipAddress) {
    session.ipAddress = context.ipAddress;
  }
  if (!session.userAgent && context.userAgent) {
    session.userAgent = context.userAgent;
  }
  if (typeof context.errors === "number") {
    session.errors = context.errors;
  }
  if (context.status) {
    session.status = context.status;
  }
}
function closeSession(session, status) {
  let context = {};
  if (status) {
    context = { status };
  } else if (session.status === "ok") {
    context = { status: "exited" };
  }
  updateSession(session, context);
}
function sessionToJSON(session) {
  return {
    sid: `${session.sid}`,
    init: session.init,
    // Make sure that sec is converted to ms for date constructor
    started: new Date(session.started * 1e3).toISOString(),
    timestamp: new Date(session.timestamp * 1e3).toISOString(),
    status: session.status,
    errors: session.errors,
    did: typeof session.did === "number" || typeof session.did === "string" ? `${session.did}` : void 0,
    duration: session.duration,
    abnormal_mechanism: session.abnormal_mechanism,
    attrs: {
      release: session.release,
      environment: session.environment,
      ip_address: session.ipAddress,
      user_agent: session.userAgent
    }
  };
}


//# sourceMappingURL=session.js.map

;// ./node_modules/@sentry/core/build/esm/utils/merge.js
function merge(initialObj, mergeObj, levels = 2) {
  if (!mergeObj || typeof mergeObj !== "object" || levels <= 0) {
    return mergeObj;
  }
  if (initialObj && Object.keys(mergeObj).length === 0) {
    return initialObj;
  }
  const output = { ...initialObj };
  for (const key in mergeObj) {
    if (Object.prototype.hasOwnProperty.call(mergeObj, key)) {
      output[key] = merge(output[key], mergeObj[key], levels - 1);
    }
  }
  return output;
}


//# sourceMappingURL=merge.js.map

;// ./node_modules/@sentry/core/build/esm/utils/propagationContext.js


function propagationContext_generateTraceId() {
  return misc_uuid4();
}
function propagationContext_generateSpanId() {
  return misc_uuid4().substring(16);
}


//# sourceMappingURL=propagationContext.js.map

;// ./node_modules/@sentry/core/build/esm/utils/weakRef.js


function weakRef_makeWeakRef(value) {
  try {
    const WeakRefImpl = worldwide_GLOBAL_OBJ.WeakRef;
    if (typeof WeakRefImpl === "function") {
      return new WeakRefImpl(value);
    }
  } catch {
  }
  return value;
}
function derefWeakRef(ref) {
  if (!ref) {
    return void 0;
  }
  if (typeof ref === "object" && "deref" in ref && typeof ref.deref === "function") {
    try {
      return ref.deref();
    } catch {
      return void 0;
    }
  }
  return ref;
}


//# sourceMappingURL=weakRef.js.map

;// ./node_modules/@sentry/core/build/esm/utils/spanOnScope.js



const SCOPE_SPAN_FIELD = "_sentrySpan";
function _setSpanForScope(scope, span) {
  if (span) {
    object_addNonEnumerableProperty(scope, SCOPE_SPAN_FIELD, weakRef_makeWeakRef(span));
  } else {
    delete scope[SCOPE_SPAN_FIELD];
  }
}
function spanOnScope_getSpanForScope(scope) {
  return derefWeakRef(scope[SCOPE_SPAN_FIELD]);
}


//# sourceMappingURL=spanOnScope.js.map

;// ./node_modules/@sentry/core/build/esm/scope.js












const DEFAULT_MAX_BREADCRUMBS = 100;
class Scope {
  // NOTE: Any field which gets added here should get added not only to the constructor but also to the `clone` method.
  constructor() {
    this._notifyingListeners = false;
    this._scopeListeners = [];
    this._eventProcessors = [];
    this._breadcrumbs = [];
    this._attachments = [];
    this._user = {};
    this._tags = {};
    this._attributes = {};
    this._extra = {};
    this._contexts = {};
    this._sdkProcessingMetadata = {};
    this._propagationContext = {
      traceId: propagationContext_generateTraceId(),
      sampleRand: safeMathRandom()
    };
  }
  /**
   * Clone all data from this scope into a new scope.
   */
  clone() {
    const newScope = new Scope();
    newScope._breadcrumbs = [...this._breadcrumbs];
    newScope._tags = { ...this._tags };
    newScope._attributes = { ...this._attributes };
    newScope._extra = { ...this._extra };
    newScope._contexts = { ...this._contexts };
    if (this._contexts.flags) {
      newScope._contexts.flags = {
        values: [...this._contexts.flags.values]
      };
    }
    newScope._user = this._user;
    newScope._level = this._level;
    newScope._session = this._session;
    newScope._transactionName = this._transactionName;
    newScope._fingerprint = this._fingerprint;
    newScope._eventProcessors = [...this._eventProcessors];
    newScope._attachments = [...this._attachments];
    newScope._sdkProcessingMetadata = { ...this._sdkProcessingMetadata };
    newScope._propagationContext = { ...this._propagationContext };
    newScope._client = this._client;
    newScope._lastEventId = this._lastEventId;
    newScope._conversationId = this._conversationId;
    _setSpanForScope(newScope, spanOnScope_getSpanForScope(this));
    return newScope;
  }
  /**
   * Update the client assigned to this scope.
   * Note that not every scope will have a client assigned - isolation scopes & the global scope will generally not have a client,
   * as well as manually created scopes.
   */
  setClient(client) {
    this._client = client;
  }
  /**
   * Set the ID of the last captured error event.
   * This is generally only captured on the isolation scope.
   */
  setLastEventId(lastEventId) {
    this._lastEventId = lastEventId;
  }
  /**
   * Get the client assigned to this scope.
   */
  getClient() {
    return this._client;
  }
  /**
   * Get the ID of the last captured error event.
   * This is generally only available on the isolation scope.
   */
  lastEventId() {
    return this._lastEventId;
  }
  /**
   * @inheritDoc
   */
  addScopeListener(callback) {
    this._scopeListeners.push(callback);
  }
  /**
   * Add an event processor that will be called before an event is sent.
   */
  addEventProcessor(callback) {
    this._eventProcessors.push(callback);
    return this;
  }
  /**
   * Set the user for this scope.
   * Set to `null` to unset the user.
   */
  setUser(user) {
    this._user = user || {
      email: void 0,
      id: void 0,
      ip_address: void 0,
      username: void 0
    };
    if (this._session) {
      updateSession(this._session, { user });
    }
    this._notifyScopeListeners();
    return this;
  }
  /**
   * Get the user from this scope.
   */
  getUser() {
    return this._user;
  }
  /**
   * Set the conversation ID for this scope.
   * Set to `null` to unset the conversation ID.
   */
  setConversationId(conversationId) {
    this._conversationId = conversationId || void 0;
    this._notifyScopeListeners();
    return this;
  }
  /**
   * Set an object that will be merged into existing tags on the scope,
   * and will be sent as tags data with the event.
   */
  setTags(tags) {
    this._tags = {
      ...this._tags,
      ...tags
    };
    this._notifyScopeListeners();
    return this;
  }
  /**
   * Set a single tag that will be sent as tags data with the event.
   */
  setTag(key, value) {
    return this.setTags({ [key]: value });
  }
  /**
   * Sets attributes onto the scope.
   *
   * These attributes are applied to logs, metrics and streamed spans.
   *
   * Supported attribute value types are `string`, `number`, `boolean`, `string[]`, `number[]` and `boolean[]`.
   *
   * @param newAttributes - The attributes to set on the scope, as key-value pairs.
   *
   * @example
   * ```typescript
   * scope.setAttributes({
   *   is_admin: true,
   *   payment_selection: 'credit_card',
   *   render_duration: 150,
   * });
   * ```
   */
  setAttributes(newAttributes) {
    this._attributes = {
      ...this._attributes,
      ...newAttributes
    };
    this._notifyScopeListeners();
    return this;
  }
  /**
   * Sets an attribute onto the scope.
   *
   * These attributes are applied to logs, metrics and streamed spans.
   *
   * Supported attribute value types are `string`, `number`, `boolean`, `string[]`, `number[]` and `boolean[]`.
   *
   * @param key - The attribute key.
   * @param value - The attribute value.
   *
   * @example
   * ```typescript
   * scope.setAttribute('is_admin', true);
   * scope.setAttribute('render_duration', 150);
   * ```
   */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  setAttribute(key, value) {
    return this.setAttributes({ [key]: value });
  }
  /**
   * Removes the attribute with the given key from the scope.
   *
   * @param key - The attribute key.
   *
   * @example
   * ```typescript
   * scope.removeAttribute('is_admin');
   * ```
   */
  removeAttribute(key) {
    if (key in this._attributes) {
      delete this._attributes[key];
      this._notifyScopeListeners();
    }
    return this;
  }
  /**
   * Set an object that will be merged into existing extra on the scope,
   * and will be sent as extra data with the event.
   */
  setExtras(extras) {
    this._extra = {
      ...this._extra,
      ...extras
    };
    this._notifyScopeListeners();
    return this;
  }
  /**
   * Set a single key:value extra entry that will be sent as extra data with the event.
   */
  setExtra(key, extra) {
    this._extra = { ...this._extra, [key]: extra };
    this._notifyScopeListeners();
    return this;
  }
  /**
   * Sets the fingerprint on the scope to send with the events.
   * @param {string[]} fingerprint Fingerprint to group events in Sentry.
   */
  setFingerprint(fingerprint) {
    this._fingerprint = fingerprint;
    this._notifyScopeListeners();
    return this;
  }
  /**
   * Sets the level on the scope for future events.
   */
  setLevel(level) {
    this._level = level;
    this._notifyScopeListeners();
    return this;
  }
  /**
   * Sets the transaction name on the scope so that the name of e.g. taken server route or
   * the page location is attached to future events.
   *
   * IMPORTANT: Calling this function does NOT change the name of the currently active
   * root span. If you want to change the name of the active root span, use
   * `Sentry.updateSpanName(rootSpan, 'new name')` instead.
   *
   * By default, the SDK updates the scope's transaction name automatically on sensible
   * occasions, such as a page navigation or when handling a new request on the server.
   */
  setTransactionName(name) {
    this._transactionName = name;
    this._notifyScopeListeners();
    return this;
  }
  /**
   * Sets context data with the given name.
   * Data passed as context will be normalized. You can also pass `null` to unset the context.
   * Note that context data will not be merged - calling `setContext` will overwrite an existing context with the same key.
   */
  setContext(key, context) {
    if (context === null) {
      delete this._contexts[key];
    } else {
      this._contexts[key] = context;
    }
    this._notifyScopeListeners();
    return this;
  }
  /**
   * Set the session for the scope.
   */
  setSession(session) {
    if (!session) {
      delete this._session;
    } else {
      this._session = session;
    }
    this._notifyScopeListeners();
    return this;
  }
  /**
   * Get the session from the scope.
   */
  getSession() {
    return this._session;
  }
  /**
   * Updates the scope with provided data. Can work in three variations:
   * - plain object containing updatable attributes
   * - Scope instance that'll extract the attributes from
   * - callback function that'll receive the current scope as an argument and allow for modifications
   */
  update(captureContext) {
    if (!captureContext) {
      return this;
    }
    const scopeToMerge = typeof captureContext === "function" ? captureContext(this) : captureContext;
    const scopeInstance = scopeToMerge instanceof Scope ? scopeToMerge.getScopeData() : is_isPlainObject(scopeToMerge) ? captureContext : void 0;
    const {
      tags,
      attributes,
      extra,
      user,
      contexts,
      level,
      fingerprint = [],
      propagationContext,
      conversationId
    } = scopeInstance || {};
    this._tags = { ...this._tags, ...tags };
    this._attributes = { ...this._attributes, ...attributes };
    this._extra = { ...this._extra, ...extra };
    this._contexts = { ...this._contexts, ...contexts };
    if (user && Object.keys(user).length) {
      this._user = user;
    }
    if (level) {
      this._level = level;
    }
    if (fingerprint.length) {
      this._fingerprint = fingerprint;
    }
    if (propagationContext) {
      this._propagationContext = propagationContext;
    }
    if (conversationId) {
      this._conversationId = conversationId;
    }
    return this;
  }
  /**
   * Clears the current scope and resets its properties.
   * Note: The client will not be cleared.
   */
  clear() {
    this._breadcrumbs = [];
    this._tags = {};
    this._attributes = {};
    this._extra = {};
    this._user = {};
    this._contexts = {};
    this._level = void 0;
    this._transactionName = void 0;
    this._fingerprint = void 0;
    this._session = void 0;
    this._conversationId = void 0;
    _setSpanForScope(this, void 0);
    this._attachments = [];
    this.setPropagationContext({
      traceId: propagationContext_generateTraceId(),
      sampleRand: safeMathRandom()
    });
    this._notifyScopeListeners();
    return this;
  }
  /**
   * Adds a breadcrumb to the scope.
   * By default, the last 100 breadcrumbs are kept.
   */
  addBreadcrumb(breadcrumb, maxBreadcrumbs) {
    const maxCrumbs = typeof maxBreadcrumbs === "number" ? maxBreadcrumbs : DEFAULT_MAX_BREADCRUMBS;
    if (maxCrumbs <= 0) {
      return this;
    }
    const mergedBreadcrumb = {
      timestamp: dateTimestampInSeconds(),
      ...breadcrumb,
      // Breadcrumb messages can theoretically be infinitely large and they're held in memory so we truncate them not to leak (too much) memory
      message: breadcrumb.message ? truncate(breadcrumb.message, 2048) : breadcrumb.message
    };
    this._breadcrumbs.push(mergedBreadcrumb);
    if (this._breadcrumbs.length > maxCrumbs) {
      this._breadcrumbs = this._breadcrumbs.slice(-maxCrumbs);
      this._client?.recordDroppedEvent("buffer_overflow", "log_item");
    }
    this._notifyScopeListeners();
    return this;
  }
  /**
   * Get the last breadcrumb of the scope.
   */
  getLastBreadcrumb() {
    return this._breadcrumbs[this._breadcrumbs.length - 1];
  }
  /**
   * Clear all breadcrumbs from the scope.
   */
  clearBreadcrumbs() {
    this._breadcrumbs = [];
    this._notifyScopeListeners();
    return this;
  }
  /**
   * Add an attachment to the scope.
   */
  addAttachment(attachment) {
    this._attachments.push(attachment);
    return this;
  }
  /**
   * Clear all attachments from the scope.
   */
  clearAttachments() {
    this._attachments = [];
    return this;
  }
  /**
   * Get the data of this scope, which should be applied to an event during processing.
   */
  getScopeData() {
    return {
      breadcrumbs: this._breadcrumbs,
      attachments: this._attachments,
      contexts: this._contexts,
      tags: this._tags,
      attributes: this._attributes,
      extra: this._extra,
      user: this._user,
      level: this._level,
      fingerprint: this._fingerprint || [],
      eventProcessors: this._eventProcessors,
      propagationContext: this._propagationContext,
      sdkProcessingMetadata: this._sdkProcessingMetadata,
      transactionName: this._transactionName,
      span: spanOnScope_getSpanForScope(this),
      conversationId: this._conversationId
    };
  }
  /**
   * Add data which will be accessible during event processing but won't get sent to Sentry.
   */
  setSDKProcessingMetadata(newData) {
    this._sdkProcessingMetadata = merge(this._sdkProcessingMetadata, newData, 2);
    return this;
  }
  /**
   * Add propagation context to the scope, used for distributed tracing
   */
  setPropagationContext(context) {
    this._propagationContext = context;
    return this;
  }
  /**
   * Get propagation context from the scope, used for distributed tracing
   */
  getPropagationContext() {
    return this._propagationContext;
  }
  /**
   * Capture an exception for this scope.
   *
   * @returns {string} The id of the captured Sentry event.
   */
  captureException(exception, hint) {
    const eventId = hint?.event_id || misc_uuid4();
    if (!this._client) {
      debug_build_DEBUG_BUILD && debug_logger_debug.warn("No client configured on scope - will not capture exception!");
      return eventId;
    }
    const syntheticException = new Error("Sentry syntheticException");
    this._client.captureException(
      exception,
      {
        originalException: exception,
        syntheticException,
        ...hint,
        event_id: eventId
      },
      this
    );
    return eventId;
  }
  /**
   * Capture a message for this scope.
   *
   * @returns {string} The id of the captured message.
   */
  captureMessage(message, level, hint) {
    const eventId = hint?.event_id || misc_uuid4();
    if (!this._client) {
      debug_build_DEBUG_BUILD && debug_logger_debug.warn("No client configured on scope - will not capture message!");
      return eventId;
    }
    const syntheticException = hint?.syntheticException ?? new Error(message);
    this._client.captureMessage(
      message,
      level,
      {
        originalException: message,
        syntheticException,
        ...hint,
        event_id: eventId
      },
      this
    );
    return eventId;
  }
  /**
   * Capture a Sentry event for this scope.
   *
   * @returns {string} The id of the captured event.
   */
  captureEvent(event, hint) {
    const eventId = event.event_id || hint?.event_id || misc_uuid4();
    if (!this._client) {
      debug_build_DEBUG_BUILD && debug_logger_debug.warn("No client configured on scope - will not capture event!");
      return eventId;
    }
    this._client.captureEvent(event, { ...hint, event_id: eventId }, this);
    return eventId;
  }
  /**
   * This will be called on every set call.
   */
  _notifyScopeListeners() {
    if (!this._notifyingListeners) {
      this._notifyingListeners = true;
      this._scopeListeners.forEach((callback) => {
        callback(this);
      });
      this._notifyingListeners = false;
    }
  }
}


//# sourceMappingURL=scope.js.map

;// ./node_modules/@sentry/core/build/esm/defaultScopes.js



function getDefaultCurrentScope() {
  return getGlobalSingleton("defaultCurrentScope", () => new Scope());
}
function getDefaultIsolationScope() {
  return getGlobalSingleton("defaultIsolationScope", () => new Scope());
}


//# sourceMappingURL=defaultScopes.js.map

;// ./node_modules/@sentry/core/build/esm/utils/chain-and-copy-promiselike.js
const isActualPromise = (p) => p instanceof Promise && !p[kChainedCopy];
const kChainedCopy = /* @__PURE__ */ Symbol("chained PromiseLike");
const chainAndCopyPromiseLike = (original, onSuccess, onError) => {
  const chained = original.then(
    (value) => {
      onSuccess(value);
      return value;
    },
    (err) => {
      onError(err);
      throw err;
    }
  );
  return isActualPromise(chained) && isActualPromise(original) ? chained : copyProps(original, chained);
};
const copyProps = (original, chained) => {
  if (!chained) return original;
  let mutated = false;
  for (const key in original) {
    if (key in chained) continue;
    mutated = true;
    const value = original[key];
    if (typeof value === "function") {
      Object.defineProperty(chained, key, {
        value: (...args) => value.apply(original, args),
        enumerable: true,
        configurable: true,
        writable: true
      });
    } else {
      chained[key] = value;
    }
  }
  if (mutated) Object.assign(chained, { [kChainedCopy]: true });
  return chained;
};


//# sourceMappingURL=chain-and-copy-promiselike.js.map

;// ./node_modules/@sentry/core/build/esm/asyncContext/stackStrategy.js






class AsyncContextStack {
  constructor(scope, isolationScope) {
    let assignedScope;
    if (!scope) {
      assignedScope = new Scope();
    } else {
      assignedScope = scope;
    }
    let assignedIsolationScope;
    if (!isolationScope) {
      assignedIsolationScope = new Scope();
    } else {
      assignedIsolationScope = isolationScope;
    }
    this._stack = [{ scope: assignedScope }];
    this._isolationScope = assignedIsolationScope;
  }
  /**
   * Fork a scope for the stack.
   */
  withScope(callback) {
    const scope = this._pushScope();
    let maybePromiseResult;
    try {
      maybePromiseResult = callback(scope);
    } catch (e) {
      this._popScope();
      throw e;
    }
    if (is_isThenable(maybePromiseResult)) {
      return chainAndCopyPromiseLike(
        maybePromiseResult,
        () => this._popScope(),
        () => this._popScope()
      );
    }
    this._popScope();
    return maybePromiseResult;
  }
  /**
   * Get the client of the stack.
   */
  getClient() {
    return this.getStackTop().client;
  }
  /**
   * Returns the scope of the top stack.
   */
  getScope() {
    return this.getStackTop().scope;
  }
  /**
   * Get the isolation scope for the stack.
   */
  getIsolationScope() {
    return this._isolationScope;
  }
  /**
   * Returns the topmost scope layer in the order domain > local > process.
   */
  getStackTop() {
    return this._stack[this._stack.length - 1];
  }
  /**
   * Push a scope to the stack.
   */
  _pushScope() {
    const scope = this.getScope().clone();
    this._stack.push({
      client: this.getClient(),
      scope
    });
    return scope;
  }
  /**
   * Pop a scope from the stack.
   */
  _popScope() {
    if (this._stack.length <= 1) return false;
    return !!this._stack.pop();
  }
}
function getAsyncContextStack() {
  const registry = carrier_getMainCarrier();
  const sentry = carrier_getSentryCarrier(registry);
  return sentry.stack = sentry.stack || new AsyncContextStack(getDefaultCurrentScope(), getDefaultIsolationScope());
}
function withScope(callback) {
  return getAsyncContextStack().withScope(callback);
}
function withSetScope(scope, callback) {
  const stack = getAsyncContextStack();
  return stack.withScope(() => {
    stack.getStackTop().scope = scope;
    return callback(scope);
  });
}
function stackStrategy_withIsolationScope(callback) {
  return getAsyncContextStack().withScope(() => {
    return callback(getAsyncContextStack().getIsolationScope());
  });
}
function getStackAsyncContextStrategy() {
  return {
    withIsolationScope: stackStrategy_withIsolationScope,
    withScope,
    withSetScope,
    withSetIsolationScope: (_isolationScope, callback) => {
      return stackStrategy_withIsolationScope(callback);
    },
    getCurrentScope: () => getAsyncContextStack().getScope(),
    getIsolationScope: () => getAsyncContextStack().getIsolationScope()
  };
}


//# sourceMappingURL=stackStrategy.js.map

;// ./node_modules/@sentry/core/build/esm/asyncContext/index.js



function setAsyncContextStrategy(strategy) {
  const registry = getMainCarrier();
  const sentry = getSentryCarrier(registry);
  sentry.acs = strategy;
}
function asyncContext_getAsyncContextStrategy(carrier) {
  const sentry = carrier_getSentryCarrier(carrier);
  if (sentry.acs) {
    return sentry.acs;
  }
  return getStackAsyncContextStrategy();
}


//# sourceMappingURL=index.js.map

;// ./node_modules/@sentry/core/build/esm/currentScopes.js





let _externalPropagationContextProvider;
function registerExternalPropagationContext(fn) {
  _externalPropagationContextProvider = fn;
}
function getExternalPropagationContext() {
  return _externalPropagationContextProvider?.();
}
function hasExternalPropagationContext() {
  return _externalPropagationContextProvider !== void 0;
}
function currentScopes_getCurrentScope() {
  const carrier = carrier_getMainCarrier();
  const acs = asyncContext_getAsyncContextStrategy(carrier);
  return acs.getCurrentScope();
}
function currentScopes_getIsolationScope() {
  const carrier = carrier_getMainCarrier();
  const acs = asyncContext_getAsyncContextStrategy(carrier);
  return acs.getIsolationScope();
}
function getGlobalScope() {
  return getGlobalSingleton("globalScope", () => new Scope());
}
function currentScopes_withScope(...rest) {
  const carrier = carrier_getMainCarrier();
  const acs = asyncContext_getAsyncContextStrategy(carrier);
  if (rest.length === 2) {
    const [scope, callback] = rest;
    if (!scope) {
      return acs.withScope(callback);
    }
    return acs.withSetScope(scope, callback);
  }
  return acs.withScope(rest[0]);
}
function currentScopes_withIsolationScope(...rest) {
  const carrier = getMainCarrier();
  const acs = getAsyncContextStrategy(carrier);
  if (rest.length === 2) {
    const [isolationScope, callback] = rest;
    if (!isolationScope) {
      return acs.withIsolationScope(callback);
    }
    return acs.withSetIsolationScope(isolationScope, callback);
  }
  return acs.withIsolationScope(rest[0]);
}
function currentScopes_getClient() {
  return currentScopes_getCurrentScope().getClient();
}
function getTraceContextFromScope(scope) {
  const externalContext = getExternalPropagationContext();
  if (externalContext) {
    return { trace_id: externalContext.traceId, span_id: externalContext.spanId };
  }
  const propagationContext = scope.getPropagationContext();
  const { traceId, parentSpanId, propagationSpanId } = propagationContext;
  const traceContext = {
    trace_id: traceId,
    span_id: propagationSpanId || propagationContext_generateSpanId()
  };
  if (parentSpanId) {
    traceContext.parent_span_id = parentSpanId;
  }
  return traceContext;
}


//# sourceMappingURL=currentScopes.js.map

;// ./node_modules/@sentry/core/build/esm/integrations/functiontostring.js




const functiontostring_INTEGRATION_NAME = "FunctionToString";
const SETUP_CLIENTS = /* @__PURE__ */ new WeakMap();
const _functionToStringIntegration = (() => {
  return {
    name: functiontostring_INTEGRATION_NAME,
    setupOnce() {
      const originalFunctionToString = Function.prototype.toString;
      try {
        Function.prototype.toString = function(...args) {
          const originalFunction = getOriginalFunction(this);
          let unwrappedFunction;
          try {
            if (SETUP_CLIENTS.has(currentScopes_getClient()) && originalFunction !== void 0) {
              unwrappedFunction = originalFunction;
            }
          } catch {
          }
          return originalFunctionToString.apply(unwrappedFunction ?? this, args);
        };
      } catch {
      }
    },
    setup(client) {
      SETUP_CLIENTS.set(client, true);
    }
  };
});
const functionToStringIntegration = defineIntegration(_functionToStringIntegration);


//# sourceMappingURL=functiontostring.js.map

;// ./node_modules/@sentry/core/build/esm/semanticAttributes.js
const semanticAttributes_SEMANTIC_ATTRIBUTE_SENTRY_SOURCE = "sentry.source";
const SEMANTIC_ATTRIBUTE_SENTRY_SAMPLE_RATE = "sentry.sample_rate";
const SEMANTIC_ATTRIBUTE_SENTRY_PREVIOUS_TRACE_SAMPLE_RATE = "sentry.previous_trace_sample_rate";
const SEMANTIC_ATTRIBUTE_SENTRY_OP = "sentry.op";
const semanticAttributes_SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN = "sentry.origin";
const semanticAttributes_SEMANTIC_ATTRIBUTE_SENTRY_STATUS_MESSAGE = "sentry.status.message";
const SEMANTIC_ATTRIBUTE_SENTRY_IDLE_SPAN_FINISH_REASON = "sentry.idle_span_finish_reason";
const SEMANTIC_ATTRIBUTE_SENTRY_MEASUREMENT_UNIT = "sentry.measurement_unit";
const SEMANTIC_ATTRIBUTE_SENTRY_MEASUREMENT_VALUE = "sentry.measurement_value";
const semanticAttributes_SEMANTIC_ATTRIBUTE_SENTRY_RELEASE = "sentry.release";
const semanticAttributes_SEMANTIC_ATTRIBUTE_SENTRY_ENVIRONMENT = "sentry.environment";
const SEMANTIC_ATTRIBUTE_SENTRY_SEGMENT_NAME = "sentry.segment.name";
const SEMANTIC_ATTRIBUTE_SENTRY_SEGMENT_ID = "sentry.segment.id";
const SEMANTIC_ATTRIBUTE_SENTRY_SDK_NAME = "sentry.sdk.name";
const SEMANTIC_ATTRIBUTE_SENTRY_SDK_VERSION = "sentry.sdk.version";
const semanticAttributes_SEMANTIC_ATTRIBUTE_SENTRY_SDK_INTEGRATIONS = "sentry.sdk.integrations";
const semanticAttributes_SEMANTIC_ATTRIBUTE_USER_ID = "user.id";
const semanticAttributes_SEMANTIC_ATTRIBUTE_USER_EMAIL = "user.email";
const semanticAttributes_SEMANTIC_ATTRIBUTE_USER_IP_ADDRESS = "user.ip_address";
const semanticAttributes_SEMANTIC_ATTRIBUTE_USER_USERNAME = "user.name";
const semanticAttributes_SEMANTIC_ATTRIBUTE_SENTRY_CUSTOM_SPAN_NAME = "sentry.custom_span_name";
const SEMANTIC_ATTRIBUTE_PROFILE_ID = "sentry.profile_id";
const SEMANTIC_ATTRIBUTE_EXCLUSIVE_TIME = "sentry.exclusive_time";
const SEMANTIC_ATTRIBUTE_CACHE_HIT = "cache.hit";
const SEMANTIC_ATTRIBUTE_CACHE_KEY = "cache.key";
const SEMANTIC_ATTRIBUTE_CACHE_ITEM_SIZE = "cache.item_size";
const semanticAttributes_SEMANTIC_ATTRIBUTE_HTTP_REQUEST_METHOD = "http.request.method";
const SEMANTIC_ATTRIBUTE_URL_FULL = "url.full";
const SEMANTIC_LINK_ATTRIBUTE_LINK_TYPE = "sentry.link.type";
const GEN_AI_CONVERSATION_ID_ATTRIBUTE = "gen_ai.conversation.id";


//# sourceMappingURL=semanticAttributes.js.map

;// ./node_modules/@sentry/core/build/esm/attributes.js


function isAttributeObject(maybeObj) {
  return typeof maybeObj === "object" && maybeObj != null && !Array.isArray(maybeObj) && Object.keys(maybeObj).includes("value");
}
function attributeValueToTypedAttributeValue(rawValue, useFallback) {
  const { value, unit } = isAttributeObject(rawValue) ? rawValue : { value: rawValue, unit: void 0 };
  const attributeValue = getTypedAttributeValue(value);
  const checkedUnit = unit && typeof unit === "string" ? { unit } : {};
  if (attributeValue) {
    return { ...attributeValue, ...checkedUnit };
  }
  if (!useFallback || useFallback === "skip-undefined" && value === void 0) {
    return;
  }
  let stringValue = "";
  try {
    stringValue = JSON.stringify(value) ?? "";
  } catch {
  }
  return {
    value: stringValue,
    type: "string",
    ...checkedUnit
  };
}
function attributes_serializeAttributes(attributes, fallback = false) {
  const serializedAttributes = {};
  for (const [key, value] of Object.entries(attributes ?? {})) {
    const typedValue = attributeValueToTypedAttributeValue(value, fallback);
    if (typedValue) {
      serializedAttributes[key] = typedValue;
    }
  }
  return serializedAttributes;
}
function estimateTypedAttributesSizeInBytes(attributes) {
  if (!attributes) {
    return 0;
  }
  let weight = 0;
  for (const [key, attr] of Object.entries(attributes)) {
    weight += key.length * 2;
    weight += attr.type.length * 2;
    weight += (attr.unit?.length ?? 0) * 2;
    const val = attr.value;
    if (Array.isArray(val)) {
      weight += estimatePrimitiveSizeInBytes(val[0]) * val.length;
    } else if (isPrimitive(val)) {
      weight += estimatePrimitiveSizeInBytes(val);
    } else {
      weight += 100;
    }
  }
  return weight;
}
function estimatePrimitiveSizeInBytes(value) {
  if (typeof value === "string") {
    return value.length * 2;
  } else if (typeof value === "boolean") {
    return 4;
  } else if (typeof value === "number") {
    return 8;
  }
  return 0;
}
function getTypedAttributeValue(value) {
  if (Array.isArray(value)) {
    return { value, type: "array" };
  }
  const primitiveType = typeof value === "string" ? "string" : typeof value === "boolean" ? "boolean" : typeof value === "number" && !Number.isNaN(value) ? Number.isInteger(value) ? "integer" : "double" : null;
  if (primitiveType) {
    return { value, type: primitiveType };
  }
}


//# sourceMappingURL=attributes.js.map

;// ./node_modules/@sentry/core/build/esm/tracing/spanstatus.js
const spanstatus_SPAN_STATUS_UNSET = 0;
const spanstatus_SPAN_STATUS_OK = 1;
const SPAN_STATUS_ERROR = 2;
function getSpanStatusFromHttpCode(httpStatus) {
  if (httpStatus < 400 && httpStatus >= 100) {
    return { code: spanstatus_SPAN_STATUS_OK };
  }
  if (httpStatus >= 400 && httpStatus < 500) {
    switch (httpStatus) {
      case 401:
        return { code: SPAN_STATUS_ERROR, message: "unauthenticated" };
      case 403:
        return { code: SPAN_STATUS_ERROR, message: "permission_denied" };
      case 404:
        return { code: SPAN_STATUS_ERROR, message: "not_found" };
      case 409:
        return { code: SPAN_STATUS_ERROR, message: "already_exists" };
      case 413:
        return { code: SPAN_STATUS_ERROR, message: "failed_precondition" };
      case 429:
        return { code: SPAN_STATUS_ERROR, message: "resource_exhausted" };
      case 499:
        return { code: SPAN_STATUS_ERROR, message: "cancelled" };
      default:
        return { code: SPAN_STATUS_ERROR, message: "invalid_argument" };
    }
  }
  if (httpStatus >= 500 && httpStatus < 600) {
    switch (httpStatus) {
      case 501:
        return { code: SPAN_STATUS_ERROR, message: "unimplemented" };
      case 503:
        return { code: SPAN_STATUS_ERROR, message: "unavailable" };
      case 504:
        return { code: SPAN_STATUS_ERROR, message: "deadline_exceeded" };
      default:
        return { code: SPAN_STATUS_ERROR, message: "internal_error" };
    }
  }
  return { code: SPAN_STATUS_ERROR, message: "internal_error" };
}
function setHttpStatus(span, httpStatus) {
  span.setAttribute("http.response.status_code", httpStatus);
  const spanStatus = getSpanStatusFromHttpCode(httpStatus);
  if (spanStatus.message !== "unknown_error") {
    span.setStatus(spanStatus);
  }
}


//# sourceMappingURL=spanstatus.js.map

;// ./node_modules/@sentry/core/build/esm/tracing/utils.js



const SCOPE_ON_START_SPAN_FIELD = "_sentryScope";
const ISOLATION_SCOPE_ON_START_SPAN_FIELD = "_sentryIsolationScope";
const OTEL_SOURCE_INFERENCE_SPAN_FIELD = /* @__PURE__ */ (/* unused pure expression or super */ null && (Symbol.for("sentry.otelSourceInference")));
const OTEL_SOURCE_EXPLICITLY_SET_SPAN_FIELD = /* @__PURE__ */ (/* unused pure expression or super */ null && (Symbol.for("sentry.otelSourceExplicitlySet")));
const TRACER_PROVIDER_SPAN_FIELD = /* @__PURE__ */ (/* unused pure expression or super */ null && (Symbol.for("sentry.tracerProviderSpan")));
function setCapturedScopesOnSpan(span, scope, isolationScope) {
  if (span) {
    addNonEnumerableProperty(span, ISOLATION_SCOPE_ON_START_SPAN_FIELD, makeWeakRef(isolationScope));
    addNonEnumerableProperty(span, SCOPE_ON_START_SPAN_FIELD, scope);
  }
}
function utils_getCapturedScopesOnSpan(span) {
  const spanWithScopes = span;
  return {
    scope: spanWithScopes[SCOPE_ON_START_SPAN_FIELD],
    isolationScope: derefWeakRef(spanWithScopes[ISOLATION_SCOPE_ON_START_SPAN_FIELD])
  };
}
function markSpanForOtelSourceInference(span) {
  addNonEnumerableProperty(span, OTEL_SOURCE_INFERENCE_SPAN_FIELD, true);
}
function spanShouldInferOtelSource(span) {
  return span[OTEL_SOURCE_INFERENCE_SPAN_FIELD] === true;
}
function markSpanSourceAsExplicit(span) {
  addNonEnumerableProperty(span, OTEL_SOURCE_EXPLICITLY_SET_SPAN_FIELD, true);
}
function spanSourceWasExplicitlySet(span) {
  return span[OTEL_SOURCE_EXPLICITLY_SET_SPAN_FIELD] === true;
}
function markSpanAsTracerProviderSpan(span) {
  addNonEnumerableProperty(span, TRACER_PROVIDER_SPAN_FIELD, true);
}
function spanIsTracerProviderSpan(span) {
  return span[TRACER_PROVIDER_SPAN_FIELD] === true;
}


//# sourceMappingURL=utils.js.map

;// ./node_modules/@sentry/core/build/esm/utils/spanUtils.js














const spanUtils_TRACE_FLAG_NONE = 0;
const TRACE_FLAG_SAMPLED = 1;
let hasShownSpanDropWarning = false;
function spanToTransactionTraceContext(span) {
  const { spanId: span_id, traceId: trace_id } = span.spanContext();
  const { data, op, parent_span_id, status, origin, links } = spanUtils_spanToJSON(span);
  return {
    parent_span_id,
    span_id,
    trace_id,
    data,
    op,
    status,
    origin,
    links
  };
}
function spanToTraceContext(span) {
  const { spanId, traceId: trace_id, isRemote } = span.spanContext();
  const parent_span_id = isRemote ? spanId : spanUtils_spanToJSON(span).parent_span_id;
  const scope = utils_getCapturedScopesOnSpan(span).scope;
  const span_id = isRemote ? scope?.getPropagationContext().propagationSpanId || propagationContext_generateSpanId() : spanId;
  return {
    parent_span_id,
    span_id,
    trace_id
  };
}
function spanToTraceHeader(span) {
  const { traceId, spanId } = span.spanContext();
  const sampled = spanIsSampled(span);
  return generateSentryTraceHeader(traceId, spanId, sampled);
}
function spanToTraceparentHeader(span) {
  const { traceId, spanId } = span.spanContext();
  const sampled = spanIsSampled(span);
  return generateTraceparentHeader(traceId, spanId, sampled);
}
function convertSpanLinksForEnvelope(links) {
  if (links && links.length > 0) {
    return links.map(({ context: { spanId, traceId, traceFlags, ...restContext }, attributes }) => ({
      span_id: spanId,
      trace_id: traceId,
      sampled: traceFlags === TRACE_FLAG_SAMPLED,
      attributes,
      ...restContext
    }));
  } else {
    return void 0;
  }
}
function getStreamedSpanLinks(links) {
  if (links?.length) {
    return links.map(({ context: { spanId, traceId, traceFlags }, attributes }) => ({
      span_id: spanId,
      trace_id: traceId,
      sampled: traceFlags === TRACE_FLAG_SAMPLED,
      attributes
    }));
  } else {
    return void 0;
  }
}
function spanTimeInputToSeconds(input) {
  if (typeof input === "number") {
    return ensureTimestampInSeconds(input);
  }
  if (Array.isArray(input)) {
    return input[0] + input[1] / 1e9;
  }
  if (input instanceof Date) {
    return ensureTimestampInSeconds(input.getTime());
  }
  return time_timestampInSeconds();
}
function ensureTimestampInSeconds(timestamp) {
  const isMs = timestamp > 9999999999;
  return isMs ? timestamp / 1e3 : timestamp;
}
function spanUtils_spanToJSON(span) {
  if (spanIsSentrySpan(span)) {
    return span.getSpanJSON();
  }
  const { spanId: span_id, traceId: trace_id } = span.spanContext();
  if (spanIsOpenTelemetrySdkTraceBaseSpan(span)) {
    const { attributes, startTime, name, endTime, status, links } = span;
    return {
      span_id,
      trace_id,
      data: attributes,
      description: name,
      parent_span_id: getOtelParentSpanId(span),
      start_timestamp: spanTimeInputToSeconds(startTime),
      // This is [0,0] by default in OTEL, in which case we want to interpret this as no end time
      timestamp: spanTimeInputToSeconds(endTime) || void 0,
      status: getStatusMessage(status),
      op: attributes[SEMANTIC_ATTRIBUTE_SENTRY_OP],
      origin: attributes[semanticAttributes_SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN],
      links: convertSpanLinksForEnvelope(links)
    };
  }
  return {
    span_id,
    trace_id,
    start_timestamp: 0,
    data: {}
  };
}
function spanUtils_spanToStreamedSpanJSON(span) {
  if (spanIsSentrySpan(span)) {
    return span.getStreamedSpanJSON();
  }
  const { spanId: span_id, traceId: trace_id } = span.spanContext();
  if (spanIsOpenTelemetrySdkTraceBaseSpan(span)) {
    const { attributes, startTime, name, endTime, status, links } = span;
    return {
      name,
      span_id,
      trace_id,
      parent_span_id: getOtelParentSpanId(span),
      start_timestamp: spanTimeInputToSeconds(startTime),
      end_timestamp: spanTimeInputToSeconds(endTime),
      is_segment: span === spanUtils_INTERNAL_getSegmentSpan(span),
      status: getSimpleStatus(status),
      attributes: addStatusMessageAttribute(attributes, status),
      links: getStreamedSpanLinks(links)
    };
  }
  return {
    span_id,
    trace_id,
    start_timestamp: 0,
    name: "",
    end_timestamp: 0,
    status: "ok",
    is_segment: span === spanUtils_INTERNAL_getSegmentSpan(span)
  };
}
function getOtelParentSpanId(span) {
  return "parentSpanId" in span ? span.parentSpanId : "parentSpanContext" in span ? span.parentSpanContext?.spanId : void 0;
}
function spanUtils_streamedSpanJsonToSerializedSpan(spanJson) {
  return {
    ...spanJson,
    attributes: attributes_serializeAttributes(spanJson.attributes),
    links: spanJson.links?.map((link) => ({
      ...link,
      attributes: attributes_serializeAttributes(link.attributes)
    }))
  };
}
function spanIsOpenTelemetrySdkTraceBaseSpan(span) {
  const castSpan = span;
  return !!castSpan.attributes && !!castSpan.startTime && !!castSpan.name && !!castSpan.endTime && !!castSpan.status;
}
function spanIsSentrySpan(span) {
  return typeof span.getSpanJSON === "function";
}
function spanIsSampled(span) {
  const { traceFlags } = span.spanContext();
  return traceFlags === TRACE_FLAG_SAMPLED;
}
function getStatusMessage(status) {
  if (!status || status.code === spanstatus_SPAN_STATUS_UNSET) {
    return void 0;
  }
  if (status.code === spanstatus_SPAN_STATUS_OK) {
    return "ok";
  }
  return status.message || "internal_error";
}
function getSimpleStatus(status) {
  return !status || status.code === SPAN_STATUS_OK || status.code === SPAN_STATUS_UNSET || status.message === "cancelled" ? "ok" : "error";
}
function addStatusMessageAttribute(attributes, status) {
  const statusMessage = getSimpleStatus(status) === "error" ? status?.message : void 0;
  return {
    ...statusMessage && { [SEMANTIC_ATTRIBUTE_SENTRY_STATUS_MESSAGE]: statusMessage },
    ...attributes
  };
}
const CHILD_SPANS_FIELD = "_sentryChildSpans";
const ROOT_SPAN_FIELD = "_sentryRootSpan";
function addChildSpanToSpan(span, childSpan) {
  const rootSpan = span[ROOT_SPAN_FIELD] || span;
  addNonEnumerableProperty(childSpan, ROOT_SPAN_FIELD, rootSpan);
  if (span[CHILD_SPANS_FIELD]) {
    span[CHILD_SPANS_FIELD].add(childSpan);
  } else {
    addNonEnumerableProperty(span, CHILD_SPANS_FIELD, /* @__PURE__ */ new Set([childSpan]));
  }
}
function removeChildSpanFromSpan(span, childSpan) {
  if (span[CHILD_SPANS_FIELD]) {
    span[CHILD_SPANS_FIELD].delete(childSpan);
  }
}
function getSpanDescendants(span) {
  const resultSet = /* @__PURE__ */ new Set();
  function addSpanChildren(span2) {
    if (resultSet.has(span2)) {
      return;
    } else if (spanIsSampled(span2)) {
      resultSet.add(span2);
      const childSpans = span2[CHILD_SPANS_FIELD] ? Array.from(span2[CHILD_SPANS_FIELD]) : [];
      for (const childSpan of childSpans) {
        addSpanChildren(childSpan);
      }
    }
  }
  addSpanChildren(span);
  return Array.from(resultSet);
}
const getRootSpan = spanUtils_INTERNAL_getSegmentSpan;
function spanUtils_INTERNAL_getSegmentSpan(span) {
  return span[ROOT_SPAN_FIELD] || span;
}
function getActiveSpan() {
  const carrier = getMainCarrier();
  const acs = getAsyncContextStrategy(carrier);
  if (acs.getActiveSpan) {
    return acs.getActiveSpan();
  }
  return _getSpanForScope(getCurrentScope());
}
function spanUtils_showSpanDropWarning() {
  if (!hasShownSpanDropWarning) {
    debug_logger_consoleSandbox(() => {
      console.warn(
        "[Sentry] Returning null from `beforeSendSpan` is disallowed. To drop certain spans, configure the respective integrations directly or use `ignoreSpans`."
      );
    });
    hasShownSpanDropWarning = true;
  }
}
function updateSpanName(span, name) {
  span.updateName(name);
  span.setAttributes({
    [SEMANTIC_ATTRIBUTE_SENTRY_SOURCE]: "custom",
    [SEMANTIC_ATTRIBUTE_SENTRY_CUSTOM_SPAN_NAME]: name
  });
}


//# sourceMappingURL=spanUtils.js.map

;// ./node_modules/@sentry/core/build/esm/integrations/conversationId.js





const conversationId_INTEGRATION_NAME = "ConversationId";
const _conversationIdIntegration = (() => {
  return {
    name: conversationId_INTEGRATION_NAME,
    setup(client) {
      client.on("spanStart", (span) => {
        const scopeData = currentScopes_getCurrentScope().getScopeData();
        const isolationScopeData = currentScopes_getIsolationScope().getScopeData();
        const conversationId = scopeData.conversationId || isolationScopeData.conversationId;
        if (conversationId) {
          const { op, data: attributes, description: name } = spanUtils_spanToJSON(span);
          if (!op?.startsWith("gen_ai.") && !attributes["ai.operationId"] && !name?.startsWith("ai.")) {
            return;
          }
          span.setAttribute(GEN_AI_CONVERSATION_ID_ATTRIBUTE, conversationId);
        }
      });
    }
  };
});
const conversationIdIntegration = defineIntegration(_conversationIdIntegration);


//# sourceMappingURL=conversationId.js.map

;// ./node_modules/@sentry/core/build/esm/integrations/dedupe.js





const dedupe_INTEGRATION_NAME = "Dedupe";
const _dedupeIntegration = (() => {
  let previousEvent;
  return {
    name: dedupe_INTEGRATION_NAME,
    processEvent(currentEvent) {
      if (currentEvent.type) {
        return currentEvent;
      }
      try {
        if (dedupe_shouldDropEvent(currentEvent, previousEvent)) {
          debug_build_DEBUG_BUILD && debug_logger_debug.warn("Event dropped due to being a duplicate of previously captured event.");
          return null;
        }
      } catch {
      }
      return previousEvent = currentEvent;
    }
  };
});
const dedupeIntegration = defineIntegration(_dedupeIntegration);
function dedupe_shouldDropEvent(currentEvent, previousEvent) {
  if (!previousEvent) {
    return false;
  }
  if (_isSameMessageEvent(currentEvent, previousEvent)) {
    return true;
  }
  if (_isSameExceptionEvent(currentEvent, previousEvent)) {
    return true;
  }
  return false;
}
function _isSameMessageEvent(currentEvent, previousEvent) {
  const currentMessage = currentEvent.message;
  const previousMessage = previousEvent.message;
  if (!currentMessage && !previousMessage) {
    return false;
  }
  if (currentMessage && !previousMessage || !currentMessage && previousMessage) {
    return false;
  }
  if (currentMessage !== previousMessage) {
    return false;
  }
  if (!_isSameFingerprint(currentEvent, previousEvent)) {
    return false;
  }
  if (!_isSameStacktrace(currentEvent, previousEvent)) {
    return false;
  }
  return true;
}
function _isSameExceptionEvent(currentEvent, previousEvent) {
  const previousException = _getExceptionFromEvent(previousEvent);
  const currentException = _getExceptionFromEvent(currentEvent);
  if (!previousException || !currentException) {
    return false;
  }
  if (previousException.type !== currentException.type || previousException.value !== currentException.value) {
    return false;
  }
  if (!_isSameFingerprint(currentEvent, previousEvent)) {
    return false;
  }
  if (!_isSameStacktrace(currentEvent, previousEvent)) {
    return false;
  }
  return true;
}
function _isSameStacktrace(currentEvent, previousEvent) {
  let currentFrames = getFramesFromEvent(currentEvent);
  let previousFrames = getFramesFromEvent(previousEvent);
  if (!currentFrames && !previousFrames) {
    return true;
  }
  if (currentFrames && !previousFrames || !currentFrames && previousFrames) {
    return false;
  }
  currentFrames = currentFrames;
  previousFrames = previousFrames;
  if (previousFrames.length !== currentFrames.length) {
    return false;
  }
  for (let i = 0; i < previousFrames.length; i++) {
    const frameA = previousFrames[i];
    const frameB = currentFrames[i];
    if (frameA.filename !== frameB.filename || frameA.lineno !== frameB.lineno || frameA.colno !== frameB.colno || frameA.function !== frameB.function) {
      return false;
    }
  }
  return true;
}
function _isSameFingerprint(currentEvent, previousEvent) {
  let currentFingerprint = currentEvent.fingerprint;
  let previousFingerprint = previousEvent.fingerprint;
  if (!currentFingerprint && !previousFingerprint) {
    return true;
  }
  if (currentFingerprint && !previousFingerprint || !currentFingerprint && previousFingerprint) {
    return false;
  }
  currentFingerprint = currentFingerprint;
  previousFingerprint = previousFingerprint;
  try {
    return !!(currentFingerprint.join("") === previousFingerprint.join(""));
  } catch {
    return false;
  }
}
function _getExceptionFromEvent(event) {
  return event.exception?.values?.[0];
}


//# sourceMappingURL=dedupe.js.map

;// ./node_modules/@sentry/core/build/esm/sdk.js




function initAndBind(clientClass, options) {
  if (options.debug === true) {
    if (debug_build_DEBUG_BUILD) {
      debug_logger_debug.enable();
    } else {
      debug_logger_consoleSandbox(() => {
        console.warn("[Sentry] Cannot initialize SDK with `debug` option using a non-debug bundle.");
      });
    }
  }
  const scope = currentScopes_getCurrentScope();
  scope.update(options.initialScope);
  const client = new clientClass(options);
  setCurrentClient(client);
  client.init();
  return client;
}
function setCurrentClient(client) {
  currentScopes_getCurrentScope().setClient(client);
}


//# sourceMappingURL=sdk.js.map

;// ./node_modules/@sentry/core/build/esm/api.js


const SENTRY_API_VERSION = "7";
function getBaseApiEndpoint(dsn) {
  const protocol = dsn.protocol ? `${dsn.protocol}:` : "";
  const port = dsn.port ? `:${dsn.port}` : "";
  return `${protocol}//${dsn.host}${port}${dsn.path ? `/${dsn.path}` : ""}/api/`;
}
function _getIngestEndpoint(dsn) {
  return `${getBaseApiEndpoint(dsn)}${dsn.projectId}/envelope/`;
}
function _encodedAuth(dsn, sdkInfo) {
  const params = {
    sentry_version: SENTRY_API_VERSION
  };
  if (dsn.publicKey) {
    params.sentry_key = dsn.publicKey;
  }
  if (sdkInfo) {
    params.sentry_client = `${sdkInfo.name}/${sdkInfo.version}`;
  }
  return new URLSearchParams(params).toString();
}
function getEnvelopeEndpointWithUrlEncodedAuth(dsn, tunnel, sdkInfo) {
  return tunnel ? tunnel : `${_getIngestEndpoint(dsn)}?${_encodedAuth(dsn, sdkInfo)}`;
}
function getReportDialogEndpoint(dsnLike, dialogOptions) {
  const dsn = makeDsn(dsnLike);
  if (!dsn) {
    return "";
  }
  const endpoint = `${getBaseApiEndpoint(dsn)}embed/error-page/`;
  let encodedOptions = `dsn=${dsnToString(dsn)}`;
  for (const key in dialogOptions) {
    if (key === "dsn") {
      continue;
    }
    if (key === "onClose") {
      continue;
    }
    if (key === "user") {
      const user = dialogOptions.user;
      if (!user) {
        continue;
      }
      if (user.name) {
        encodedOptions += `&name=${encodeURIComponent(user.name)}`;
      }
      if (user.email) {
        encodedOptions += `&email=${encodeURIComponent(user.email)}`;
      }
    } else {
      encodedOptions += `&${encodeURIComponent(key)}=${encodeURIComponent(dialogOptions[key])}`;
    }
  }
  return `${endpoint}?${encodedOptions}`;
}


//# sourceMappingURL=api.js.map

;// ./node_modules/@sentry/core/build/esm/constants.js
const constants_DEFAULT_ENVIRONMENT = "production";
const DEV_ENVIRONMENT = "development";


//# sourceMappingURL=constants.js.map

;// ./node_modules/@sentry/core/build/esm/utils/dsn.js



const ORG_ID_REGEX = /^o(\d+)\./;
const DSN_REGEX = /^(?:(\w+):)\/\/(?:(\w+)(?::(\w+)?)?@)((?:\[[:.%\w]+\]|[\w.-]+))(?::(\d+))?\/(.+)/;
function isValidProtocol(protocol) {
  return protocol === "http" || protocol === "https";
}
function dsn_dsnToString(dsn, withPassword = false) {
  const { host, path, pass, port, projectId, protocol, publicKey } = dsn;
  return `${protocol}://${publicKey}${withPassword && pass ? `:${pass}` : ""}@${host}${port ? `:${port}` : ""}/${path ? `${path}/` : path}${projectId}`;
}
function dsnFromString(str) {
  const match = DSN_REGEX.exec(str);
  if (!match) {
    debug_logger_consoleSandbox(() => {
      console.error(`Invalid Sentry Dsn: ${str}`);
    });
    return void 0;
  }
  const [protocol, publicKey, pass = "", host = "", port = "", lastPath = ""] = match.slice(1);
  let path = "";
  let projectId = lastPath;
  const split = projectId.split("/");
  if (split.length > 1) {
    path = split.slice(0, -1).join("/");
    projectId = split.pop();
  }
  if (projectId) {
    const projectMatch = projectId.match(/^\d+/);
    if (projectMatch) {
      projectId = projectMatch[0];
    }
  }
  return dsnFromComponents({ host, pass, path, projectId, port, protocol, publicKey });
}
function dsnFromComponents(components) {
  return {
    protocol: components.protocol,
    publicKey: components.publicKey || "",
    pass: components.pass || "",
    host: components.host,
    port: components.port || "",
    path: components.path || "",
    projectId: components.projectId
  };
}
function validateDsn(dsn) {
  if (!debug_build_DEBUG_BUILD) {
    return true;
  }
  const { port, projectId, protocol } = dsn;
  const requiredComponents = ["protocol", "publicKey", "host", "projectId"];
  const hasMissingRequiredComponent = requiredComponents.find((component) => {
    if (!dsn[component]) {
      debug_logger_debug.error(`Invalid Sentry Dsn: ${component} missing`);
      return true;
    }
    return false;
  });
  if (hasMissingRequiredComponent) {
    return false;
  }
  if (!projectId.match(/^\d+$/)) {
    debug_logger_debug.error(`Invalid Sentry Dsn: Invalid projectId ${projectId}`);
    return false;
  }
  if (!isValidProtocol(protocol)) {
    debug_logger_debug.error(`Invalid Sentry Dsn: Invalid protocol ${protocol}`);
    return false;
  }
  if (port && isNaN(parseInt(port, 10))) {
    debug_logger_debug.error(`Invalid Sentry Dsn: Invalid port ${port}`);
    return false;
  }
  return true;
}
function extractOrgIdFromDsnHost(host) {
  const match = host.match(ORG_ID_REGEX);
  return match?.[1];
}
function extractOrgIdFromClient(client) {
  const options = client.getOptions();
  const { host } = client.getDsn() || {};
  let org_id;
  if (options.orgId) {
    org_id = String(options.orgId);
  } else if (host) {
    org_id = extractOrgIdFromDsnHost(host);
  }
  return org_id;
}
function dsn_makeDsn(from) {
  const components = typeof from === "string" ? dsnFromString(from) : dsnFromComponents(from);
  if (!components || !validateDsn(components)) {
    return void 0;
  }
  return components;
}


//# sourceMappingURL=dsn.js.map

;// ./node_modules/@sentry/core/build/esm/utils/envelope.js






function envelope_createEnvelope(headers, items = []) {
  return [headers, items];
}
function addItemToEnvelope(envelope, newItem) {
  const [headers, items] = envelope;
  return [headers, [...items, newItem]];
}
function forEachEnvelopeItem(envelope, callback) {
  const envelopeItems = envelope[1];
  for (const envelopeItem of envelopeItems) {
    const envelopeItemType = envelopeItem[0].type;
    const result = callback(envelopeItem, envelopeItemType);
    if (result) {
      return true;
    }
  }
  return false;
}
function envelopeContainsItemType(envelope, types) {
  return forEachEnvelopeItem(envelope, (_, type) => types.includes(type));
}
function encodeUTF8(input) {
  const carrier = carrier_getSentryCarrier(worldwide_GLOBAL_OBJ);
  return carrier.encodePolyfill ? carrier.encodePolyfill(input) : new TextEncoder().encode(input);
}
function decodeUTF8(input) {
  const carrier = getSentryCarrier(GLOBAL_OBJ);
  return carrier.decodePolyfill ? carrier.decodePolyfill(input) : new TextDecoder().decode(input);
}
function serializeEnvelope(envelope) {
  const [envHeaders, items] = envelope;
  let parts = JSON.stringify(envHeaders);
  function append(next) {
    if (typeof parts === "string") {
      parts = typeof next === "string" ? parts + next : [encodeUTF8(parts), next];
    } else {
      parts.push(typeof next === "string" ? encodeUTF8(next) : next);
    }
  }
  for (const item of items) {
    const [itemHeaders, payload] = item;
    append(`
${JSON.stringify(itemHeaders)}
`);
    if (typeof payload === "string" || payload instanceof Uint8Array) {
      append(payload);
    } else {
      let stringifiedPayload;
      try {
        stringifiedPayload = JSON.stringify(payload);
      } catch {
        stringifiedPayload = JSON.stringify(normalize(payload));
      }
      append(stringifiedPayload);
    }
  }
  return typeof parts === "string" ? parts : concatBuffers(parts);
}
function concatBuffers(buffers) {
  const totalLength = buffers.reduce((acc, buf) => acc + buf.length, 0);
  const merged = new Uint8Array(totalLength);
  let offset = 0;
  for (const buffer of buffers) {
    merged.set(buffer, offset);
    offset += buffer.length;
  }
  return merged;
}
function parseEnvelope(env) {
  let buffer = typeof env === "string" ? encodeUTF8(env) : env;
  function readBinary(length) {
    const bin = buffer.subarray(0, length);
    buffer = buffer.subarray(length + 1);
    return bin;
  }
  function readJson() {
    let i = buffer.indexOf(10);
    if (i < 0) {
      i = buffer.length;
    }
    return JSON.parse(decodeUTF8(readBinary(i)));
  }
  const envelopeHeader = readJson();
  const items = [];
  while (buffer.length) {
    const itemHeader = readJson();
    const binaryLength = typeof itemHeader.length === "number" ? itemHeader.length : void 0;
    items.push([itemHeader, binaryLength ? readBinary(binaryLength) : readJson()]);
  }
  return [envelopeHeader, items];
}
function envelope_createSpanEnvelopeItem(spanJson) {
  const spanHeaders = {
    type: "span"
  };
  return [spanHeaders, spanJson];
}
function createAttachmentEnvelopeItem(attachment) {
  const buffer = typeof attachment.data === "string" ? encodeUTF8(attachment.data) : attachment.data;
  return [
    {
      type: "attachment",
      length: buffer.length,
      filename: attachment.filename,
      content_type: attachment.contentType,
      attachment_type: attachment.attachmentType
    },
    buffer
  ];
}
const DATA_CATEGORY_OVERRIDES = {
  sessions: "session",
  event: "error",
  client_report: "internal",
  user_report: "default",
  profile_chunk: "profile",
  replay_event: "replay",
  replay_recording: "replay",
  check_in: "monitor",
  raw_security: "security",
  log: "log_item",
  trace_metric: "metric"
};
function _isOverriddenType(type) {
  return type in DATA_CATEGORY_OVERRIDES;
}
function envelopeItemTypeToDataCategory(type) {
  return _isOverriddenType(type) ? DATA_CATEGORY_OVERRIDES[type] : type;
}
function getSdkMetadataForEnvelopeHeader(metadataOrEvent) {
  if (!metadataOrEvent?.sdk) {
    return;
  }
  const { name, version } = metadataOrEvent.sdk;
  return { name, version };
}
function createEventEnvelopeHeaders(event, sdkInfo, tunnel, dsn) {
  const dynamicSamplingContext = event.sdkProcessingMetadata?.dynamicSamplingContext;
  return {
    event_id: event.event_id,
    sent_at: new Date(randomSafeContext_safeDateNow()).toISOString(),
    ...sdkInfo && { sdk: sdkInfo },
    ...!!tunnel && dsn && { dsn: dsn_dsnToString(dsn) },
    ...dynamicSamplingContext && {
      trace: dynamicSamplingContext
    }
  };
}


//# sourceMappingURL=envelope.js.map

;// ./node_modules/@sentry/core/build/esm/envelope.js








function _enhanceEventWithSdkInfo(event, newSdkInfo) {
  if (!newSdkInfo) {
    return event;
  }
  const eventSdkInfo = event.sdk || {};
  event.sdk = {
    ...eventSdkInfo,
    name: eventSdkInfo.name || newSdkInfo.name,
    version: eventSdkInfo.version || newSdkInfo.version,
    integrations: [...event.sdk?.integrations || [], ...newSdkInfo.integrations || []],
    packages: [...event.sdk?.packages || [], ...newSdkInfo.packages || []],
    settings: event.sdk?.settings || newSdkInfo.settings ? {
      ...event.sdk?.settings,
      ...newSdkInfo.settings
    } : void 0
  };
  return event;
}
function createSessionEnvelope(session, dsn, metadata, tunnel) {
  const sdkInfo = getSdkMetadataForEnvelopeHeader(metadata);
  const envelopeHeaders = {
    sent_at: new Date(randomSafeContext_safeDateNow()).toISOString(),
    ...sdkInfo && { sdk: sdkInfo },
    ...!!tunnel && dsn && { dsn: dsn_dsnToString(dsn) }
  };
  const envelopeItem = "aggregates" in session ? [{ type: "sessions" }, session] : [{ type: "session" }, session.toJSON()];
  return envelope_createEnvelope(envelopeHeaders, [envelopeItem]);
}
function createEventEnvelope(event, dsn, metadata, tunnel) {
  const sdkInfo = getSdkMetadataForEnvelopeHeader(metadata);
  const eventType = event.type && event.type !== "replay_event" ? event.type : "event";
  _enhanceEventWithSdkInfo(event, metadata?.sdk);
  const envelopeHeaders = createEventEnvelopeHeaders(event, sdkInfo, tunnel, dsn);
  delete event.sdkProcessingMetadata;
  const eventItem = [{ type: eventType }, event];
  return envelope_createEnvelope(envelopeHeaders, [eventItem]);
}
function createSpanEnvelope(spans, client) {
  function dscHasRequiredProps(dsc2) {
    return !!dsc2.trace_id && !!dsc2.public_key;
  }
  const dsc = getDynamicSamplingContextFromSpan(spans[0]);
  const dsn = client?.getDsn();
  const tunnel = client?.getOptions().tunnel;
  const headers = {
    sent_at: new Date(safeDateNow()).toISOString(),
    ...dscHasRequiredProps(dsc) && { trace: dsc },
    ...!!tunnel && dsn && { dsn: dsnToString(dsn) }
  };
  const { beforeSendSpan, ignoreSpans } = client?.getOptions() || {};
  const filteredSpans = ignoreSpans?.length ? spans.filter((span) => {
    const json = spanToJSON(span);
    return !shouldIgnoreSpan({ description: json.description, op: json.op, attributes: json.data }, ignoreSpans);
  }) : spans;
  const droppedSpans = spans.length - filteredSpans.length;
  if (droppedSpans) {
    client?.recordDroppedEvent("before_send", "span", droppedSpans);
  }
  const convertToSpanJSON = beforeSendSpan ? (span) => {
    const spanJson = spanToJSON(span);
    const processedSpan = !isStreamedBeforeSendSpanCallback(beforeSendSpan) ? beforeSendSpan(spanJson) : spanJson;
    if (!processedSpan) {
      showSpanDropWarning();
      return spanJson;
    }
    return processedSpan;
  } : spanToJSON;
  const items = [];
  for (const span of filteredSpans) {
    const spanJson = convertToSpanJSON(span);
    if (spanJson) {
      items.push(createSpanEnvelopeItem(spanJson));
    }
  }
  return createEnvelope(headers, items);
}


//# sourceMappingURL=envelope.js.map

;// ./node_modules/@sentry/core/build/esm/utils/env.js
function isBrowserBundle() {
  return typeof __SENTRY_BROWSER_BUNDLE__ !== "undefined" && !!__SENTRY_BROWSER_BUNDLE__;
}
function getSDKSource() {
  /*! __SENTRY_SDK_SOURCE__ */
  return "npm";
}


//# sourceMappingURL=env.js.map

;// ./node_modules/@sentry/core/build/esm/utils/node.js


function isNodeEnv() {
  return !isBrowserBundle() && Object.prototype.toString.call(typeof process !== "undefined" ? process : 0) === "[object process]";
}
function dynamicRequire(mod, request) {
  return mod.require(request);
}
function loadModule(moduleName, existingModule = module) {
  let mod;
  try {
    mod = dynamicRequire(existingModule, moduleName);
  } catch {
  }
  if (!mod) {
    try {
      const { cwd } = dynamicRequire(existingModule, "process");
      mod = dynamicRequire(existingModule, `${cwd()}/node_modules/${moduleName}`);
    } catch {
    }
  }
  return mod;
}


//# sourceMappingURL=node.js.map

;// ./node_modules/@sentry/core/build/esm/utils/isBrowser.js



function isBrowser() {
  return typeof window !== "undefined" && (!isNodeEnv() || isElectronNodeRenderer());
}
function isElectronNodeRenderer() {
  const process = worldwide_GLOBAL_OBJ.process;
  return process?.type === "renderer";
}


//# sourceMappingURL=isBrowser.js.map

;// ./node_modules/@sentry/core/build/esm/logs/envelope.js




function createLogContainerEnvelopeItem(items, inferUserData) {
  const inferSetting = inferUserData ? "auto" : "never";
  return [
    {
      type: "log",
      item_count: items.length,
      content_type: "application/vnd.sentry.items.log+json"
    },
    {
      version: 2,
      ...isBrowser() && {
        ingest_settings: { infer_ip: inferSetting, infer_user_agent: inferSetting }
      },
      items
    }
  ];
}
function createLogEnvelope(logs, metadata, tunnel, dsn, inferUserData) {
  const headers = {};
  if (metadata?.sdk) {
    headers.sdk = {
      name: metadata.sdk.name,
      version: metadata.sdk.version
    };
  }
  if (!!tunnel && !!dsn) {
    headers.dsn = dsn_dsnToString(dsn);
  }
  return envelope_createEnvelope(headers, [createLogContainerEnvelopeItem(logs, inferUserData)]);
}


//# sourceMappingURL=envelope.js.map

;// ./node_modules/@sentry/core/build/esm/logs/internal.js














const MAX_LOG_BUFFER_SIZE = 100;
function setLogAttribute(logAttributes, key, value, setEvenIfPresent = true) {
  if (value && (!logAttributes[key] || setEvenIfPresent)) {
    logAttributes[key] = value;
  }
}
function _INTERNAL_captureSerializedLog(client, serializedLog) {
  const bufferMap = _getBufferMap();
  const logBuffer = _INTERNAL_getLogBuffer(client);
  if (logBuffer === void 0) {
    bufferMap.set(client, [serializedLog]);
  } else {
    if (logBuffer.length >= MAX_LOG_BUFFER_SIZE) {
      _INTERNAL_flushLogsBuffer(client, logBuffer);
      bufferMap.set(client, [serializedLog]);
    } else {
      bufferMap.set(client, [...logBuffer, serializedLog]);
    }
  }
}
function _INTERNAL_captureLog(beforeLog, currentScope = getCurrentScope(), captureSerializedLog = _INTERNAL_captureSerializedLog) {
  const client = currentScope?.getClient() ?? getClient();
  if (!client) {
    DEBUG_BUILD && debug.warn("No client available to capture log.");
    return;
  }
  const { release, environment, enableLogs = false, beforeSendLog } = client.getOptions();
  if (!enableLogs) {
    DEBUG_BUILD && debug.warn("logging option not enabled, log will not be captured.");
    return;
  }
  const [, traceContext] = _getTraceInfoFromScope(client, currentScope);
  const processedLogAttributes = {
    ...beforeLog.attributes
  };
  const {
    user: { id, email, username },
    attributes: scopeAttributes = {}
  } = getCombinedScopeData(getIsolationScope(), currentScope);
  setLogAttribute(processedLogAttributes, "user.id", id, false);
  setLogAttribute(processedLogAttributes, "user.email", email, false);
  setLogAttribute(processedLogAttributes, "user.name", username, false);
  setLogAttribute(processedLogAttributes, "sentry.release", release);
  setLogAttribute(processedLogAttributes, "sentry.environment", environment);
  const { name, version } = client.getSdkMetadata()?.sdk ?? {};
  setLogAttribute(processedLogAttributes, "sentry.sdk.name", name);
  setLogAttribute(processedLogAttributes, "sentry.sdk.version", version);
  const replay = client.getIntegrationByName("Replay");
  const replayId = replay?.getReplayId(true);
  setLogAttribute(processedLogAttributes, "sentry.replay_id", replayId);
  if (replayId && replay?.getRecordingMode() === "buffer") {
    setLogAttribute(processedLogAttributes, "sentry._internal.replay_is_buffering", true);
  }
  const beforeLogMessage = beforeLog.message;
  if (isParameterizedString(beforeLogMessage)) {
    const { __sentry_template_string__, __sentry_template_values__ = [] } = beforeLogMessage;
    if (__sentry_template_values__?.length) {
      processedLogAttributes["sentry.message.template"] = __sentry_template_string__;
    }
    __sentry_template_values__.forEach((param, index) => {
      processedLogAttributes[`sentry.message.parameter.${index}`] = param;
    });
  }
  const span = _getSpanForScope(currentScope);
  setLogAttribute(processedLogAttributes, "sentry.trace.parent_span_id", span?.spanContext().spanId);
  const processedLog = { ...beforeLog, attributes: processedLogAttributes };
  client.emit("beforeCaptureLog", processedLog);
  const log = beforeSendLog ? consoleSandbox(() => beforeSendLog(processedLog)) : processedLog;
  if (!log) {
    client.recordDroppedEvent("before_send", "log_item", 1);
    DEBUG_BUILD && debug.warn("beforeSendLog returned null, log will not be captured.");
    return;
  }
  const { level, message, attributes: logAttributes = {}, severityNumber } = log;
  const timestamp = timestampInSeconds();
  const sequenceAttr = getSequenceAttribute(timestamp);
  const serializedLog = {
    timestamp,
    level,
    body: _removeLoneSurrogates(String(message)),
    trace_id: traceContext?.trace_id,
    severity_number: severityNumber ?? SEVERITY_TEXT_TO_SEVERITY_NUMBER[level],
    attributes: sanitizeLogAttributes({
      ...serializeAttributes(scopeAttributes),
      ...serializeAttributes(logAttributes, true),
      [sequenceAttr.key]: sequenceAttr.value
    })
  };
  captureSerializedLog(client, serializedLog);
  client.emit("afterCaptureLog", log);
}
function _INTERNAL_flushLogsBuffer(client, maybeLogBuffer) {
  const logBuffer = maybeLogBuffer ?? _INTERNAL_getLogBuffer(client) ?? [];
  if (logBuffer.length === 0) {
    return;
  }
  const clientOptions = client.getOptions();
  const envelope = createLogEnvelope(
    logBuffer,
    clientOptions._metadata,
    clientOptions.tunnel,
    client.getDsn(),
    client.getDataCollectionOptions().userInfo
  );
  _getBufferMap().set(client, []);
  client.emit("flushLogs");
  client.sendEnvelope(envelope);
}
function _INTERNAL_getLogBuffer(client) {
  return _getBufferMap().get(client);
}
function _getBufferMap() {
  return getGlobalSingleton("clientToLogBufferMap", () => /* @__PURE__ */ new WeakMap());
}
function sanitizeLogAttributes(attributes) {
  const sanitized = {};
  for (const [key, attr] of Object.entries(attributes)) {
    const sanitizedKey = _removeLoneSurrogates(key);
    if (attr.type === "string") {
      sanitized[sanitizedKey] = { ...attr, value: _removeLoneSurrogates(attr.value) };
    } else {
      sanitized[sanitizedKey] = attr;
    }
  }
  return sanitized;
}
function _removeLoneSurrogates(str) {
  const strObj = Object(str);
  const isWellFormed = strObj["isWellFormed"];
  const toWellFormed = strObj["toWellFormed"];
  if (typeof isWellFormed === "function" && typeof toWellFormed === "function") {
    return isWellFormed.call(str) ? str : toWellFormed.call(str);
  }
  return str;
}


//# sourceMappingURL=internal.js.map

;// ./node_modules/@sentry/core/build/esm/metrics/envelope.js




function createMetricContainerEnvelopeItem(items, inferUserData) {
  const inferSetting = inferUserData ? "auto" : "never";
  return [
    {
      type: "trace_metric",
      item_count: items.length,
      content_type: "application/vnd.sentry.items.trace-metric+json"
    },
    {
      version: 2,
      ...isBrowser() && {
        ingest_settings: { infer_ip: inferSetting, infer_user_agent: inferSetting }
      },
      items
    }
  ];
}
function createMetricEnvelope(metrics, metadata, tunnel, dsn, inferUserData) {
  const headers = {};
  if (metadata?.sdk) {
    headers.sdk = {
      name: metadata.sdk.name,
      version: metadata.sdk.version
    };
  }
  if (!!tunnel && !!dsn) {
    headers.dsn = dsn_dsnToString(dsn);
  }
  return envelope_createEnvelope(headers, [createMetricContainerEnvelopeItem(metrics, inferUserData)]);
}


//# sourceMappingURL=envelope.js.map

;// ./node_modules/@sentry/core/build/esm/metrics/internal.js












const MAX_METRIC_BUFFER_SIZE = 1e3;
function setMetricAttribute(metricAttributes, key, value, setEvenIfPresent = true) {
  if (value && (setEvenIfPresent || !(key in metricAttributes))) {
    metricAttributes[key] = value;
  }
}
function _INTERNAL_captureSerializedMetric(client, serializedMetric) {
  const bufferMap = internal_getBufferMap();
  const metricBuffer = _INTERNAL_getMetricBuffer(client);
  if (metricBuffer === void 0) {
    bufferMap.set(client, [serializedMetric]);
  } else {
    if (metricBuffer.length >= MAX_METRIC_BUFFER_SIZE) {
      _INTERNAL_flushMetricsBuffer(client, metricBuffer);
      bufferMap.set(client, [serializedMetric]);
    } else {
      bufferMap.set(client, [...metricBuffer, serializedMetric]);
    }
  }
}
function _enrichMetricAttributes(beforeMetric, client, user) {
  const { release, environment } = client.getOptions();
  const processedMetricAttributes = {
    ...beforeMetric.attributes
  };
  setMetricAttribute(processedMetricAttributes, "user.id", user.id, false);
  setMetricAttribute(processedMetricAttributes, "user.email", user.email, false);
  setMetricAttribute(processedMetricAttributes, "user.name", user.username, false);
  setMetricAttribute(processedMetricAttributes, "sentry.release", release);
  setMetricAttribute(processedMetricAttributes, "sentry.environment", environment);
  const { name, version } = client.getSdkMetadata()?.sdk ?? {};
  setMetricAttribute(processedMetricAttributes, "sentry.sdk.name", name);
  setMetricAttribute(processedMetricAttributes, "sentry.sdk.version", version);
  const replay = client.getIntegrationByName("Replay");
  const replayId = replay?.getReplayId(true);
  setMetricAttribute(processedMetricAttributes, "sentry.replay_id", replayId);
  if (replayId && replay?.getRecordingMode() === "buffer") {
    setMetricAttribute(processedMetricAttributes, "sentry._internal.replay_is_buffering", true);
  }
  return {
    ...beforeMetric,
    attributes: processedMetricAttributes
  };
}
function _buildSerializedMetric(metric, client, currentScope, scopeAttributes) {
  const [, traceContext] = _getTraceInfoFromScope(client, currentScope);
  const span = _getSpanForScope(currentScope);
  const traceId = span ? span.spanContext().traceId : traceContext?.trace_id;
  const spanId = span ? span.spanContext().spanId : void 0;
  const timestamp = timestampInSeconds();
  const sequenceAttr = getSequenceAttribute(timestamp);
  return {
    timestamp,
    trace_id: traceId ?? "",
    span_id: spanId,
    name: metric.name,
    type: metric.type,
    unit: metric.unit,
    value: metric.value,
    attributes: {
      ...serializeAttributes(scopeAttributes),
      ...serializeAttributes(metric.attributes, "skip-undefined"),
      [sequenceAttr.key]: sequenceAttr.value
    }
  };
}
function _INTERNAL_captureMetric(beforeMetric, options) {
  const currentScope = options?.scope ?? getCurrentScope();
  const captureSerializedMetric = options?.captureSerializedMetric ?? _INTERNAL_captureSerializedMetric;
  const client = currentScope?.getClient() ?? getClient();
  if (!client) {
    DEBUG_BUILD && debug.warn("No client available to capture metric.");
    return;
  }
  const { _experiments, enableMetrics, beforeSendMetric } = client.getOptions();
  const metricsEnabled = enableMetrics ?? _experiments?.enableMetrics ?? true;
  if (!metricsEnabled) {
    DEBUG_BUILD && debug.warn("metrics option not enabled, metric will not be captured.");
    return;
  }
  const { user, attributes: scopeAttributes } = getCombinedScopeData(getIsolationScope(), currentScope);
  const enrichedMetric = _enrichMetricAttributes(beforeMetric, client, user);
  client.emit("processMetric", enrichedMetric);
  const beforeSendCallback = beforeSendMetric || _experiments?.beforeSendMetric;
  const processedMetric = beforeSendCallback ? beforeSendCallback(enrichedMetric) : enrichedMetric;
  if (!processedMetric) {
    DEBUG_BUILD && debug.log("`beforeSendMetric` returned `null`, will not send metric.");
    return;
  }
  const serializedMetric = _buildSerializedMetric(processedMetric, client, currentScope, scopeAttributes);
  DEBUG_BUILD && debug.log("[Metric]", serializedMetric);
  captureSerializedMetric(client, serializedMetric);
  client.emit("afterCaptureMetric", processedMetric);
}
function _INTERNAL_flushMetricsBuffer(client, maybeMetricBuffer) {
  const metricBuffer = maybeMetricBuffer ?? _INTERNAL_getMetricBuffer(client) ?? [];
  if (metricBuffer.length === 0) {
    return;
  }
  const clientOptions = client.getOptions();
  const envelope = createMetricEnvelope(
    metricBuffer,
    clientOptions._metadata,
    clientOptions.tunnel,
    client.getDsn(),
    client.getDataCollectionOptions().userInfo
  );
  internal_getBufferMap().set(client, []);
  client.emit("flushMetrics");
  client.sendEnvelope(envelope);
}
function _INTERNAL_getMetricBuffer(client) {
  return internal_getBufferMap().get(client);
}
function internal_getBufferMap() {
  return getGlobalSingleton("clientToMetricBufferMap", () => /* @__PURE__ */ new WeakMap());
}


//# sourceMappingURL=internal.js.map

;// ./node_modules/@sentry/core/build/esm/utils/baggage.js




const SENTRY_BAGGAGE_KEY_PREFIX = "sentry-";
const SENTRY_BAGGAGE_KEY_PREFIX_REGEX = /^sentry-/;
const MAX_BAGGAGE_STRING_LENGTH = 8192;
function baggageHeaderToDynamicSamplingContext(baggageHeader) {
  const baggageObject = parseBaggageHeader(baggageHeader);
  if (!baggageObject) {
    return void 0;
  }
  const dynamicSamplingContext = Object.entries(baggageObject).reduce((acc, [key, value]) => {
    if (key.startsWith(SENTRY_BAGGAGE_KEY_PREFIX)) {
      const nonPrefixedKey = key.slice(SENTRY_BAGGAGE_KEY_PREFIX.length);
      acc[nonPrefixedKey] = value;
    }
    return acc;
  }, {});
  if (Object.keys(dynamicSamplingContext).length > 0) {
    return dynamicSamplingContext;
  } else {
    return void 0;
  }
}
function baggage_dynamicSamplingContextToSentryBaggageHeader(dynamicSamplingContext) {
  if (!dynamicSamplingContext) {
    return void 0;
  }
  const sentryPrefixedDSC = Object.entries(dynamicSamplingContext).reduce(
    (acc, [dscKey, dscValue]) => {
      if (dscValue) {
        acc[`${SENTRY_BAGGAGE_KEY_PREFIX}${dscKey}`] = dscValue;
      }
      return acc;
    },
    {}
  );
  return objectToBaggageHeader(sentryPrefixedDSC);
}
function parseBaggageHeader(baggageHeader) {
  if (!baggageHeader || !is_isString(baggageHeader) && !Array.isArray(baggageHeader)) {
    return void 0;
  }
  if (Array.isArray(baggageHeader)) {
    return baggageHeader.reduce((acc, curr) => {
      const currBaggageObject = baggageHeaderToObject(curr);
      Object.entries(currBaggageObject).forEach(([key, value]) => {
        acc[key] = value;
      });
      return acc;
    }, {});
  }
  return baggageHeaderToObject(baggageHeader);
}
function baggageHeaderToObject(baggageHeader) {
  return baggageHeader.split(",").map((baggageEntry) => {
    const eqIdx = baggageEntry.indexOf("=");
    if (eqIdx === -1) {
      return [];
    }
    const key = baggageEntry.slice(0, eqIdx);
    const value = baggageEntry.slice(eqIdx + 1);
    return [key, value].map((keyOrValue) => {
      try {
        return decodeURIComponent(keyOrValue.trim());
      } catch {
        return;
      }
    });
  }).reduce((acc, [key, value]) => {
    if (key && value) {
      acc[key] = value;
    }
    return acc;
  }, {});
}
function objectToBaggageHeader(object) {
  if (Object.keys(object).length === 0) {
    return void 0;
  }
  return Object.entries(object).reduce((baggageHeader, [objectKey, objectValue], currentIndex) => {
    const baggageEntry = `${encodeURIComponent(objectKey)}=${encodeURIComponent(objectValue)}`;
    const newBaggageHeader = currentIndex === 0 ? baggageEntry : `${baggageHeader},${baggageEntry}`;
    if (newBaggageHeader.length > MAX_BAGGAGE_STRING_LENGTH) {
      DEBUG_BUILD && debug.warn(
        `Not adding key: ${objectKey} with val: ${objectValue} to baggage header due to exceeding baggage size limits.`
      );
      return baggageHeader;
    } else {
      return newBaggageHeader;
    }
  }, "");
}
function mergeBaggageHeaders(existing, incoming) {
  if (!existing) {
    return incoming;
  }
  const existingEntries = parseBaggageHeader(existing);
  const incomingEntries = parseBaggageHeader(incoming);
  if (!incomingEntries) {
    return existing;
  }
  const merged = {};
  let hasNewSentryEntries = false;
  const newSentryEntries = {};
  const newNonSentryEntries = {};
  for (const [key, value] of Object.entries(incomingEntries)) {
    if (key.startsWith(SENTRY_BAGGAGE_KEY_PREFIX)) {
      newSentryEntries[key] = value;
      hasNewSentryEntries = true;
    } else {
      newNonSentryEntries[key] = value;
    }
  }
  if (existingEntries) {
    for (const [key, value] of Object.entries(existingEntries)) {
      if (!hasNewSentryEntries || !key.startsWith(SENTRY_BAGGAGE_KEY_PREFIX)) {
        merged[key] = value;
      }
    }
  }
  if (hasNewSentryEntries) {
    Object.assign(merged, newSentryEntries);
  }
  for (const [key, value] of Object.entries(newNonSentryEntries)) {
    merged[key] ?? (merged[key] = value);
  }
  return objectToBaggageHeader(merged);
}


//# sourceMappingURL=baggage.js.map

;// ./node_modules/@sentry/core/build/esm/utils/hasSpansEnabled.js


function hasSpansEnabled(maybeOptions) {
  if (typeof __SENTRY_TRACING__ === "boolean" && !__SENTRY_TRACING__) {
    return false;
  }
  const options = maybeOptions || currentScopes_getClient()?.getOptions();
  return !!options && // Note: This check is `!= null`, meaning "nullish". `0` is not "nullish", `undefined` and `null` are. (This comment was brought to you by 15 minutes of questioning life)
  (options.tracesSampleRate != null || !!options.tracesSampler);
}


//# sourceMappingURL=hasSpansEnabled.js.map

;// ./node_modules/@sentry/core/build/esm/tracing/sentryNonRecordingSpan.js




const NON_RECORDING_SPAN_FIELD = /* @__PURE__ */ Symbol.for("sentry.nonRecordingSpan");
class SentryNonRecordingSpan {
  constructor(spanContext = {}) {
    this._traceId = spanContext.traceId || generateTraceId();
    this._spanId = spanContext.spanId || generateSpanId();
    this.dropReason = spanContext.dropReason;
    addNonEnumerableProperty(this, NON_RECORDING_SPAN_FIELD, true);
  }
  /** @inheritdoc */
  spanContext() {
    return {
      spanId: this._spanId,
      traceId: this._traceId,
      traceFlags: TRACE_FLAG_NONE
    };
  }
  /** @inheritdoc */
  end(_timestamp) {
  }
  /** @inheritdoc */
  setAttribute(_key, _value) {
    return this;
  }
  /** @inheritdoc */
  setAttributes(_values) {
    return this;
  }
  /** @inheritdoc */
  setStatus(_status) {
    return this;
  }
  /** @inheritdoc */
  updateName(_name) {
    return this;
  }
  /** @inheritdoc */
  isRecording() {
    return false;
  }
  /** @inheritdoc */
  addEvent(_name, _attributesOrStartTime, _startTime) {
    return this;
  }
  /** @inheritDoc */
  addLink(_link) {
    return this;
  }
  /** @inheritDoc */
  addLinks(_links) {
    return this;
  }
  /**
   * This should generally not be used,
   * but we need it for being compliant with the OTEL Span interface.
   *
   * @hidden
   * @internal
   */
  recordException(_exception, _time) {
  }
}
function spanIsNonRecordingSpan(span) {
  return !!span && span[NON_RECORDING_SPAN_FIELD] === true;
}


//# sourceMappingURL=sentryNonRecordingSpan.js.map

;// ./node_modules/@sentry/core/build/esm/tracing/dynamicSamplingContext.js











const FROZEN_DSC_FIELD = "_frozenDsc";
function freezeDscOnSpan(span, dsc) {
  const spanWithMaybeDsc = span;
  addNonEnumerableProperty(spanWithMaybeDsc, FROZEN_DSC_FIELD, dsc);
}
function getDynamicSamplingContextFromClient(trace_id, client) {
  const options = client.getOptions();
  const { publicKey: public_key } = client.getDsn() || {};
  const dsc = {
    environment: options.environment || constants_DEFAULT_ENVIRONMENT,
    release: options.release,
    public_key,
    trace_id,
    org_id: extractOrgIdFromClient(client)
  };
  client.emit("createDsc", dsc);
  return dsc;
}
function getDynamicSamplingContextFromScope(client, scope) {
  const propagationContext = scope.getPropagationContext();
  return propagationContext.dsc || getDynamicSamplingContextFromClient(propagationContext.traceId, client);
}
function dynamicSamplingContext_getDynamicSamplingContextFromSpan(span) {
  const client = currentScopes_getClient();
  if (!client) {
    return {};
  }
  const rootSpan = getRootSpan(span);
  const rootSpanJson = spanUtils_spanToJSON(rootSpan);
  const rootSpanAttributes = rootSpanJson.data;
  const traceState = rootSpan.spanContext().traceState;
  const rootSpanSampleRate = traceState?.get("sentry.sample_rate") ?? rootSpanAttributes[SEMANTIC_ATTRIBUTE_SENTRY_SAMPLE_RATE] ?? rootSpanAttributes[SEMANTIC_ATTRIBUTE_SENTRY_PREVIOUS_TRACE_SAMPLE_RATE];
  function applyLocalSampleRateToDsc(dsc2) {
    if (typeof rootSpanSampleRate === "number" || typeof rootSpanSampleRate === "string") {
      dsc2.sample_rate = `${rootSpanSampleRate}`;
    }
    return dsc2;
  }
  const frozenDsc = rootSpan[FROZEN_DSC_FIELD];
  if (frozenDsc) {
    return applyLocalSampleRateToDsc(frozenDsc);
  }
  const isNonRecordingRoot = spanIsNonRecordingSpan(rootSpan);
  const isIgnoredRoot = isNonRecordingRoot && rootSpan.dropReason === "ignored";
  if (isNonRecordingRoot && (!hasSpansEnabled(client.getOptions()) || isIgnoredRoot)) {
    const capturedScope = utils_getCapturedScopesOnSpan(rootSpan).scope;
    if (capturedScope) {
      const dsc2 = { ...getDynamicSamplingContextFromScope(client, capturedScope) };
      if (isIgnoredRoot) {
        dsc2.sampled = "false";
      }
      return applyLocalSampleRateToDsc(dsc2);
    }
  }
  const traceStateDsc = traceState?.get("sentry.dsc");
  const dscOnTraceState = traceStateDsc && baggageHeaderToDynamicSamplingContext(traceStateDsc);
  if (dscOnTraceState) {
    return applyLocalSampleRateToDsc(dscOnTraceState);
  }
  const dsc = getDynamicSamplingContextFromClient(span.spanContext().traceId, client);
  const source = rootSpanAttributes[semanticAttributes_SEMANTIC_ATTRIBUTE_SENTRY_SOURCE] ?? rootSpanAttributes["sentry.segment.name.source"];
  const name = rootSpanJson.description;
  if (source !== "url" && name) {
    dsc.transaction = name;
  }
  if (hasSpansEnabled()) {
    dsc.sampled = String(spanIsSampled(rootSpan));
    dsc.sample_rand = // In OTEL we store the sample rand on the trace state because we cannot access scopes for NonRecordingSpans
    // The Sentry OTEL SpanSampler takes care of writing the sample rand on the root span
    traceState?.get("sentry.sample_rand") ?? // On all other platforms we can actually get the scopes from a root span (we use this as a fallback)
    utils_getCapturedScopesOnSpan(rootSpan).scope?.getPropagationContext().sampleRand.toString();
  }
  applyLocalSampleRateToDsc(dsc);
  client.emit("createDsc", dsc, rootSpan);
  return dsc;
}
function spanToBaggageHeader(span) {
  const dsc = dynamicSamplingContext_getDynamicSamplingContextFromSpan(span);
  return dynamicSamplingContextToSentryBaggageHeader(dsc);
}


//# sourceMappingURL=dynamicSamplingContext.js.map

;// ./node_modules/@sentry/core/build/esm/tracing/spans/beforeSendSpan.js


function withStreamedSpan(callback) {
  addNonEnumerableProperty(callback, "_streamed", true);
  return callback;
}
function beforeSendSpan_isStreamedBeforeSendSpanCallback(callback) {
  return !!callback && typeof callback === "function" && "_streamed" in callback && !!callback._streamed;
}


//# sourceMappingURL=beforeSendSpan.js.map

;// ./node_modules/@sentry/core/build/esm/tracing/spans/hasSpanStreamingEnabled.js
function hasSpanStreamingEnabled(client) {
  return client.getOptions().traceLifecycle === "stream";
}


//# sourceMappingURL=hasSpanStreamingEnabled.js.map

;// ./node_modules/@sentry/core/build/esm/tracing/spans/spanJsonToStreamedSpan.js


function spanJsonToSerializedStreamedSpan(span) {
  const streamedSpan = {
    trace_id: span.trace_id,
    span_id: span.span_id,
    parent_span_id: span.parent_span_id,
    name: span.description || "",
    start_timestamp: span.start_timestamp,
    end_timestamp: span.timestamp || span.start_timestamp,
    status: !span.status || span.status === "ok" || span.status === "cancelled" ? "ok" : "error",
    is_segment: false,
    attributes: { ...span.data },
    links: span.links
  };
  return spanUtils_streamedSpanJsonToSerializedSpan(streamedSpan);
}


//# sourceMappingURL=spanJsonToStreamedSpan.js.map

;// ./node_modules/@sentry/core/build/esm/tracing/spans/extractGenAiSpans.js




function extractGenAiSpansFromEvent(event, client) {
  if (event.type !== "transaction" || !event.spans?.length || !event.sdkProcessingMetadata?.hasGenAiSpans || client.getOptions().streamGenAiSpans === false || hasSpanStreamingEnabled(client)) {
    return void 0;
  }
  const genAiSpans = [];
  const remainingSpans = [];
  for (const span of event.spans) {
    if (span.op?.startsWith("gen_ai.")) {
      genAiSpans.push(spanJsonToSerializedStreamedSpan(span));
    } else {
      remainingSpans.push(span);
    }
  }
  if (genAiSpans.length === 0) {
    return void 0;
  }
  event.spans = remainingSpans;
  const inferSetting = client.getDataCollectionOptions().userInfo ? "auto" : "never";
  return [
    { type: "span", item_count: genAiSpans.length, content_type: "application/vnd.sentry.items.span.v2+json" },
    {
      version: 2,
      ...isBrowser() && {
        ingest_settings: { infer_ip: inferSetting, infer_user_agent: inferSetting }
      },
      items: genAiSpans
    }
  ];
}


//# sourceMappingURL=extractGenAiSpans.js.map

;// ./node_modules/@sentry/core/build/esm/utils/syncpromise.js


const STATE_PENDING = 0;
const STATE_RESOLVED = 1;
const STATE_REJECTED = 2;
function resolvedSyncPromise(value) {
  return new SyncPromise((resolve) => {
    resolve(value);
  });
}
function rejectedSyncPromise(reason) {
  return new SyncPromise((_, reject) => {
    reject(reason);
  });
}
class SyncPromise {
  constructor(executor) {
    this._state = STATE_PENDING;
    this._handlers = [];
    this._runExecutor(executor);
  }
  /** @inheritdoc */
  then(onfulfilled, onrejected) {
    return new SyncPromise((resolve, reject) => {
      this._handlers.push([
        false,
        (result) => {
          if (!onfulfilled) {
            resolve(result);
          } else {
            try {
              resolve(onfulfilled(result));
            } catch (e) {
              reject(e);
            }
          }
        },
        (reason) => {
          if (!onrejected) {
            reject(reason);
          } else {
            try {
              resolve(onrejected(reason));
            } catch (e) {
              reject(e);
            }
          }
        }
      ]);
      this._executeHandlers();
    });
  }
  /** @inheritdoc */
  catch(onrejected) {
    return this.then((val) => val, onrejected);
  }
  /** @inheritdoc */
  finally(onfinally) {
    return new SyncPromise((resolve, reject) => {
      let val;
      let isRejected;
      return this.then(
        (value) => {
          isRejected = false;
          val = value;
          if (onfinally) {
            onfinally();
          }
        },
        (reason) => {
          isRejected = true;
          val = reason;
          if (onfinally) {
            onfinally();
          }
        }
      ).then(() => {
        if (isRejected) {
          reject(val);
          return;
        }
        resolve(val);
      });
    });
  }
  /** Excute the resolve/reject handlers. */
  _executeHandlers() {
    if (this._state === STATE_PENDING) {
      return;
    }
    const cachedHandlers = this._handlers.slice();
    this._handlers = [];
    cachedHandlers.forEach((handler) => {
      if (handler[0]) {
        return;
      }
      if (this._state === STATE_RESOLVED) {
        handler[1](this._value);
      }
      if (this._state === STATE_REJECTED) {
        handler[2](this._value);
      }
      handler[0] = true;
    });
  }
  /** Run the executor for the SyncPromise. */
  _runExecutor(executor) {
    const setResult = (state, value) => {
      if (this._state !== STATE_PENDING) {
        return;
      }
      if (is_isThenable(value)) {
        void value.then(resolve, reject);
        return;
      }
      this._state = state;
      this._value = value;
      this._executeHandlers();
    };
    const resolve = (value) => {
      setResult(STATE_RESOLVED, value);
    };
    const reject = (reason) => {
      setResult(STATE_REJECTED, reason);
    };
    try {
      executor(resolve, reject);
    } catch (e) {
      reject(e);
    }
  }
}


//# sourceMappingURL=syncpromise.js.map

;// ./node_modules/@sentry/core/build/esm/utils/timer.js
function safeUnref(timer) {
  if (typeof timer === "object" && typeof timer.unref === "function") {
    timer.unref();
  }
  return timer;
}


//# sourceMappingURL=timer.js.map

;// ./node_modules/@sentry/core/build/esm/utils/promisebuffer.js



const SENTRY_BUFFER_FULL_ERROR = /* @__PURE__ */ Symbol.for("SentryBufferFullError");
function makePromiseBuffer(limit = 100) {
  const buffer = /* @__PURE__ */ new Set();
  function isReady() {
    return buffer.size < limit;
  }
  function remove(task) {
    buffer.delete(task);
  }
  function add(taskProducer) {
    if (!isReady()) {
      return rejectedSyncPromise(SENTRY_BUFFER_FULL_ERROR);
    }
    const task = taskProducer();
    buffer.add(task);
    void task.then(
      () => remove(task),
      () => remove(task)
    );
    return task;
  }
  function drain(timeout) {
    if (!buffer.size) {
      return resolvedSyncPromise(true);
    }
    const drainPromise = Promise.allSettled(Array.from(buffer)).then(() => true);
    if (!timeout) {
      return drainPromise;
    }
    const promises = [
      drainPromise,
      new Promise((resolve) => safeUnref(setTimeout(() => resolve(false), timeout)))
    ];
    return Promise.race(promises);
  }
  return {
    get $() {
      return Array.from(buffer);
    },
    add,
    drain
  };
}


//# sourceMappingURL=promisebuffer.js.map

;// ./node_modules/@sentry/core/build/esm/utils/ratelimit.js


const DEFAULT_RETRY_AFTER = 60 * 1e3;
function parseRetryAfterHeader(header, now = randomSafeContext_safeDateNow()) {
  const headerDelay = parseInt(`${header}`, 10);
  if (!isNaN(headerDelay)) {
    return headerDelay * 1e3;
  }
  const headerDate = Date.parse(`${header}`);
  if (!isNaN(headerDate)) {
    return headerDate - now;
  }
  return DEFAULT_RETRY_AFTER;
}
function disabledUntil(limits, dataCategory) {
  return limits[dataCategory] || limits.all || 0;
}
function isRateLimited(limits, dataCategory, now = randomSafeContext_safeDateNow()) {
  return disabledUntil(limits, dataCategory) > now;
}
function updateRateLimits(limits, { statusCode, headers }, now = randomSafeContext_safeDateNow()) {
  const updatedRateLimits = {
    ...limits
  };
  const rateLimitHeader = headers?.["x-sentry-rate-limits"];
  const retryAfterHeader = headers?.["retry-after"];
  if (rateLimitHeader) {
    for (const limit of rateLimitHeader.trim().split(",")) {
      const [retryAfter, categories, , , namespaces] = limit.split(":", 5);
      const headerDelay = parseInt(retryAfter, 10);
      const delay = (!isNaN(headerDelay) ? headerDelay : 60) * 1e3;
      if (!categories) {
        updatedRateLimits.all = now + delay;
      } else {
        for (const category of categories.split(";")) {
          if (category === "metric_bucket") {
            if (!namespaces || namespaces.split(";").includes("custom")) {
              updatedRateLimits[category] = now + delay;
            }
          } else {
            updatedRateLimits[category] = now + delay;
          }
        }
      }
    }
  } else if (retryAfterHeader) {
    updatedRateLimits.all = now + parseRetryAfterHeader(retryAfterHeader, now);
  } else if (statusCode === 429) {
    updatedRateLimits.all = now + 60 * 1e3;
  }
  return updatedRateLimits;
}


//# sourceMappingURL=ratelimit.js.map

;// ./node_modules/@sentry/core/build/esm/transports/base.js






const DEFAULT_TRANSPORT_BUFFER_SIZE = 64;
function createTransport(options, makeRequest, buffer = makePromiseBuffer(
  options.bufferSize || DEFAULT_TRANSPORT_BUFFER_SIZE
)) {
  let rateLimits = {};
  const flush = (timeout) => buffer.drain(timeout);
  function send(envelope) {
    const filteredEnvelopeItems = [];
    forEachEnvelopeItem(envelope, (item, type) => {
      const dataCategory = envelopeItemTypeToDataCategory(type);
      if (isRateLimited(rateLimits, dataCategory)) {
        options.recordDroppedEvent("ratelimit_backoff", dataCategory);
      } else {
        filteredEnvelopeItems.push(item);
      }
    });
    if (filteredEnvelopeItems.length === 0) {
      return Promise.resolve({});
    }
    const filteredEnvelope = envelope_createEnvelope(envelope[0], filteredEnvelopeItems);
    const recordEnvelopeLoss = (reason) => {
      if (envelopeContainsItemType(filteredEnvelope, ["client_report"])) {
        debug_build_DEBUG_BUILD && debug_logger_debug.warn(`Dropping client report. Will not send outcomes (reason: ${reason}).`);
        return;
      }
      forEachEnvelopeItem(filteredEnvelope, (item, type) => {
        options.recordDroppedEvent(reason, envelopeItemTypeToDataCategory(type));
      });
    };
    const requestTask = () => makeRequest({ body: serializeEnvelope(filteredEnvelope) }).then(
      (response) => {
        if (response.statusCode === 413) {
          debug_build_DEBUG_BUILD && debug_logger_debug.error(
            "Sentry responded with status code 413. Envelope was discarded due to exceeding size limits."
          );
          recordEnvelopeLoss("send_error");
          return response;
        }
        if (debug_build_DEBUG_BUILD && response.statusCode !== void 0 && (response.statusCode < 200 || response.statusCode >= 300)) {
          debug_logger_debug.warn(`Sentry responded with status code ${response.statusCode} to sent event.`);
        }
        rateLimits = updateRateLimits(rateLimits, response);
        return response;
      },
      (error) => {
        recordEnvelopeLoss("network_error");
        debug_build_DEBUG_BUILD && debug_logger_debug.error("Encountered error running transport request:", error);
        throw error;
      }
    );
    return buffer.add(requestTask).then(
      (result) => result,
      (error) => {
        if (error === SENTRY_BUFFER_FULL_ERROR) {
          debug_build_DEBUG_BUILD && debug_logger_debug.error("Skipped sending event because buffer is full.");
          recordEnvelopeLoss("queue_overflow");
          return Promise.resolve({});
        } else {
          throw error;
        }
      }
    );
  }
  return {
    send,
    flush
  };
}


//# sourceMappingURL=base.js.map

;// ./node_modules/@sentry/core/build/esm/utils/clientreport.js



function createClientReportEnvelope(discarded_events, dsn, timestamp) {
  const clientReportItem = [
    { type: "client_report" },
    {
      timestamp: timestamp || dateTimestampInSeconds(),
      discarded_events
    }
  ];
  return envelope_createEnvelope(dsn ? { dsn } : {}, [clientReportItem]);
}


//# sourceMappingURL=clientreport.js.map

;// ./node_modules/@sentry/core/build/esm/utils/parseSampleRate.js
function parseSampleRate(sampleRate) {
  if (typeof sampleRate === "boolean") {
    return Number(sampleRate);
  }
  const rate = typeof sampleRate === "string" ? parseFloat(sampleRate) : sampleRate;
  if (typeof rate !== "number" || isNaN(rate) || rate < 0 || rate > 1) {
    return void 0;
  }
  return rate;
}


//# sourceMappingURL=parseSampleRate.js.map

;// ./node_modules/@sentry/core/build/esm/eventProcessors.js





function notifyEventProcessors(processors, event, hint, index = 0) {
  try {
    const result = _notifyEventProcessors(event, hint, processors, index);
    return is_isThenable(result) ? result : resolvedSyncPromise(result);
  } catch (error) {
    return rejectedSyncPromise(error);
  }
}
function _notifyEventProcessors(event, hint, processors, index) {
  const processor = processors[index];
  if (!event || !processor) {
    return event;
  }
  const result = processor({ ...event }, hint);
  debug_build_DEBUG_BUILD && result === null && debug_logger_debug.log(`Event processor "${processor.id || "?"}" dropped event`);
  if (is_isThenable(result)) {
    return result.then((final) => _notifyEventProcessors(final, hint, processors, index + 1));
  }
  return _notifyEventProcessors(result, hint, processors, index + 1);
}


//# sourceMappingURL=eventProcessors.js.map

;// ./node_modules/@sentry/core/build/esm/utils/debug-ids.js



let parsedStackResults;
let lastSentryKeysCount;
let lastNativeKeysCount;
let cachedFilenameDebugIds;
function getFilenameToDebugIdMap(stackParser) {
  const sentryDebugIdMap = worldwide_GLOBAL_OBJ._sentryDebugIds;
  const nativeDebugIdMap = worldwide_GLOBAL_OBJ._debugIds;
  if (!sentryDebugIdMap && !nativeDebugIdMap) {
    return {};
  }
  const sentryDebugIdKeys = sentryDebugIdMap ? Object.keys(sentryDebugIdMap) : [];
  const nativeDebugIdKeys = nativeDebugIdMap ? Object.keys(nativeDebugIdMap) : [];
  if (cachedFilenameDebugIds && sentryDebugIdKeys.length === lastSentryKeysCount && nativeDebugIdKeys.length === lastNativeKeysCount) {
    return cachedFilenameDebugIds;
  }
  lastSentryKeysCount = sentryDebugIdKeys.length;
  lastNativeKeysCount = nativeDebugIdKeys.length;
  cachedFilenameDebugIds = {};
  if (!parsedStackResults) {
    parsedStackResults = {};
  }
  const processDebugIds = (debugIdKeys, debugIdMap) => {
    for (const key of debugIdKeys) {
      const debugId = debugIdMap[key];
      const result = parsedStackResults?.[key];
      if (result && cachedFilenameDebugIds && debugId) {
        cachedFilenameDebugIds[result[0]] = debugId;
        if (parsedStackResults) {
          parsedStackResults[key] = [result[0], debugId];
        }
      } else if (debugId) {
        const parsedStack = stackParser(key);
        for (let i = parsedStack.length - 1; i >= 0; i--) {
          const stackFrame = parsedStack[i];
          const filename = stackFrame?.filename;
          if (filename && cachedFilenameDebugIds && parsedStackResults) {
            cachedFilenameDebugIds[filename] = debugId;
            parsedStackResults[key] = [filename, debugId];
            break;
          }
        }
      }
    }
  };
  if (sentryDebugIdMap) {
    processDebugIds(sentryDebugIdKeys, sentryDebugIdMap);
  }
  if (nativeDebugIdMap) {
    processDebugIds(nativeDebugIdKeys, nativeDebugIdMap);
  }
  return cachedFilenameDebugIds;
}
function getDebugImagesForResources(stackParser, resource_paths) {
  const filenameDebugIdMap = getFilenameToDebugIdMap(stackParser);
  if (!filenameDebugIdMap) {
    return [];
  }
  const images = [];
  for (const path of resource_paths) {
    const normalizedPath = normalizeStackTracePath(path);
    if (normalizedPath && filenameDebugIdMap[normalizedPath]) {
      images.push({
        type: "sourcemap",
        code_file: path,
        debug_id: filenameDebugIdMap[normalizedPath]
      });
    }
  }
  return images;
}


//# sourceMappingURL=debug-ids.js.map

;// ./node_modules/@sentry/core/build/esm/utils/scopeData.js





function applyScopeDataToEvent(event, data) {
  const { fingerprint, span, breadcrumbs, sdkProcessingMetadata } = data;
  applyDataToEvent(event, data);
  if (span) {
    applySpanToEvent(event, span);
  }
  applyFingerprintToEvent(event, fingerprint);
  applyBreadcrumbsToEvent(event, breadcrumbs);
  applySdkMetadataToEvent(event, sdkProcessingMetadata);
}
function mergeScopeData(data, mergeData) {
  const {
    extra,
    tags,
    attributes,
    user,
    contexts,
    level,
    sdkProcessingMetadata,
    breadcrumbs,
    fingerprint,
    eventProcessors,
    attachments,
    propagationContext,
    transactionName,
    span
  } = mergeData;
  mergeAndOverwriteScopeData(data, "extra", extra);
  mergeAndOverwriteScopeData(data, "tags", tags);
  mergeAndOverwriteScopeData(data, "attributes", attributes);
  mergeAndOverwriteScopeData(data, "user", user);
  mergeAndOverwriteScopeData(data, "contexts", contexts);
  data.sdkProcessingMetadata = merge(data.sdkProcessingMetadata, sdkProcessingMetadata, 2);
  if (level) {
    data.level = level;
  }
  if (transactionName) {
    data.transactionName = transactionName;
  }
  if (span) {
    data.span = span;
  }
  if (breadcrumbs.length) {
    data.breadcrumbs = [...data.breadcrumbs, ...breadcrumbs];
  }
  if (fingerprint.length) {
    data.fingerprint = [...data.fingerprint, ...fingerprint];
  }
  if (eventProcessors.length) {
    data.eventProcessors = [...data.eventProcessors, ...eventProcessors];
  }
  if (attachments.length) {
    data.attachments = [...data.attachments, ...attachments];
  }
  data.propagationContext = { ...data.propagationContext, ...propagationContext };
}
function mergeAndOverwriteScopeData(data, prop, mergeVal) {
  data[prop] = merge(data[prop], mergeVal, 1);
}
function scopeData_getCombinedScopeData(isolationScope, currentScope) {
  const scopeData = getGlobalScope().getScopeData();
  isolationScope && mergeScopeData(scopeData, isolationScope.getScopeData());
  currentScope && mergeScopeData(scopeData, currentScope.getScopeData());
  return scopeData;
}
function applyDataToEvent(event, data) {
  const { extra, tags, user, contexts, level, transactionName } = data;
  if (Object.keys(extra).length) {
    event.extra = { ...extra, ...event.extra };
  }
  if (Object.keys(tags).length) {
    event.tags = { ...tags, ...event.tags };
  }
  if (Object.keys(user).length) {
    event.user = { ...user, ...event.user };
  }
  if (Object.keys(contexts).length) {
    event.contexts = { ...contexts, ...event.contexts };
  }
  if (level) {
    event.level = level;
  }
  if (transactionName && event.type !== "transaction") {
    event.transaction = transactionName;
  }
}
function applyBreadcrumbsToEvent(event, breadcrumbs) {
  const mergedBreadcrumbs = [...event.breadcrumbs || [], ...breadcrumbs];
  event.breadcrumbs = mergedBreadcrumbs.length ? mergedBreadcrumbs : void 0;
}
function applySdkMetadataToEvent(event, sdkProcessingMetadata) {
  event.sdkProcessingMetadata = {
    ...event.sdkProcessingMetadata,
    ...sdkProcessingMetadata
  };
}
function applySpanToEvent(event, span) {
  event.contexts = {
    trace: spanToTraceContext(span),
    ...event.contexts
  };
  event.sdkProcessingMetadata = {
    dynamicSamplingContext: dynamicSamplingContext_getDynamicSamplingContextFromSpan(span),
    ...event.sdkProcessingMetadata
  };
  const rootSpan = getRootSpan(span);
  const transactionName = spanUtils_spanToJSON(rootSpan).description;
  if (transactionName && !event.transaction && event.type === "transaction") {
    event.transaction = transactionName;
  }
}
function applyFingerprintToEvent(event, fingerprint) {
  event.fingerprint = event.fingerprint ? Array.isArray(event.fingerprint) ? event.fingerprint : [event.fingerprint] : [];
  if (fingerprint) {
    event.fingerprint = event.fingerprint.concat(fingerprint);
  }
  if (!event.fingerprint.length) {
    delete event.fingerprint;
  }
}


//# sourceMappingURL=scopeData.js.map

;// ./node_modules/@sentry/core/build/esm/utils/prepareEvent.js











function prepareEvent(options, event, hint, scope, client, isolationScope) {
  const { normalizeDepth = 3, normalizeMaxBreadth = 1e3 } = options;
  const prepared = {
    ...event,
    event_id: event.event_id || hint.event_id || misc_uuid4(),
    timestamp: event.timestamp || dateTimestampInSeconds()
  };
  const integrations = hint.integrations || options.integrations.map((i) => i.name);
  applyClientOptions(prepared, options);
  applyIntegrationsMetadata(prepared, integrations);
  if (client) {
    client.emit("applyFrameMetadata", event);
  }
  if (event.type === void 0) {
    applyDebugIds(prepared, options.stackParser);
  }
  const finalScope = getFinalScope(scope, hint.captureContext);
  if (hint.mechanism) {
    misc_addExceptionMechanism(prepared, hint.mechanism);
  }
  const clientEventProcessors = client ? client.getEventProcessors() : [];
  const data = scopeData_getCombinedScopeData(isolationScope, finalScope);
  const attachments = [...hint.attachments || [], ...data.attachments];
  if (attachments.length) {
    hint.attachments = attachments;
  }
  applyScopeDataToEvent(prepared, data);
  const eventProcessors = [
    ...clientEventProcessors,
    // Run scope event processors _after_ all other processors
    ...data.eventProcessors
  ];
  const isInternalException = hint.data && hint.data.__sentry__ === true;
  const result = isInternalException ? resolvedSyncPromise(prepared) : notifyEventProcessors(eventProcessors, prepared, hint);
  return result.then((evt) => {
    if (evt) {
      applyDebugMeta(evt);
    }
    if (typeof normalizeDepth === "number" && normalizeDepth > 0) {
      return normalizeEvent(evt, normalizeDepth, normalizeMaxBreadth);
    }
    return evt;
  });
}
function applyClientOptions(event, options) {
  const { environment, release, dist, maxValueLength } = options;
  event.environment = event.environment || environment || constants_DEFAULT_ENVIRONMENT;
  if (!event.release && release) {
    event.release = release;
  }
  if (!event.dist && dist) {
    event.dist = dist;
  }
  const request = event.request;
  if (request?.url && maxValueLength) {
    request.url = truncate(request.url, maxValueLength);
  }
  if (maxValueLength) {
    event.exception?.values?.forEach((exception) => {
      if (exception.value) {
        exception.value = truncate(exception.value, maxValueLength);
      }
    });
  }
}
function applyDebugIds(event, stackParser) {
  const filenameDebugIdMap = getFilenameToDebugIdMap(stackParser);
  event.exception?.values?.forEach((exception) => {
    exception.stacktrace?.frames?.forEach((frame) => {
      if (frame.filename) {
        frame.debug_id = filenameDebugIdMap[frame.filename];
      }
    });
  });
}
function applyDebugMeta(event) {
  const filenameDebugIdMap = {};
  event.exception?.values?.forEach((exception) => {
    exception.stacktrace?.frames?.forEach((frame) => {
      if (frame.debug_id) {
        if (frame.abs_path) {
          filenameDebugIdMap[frame.abs_path] = frame.debug_id;
        } else if (frame.filename) {
          filenameDebugIdMap[frame.filename] = frame.debug_id;
        }
        delete frame.debug_id;
      }
    });
  });
  if (Object.keys(filenameDebugIdMap).length === 0) {
    return;
  }
  event.debug_meta = event.debug_meta || {};
  event.debug_meta.images = event.debug_meta.images || [];
  const images = event.debug_meta.images;
  Object.entries(filenameDebugIdMap).forEach(([filename, debug_id]) => {
    images.push({
      type: "sourcemap",
      code_file: filename,
      debug_id
    });
  });
}
function applyIntegrationsMetadata(event, integrationNames) {
  if (integrationNames.length > 0) {
    event.sdk = event.sdk || {};
    event.sdk.integrations = [...event.sdk.integrations || [], ...integrationNames];
  }
}
function normalizeEvent(event, depth, maxBreadth) {
  if (!event) {
    return null;
  }
  const normalized = {
    ...event,
    ...event.breadcrumbs && {
      breadcrumbs: event.breadcrumbs.map((b) => ({
        ...b,
        ...b.data && {
          data: normalize(b.data, depth, maxBreadth)
        }
      }))
    },
    ...event.user && {
      user: normalize(event.user, depth, maxBreadth)
    },
    ...event.contexts && {
      contexts: normalize(event.contexts, depth, maxBreadth)
    },
    ...event.extra && {
      extra: normalize(event.extra, depth, maxBreadth)
    }
  };
  if (event.contexts?.trace && normalized.contexts) {
    normalized.contexts.trace = event.contexts.trace;
    if (event.contexts.trace.data) {
      normalized.contexts.trace.data = normalize(event.contexts.trace.data, depth, maxBreadth);
    }
  }
  if (event.spans) {
    normalized.spans = event.spans.map((span) => {
      return {
        ...span,
        ...span.data && {
          data: normalize(span.data, depth, maxBreadth)
        }
      };
    });
  }
  if (event.contexts?.flags && normalized.contexts) {
    normalized.contexts.flags = normalize(event.contexts.flags, 3, maxBreadth);
  }
  return normalized;
}
function getFinalScope(scope, captureContext) {
  if (!captureContext) {
    return scope;
  }
  const finalScope = scope ? scope.clone() : new Scope();
  finalScope.update(captureContext);
  return finalScope;
}
function parseEventHintOrCaptureContext(hint) {
  if (!hint) {
    return void 0;
  }
  if (hintIsScopeOrFunction(hint)) {
    return { captureContext: hint };
  }
  if (hintIsScopeContext(hint)) {
    return {
      captureContext: hint
    };
  }
  return hint;
}
function hintIsScopeOrFunction(hint) {
  return hint instanceof Scope || typeof hint === "function";
}
const captureContextKeys = [
  "user",
  "level",
  "extra",
  "contexts",
  "tags",
  "fingerprint",
  "propagationContext"
];
function hintIsScopeContext(hint) {
  return Object.keys(hint).some((key) => captureContextKeys.includes(key));
}


//# sourceMappingURL=prepareEvent.js.map

;// ./node_modules/@sentry/core/build/esm/utils/should-ignore-span.js




function logIgnoredSpan(droppedSpan) {
  debug_logger_debug.log(`Ignoring span ${droppedSpan.op} - ${droppedSpan.description} because it matches \`ignoreSpans\`.`);
}
function should_ignore_span_shouldIgnoreSpan(span, ignoreSpans) {
  if (!ignoreSpans?.length) {
    return false;
  }
  for (const pattern of ignoreSpans) {
    if (isStringOrRegExp(pattern)) {
      if (span.description && isMatchingPattern(span.description, pattern)) {
        debug_build_DEBUG_BUILD && logIgnoredSpan(span);
        return true;
      }
      continue;
    }
    const hasAttributes = !!pattern.attributes && Object.keys(pattern.attributes).length > 0;
    if (!pattern.name && !pattern.op && !hasAttributes) {
      continue;
    }
    const nameMatches = pattern.name ? span.description && isMatchingPattern(span.description, pattern.name) : true;
    const opMatches = pattern.op ? span.op && isMatchingPattern(span.op, pattern.op) : true;
    const attrsMatch = pattern.attributes ? Object.entries(pattern.attributes).every(
      ([key, valuePattern]) => _matchesAttributeValue(span.attributes?.[key], valuePattern)
    ) : true;
    if (nameMatches && opMatches && attrsMatch) {
      debug_build_DEBUG_BUILD && logIgnoredSpan(span);
      return true;
    }
  }
  return false;
}
function _matchesAttributeValue(actual, pat) {
  if (typeof actual === "string" && (typeof pat === "string" || pat instanceof RegExp)) {
    return isMatchingPattern(actual, pat);
  }
  if (Array.isArray(actual) && Array.isArray(pat)) {
    return actual.length === pat.length && actual.every((v, i) => v === pat[i]);
  }
  return actual === pat;
}
function reparentChildSpans(spans, dropSpan) {
  const droppedSpanParentId = dropSpan.parent_span_id;
  const droppedSpanId = dropSpan.span_id;
  if (!droppedSpanParentId) {
    return;
  }
  for (const span of spans) {
    if (span.parent_span_id === droppedSpanId) {
      span.parent_span_id = droppedSpanParentId;
    }
  }
}
function isStringOrRegExp(value) {
  return typeof value === "string" || value instanceof RegExp;
}


//# sourceMappingURL=should-ignore-span.js.map

;// ./node_modules/@sentry/core/build/esm/utils/transactionEvent.js


function convertTransactionEventToSpanJson(event) {
  const { trace_id, parent_span_id, span_id, status, origin, data, op } = event.contexts?.trace ?? {};
  return {
    data: data ?? {},
    description: event.transaction,
    op,
    parent_span_id,
    span_id: span_id ?? "",
    start_timestamp: event.start_timestamp ?? 0,
    status,
    timestamp: event.timestamp,
    trace_id: trace_id ?? "",
    origin,
    profile_id: data?.[SEMANTIC_ATTRIBUTE_PROFILE_ID],
    exclusive_time: data?.[SEMANTIC_ATTRIBUTE_EXCLUSIVE_TIME],
    measurements: event.measurements,
    is_segment: true
  };
}
function convertSpanJsonToTransactionEvent(span) {
  return {
    type: "transaction",
    timestamp: span.timestamp,
    start_timestamp: span.start_timestamp,
    transaction: span.description,
    contexts: {
      trace: {
        trace_id: span.trace_id,
        span_id: span.span_id,
        parent_span_id: span.parent_span_id,
        op: span.op,
        status: span.status,
        origin: span.origin,
        data: {
          ...span.data,
          ...span.profile_id && { [SEMANTIC_ATTRIBUTE_PROFILE_ID]: span.profile_id },
          ...span.exclusive_time && { [SEMANTIC_ATTRIBUTE_EXCLUSIVE_TIME]: span.exclusive_time }
        }
      }
    },
    measurements: span.measurements
  };
}


//# sourceMappingURL=transactionEvent.js.map

;// ./node_modules/@sentry/core/build/esm/utils/data-collection/filtering-snippets.js
const FILTERED_VALUE = "[Filtered]";
const PII_HEADER_SNIPPETS = ["forwarded", "-ip", "remote-", "via", "-user"];
const SENSITIVE_KEY_SNIPPETS = (/* unused pure expression or super */ null && ([
  "auth",
  "token",
  "secret",
  "session",
  // for the user_session cookie
  "password",
  "passwd",
  "pwd",
  "key",
  "jwt",
  "bearer",
  "sso",
  "saml",
  "csrf",
  "xsrf",
  "credentials",
  "sid",
  "identity",
  // Always treat cookie headers as sensitive in case individual key-value cookie pairs cannot properly be extracted
  "set-cookie",
  "cookie"
]));
const SENSITIVE_COOKIE_NAME_SNIPPETS = (/* unused pure expression or super */ null && ([
  // Express / Connect default session cookie
  ".sid",
  // Opaque session ids (PHPSESSID, ASPSESSIONID*, BIGipServer*, *sessid*, …)
  "sessid",
  // Laravel etc. "remember me" tokens
  "remember",
  // OIDC / OAuth auxiliary (`oauth*` covered by header snippet `auth`)
  "oidc",
  "pkce",
  "nonce",
  // RFC 6265bis high-security cookie name prefixes
  "__secure-",
  "__host-",
  // Load balancer / CDN sticky-session cookies (opaque routing tokens)
  "awsalb",
  "awselb",
  "akamai",
  // BaaS / IdP session cookies (names often omit "session")
  "__stripe",
  "cognito",
  "firebase",
  "supabase",
  "sb-",
  // Step-up / MFA cookies
  "mfa",
  "2fa"
]));


//# sourceMappingURL=filtering-snippets.js.map

;// ./node_modules/@sentry/core/build/esm/utils/data-collection/defaultPiiToCollectionOptions.js


function defaultPiiToCollectionOptions(sendDefaultPii) {
  return sendDefaultPii === true ? {
    userInfo: true,
    cookies: true,
    httpHeaders: { request: true, response: true },
    httpBodies: ["incomingRequest", "outgoingRequest", "incomingResponse", "outgoingResponse"],
    urlQueryParams: true,
    graphQL: { document: true, variables: true },
    genAI: { inputs: true, outputs: true },
    databaseQueryData: true,
    stackFrameVariables: true,
    frameContextLines: 7
    // default should be 5, but ContextLines integration uses 7
  } : {
    userInfo: false,
    cookies: { deny: PII_HEADER_SNIPPETS },
    httpHeaders: { request: { deny: PII_HEADER_SNIPPETS }, response: { deny: PII_HEADER_SNIPPETS } },
    httpBodies: [],
    urlQueryParams: { deny: PII_HEADER_SNIPPETS },
    // The GraphQL document has literal values redacted at collection time, so it was historically
    // always attached regardless of `sendDefaultPii`; keep it on to preserve that behavior.
    graphQL: { document: true, variables: true },
    genAI: { inputs: false, outputs: false },
    // Database query values were only sent with `sendDefaultPii: true` (e.g. Supabase gated on it),
    // so map the legacy "off" state to `false`.
    databaseQueryData: false,
    stackFrameVariables: true,
    frameContextLines: 7
    // default should be 5, but ContextLines integration uses 7
  };
}


//# sourceMappingURL=defaultPiiToCollectionOptions.js.map

;// ./node_modules/@sentry/core/build/esm/utils/data-collection/resolveDataCollectionOptions.js


const DEFAULTS = {
  userInfo: true,
  cookies: true,
  httpHeaders: { request: true, response: true },
  httpBodies: ["incomingRequest", "outgoingRequest", "incomingResponse", "outgoingResponse"],
  urlQueryParams: true,
  graphQL: { document: true, variables: true },
  genAI: { inputs: true, outputs: true },
  databaseQueryData: true,
  stackFrameVariables: true,
  frameContextLines: 5
};
function resolveDataCollectionOptions(options) {
  const base = options.dataCollection != null ? DEFAULTS : defaultPiiToCollectionOptions(options.sendDefaultPii);
  const dc = options.dataCollection ?? {};
  return {
    userInfo: dc.userInfo ?? base.userInfo,
    cookies: dc.cookies ?? base.cookies,
    httpHeaders: {
      request: dc.httpHeaders?.request ?? base.httpHeaders.request,
      response: dc.httpHeaders?.response ?? base.httpHeaders.response
    },
    httpBodies: dc.httpBodies ?? base.httpBodies,
    // oxlint-disable-next-line typescript/no-deprecated
    urlQueryParams: dc.urlQueryParams ?? dc.queryParams ?? base.urlQueryParams,
    graphQL: {
      document: dc.graphQL?.document ?? base.graphQL.document,
      variables: dc.graphQL?.variables ?? base.graphQL.variables
    },
    genAI: {
      inputs: dc.genAI?.inputs ?? base.genAI.inputs,
      outputs: dc.genAI?.outputs ?? base.genAI.outputs
    },
    databaseQueryData: dc.databaseQueryData ?? base.databaseQueryData,
    stackFrameVariables: dc.stackFrameVariables ?? base.stackFrameVariables,
    frameContextLines: dc.frameContextLines ?? base.frameContextLines
  };
}


//# sourceMappingURL=resolveDataCollectionOptions.js.map

;// ./node_modules/@sentry/core/build/esm/client.js































const ALREADY_SEEN_ERROR = "Not capturing exception because it's already been captured.";
const MISSING_RELEASE_FOR_SESSION_ERROR = "Discarded session because of missing or non-string release";
const INTERNAL_ERROR_SYMBOL = /* @__PURE__ */ Symbol.for("SentryInternalError");
const DO_NOT_SEND_EVENT_SYMBOL = /* @__PURE__ */ Symbol.for("SentryDoNotSendEventError");
const DEFAULT_FLUSH_INTERVAL = 5e3;
function _makeInternalError(message) {
  return {
    message,
    [INTERNAL_ERROR_SYMBOL]: true
  };
}
function _makeDoNotSendEventError(message) {
  return {
    message,
    [DO_NOT_SEND_EVENT_SYMBOL]: true
  };
}
function _isInternalError(error) {
  return isObjectLike(error) && INTERNAL_ERROR_SYMBOL in error;
}
function _isDoNotSendEventError(error) {
  return isObjectLike(error) && DO_NOT_SEND_EVENT_SYMBOL in error;
}
function setupWeightBasedFlushing(client, afterCaptureHook, flushHook, estimateSizeFn, flushFn) {
  let weight = 0;
  let flushTimeout;
  let isTimerActive = false;
  client.on(flushHook, () => {
    weight = 0;
    clearTimeout(flushTimeout);
    isTimerActive = false;
  });
  client.on(afterCaptureHook, (item) => {
    weight += estimateSizeFn(item);
    if (weight >= 8e5) {
      flushFn(client);
    } else if (!isTimerActive) {
      const flushInterval = client.getOptions()._flushInterval ?? DEFAULT_FLUSH_INTERVAL;
      if (flushInterval > 0) {
        isTimerActive = true;
        flushTimeout = safeUnref(
          setTimeout(() => {
            flushFn(client);
          }, flushInterval)
        );
      }
    }
  });
  client.on("flush", () => {
    flushFn(client);
  });
}
class Client {
  /**
   * Initializes this client instance.
   *
   * @param options Options for the client.
   */
  constructor(options) {
    this._options = options;
    this._integrations = {};
    this._numProcessing = 0;
    this._outcomes = {};
    this._hooks = {};
    this._eventProcessors = [];
    this._promiseBuffer = makePromiseBuffer(options.transportOptions?.bufferSize ?? DEFAULT_TRANSPORT_BUFFER_SIZE);
    this._dataCollection = resolveDataCollectionOptions(options);
    if (options.dsn) {
      this._dsn = dsn_makeDsn(options.dsn);
    } else {
      debug_build_DEBUG_BUILD && debug_logger_debug.warn("No DSN provided, client will not send events.");
    }
    if (this._dsn) {
      const url = getEnvelopeEndpointWithUrlEncodedAuth(
        this._dsn,
        options.tunnel,
        options._metadata ? options._metadata.sdk : void 0
      );
      this._transport = options.transport({
        tunnel: this._options.tunnel,
        recordDroppedEvent: this.recordDroppedEvent.bind(this),
        ...options.transportOptions,
        url
      });
    }
    this._options.enableLogs = this._options.enableLogs ?? this._options._experiments?.enableLogs;
    if (this._options.enableLogs) {
      setupWeightBasedFlushing(this, "afterCaptureLog", "flushLogs", estimateLogSizeInBytes, _INTERNAL_flushLogsBuffer);
    }
    const enableMetrics = this._options.enableMetrics ?? this._options._experiments?.enableMetrics ?? true;
    if (enableMetrics) {
      setupWeightBasedFlushing(
        this,
        "afterCaptureMetric",
        "flushMetrics",
        estimateMetricSizeInBytes,
        _INTERNAL_flushMetricsBuffer
      );
    }
  }
  /**
   * Captures an exception event and sends it to Sentry.
   *
   * Unlike `captureException` exported from every SDK, this method requires that you pass it the current scope.
   */
  captureException(exception, hint, scope) {
    const eventId = misc_uuid4();
    if (checkOrSetAlreadyCaught(exception)) {
      debug_build_DEBUG_BUILD && debug_logger_debug.log(ALREADY_SEEN_ERROR);
      return eventId;
    }
    const hintWithEventId = {
      event_id: eventId,
      ...hint
    };
    this._process(
      () => this.eventFromException(exception, hintWithEventId).then((event) => this._captureEvent(event, hintWithEventId, scope)).then((res) => res),
      "error"
    );
    return hintWithEventId.event_id;
  }
  /**
   * Captures a message event and sends it to Sentry.
   *
   * Unlike `captureMessage` exported from every SDK, this method requires that you pass it the current scope.
   */
  captureMessage(message, level, hint, currentScope) {
    const hintWithEventId = {
      event_id: misc_uuid4(),
      ...hint
    };
    const eventMessage = is_isParameterizedString(message) ? message : String(message);
    const isMessage = is_isPrimitive(message);
    const promisedEvent = isMessage ? this.eventFromMessage(eventMessage, level, hintWithEventId) : this.eventFromException(message, hintWithEventId);
    this._process(
      () => promisedEvent.then((event) => this._captureEvent(event, hintWithEventId, currentScope)),
      isMessage ? "unknown" : "error"
    );
    return hintWithEventId.event_id;
  }
  /**
   * Captures a manually created event and sends it to Sentry.
   *
   * Unlike `captureEvent` exported from every SDK, this method requires that you pass it the current scope.
   */
  captureEvent(event, hint, currentScope) {
    const eventId = misc_uuid4();
    if (hint?.originalException && checkOrSetAlreadyCaught(hint.originalException)) {
      debug_build_DEBUG_BUILD && debug_logger_debug.log(ALREADY_SEEN_ERROR);
      return eventId;
    }
    const hintWithEventId = {
      event_id: eventId,
      ...hint
    };
    const sdkProcessingMetadata = event.sdkProcessingMetadata || {};
    const capturedSpanScope = sdkProcessingMetadata.capturedSpanScope;
    const capturedSpanIsolationScope = sdkProcessingMetadata.capturedSpanIsolationScope;
    const dataCategory = getDataCategoryByType(event.type);
    this._process(
      () => this._captureEvent(event, hintWithEventId, capturedSpanScope || currentScope, capturedSpanIsolationScope),
      dataCategory
    );
    return hintWithEventId.event_id;
  }
  /**
   * Captures a session.
   */
  captureSession(session) {
    this.sendSession(session);
    updateSession(session, { init: false });
  }
  /**
   * Get the current Dsn.
   */
  getDsn() {
    return this._dsn;
  }
  /**
   * Get the current options.
   */
  getOptions() {
    return this._options;
  }
  /**
   * Get the resolved data collection configuration.
   */
  getDataCollectionOptions() {
    return this._dataCollection;
  }
  /**
   * Get the SDK metadata.
   * @see SdkMetadata
   */
  getSdkMetadata() {
    return this._options._metadata;
  }
  /**
   * Returns the transport that is used by the client.
   * Please note that the transport gets lazy initialized so it will only be there once the first event has been sent.
   */
  getTransport() {
    return this._transport;
  }
  /**
   * Wait for all events to be sent or the timeout to expire, whichever comes first.
   *
   * @param timeout Maximum time in ms the client should wait for events to be flushed. Omitting this parameter will
   *   cause the client to wait until all events are sent before resolving the promise.
   * @returns A promise that will resolve with `true` if all events are sent before the timeout, or `false` if there are
   * still events in the queue when the timeout is reached.
   */
  // @ts-expect-error - PromiseLike is a subset of Promise
  async flush(timeout) {
    const transport = this._transport;
    this.emit("flush");
    if (!transport) {
      return true;
    }
    const clientFinished = await this._isClientDoneProcessing(timeout);
    const transportFlushed = await transport.flush(timeout);
    return clientFinished && transportFlushed;
  }
  /**
   * Flush the event queue and set the client to `enabled = false`. See {@link Client.flush}.
   *
   * @param {number} timeout Maximum time in ms the client should wait before shutting down. Omitting this parameter will cause
   *   the client to wait until all events are sent before disabling itself.
   * @returns {Promise<boolean>} A promise which resolves to `true` if the flush completes successfully before the timeout, or `false` if
   * it doesn't.
   */
  // @ts-expect-error - PromiseLike is a subset of Promise
  async close(timeout) {
    const result = await this.flush(timeout);
    this.getOptions().enabled = false;
    this.emit("close");
    return result;
  }
  /**
   * Get all installed event processors.
   */
  getEventProcessors() {
    return this._eventProcessors;
  }
  /**
   * Adds an event processor that applies to any event processed by this client.
   */
  addEventProcessor(eventProcessor) {
    this._eventProcessors.push(eventProcessor);
  }
  /**
   * Initialize this client.
   * Call this after the client was set on a scope.
   */
  init() {
    if (this._isEnabled() || // Force integrations to be setup even if no DSN was set when we have
    // Spotlight enabled. This is particularly important for browser as we
    // don't support the `spotlight` option there and rely on the users
    // adding the `spotlightBrowserIntegration()` to their integrations which
    // wouldn't get initialized with the check below when there's no DSN set.
    this._options.integrations.some(({ name }) => name.startsWith("Spotlight"))) {
      this._setupIntegrations();
    }
  }
  /**
   * Gets an installed integration by its name.
   *
   * @returns {Integration|undefined} The installed integration or `undefined` if no integration with that `name` was installed.
   */
  getIntegrationByName(integrationName) {
    return this._integrations[integrationName];
  }
  /**
   * Returns the names of all installed integrations.
   */
  getIntegrationNames() {
    return Object.keys(this._integrations);
  }
  /**
   * Add an integration to the client.
   * This can be used to e.g. lazy load integrations.
   * In most cases, this should not be necessary,
   * and you're better off just passing the integrations via `integrations: []` at initialization time.
   * However, if you find the need to conditionally load & add an integration, you can use `addIntegration` to do so.
   */
  addIntegration(integration) {
    const isAlreadyInstalled = this._integrations[integration.name];
    if (!isAlreadyInstalled && integration.beforeSetup) {
      integration.beforeSetup(this);
    }
    setupIntegration(this, integration, this._integrations);
    if (!isAlreadyInstalled) {
      afterSetupIntegrations(this, [integration]);
    }
  }
  /**
   * Send a fully prepared event to Sentry.
   */
  sendEvent(event, hint = {}) {
    this.emit("beforeSendEvent", event, hint);
    const genAiSpanItem = extractGenAiSpansFromEvent(event, this);
    let env = createEventEnvelope(event, this._dsn, this._options._metadata, this._options.tunnel);
    for (const attachment of hint.attachments || []) {
      env = addItemToEnvelope(env, createAttachmentEnvelopeItem(attachment));
    }
    if (genAiSpanItem) {
      env = addItemToEnvelope(env, genAiSpanItem);
    }
    this.sendEnvelope(env).then((sendResponse) => this.emit("afterSendEvent", event, sendResponse));
  }
  /**
   * Send a session or session aggregrates to Sentry.
   */
  sendSession(session) {
    const { release: clientReleaseOption, environment: clientEnvironmentOption = constants_DEFAULT_ENVIRONMENT } = this._options;
    if ("aggregates" in session) {
      const sessionAttrs = session.attrs || {};
      if (!sessionAttrs.release && !clientReleaseOption) {
        debug_build_DEBUG_BUILD && debug_logger_debug.warn(MISSING_RELEASE_FOR_SESSION_ERROR);
        return;
      }
      sessionAttrs.release = sessionAttrs.release || clientReleaseOption;
      sessionAttrs.environment = sessionAttrs.environment || clientEnvironmentOption;
      session.attrs = sessionAttrs;
    } else {
      if (!session.release && !clientReleaseOption) {
        debug_build_DEBUG_BUILD && debug_logger_debug.warn(MISSING_RELEASE_FOR_SESSION_ERROR);
        return;
      }
      session.release = session.release || clientReleaseOption;
      session.environment = session.environment || clientEnvironmentOption;
    }
    this.emit("beforeSendSession", session);
    const env = createSessionEnvelope(session, this._dsn, this._options._metadata, this._options.tunnel);
    this.sendEnvelope(env);
  }
  /**
   * Record on the client that an event got dropped (ie, an event that will not be sent to Sentry).
   */
  recordDroppedEvent(reason, category, count = 1) {
    if (this._options.sendClientReports) {
      const key = `${reason}:${category}`;
      debug_build_DEBUG_BUILD && debug_logger_debug.log(`Recording outcome: "${key}"${count > 1 ? ` (${count} times)` : ""}`);
      this._outcomes[key] = (this._outcomes[key] || 0) + count;
    }
  }
  /**
   * Register a hook on this client.
   */
  on(hook, callback) {
    const hookCallbacks = this._hooks[hook] = this._hooks[hook] || /* @__PURE__ */ new Set();
    const uniqueCallback = (...args) => callback(...args);
    hookCallbacks.add(uniqueCallback);
    return () => {
      hookCallbacks.delete(uniqueCallback);
    };
  }
  /**
   * Emit a hook that was previously registered via `on()`.
   */
  emit(hook, ...rest) {
    const callbacks = this._hooks[hook];
    if (callbacks) {
      callbacks.forEach((callback) => callback(...rest));
    }
  }
  /**
   * Send an envelope to Sentry.
   */
  // @ts-expect-error - PromiseLike is a subset of Promise
  async sendEnvelope(envelope) {
    this.emit("beforeEnvelope", envelope);
    if (this._isEnabled() && this._transport) {
      try {
        return await this._transport.send(envelope);
      } catch (reason) {
        debug_build_DEBUG_BUILD && debug_logger_debug.error("Error while sending envelope:", reason);
        return {};
      }
    }
    debug_build_DEBUG_BUILD && debug_logger_debug.error("Transport disabled");
    return {};
  }
  /**
   * Register a cleanup function to be called when the client is disposed.
   * This is useful for integrations that need to clean up global state.
   *
   * NOTE: This is a no-op in the base `Client` class. Subclasses like `ServerRuntimeClient`
   * override this method to actually register and execute cleanup callbacks.
   */
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  registerCleanup(callback) {
  }
  /**
   * Disposes of the client and releases all resources.
   *
   * Subclasses should override this method to clean up their own resources, including invoking
   * any callbacks registered via {@link Client.registerCleanup}. The base implementation is a
   * no-op and does NOT execute registered cleanup callbacks.
   *
   * After calling dispose(), the client should not be used anymore.
   */
  dispose() {
  }
  /* eslint-enable @typescript-eslint/unified-signatures */
  /** Setup integrations for this client. */
  _setupIntegrations() {
    const { integrations } = this._options;
    this._integrations = setupIntegrations(this, integrations);
    afterSetupIntegrations(this, integrations);
  }
  /** Updates existing session based on the provided event */
  _updateSessionFromEvent(session, event) {
    let crashed = event.level === "fatal";
    let errored = false;
    const exceptions = event.exception?.values;
    if (exceptions) {
      errored = true;
      crashed = false;
      for (const ex of exceptions) {
        if (ex.mechanism?.handled === false) {
          crashed = true;
          break;
        }
      }
    }
    const sessionNonTerminal = session.status === "ok";
    const shouldUpdateAndSend = sessionNonTerminal && session.errors === 0 || sessionNonTerminal && crashed;
    if (shouldUpdateAndSend) {
      updateSession(session, {
        ...crashed && { status: "crashed" },
        errors: session.errors || Number(errored || crashed)
      });
      this.captureSession(session);
    }
  }
  /**
   * Determine if the client is finished processing. Returns a promise because it will wait `timeout` ms before saying
   * "no" (resolving to `false`) in order to give the client a chance to potentially finish first.
   *
   * @param timeout The time, in ms, after which to resolve to `false` if the client is still busy. Passing `0` (or not
   * passing anything) will make the promise wait as long as it takes for processing to finish before resolving to
   * `true`.
   * @returns A promise which will resolve to `true` if processing is already done or finishes before the timeout, and
   * `false` otherwise
   */
  async _isClientDoneProcessing(timeout) {
    let ticked = 0;
    while (!timeout || ticked < timeout) {
      await new Promise((resolve) => setTimeout(resolve, 1));
      if (!this._numProcessing) {
        return true;
      }
      ticked++;
    }
    return false;
  }
  /** Determines whether this SDK is enabled and a transport is present. */
  _isEnabled() {
    return this.getOptions().enabled !== false && this._transport !== void 0;
  }
  /**
   * Adds common information to events.
   *
   * The information includes release and environment from `options`,
   * breadcrumbs and context (extra, tags and user) from the scope.
   *
   * Information that is already present in the event is never overwritten. For
   * nested objects, such as the context, keys are merged.
   *
   * @param event The original event.
   * @param hint May contain additional information about the original exception.
   * @param currentScope A scope containing event metadata.
   * @returns A new event with more information.
   */
  _prepareEvent(event, hint, currentScope, isolationScope) {
    const options = this.getOptions();
    const integrations = this.getIntegrationNames();
    if (!hint.integrations && integrations.length) {
      hint.integrations = integrations;
    }
    this.emit("preprocessEvent", event, hint);
    if (!event.type) {
      isolationScope.setLastEventId(event.event_id || hint.event_id);
    }
    return prepareEvent(options, event, hint, currentScope, this, isolationScope).then((evt) => {
      if (evt === null) {
        return evt;
      }
      this.emit("postprocessEvent", evt, hint);
      evt.contexts = {
        trace: { ...evt.contexts?.trace, ...getTraceContextFromScope(currentScope) },
        ...evt.contexts
      };
      const dynamicSamplingContext = getDynamicSamplingContextFromScope(this, currentScope);
      evt.sdkProcessingMetadata = {
        dynamicSamplingContext,
        ...evt.sdkProcessingMetadata
      };
      return evt;
    });
  }
  /**
   * Processes the event and logs an error in case of rejection
   * @param event
   * @param hint
   * @param scope
   */
  _captureEvent(event, hint = {}, currentScope = currentScopes_getCurrentScope(), isolationScope = currentScopes_getIsolationScope()) {
    if (debug_build_DEBUG_BUILD && client_isErrorEvent(event)) {
      debug_logger_debug.log(`Captured error event \`${getPossibleEventMessages(event)[0] || "<unknown>"}\``);
    }
    return this._processEvent(event, hint, currentScope, isolationScope).then(
      (finalEvent) => {
        return finalEvent.event_id;
      },
      (reason) => {
        if (debug_build_DEBUG_BUILD) {
          if (_isDoNotSendEventError(reason)) {
            debug_logger_debug.log(reason.message);
          } else if (_isInternalError(reason)) {
            debug_logger_debug.warn(reason.message);
          } else {
            debug_logger_debug.warn(reason);
          }
        }
        return void 0;
      }
    );
  }
  /**
   * Processes an event (either error or message) and sends it to Sentry.
   *
   * This also adds breadcrumbs and context information to the event. However,
   * platform specific meta data (such as the User's IP address) must be added
   * by the SDK implementor.
   *
   *
   * @param event The event to send to Sentry.
   * @param hint May contain additional information about the original exception.
   * @param currentScope A scope containing event metadata.
   * @returns A SyncPromise that resolves with the event or rejects in case event was/will not be send.
   */
  _processEvent(event, hint, currentScope, isolationScope) {
    const options = this.getOptions();
    const { sampleRate } = options;
    const isTransaction = isTransactionEvent(event);
    const isError = client_isErrorEvent(event);
    const eventType = event.type || "error";
    const beforeSendLabel = `before send for type \`${eventType}\``;
    const parsedSampleRate = typeof sampleRate === "undefined" ? void 0 : parseSampleRate(sampleRate);
    const dataCategory = getDataCategoryByType(event.type);
    return this._prepareEvent(event, hint, currentScope, isolationScope).then((prepared) => {
      if (prepared === null) {
        this.recordDroppedEvent("event_processor", dataCategory);
        throw _makeDoNotSendEventError("An event processor returned `null`, will not send event.");
      }
      const isInternalException = hint.data?.__sentry__ === true;
      if (isInternalException) {
        return prepared;
      }
      const result = processBeforeSend(this, options, prepared, hint);
      return _validateBeforeSendResult(result, beforeSendLabel);
    }).then((processedEvent) => {
      if (processedEvent === null) {
        this.recordDroppedEvent("before_send", dataCategory);
        if (isTransaction) {
          const spans = event.spans || [];
          const spanCount = 1 + spans.length;
          this.recordDroppedEvent("before_send", "span", spanCount);
        }
        throw _makeDoNotSendEventError(`${beforeSendLabel} returned \`null\`, will not send event.`);
      }
      const session = currentScope.getSession() || isolationScope.getSession();
      if (isError && session) {
        this._updateSessionFromEvent(session, processedEvent);
      }
      if (isError && typeof parsedSampleRate === "number" && safeMathRandom() > parsedSampleRate) {
        this.recordDroppedEvent("sample_rate", "error");
        throw _makeDoNotSendEventError(
          `Discarding event because it's not included in the random sample (sampling rate = ${sampleRate})`
        );
      }
      if (isTransaction) {
        const spanCountBefore = processedEvent.sdkProcessingMetadata?.spanCountBeforeProcessing || 0;
        const spanCountAfter = processedEvent.spans ? processedEvent.spans.length : 0;
        const droppedSpanCount = spanCountBefore - spanCountAfter;
        if (droppedSpanCount > 0) {
          this.recordDroppedEvent("before_send", "span", droppedSpanCount);
        }
      }
      const transactionInfo = processedEvent.transaction_info;
      if (isTransaction && transactionInfo && processedEvent.transaction !== event.transaction) {
        const source = "custom";
        processedEvent.transaction_info = {
          ...transactionInfo,
          source
        };
      }
      this.sendEvent(processedEvent, hint);
      return processedEvent;
    }).then(null, (reason) => {
      if (_isDoNotSendEventError(reason) || _isInternalError(reason)) {
        throw reason;
      }
      this.captureException(reason, {
        mechanism: {
          handled: false,
          type: "internal"
        },
        data: {
          __sentry__: true
        },
        originalException: reason
      });
      throw _makeInternalError(
        `Event processing pipeline threw an error, original event will not be sent. Details have been sent as a new event.
Reason: ${reason}`
      );
    });
  }
  /**
   * Occupies the client with processing and event
   */
  _process(taskProducer, dataCategory) {
    this._numProcessing++;
    void this._promiseBuffer.add(taskProducer).then(
      (value) => {
        this._numProcessing--;
        return value;
      },
      (reason) => {
        this._numProcessing--;
        if (reason === SENTRY_BUFFER_FULL_ERROR) {
          this.recordDroppedEvent("queue_overflow", dataCategory);
        }
        return reason;
      }
    );
  }
  /**
   * Clears outcomes on this client and returns them.
   */
  _clearOutcomes() {
    const outcomes = this._outcomes;
    this._outcomes = {};
    return Object.entries(outcomes).map(([key, quantity]) => {
      const [reason, category] = key.split(":");
      return {
        reason,
        category,
        quantity
      };
    });
  }
  /**
   * Sends client reports as an envelope.
   */
  _flushOutcomes() {
    debug_build_DEBUG_BUILD && debug_logger_debug.log("Flushing outcomes...");
    const outcomes = this._clearOutcomes();
    if (outcomes.length === 0) {
      debug_build_DEBUG_BUILD && debug_logger_debug.log("No outcomes to send");
      return;
    }
    if (!this._dsn) {
      debug_build_DEBUG_BUILD && debug_logger_debug.log("No dsn provided, will not send outcomes");
      return;
    }
    debug_build_DEBUG_BUILD && debug_logger_debug.log("Sending outcomes:", outcomes);
    const envelope = createClientReportEnvelope(outcomes, this._options.tunnel && dsn_dsnToString(this._dsn));
    this.sendEnvelope(envelope);
  }
}
function getDataCategoryByType(type) {
  return type === "replay_event" ? "replay" : type || "error";
}
function _validateBeforeSendResult(beforeSendResult, beforeSendLabel) {
  const invalidValueError = `${beforeSendLabel} must return \`null\` or a valid event.`;
  if (is_isThenable(beforeSendResult)) {
    return beforeSendResult.then(
      (event) => {
        if (!is_isPlainObject(event) && event !== null) {
          throw _makeInternalError(invalidValueError);
        }
        return event;
      },
      (e) => {
        throw _makeInternalError(`${beforeSendLabel} rejected with ${e}`);
      }
    );
  } else if (!is_isPlainObject(beforeSendResult) && beforeSendResult !== null) {
    throw _makeInternalError(invalidValueError);
  }
  return beforeSendResult;
}
function processBeforeSend(client, options, event, hint) {
  const { beforeSend, beforeSendTransaction, ignoreSpans } = options;
  const beforeSendSpan = !beforeSendSpan_isStreamedBeforeSendSpanCallback(options.beforeSendSpan) && options.beforeSendSpan;
  let processedEvent = event;
  if (client_isErrorEvent(processedEvent) && beforeSend) {
    return beforeSend(processedEvent, hint);
  }
  if (isTransactionEvent(processedEvent)) {
    if (beforeSendSpan || ignoreSpans) {
      const rootSpanJson = convertTransactionEventToSpanJson(processedEvent);
      if (ignoreSpans?.length && should_ignore_span_shouldIgnoreSpan(
        { description: rootSpanJson.description, op: rootSpanJson.op, attributes: rootSpanJson.data },
        ignoreSpans
      )) {
        return null;
      }
      if (beforeSendSpan) {
        const processedRootSpanJson = beforeSendSpan(rootSpanJson);
        if (!processedRootSpanJson) {
          spanUtils_showSpanDropWarning();
        } else {
          processedEvent = merge(event, convertSpanJsonToTransactionEvent(processedRootSpanJson));
        }
      }
      if (processedEvent.spans) {
        const processedSpans = [];
        const initialSpans = processedEvent.spans;
        for (const span of initialSpans) {
          if (ignoreSpans?.length && should_ignore_span_shouldIgnoreSpan({ description: span.description, op: span.op, attributes: span.data }, ignoreSpans)) {
            reparentChildSpans(initialSpans, span);
            continue;
          }
          if (beforeSendSpan) {
            const processedSpan = beforeSendSpan(span);
            if (!processedSpan) {
              spanUtils_showSpanDropWarning();
              processedSpans.push(span);
            } else {
              processedSpans.push(processedSpan);
            }
          } else {
            processedSpans.push(span);
          }
        }
        const droppedSpans = processedEvent.spans.length - processedSpans.length;
        if (droppedSpans) {
          client.recordDroppedEvent("before_send", "span", droppedSpans);
        }
        processedEvent.spans = processedSpans;
      }
    }
    if (beforeSendTransaction) {
      if (processedEvent.spans) {
        const spanCountBefore = processedEvent.spans.length;
        processedEvent.sdkProcessingMetadata = {
          ...event.sdkProcessingMetadata,
          spanCountBeforeProcessing: spanCountBefore
        };
      }
      return beforeSendTransaction(processedEvent, hint);
    }
  }
  return processedEvent;
}
function client_isErrorEvent(event) {
  return event.type === void 0;
}
function isTransactionEvent(event) {
  return event.type === "transaction";
}
function estimateMetricSizeInBytes(metric) {
  let weight = 0;
  if (metric.name) {
    weight += metric.name.length * 2;
  }
  weight += 8;
  return weight + estimateAttributesSizeInBytes(metric.attributes);
}
function estimateLogSizeInBytes(log) {
  let weight = 0;
  if (log.message) {
    weight += log.message.length * 2;
  }
  return weight + estimateAttributesSizeInBytes(log.attributes);
}
function estimateAttributesSizeInBytes(attributes) {
  if (!attributes) {
    return 0;
  }
  let weight = 0;
  Object.values(attributes).forEach((value) => {
    if (Array.isArray(value)) {
      weight += value.length * client_estimatePrimitiveSizeInBytes(value[0]);
    } else if (is_isPrimitive(value)) {
      weight += client_estimatePrimitiveSizeInBytes(value);
    } else {
      weight += 100;
    }
  });
  return weight;
}
function client_estimatePrimitiveSizeInBytes(value) {
  if (typeof value === "string") {
    return value.length * 2;
  } else if (typeof value === "number") {
    return 8;
  } else if (typeof value === "boolean") {
    return 4;
  }
  return 0;
}


//# sourceMappingURL=client.js.map

;// ./node_modules/@sentry/core/build/esm/utils/sdkMetadata.js


function applySdkMetadata(options, name, names = [name], source = "npm") {
  const sdk = (options._metadata = options._metadata || {}).sdk = options._metadata.sdk || {};
  if (!sdk.name) {
    sdk.name = `sentry.javascript.${name}`;
    sdk.packages = names.map((name2) => ({
      name: `${source}:@sentry/${name2}`,
      version: SDK_VERSION
    }));
    sdk.version = SDK_VERSION;
  }
}


//# sourceMappingURL=sdkMetadata.js.map

;// ./node_modules/@sentry/core/build/esm/utils/ipAddress.js
function addAutoIpAddressToUser(objWithMaybeUser) {
  if (objWithMaybeUser.user?.ip_address === void 0) {
    objWithMaybeUser.user = {
      ...objWithMaybeUser.user,
      ip_address: "{{auto}}"
    };
  }
}
function addAutoIpAddressToSession(session) {
  if ("aggregates" in session) {
    if (session.attrs?.["ip_address"] === void 0) {
      session.attrs = {
        ...session.attrs,
        ip_address: "{{auto}}"
      };
    }
  } else {
    if (session.ipAddress === void 0) {
      session.ipAddress = "{{auto}}";
    }
  }
}


//# sourceMappingURL=ipAddress.js.map

;// ./node_modules/@sentry/core/build/esm/utils/eventbuilder.js





function parseStackFrames(stackParser, error) {
  return stackParser(error.stack || "", 1);
}
function hasSentryFetchUrlHost(error) {
  return is_isError(error) && "__sentry_fetch_url_host__" in error && typeof error.__sentry_fetch_url_host__ === "string";
}
function _enhanceErrorWithSentryInfo(error) {
  if (hasSentryFetchUrlHost(error)) {
    return `${error.message} (${error.__sentry_fetch_url_host__})`;
  }
  return error.message;
}
function exceptionFromError(stackParser, error) {
  const exception = {
    type: error.name || error.constructor.name,
    value: _enhanceErrorWithSentryInfo(error)
  };
  const frames = parseStackFrames(stackParser, error);
  if (frames.length) {
    exception.stacktrace = { frames };
  }
  return exception;
}
function getErrorPropertyFromObject(obj) {
  for (const prop in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, prop)) {
      const value = obj[prop];
      if (isError(value)) {
        return value;
      }
    }
  }
  return void 0;
}
function getMessageForObject(exception) {
  if ("name" in exception && typeof exception.name === "string") {
    let message = `'${exception.name}' captured as exception`;
    if ("message" in exception && typeof exception.message === "string") {
      message += ` with message '${exception.message}'`;
    }
    return message;
  } else if ("message" in exception && typeof exception.message === "string") {
    return exception.message;
  }
  const keys = extractExceptionKeysForMessage(exception);
  if (isErrorEvent(exception)) {
    return `Event \`ErrorEvent\` captured as exception with message \`${exception.message}\``;
  }
  const className = getObjectClassName(exception);
  return `${className && className !== "Object" ? `'${className}'` : "Object"} captured as exception with keys: ${keys}`;
}
function getObjectClassName(obj) {
  try {
    const prototype = Object.getPrototypeOf(obj);
    return prototype ? prototype.constructor.name : void 0;
  } catch {
  }
}
function getException(client, mechanism, exception, hint) {
  if (isError(exception)) {
    return [exception, void 0];
  }
  mechanism.synthetic = true;
  if (isPlainObject(exception)) {
    const normalizeDepth = client?.getOptions().normalizeDepth;
    const extras = { ["__serialized__"]: normalizeToSize(exception, normalizeDepth) };
    const errorFromProp = getErrorPropertyFromObject(exception);
    if (errorFromProp) {
      return [errorFromProp, extras];
    }
    const message = getMessageForObject(exception);
    const ex2 = hint?.syntheticException || new Error(message);
    ex2.message = message;
    return [ex2, extras];
  }
  const ex = hint?.syntheticException || new Error(exception);
  ex.message = `${exception}`;
  return [ex, void 0];
}
function eventFromUnknownInput(client, stackParser, exception, hint) {
  const providedMechanism = hint?.data && hint.data.mechanism;
  const mechanism = providedMechanism || {
    handled: true,
    type: "generic"
  };
  const [ex, extras] = getException(client, mechanism, exception, hint);
  const event = {
    exception: {
      values: [exceptionFromError(stackParser, ex)]
    }
  };
  if (extras) {
    event.extra = extras;
  }
  addExceptionTypeValue(event, void 0, void 0);
  addExceptionMechanism(event, mechanism);
  return {
    ...event,
    event_id: hint?.event_id
  };
}
function eventFromMessage(stackParser, message, level = "info", hint, attachStacktrace) {
  const event = {
    event_id: hint?.event_id,
    level
  };
  if (attachStacktrace && hint?.syntheticException) {
    const frames = parseStackFrames(stackParser, hint.syntheticException);
    if (frames.length) {
      event.exception = {
        values: [
          {
            value: message,
            stacktrace: { frames }
          }
        ]
      };
      addExceptionMechanism(event, { synthetic: true });
    }
  }
  if (isParameterizedString(message)) {
    const { __sentry_template_string__, __sentry_template_values__ } = message;
    event.logentry = {
      message: __sentry_template_string__,
      params: __sentry_template_values__
    };
    return event;
  }
  event.message = message;
  return event;
}


//# sourceMappingURL=eventbuilder.js.map

;// ./node_modules/@sentry/browser/build/npm/esm/prod/eventbuilder.js


function eventbuilder_exceptionFromError(stackParser, ex) {
  const frames = eventbuilder_parseStackFrames(stackParser, ex);
  const exception = {
    type: extractType(ex),
    value: extractMessage(ex)
  };
  if (frames.length) {
    exception.stacktrace = { frames };
  }
  if (exception.type === void 0 && exception.value === "") {
    exception.value = "Unrecoverable error caught";
  }
  return exception;
}
function eventFromPlainObject(stackParser, exception, syntheticException, isUnhandledRejection) {
  const client = currentScopes_getClient();
  const normalizeDepth = client?.getOptions().normalizeDepth;
  const errorFromProp = eventbuilder_getErrorPropertyFromObject(exception);
  const extra = {
    __serialized__: normalize_normalizeToSize(exception, normalizeDepth)
  };
  if (errorFromProp) {
    return {
      exception: {
        values: [eventbuilder_exceptionFromError(stackParser, errorFromProp)]
      },
      extra
    };
  }
  const event = {
    exception: {
      values: [
        {
          type: isEvent(exception) ? exception.constructor.name : isUnhandledRejection ? "UnhandledRejection" : "Error",
          value: getNonErrorObjectExceptionValue(exception, { isUnhandledRejection })
        }
      ]
    },
    extra
  };
  if (syntheticException) {
    const frames = eventbuilder_parseStackFrames(stackParser, syntheticException);
    if (frames.length) {
      event.exception.values[0].stacktrace = { frames };
    }
  }
  return event;
}
function eventFromError(stackParser, ex) {
  return {
    exception: {
      values: [eventbuilder_exceptionFromError(stackParser, ex)]
    }
  };
}
function eventbuilder_parseStackFrames(stackParser, ex) {
  const stacktrace = ex.stacktrace || ex.stack || "";
  const skipLines = getSkipFirstStackStringLines(ex);
  const framesToPop = getPopFirstTopFrames(ex);
  try {
    return stackParser(stacktrace, skipLines, framesToPop);
  } catch {
  }
  return [];
}
const reactMinifiedRegexp = /Minified React error #\d+;/i;
function getSkipFirstStackStringLines(ex) {
  if (ex && reactMinifiedRegexp.test(ex.message)) {
    return 1;
  }
  return 0;
}
function getPopFirstTopFrames(ex) {
  if (typeof ex.framesToPop === "number") {
    return ex.framesToPop;
  }
  return 0;
}
function isWebAssemblyException(exception) {
  if (typeof WebAssembly !== "undefined" && typeof WebAssembly.Exception !== "undefined") {
    return exception instanceof WebAssembly.Exception;
  } else {
    return false;
  }
}
function extractType(ex) {
  const name = ex?.name;
  if (!name && isWebAssemblyException(ex)) {
    const hasTypeInMessage = ex.message && Array.isArray(ex.message) && ex.message.length == 2;
    return hasTypeInMessage ? ex.message[0] : "WebAssembly.Exception";
  }
  return name;
}
function extractMessage(ex) {
  const message = ex?.message;
  if (isWebAssemblyException(ex)) {
    if (Array.isArray(ex.message) && ex.message.length == 2) {
      return ex.message[1];
    }
    return "wasm exception";
  }
  if (!message) {
    return "No error message";
  }
  if (message.error && typeof message.error.message === "string") {
    return _enhanceErrorWithSentryInfo(message.error);
  }
  return _enhanceErrorWithSentryInfo(ex);
}
function eventFromException(stackParser, exception, hint, attachStacktrace) {
  const syntheticException = hint?.syntheticException || void 0;
  const event = eventbuilder_eventFromUnknownInput(stackParser, exception, syntheticException, attachStacktrace);
  misc_addExceptionMechanism(event);
  event.level = "error";
  if (hint?.event_id) {
    event.event_id = hint.event_id;
  }
  return resolvedSyncPromise(event);
}
function eventbuilder_eventFromMessage(stackParser, message, level = "info", hint, attachStacktrace) {
  const syntheticException = hint?.syntheticException || void 0;
  const event = eventFromString(stackParser, message, syntheticException, attachStacktrace);
  event.level = level;
  if (hint?.event_id) {
    event.event_id = hint.event_id;
  }
  return resolvedSyncPromise(event);
}
function eventbuilder_eventFromUnknownInput(stackParser, exception, syntheticException, attachStacktrace, isUnhandledRejection) {
  let event;
  if (is_isErrorEvent(exception) && exception.error) {
    const errorEvent = exception;
    return eventFromError(stackParser, errorEvent.error);
  }
  if (isDOMError(exception) || isDOMException(exception)) {
    const domException = exception;
    if ("stack" in exception) {
      event = eventFromError(stackParser, exception);
      const firstException = event.exception?.values?.[0];
      if (attachStacktrace && syntheticException && firstException && !firstException.stacktrace) {
        const frames = eventbuilder_parseStackFrames(stackParser, syntheticException);
        if (frames.length) {
          firstException.stacktrace = { frames };
          misc_addExceptionMechanism(event, { synthetic: true });
        }
      }
    } else {
      const name = domException.name || (isDOMError(domException) ? "DOMError" : "DOMException");
      const message = domException.message ? `${name}: ${domException.message}` : name;
      event = eventFromString(stackParser, message, syntheticException, attachStacktrace);
      misc_addExceptionTypeValue(event, message);
    }
    if ("code" in domException) {
      event.tags = { ...event.tags, "DOMException.code": `${domException.code}` };
    }
    return event;
  }
  if (is_isError(exception)) {
    return eventFromError(stackParser, exception);
  }
  if (is_isPlainObject(exception) || isEvent(exception)) {
    const objectException = exception;
    event = eventFromPlainObject(stackParser, objectException, syntheticException, isUnhandledRejection);
    misc_addExceptionMechanism(event, {
      synthetic: true
    });
    return event;
  }
  event = eventFromString(stackParser, exception, syntheticException, attachStacktrace);
  misc_addExceptionTypeValue(event, `${exception}`, void 0);
  misc_addExceptionMechanism(event, {
    synthetic: true
  });
  return event;
}
function eventFromString(stackParser, message, syntheticException, attachStacktrace) {
  const event = {};
  if (attachStacktrace && syntheticException) {
    const frames = eventbuilder_parseStackFrames(stackParser, syntheticException);
    if (frames.length) {
      event.exception = {
        values: [{ value: message, stacktrace: { frames } }]
      };
    }
    misc_addExceptionMechanism(event, { synthetic: true });
  }
  if (is_isParameterizedString(message)) {
    const { __sentry_template_string__, __sentry_template_values__ } = message;
    event.logentry = {
      message: __sentry_template_string__,
      params: __sentry_template_values__
    };
    return event;
  }
  event.message = message;
  return event;
}
function getNonErrorObjectExceptionValue(exception, { isUnhandledRejection }) {
  const keys = object_extractExceptionKeysForMessage(exception);
  const captureType = isUnhandledRejection ? "promise rejection" : "exception";
  if (is_isErrorEvent(exception)) {
    return `Event \`ErrorEvent\` captured as ${captureType} with message \`${exception.message}\``;
  }
  if (isEvent(exception)) {
    const className = eventbuilder_getObjectClassName(exception);
    return `Event \`${className}\` (type=${exception.type}) captured as ${captureType}`;
  }
  return `Object captured as ${captureType} with keys: ${keys}`;
}
function eventbuilder_getObjectClassName(obj) {
  try {
    const prototype = Object.getPrototypeOf(obj);
    return prototype ? prototype.constructor.name : void 0;
  } catch {
  }
}
function eventbuilder_getErrorPropertyFromObject(obj) {
  return Object.values(obj).find(is_isError);
}


//# sourceMappingURL=eventbuilder.js.map

;// ./node_modules/@sentry/core/build/esm/exports.js












function captureException(exception, hint) {
  return currentScopes_getCurrentScope().captureException(exception, parseEventHintOrCaptureContext(hint));
}
function captureMessage(message, captureContext) {
  const level = typeof captureContext === "string" ? captureContext : void 0;
  const hint = typeof captureContext !== "string" ? { captureContext } : void 0;
  return getCurrentScope().captureMessage(message, level, hint);
}
function captureEvent(event, hint) {
  return currentScopes_getCurrentScope().captureEvent(event, hint);
}
function setContext(name, context) {
  getIsolationScope().setContext(name, context);
}
function setExtras(extras) {
  getIsolationScope().setExtras(extras);
}
function setExtra(key, extra) {
  getIsolationScope().setExtra(key, extra);
}
function setTags(tags) {
  getIsolationScope().setTags(tags);
}
function setTag(key, value) {
  getIsolationScope().setTag(key, value);
}
function setAttributes(attributes) {
  getIsolationScope().setAttributes(attributes);
}
function setAttribute(key, value) {
  getIsolationScope().setAttribute(key, value);
}
function setUser(user) {
  getIsolationScope().setUser(user);
}
function setConversationId(conversationId) {
  getIsolationScope().setConversationId(conversationId);
}
function lastEventId() {
  return getIsolationScope().lastEventId();
}
function captureCheckIn(checkIn, upsertMonitorConfig) {
  const scope = getCurrentScope();
  const client = getClient();
  if (!client) {
    DEBUG_BUILD && debug.warn("Cannot capture check-in. No client defined.");
  } else if (!client.captureCheckIn) {
    DEBUG_BUILD && debug.warn("Cannot capture check-in. Client does not support sending check-ins.");
  } else {
    return client.captureCheckIn(checkIn, upsertMonitorConfig, scope);
  }
  return uuid4();
}
function withMonitor(monitorSlug, callback, upsertMonitorConfig) {
  function runCallback() {
    const checkInId = captureCheckIn({ monitorSlug, status: "in_progress" }, upsertMonitorConfig);
    const now = timestampInSeconds();
    function finishCheckIn(status) {
      captureCheckIn({ monitorSlug, status, checkInId, duration: timestampInSeconds() - now });
    }
    let maybePromiseResult;
    try {
      maybePromiseResult = callback();
    } catch (e) {
      finishCheckIn("error");
      throw e;
    }
    if (isThenable(maybePromiseResult)) {
      return maybePromiseResult.then(
        (r) => {
          finishCheckIn("ok");
          return r;
        },
        (e) => {
          finishCheckIn("error");
          throw e;
        }
      );
    }
    finishCheckIn("ok");
    return maybePromiseResult;
  }
  return withIsolationScope(() => upsertMonitorConfig?.isolateTrace ? startNewTrace(runCallback) : runCallback());
}
async function flush(timeout) {
  const client = getClient();
  if (client) {
    return client.flush(timeout);
  }
  DEBUG_BUILD && debug.warn("Cannot flush events. No client defined.");
  return Promise.resolve(false);
}
async function exports_close(timeout) {
  const client = getClient();
  if (client) {
    return client.close(timeout);
  }
  DEBUG_BUILD && debug.warn("Cannot flush events and disable SDK. No client defined.");
  return Promise.resolve(false);
}
function isInitialized() {
  return !!getClient();
}
function exports_isEnabled() {
  const client = getClient();
  return client?.getOptions().enabled !== false && !!client?.getTransport();
}
function addEventProcessor(callback) {
  getIsolationScope().addEventProcessor(callback);
}
function startSession(context) {
  const isolationScope = currentScopes_getIsolationScope();
  const { user } = scopeData_getCombinedScopeData(isolationScope, currentScopes_getCurrentScope());
  const { userAgent } = worldwide_GLOBAL_OBJ.navigator || {};
  const session = makeSession({
    user,
    ...userAgent && { userAgent },
    ...context
  });
  const currentSession = isolationScope.getSession();
  if (currentSession?.status === "ok") {
    updateSession(currentSession, { status: "exited" });
  }
  endSession();
  isolationScope.setSession(session);
  return session;
}
function endSession() {
  const isolationScope = currentScopes_getIsolationScope();
  const currentScope = currentScopes_getCurrentScope();
  const session = currentScope.getSession() || isolationScope.getSession();
  if (session) {
    closeSession(session);
  }
  _sendSessionUpdate();
  isolationScope.setSession();
}
function _sendSessionUpdate() {
  const isolationScope = currentScopes_getIsolationScope();
  const client = currentScopes_getClient();
  const session = isolationScope.getSession();
  if (session && client) {
    client.captureSession(session);
  }
}
function captureSession(end = false) {
  if (end) {
    endSession();
    return;
  }
  _sendSessionUpdate();
}


//# sourceMappingURL=exports.js.map

;// ./node_modules/@sentry/core/build/esm/utils/browser.js



const WINDOW = worldwide_GLOBAL_OBJ;
const DEFAULT_MAX_STRING_LENGTH = 80;
function htmlTreeAsString(elem, options = {}) {
  if (!elem) {
    return "<unknown>";
  }
  try {
    let currentElem = elem;
    const MAX_TRAVERSE_HEIGHT = 5;
    const out = [];
    let height = 0;
    let len = 0;
    const separator = " > ";
    const sepLength = separator.length;
    let nextStr;
    const keyAttrs = Array.isArray(options) ? options : options.keyAttrs;
    const maxStringLength = !Array.isArray(options) && options.maxStringLength || DEFAULT_MAX_STRING_LENGTH;
    while (currentElem && height++ < MAX_TRAVERSE_HEIGHT) {
      nextStr = _htmlElementAsString(currentElem, keyAttrs);
      if (nextStr === "html" || height > 1 && len + out.length * sepLength + nextStr.length >= maxStringLength) {
        break;
      }
      out.push(nextStr);
      len += nextStr.length;
      currentElem = currentElem.parentNode;
    }
    return out.reverse().join(separator);
  } catch {
    return "<unknown>";
  }
}
function _htmlElementAsString(el, keyAttrs) {
  const elem = el;
  const out = [];
  if (!elem?.tagName) {
    return "";
  }
  if (WINDOW.HTMLElement) {
    if (elem instanceof HTMLElement && elem.dataset) {
      if (elem.dataset["sentryComponent"]) {
        return elem.dataset["sentryComponent"];
      }
      if (elem.dataset["sentryElement"]) {
        return elem.dataset["sentryElement"];
      }
    }
  }
  out.push(elem.tagName.toLowerCase());
  const keyAttrPairs = keyAttrs?.length ? keyAttrs.filter((keyAttr) => elem.getAttribute(keyAttr)).map((keyAttr) => [keyAttr, elem.getAttribute(keyAttr)]) : null;
  if (keyAttrPairs?.length) {
    keyAttrPairs.forEach((keyAttrPair) => {
      out.push(`[${keyAttrPair[0]}="${keyAttrPair[1]}"]`);
    });
  } else {
    if (elem.id) {
      out.push(`#${elem.id}`);
    }
    const className = elem.className;
    if (className && isString(className)) {
      const classes = className.split(/\s+/);
      for (const c of classes) {
        out.push(`.${c}`);
      }
    }
  }
  for (const k of ["aria-label", "type", "name", "title", "alt"]) {
    const attr = elem.getAttribute(k);
    if (attr) {
      out.push(`[${k}="${attr}"]`);
    }
  }
  return out.join("");
}
function getLocationHref() {
  try {
    return WINDOW.document.location.href;
  } catch {
    return "";
  }
}
function getComponentName(elem, maxTraverseHeight = 5) {
  if (!WINDOW.HTMLElement) {
    return null;
  }
  let currentElem = elem;
  for (let i = 0; i < maxTraverseHeight; i++) {
    if (!currentElem) {
      return null;
    }
    if (currentElem instanceof HTMLElement) {
      if (currentElem.dataset["sentryComponent"]) {
        return currentElem.dataset["sentryComponent"];
      }
      if (currentElem.dataset["sentryElement"]) {
        return currentElem.dataset["sentryElement"];
      }
    }
    currentElem = currentElem.parentNode;
  }
  return null;
}


//# sourceMappingURL=browser.js.map

;// ./node_modules/@sentry/browser/build/npm/esm/prod/helpers.js


const helpers_WINDOW = worldwide_GLOBAL_OBJ;
let ignoreOnError = 0;
function shouldIgnoreOnError() {
  return ignoreOnError > 0;
}
function ignoreNextOnError() {
  ignoreOnError++;
  setTimeout(() => {
    ignoreOnError--;
  });
}
function wrap(fn, options = {}) {
  function isFunction(fn2) {
    return typeof fn2 === "function";
  }
  if (!isFunction(fn)) {
    return fn;
  }
  try {
    const hasOwnWrapper = Object.prototype.hasOwnProperty.call(fn, "__sentry_wrapped__");
    if (hasOwnWrapper) {
      const wrapper = fn.__sentry_wrapped__;
      if (typeof wrapper === "function") {
        return wrapper;
      } else {
        return fn;
      }
    }
    if (getOriginalFunction(fn)) {
      return fn;
    }
  } catch {
    return fn;
  }
  const sentryWrapped = function(...args) {
    worldwide_GLOBAL_OBJ._sentryWrappedDepth = (worldwide_GLOBAL_OBJ._sentryWrappedDepth || 0) + 1;
    try {
      const wrappedArguments = args.map((arg) => wrap(arg, options));
      return fn.apply(this, wrappedArguments);
    } catch (ex) {
      ignoreNextOnError();
      currentScopes_withScope((scope) => {
        scope.addEventProcessor((event) => {
          if (options.mechanism) {
            misc_addExceptionTypeValue(event, void 0, void 0);
            misc_addExceptionMechanism(event, options.mechanism);
          }
          event.extra = {
            ...event.extra,
            arguments: args
          };
          return event;
        });
        captureException(ex);
      });
      throw ex;
    } finally {
      worldwide_GLOBAL_OBJ._sentryWrappedDepth = (worldwide_GLOBAL_OBJ._sentryWrappedDepth || 0) - 1;
    }
  };
  try {
    for (const property in fn) {
      if (Object.prototype.hasOwnProperty.call(fn, property)) {
        sentryWrapped[property] = fn[property];
      }
    }
  } catch {
  }
  markFunctionWrapped(sentryWrapped, fn);
  object_addNonEnumerableProperty(fn, "__sentry_wrapped__", sentryWrapped);
  try {
    const descriptor = Object.getOwnPropertyDescriptor(sentryWrapped, "name");
    if (descriptor.configurable) {
      Object.defineProperty(sentryWrapped, "name", {
        get() {
          return fn.name;
        }
      });
    }
  } catch {
  }
  return sentryWrapped;
}
function getHttpRequestData() {
  const url = getLocationHref();
  const { referrer } = helpers_WINDOW.document || {};
  const { userAgent } = helpers_WINDOW.navigator || {};
  const headers = {
    ...referrer && { Referer: referrer },
    ...userAgent && { "User-Agent": userAgent }
  };
  const request = {
    url,
    headers
  };
  return request;
}


//# sourceMappingURL=helpers.js.map

;// ./node_modules/@sentry/browser/build/npm/esm/prod/client.js




class BrowserClient extends Client {
  /**
   * Creates a new Browser SDK instance.
   *
   * @param options Configuration options for this SDK.
   */
  constructor(options) {
    const opts = applyDefaultOptions(options);
    const sdkSource = helpers_WINDOW.SENTRY_SDK_SOURCE || getSDKSource();
    applySdkMetadata(opts, "browser", ["browser"], sdkSource);
    super(opts);
    const { userInfo } = this.getDataCollectionOptions();
    if (opts._metadata?.sdk) {
      opts._metadata.sdk.settings = {
        // Only allow IP inferral by Relay if the user opted in via dataCollection
        infer_ip: userInfo ? "auto" : "never",
        // purposefully allowing already passed settings to override the default
        ...opts._metadata.sdk.settings
      };
    }
    const { sendClientReports } = this._options;
    if (helpers_WINDOW.document) {
      helpers_WINDOW.document.addEventListener("visibilitychange", () => {
        if (helpers_WINDOW.document.visibilityState === "hidden") {
          if (sendClientReports) {
            this._flushOutcomes();
          }
          queueMicrotask(() => {
            void this.flush();
          });
        }
      });
    }
    if (userInfo) {
      this.on("beforeSendSession", addAutoIpAddressToSession);
    }
  }
  /**
   * @inheritDoc
   */
  eventFromException(exception, hint) {
    return eventFromException(this._options.stackParser, exception, hint, this._options.attachStacktrace);
  }
  /**
   * @inheritDoc
   */
  eventFromMessage(message, level = "info", hint) {
    return eventbuilder_eventFromMessage(this._options.stackParser, message, level, hint, this._options.attachStacktrace);
  }
  /**
   * @inheritDoc
   */
  _prepareEvent(event, hint, currentScope, isolationScope) {
    event.platform = event.platform || "javascript";
    return super._prepareEvent(event, hint, currentScope, isolationScope);
  }
}
function applyDefaultOptions(optionsArg) {
  return {
    release: typeof __SENTRY_RELEASE__ === "string" ? __SENTRY_RELEASE__ : helpers_WINDOW.SENTRY_RELEASE?.id,
    // This supports the variable that sentry-webpack-plugin injects
    sendClientReports: true,
    // We default this to true, as it is the safer scenario
    parentSpanIsAlwaysRootSpan: true,
    ...optionsArg
  };
}


//# sourceMappingURL=client.js.map

;// ./node_modules/@sentry/core/build/esm/instrument/handlers.js




const handlers = {};
const instrumented = {};
function handlers_addHandler(type, handler) {
  handlers[type] = handlers[type] || [];
  handlers[type].push(handler);
  return () => {
    const typeHandlers = handlers[type];
    if (typeHandlers) {
      const index = typeHandlers.indexOf(handler);
      if (index !== -1) {
        typeHandlers.splice(index, 1);
      }
    }
  };
}
function resetInstrumentationHandlers() {
  Object.keys(handlers).forEach((key) => {
    handlers[key] = void 0;
  });
}
function handlers_maybeInstrument(type, instrumentFn) {
  if (!instrumented[type]) {
    instrumented[type] = true;
    try {
      instrumentFn();
    } catch (e) {
      debug_build_DEBUG_BUILD && debug_logger_debug.error(`Error while instrumenting ${type}`, e);
    }
  }
}
function handlers_triggerHandlers(type, data) {
  const typeHandlers = type && handlers[type];
  if (!typeHandlers) {
    return;
  }
  for (const handler of typeHandlers) {
    try {
      handler(data);
    } catch (e) {
      debug_build_DEBUG_BUILD && debug_logger_debug.error(
        `Error while triggering instrumentation handler.
Type: ${type}
Name: ${getFunctionName(handler)}
Error:`,
        e
      );
    }
  }
}


//# sourceMappingURL=handlers.js.map

;// ./node_modules/@sentry/core/build/esm/instrument/console.js







const _filter = /* @__PURE__ */ new Set([]);
function addConsoleInstrumentationHandler(handler) {
  const type = "console";
  const removeHandler = handlers_addHandler(type, handler);
  handlers_maybeInstrument(type, instrumentConsole);
  return removeHandler;
}
function addConsoleInstrumentationFilter(filter) {
  for (const f of filter) {
    _filter.add(f);
  }
  return () => {
    for (const f of filter) {
      _filter.delete(f);
    }
  };
}
const instrumentedLevels = /* @__PURE__ */ new Set();
function instrumentConsole() {
  if (!("console" in worldwide_GLOBAL_OBJ)) {
    return;
  }
  CONSOLE_LEVELS.forEach(function(level) {
    if (instrumentedLevels.has(level) || !(level in worldwide_GLOBAL_OBJ.console)) {
      return;
    }
    instrumentedLevels.add(level);
    fill(worldwide_GLOBAL_OBJ.console, level, function(originalConsoleMethod) {
      originalConsoleMethods[level] = originalConsoleMethod;
      return function(...args) {
        const firstArg = args[0];
        const log = originalConsoleMethods[level];
        const isFiltered = _filter.size && typeof firstArg === "string" && stringMatchesSomePattern(firstArg, _filter);
        if (!isFiltered) {
          handlers_triggerHandlers("console", { args, level });
        }
        if (!isFiltered || debug_build_DEBUG_BUILD && debug_logger_debug.isEnabled()) {
          log?.apply(worldwide_GLOBAL_OBJ.console, args);
        }
      };
    });
  });
}


//# sourceMappingURL=console.js.map

;// ./node_modules/@sentry/core/build/esm/utils/supports.js




const supports_WINDOW = worldwide_GLOBAL_OBJ;
function supportsErrorEvent() {
  try {
    new ErrorEvent("");
    return true;
  } catch {
    return false;
  }
}
function supportsDOMError() {
  try {
    new DOMError("");
    return true;
  } catch {
    return false;
  }
}
function supportsDOMException() {
  try {
    new DOMException("");
    return true;
  } catch {
    return false;
  }
}
function supportsHistory() {
  return "history" in supports_WINDOW && !!supports_WINDOW.history;
}
const supportsFetch = (/* unused pure expression or super */ null && (_isFetchSupported));
function _isFetchSupported() {
  if (!("fetch" in supports_WINDOW)) {
    return false;
  }
  try {
    new Headers();
    new Request("data:,");
    new Response();
    return true;
  } catch {
    return false;
  }
}
function isNativeFunction(func) {
  return func && /^function\s+\w+\(\)\s+\{\s+\[native code\]\s+\}$/.test(func.toString());
}
function supportsNativeFetch() {
  if (typeof EdgeRuntime === "string") {
    return true;
  }
  if (!_isFetchSupported()) {
    return false;
  }
  if (isNativeFunction(supports_WINDOW.fetch)) {
    return true;
  }
  let result = false;
  const doc = supports_WINDOW.document;
  if (doc && typeof doc.createElement === "function") {
    try {
      const sandbox = doc.createElement("iframe");
      sandbox.hidden = true;
      doc.head.appendChild(sandbox);
      if (sandbox.contentWindow?.fetch) {
        result = isNativeFunction(sandbox.contentWindow.fetch);
      }
      doc.head.removeChild(sandbox);
    } catch (err) {
      debug_build_DEBUG_BUILD && debug_logger_debug.warn("Could not create sandbox iframe for pure fetch check, bailing to window.fetch: ", err);
    }
  }
  return result;
}
function supportsReportingObserver() {
  return "ReportingObserver" in supports_WINDOW;
}
function supportsReferrerPolicy() {
  if (!_isFetchSupported()) {
    return false;
  }
  try {
    new Request("_", {
      referrerPolicy: "origin"
    });
    return true;
  } catch {
    return false;
  }
}


//# sourceMappingURL=supports.js.map

;// ./node_modules/@sentry/core/build/esm/instrument/fetch.js








function addFetchInstrumentationHandler(handler, skipNativeFetchCheck) {
  const type = "fetch";
  const removeHandler = handlers_addHandler(type, handler);
  handlers_maybeInstrument(type, () => instrumentFetch(void 0, skipNativeFetchCheck));
  return removeHandler;
}
function addFetchEndInstrumentationHandler(handler) {
  const type = "fetch-body-resolved";
  const removeHandler = addHandler(type, handler);
  maybeInstrument(type, () => instrumentFetch(streamHandler));
  return removeHandler;
}
function instrumentFetch(onFetchResolved, skipNativeFetchCheck = false) {
  if (skipNativeFetchCheck && !supportsNativeFetch()) {
    return;
  }
  fill(worldwide_GLOBAL_OBJ, "fetch", function(originalFetch) {
    return function(...args) {
      const virtualError = new Error();
      const { method, url } = parseFetchArgs(args);
      const handlerData = {
        args,
        fetchData: {
          method,
          url
        },
        startTimestamp: time_timestampInSeconds() * 1e3,
        // // Adding the error to be able to fingerprint the failed fetch event in HttpClient instrumentation
        virtualError,
        headers: getHeadersFromFetchArgs(args)
      };
      if (!onFetchResolved) {
        handlers_triggerHandlers("fetch", {
          ...handlerData
        });
      }
      return originalFetch.apply(worldwide_GLOBAL_OBJ, args).then(
        async (response) => {
          if (onFetchResolved) {
            onFetchResolved(response);
          } else {
            handlers_triggerHandlers("fetch", {
              ...handlerData,
              endTimestamp: time_timestampInSeconds() * 1e3,
              response
            });
          }
          return response;
        },
        (error) => {
          handlers_triggerHandlers("fetch", {
            ...handlerData,
            endTimestamp: time_timestampInSeconds() * 1e3,
            error
          });
          if (is_isError(error) && error.stack === void 0) {
            error.stack = virtualError.stack;
            object_addNonEnumerableProperty(error, "framesToPop", 1);
          }
          const client = currentScopes_getClient();
          const enhanceOption = client?.getOptions().enhanceFetchErrorMessages ?? "always";
          const shouldEnhance = enhanceOption !== false;
          if (shouldEnhance && is_isError(error) && error.name === "TypeError" && (error.message === "Failed to fetch" || error.message === "Load failed" || error.message === "NetworkError when attempting to fetch resource.")) {
            try {
              const url2 = new URL(handlerData.fetchData.url);
              const hostname = url2.host;
              if (enhanceOption === "always") {
                error.message = `${error.message} (${hostname})`;
              } else {
                object_addNonEnumerableProperty(error, "__sentry_fetch_url_host__", hostname);
              }
            } catch {
            }
          }
          throw error;
        }
      );
    };
  });
}
async function resolveResponse(res, onFinishedResolving) {
  if (res?.body) {
    const body = res.body;
    const responseReader = body.getReader();
    const maxFetchDurationTimeout = setTimeout(
      () => {
        body.cancel().then(null, () => {
        });
      },
      90 * 1e3
      // 90s
    );
    let readingActive = true;
    while (readingActive) {
      let chunkTimeout;
      try {
        chunkTimeout = setTimeout(() => {
          body.cancel().then(null, () => {
          });
        }, 5e3);
        const { done } = await responseReader.read();
        clearTimeout(chunkTimeout);
        if (done) {
          onFinishedResolving();
          readingActive = false;
        }
      } catch {
        readingActive = false;
      } finally {
        clearTimeout(chunkTimeout);
      }
    }
    clearTimeout(maxFetchDurationTimeout);
    responseReader.releaseLock();
    body.cancel().then(null, () => {
    });
  }
}
function streamHandler(response) {
  let clonedResponseForResolving;
  try {
    clonedResponseForResolving = response.clone();
  } catch {
    return;
  }
  resolveResponse(clonedResponseForResolving, () => {
    triggerHandlers("fetch-body-resolved", {
      endTimestamp: timestampInSeconds() * 1e3,
      response
    });
  });
}
function hasProp(obj, prop) {
  return isObjectLike(obj) && !!obj[prop];
}
function getUrlFromResource(resource) {
  if (typeof resource === "string") {
    return resource;
  }
  if (!resource) {
    return "";
  }
  if (hasProp(resource, "url")) {
    return resource.url;
  }
  if (resource.toString) {
    return resource.toString();
  }
  return "";
}
function parseFetchArgs(fetchArgs) {
  if (fetchArgs.length === 0) {
    return { method: "GET", url: "" };
  }
  if (fetchArgs.length === 2) {
    const [resource, options] = fetchArgs;
    return {
      url: getUrlFromResource(resource),
      method: hasProp(options, "method") ? String(options.method).toUpperCase() : (
        // Request object as first argument
        isRequest(resource) && hasProp(resource, "method") ? String(resource.method).toUpperCase() : "GET"
      )
    };
  }
  const arg = fetchArgs[0];
  return {
    url: getUrlFromResource(arg),
    method: hasProp(arg, "method") ? String(arg.method).toUpperCase() : "GET"
  };
}
function getHeadersFromFetchArgs(fetchArgs) {
  const [requestArgument, optionsArgument] = fetchArgs;
  try {
    if (typeof optionsArgument === "object" && optionsArgument !== null && "headers" in optionsArgument && optionsArgument.headers) {
      return new Headers(optionsArgument.headers);
    }
    if (isRequest(requestArgument)) {
      return new Headers(requestArgument.headers);
    }
  } catch {
  }
  return;
}


//# sourceMappingURL=fetch.js.map

;// ./node_modules/@sentry/core/build/esm/breadcrumbs.js




const DEFAULT_BREADCRUMBS = 100;
function addBreadcrumb(breadcrumb, hint) {
  const client = currentScopes_getClient();
  const isolationScope = currentScopes_getIsolationScope();
  if (!client) return;
  const { beforeBreadcrumb = null, maxBreadcrumbs = DEFAULT_BREADCRUMBS } = client.getOptions();
  if (maxBreadcrumbs <= 0) return;
  const timestamp = dateTimestampInSeconds();
  const mergedBreadcrumb = { timestamp, ...breadcrumb };
  const finalBreadcrumb = beforeBreadcrumb ? debug_logger_consoleSandbox(() => beforeBreadcrumb(mergedBreadcrumb, hint)) : mergedBreadcrumb;
  if (finalBreadcrumb === null) return;
  if (client.emit) {
    client.emit("beforeAddBreadcrumb", finalBreadcrumb, hint);
  }
  isolationScope.addBreadcrumb(finalBreadcrumb, maxBreadcrumbs);
}


//# sourceMappingURL=breadcrumbs.js.map

;// ./node_modules/@sentry/core/build/esm/utils/severity.js
function severityLevelFromString(level) {
  return level === "warn" ? "warning" : ["fatal", "error", "warning", "log", "info", "debug"].includes(level) ? level : "log";
}


//# sourceMappingURL=severity.js.map

;// ./node_modules/@sentry/core/build/esm/utils/breadcrumb-log-level.js
function getBreadcrumbLogLevelFromHttpStatusCode(statusCode) {
  if (statusCode === void 0) {
    return void 0;
  } else if (statusCode >= 400 && statusCode < 500) {
    return "warning";
  } else if (statusCode >= 500) {
    return "error";
  } else {
    return void 0;
  }
}


//# sourceMappingURL=breadcrumb-log-level.js.map

;// ./node_modules/@sentry/core/build/esm/utils/url.js



const DEFAULT_BASE_URL = "thismessage:/";
function isURLObjectRelative(url) {
  return "isRelative" in url;
}
function parseStringToURLObject(url, urlBase) {
  const isRelative = url.indexOf("://") <= 0 && url.indexOf("//") !== 0;
  const base = urlBase ?? (isRelative ? DEFAULT_BASE_URL : void 0);
  try {
    if ("canParse" in URL && !URL.canParse(url, base)) {
      return void 0;
    }
    const fullUrlObject = new URL(url, base);
    if (isRelative) {
      return {
        isRelative,
        pathname: fullUrlObject.pathname,
        search: fullUrlObject.search,
        hash: fullUrlObject.hash
      };
    }
    return fullUrlObject;
  } catch {
  }
  return void 0;
}
function getSanitizedUrlStringFromUrlObject(url) {
  if (isURLObjectRelative(url)) {
    return url.pathname;
  }
  const newUrl = new URL(url);
  newUrl.search = "";
  newUrl.hash = "";
  if (["80", "443"].includes(newUrl.port)) {
    newUrl.port = "";
  }
  if (newUrl.password) {
    newUrl.password = "%filtered%";
  }
  if (newUrl.username) {
    newUrl.username = "%filtered%";
  }
  return newUrl.toString();
}
function getHttpSpanNameFromUrlObject(urlObject, kind, request, routeName) {
  const method = request?.method?.toUpperCase() ?? "GET";
  const route = routeName ? routeName : urlObject ? kind === "client" ? getSanitizedUrlStringFromUrlObject(urlObject) : urlObject.pathname : "/";
  return `${method} ${route}`;
}
function getHttpSpanDetailsFromUrlObject(urlObject, kind, spanOrigin, request, routeName) {
  const attributes = {
    [SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN]: spanOrigin,
    [SEMANTIC_ATTRIBUTE_SENTRY_SOURCE]: "url"
  };
  if (routeName) {
    attributes[kind === "server" ? "http.route" : "url.template"] = routeName;
    attributes[SEMANTIC_ATTRIBUTE_SENTRY_SOURCE] = "route";
  }
  if (request?.method) {
    attributes[SEMANTIC_ATTRIBUTE_HTTP_REQUEST_METHOD] = request.method.toUpperCase();
  }
  if (urlObject) {
    if (urlObject.search) {
      attributes["url.query"] = urlObject.search;
    }
    if (urlObject.hash) {
      attributes["url.fragment"] = urlObject.hash;
    }
    if (urlObject.pathname) {
      attributes["url.path"] = urlObject.pathname;
      if (urlObject.pathname === "/") {
        attributes[SEMANTIC_ATTRIBUTE_SENTRY_SOURCE] = "route";
      }
    }
    if (!isURLObjectRelative(urlObject)) {
      attributes[URL_FULL] = urlObject.href;
      if (urlObject.port) {
        attributes["url.port"] = urlObject.port;
      }
      if (urlObject.protocol) {
        attributes["url.scheme"] = urlObject.protocol;
      }
      if (urlObject.hostname) {
        attributes[kind === "server" ? "server.address" : "url.domain"] = urlObject.hostname;
      }
    }
  }
  return [getHttpSpanNameFromUrlObject(urlObject, kind, request, routeName), attributes];
}
function url_parseUrl(url) {
  if (!url) {
    return {};
  }
  const match = url.match(/^(([^:/?#]+):)?(\/\/([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?$/);
  if (!match) {
    return {};
  }
  const query = match[6] || "";
  const fragment = match[8] || "";
  return {
    host: match[4],
    path: match[5],
    protocol: match[2],
    search: query,
    hash: fragment,
    relative: match[5] + query + fragment
    // everything minus origin
  };
}
function stripUrlQueryAndFragment(urlPath) {
  return urlPath.split(/[?#]/, 1)[0];
}
function getSanitizedUrlString(url) {
  const { protocol, host, path } = url;
  const filteredHost = host?.replace(/^.*@/, "[filtered]:[filtered]@").replace(/(:80)$/, "").replace(/(:443)$/, "") || "";
  return `${protocol ? `${protocol}://` : ""}${filteredHost}${path}`;
}
function stripDataUrlContent(url, includeDataPrefix = true) {
  if (url.startsWith("data:")) {
    const match = url.match(/^data:([^;,]+)/);
    const mimeType = match ? match[1] : "text/plain";
    const isBase64 = url.includes(";base64,");
    const dataStart = url.indexOf(",");
    let dataPrefix = "";
    if (includeDataPrefix && dataStart !== -1) {
      const data = url.slice(dataStart + 1);
      dataPrefix = data.length > 10 ? `${data.slice(0, 10)}... [truncated]` : data;
    }
    return `data:${mimeType}${isBase64 ? ",base64" : ""}${dataPrefix ? `,${dataPrefix}` : ""}`;
  }
  return url;
}


//# sourceMappingURL=url.js.map

;// ./node_modules/@sentry/browser-utils/build/esm/types.js


const types_WINDOW = worldwide_GLOBAL_OBJ;


//# sourceMappingURL=types.js.map

;// ./node_modules/@sentry/browser-utils/build/esm/instrument/dom.js



const DEBOUNCE_DURATION = 1e3;
let debounceTimerID;
let lastCapturedEventType;
let lastCapturedEventTargetId;
function addClickKeypressInstrumentationHandler(handler) {
  const type = "dom";
  handlers_addHandler(type, handler);
  handlers_maybeInstrument(type, instrumentDOM);
}
function instrumentDOM() {
  if (!types_WINDOW.document) {
    return;
  }
  const triggerDOMHandler = handlers_triggerHandlers.bind(null, "dom");
  const globalDOMEventHandler = makeDOMEventHandler(triggerDOMHandler, true);
  types_WINDOW.document.addEventListener("click", globalDOMEventHandler, false);
  types_WINDOW.document.addEventListener("keypress", globalDOMEventHandler, false);
  ["EventTarget", "Node"].forEach((target) => {
    const globalObject = types_WINDOW;
    const proto = globalObject[target]?.prototype;
    if (!proto?.hasOwnProperty?.("addEventListener")) {
      return;
    }
    fill(proto, "addEventListener", function(originalAddEventListener) {
      return function(type, listener, options) {
        if (type === "click" || type == "keypress") {
          try {
            const handlers = this.__sentry_instrumentation_handlers__ = this.__sentry_instrumentation_handlers__ || {};
            const handlerForType = handlers[type] = handlers[type] || { refCount: 0 };
            if (!handlerForType.handler) {
              const handler = makeDOMEventHandler(triggerDOMHandler);
              handlerForType.handler = handler;
              originalAddEventListener.call(this, type, handler, options);
            }
            handlerForType.refCount++;
          } catch {
          }
        }
        return originalAddEventListener.call(this, type, listener, options);
      };
    });
    fill(
      proto,
      "removeEventListener",
      function(originalRemoveEventListener) {
        return function(type, listener, options) {
          if (type === "click" || type == "keypress") {
            try {
              const handlers = this.__sentry_instrumentation_handlers__ || {};
              const handlerForType = handlers[type];
              if (handlerForType) {
                handlerForType.refCount--;
                if (handlerForType.refCount <= 0) {
                  originalRemoveEventListener.call(this, type, handlerForType.handler, options);
                  handlerForType.handler = void 0;
                  delete handlers[type];
                }
                if (Object.keys(handlers).length === 0) {
                  delete this.__sentry_instrumentation_handlers__;
                }
              }
            } catch {
            }
          }
          return originalRemoveEventListener.call(this, type, listener, options);
        };
      }
    );
  });
}
function isSimilarToLastCapturedEvent(event) {
  if (event.type !== lastCapturedEventType) {
    return false;
  }
  try {
    if (!event.target || event.target._sentryId !== lastCapturedEventTargetId) {
      return false;
    }
  } catch {
  }
  return true;
}
function shouldSkipDOMEvent(eventType, target) {
  if (eventType !== "keypress") {
    return false;
  }
  if (!target?.tagName) {
    return true;
  }
  if (target.tagName === "INPUT" || target.tagName === "TEXTAREA" || target.isContentEditable) {
    return false;
  }
  return true;
}
function makeDOMEventHandler(handler, globalListener = false) {
  return (event) => {
    if (!event || event["_sentryCaptured"]) {
      return;
    }
    const target = getEventTarget(event);
    if (shouldSkipDOMEvent(event.type, target)) {
      return;
    }
    object_addNonEnumerableProperty(event, "_sentryCaptured", true);
    if (target && !target._sentryId) {
      object_addNonEnumerableProperty(target, "_sentryId", misc_uuid4());
    }
    const name = event.type === "keypress" ? "input" : event.type;
    if (!isSimilarToLastCapturedEvent(event)) {
      const handlerData = { event, name, global: globalListener };
      handler(handlerData);
      lastCapturedEventType = event.type;
      lastCapturedEventTargetId = target ? target._sentryId : void 0;
    }
    clearTimeout(debounceTimerID);
    debounceTimerID = types_WINDOW.setTimeout(() => {
      lastCapturedEventTargetId = void 0;
      lastCapturedEventType = void 0;
    }, DEBOUNCE_DURATION);
  };
}
function getEventTarget(event) {
  try {
    return event.target;
  } catch {
    return null;
  }
}


//# sourceMappingURL=dom.js.map

;// ./node_modules/@sentry/browser-utils/build/esm/instrument/xhr.js



const SENTRY_XHR_DATA_KEY = "__sentry_xhr_v3__";
function addXhrInstrumentationHandler(handler) {
  const type = "xhr";
  handlers_addHandler(type, handler);
  handlers_maybeInstrument(type, instrumentXHR);
}
function instrumentXHR() {
  if (!types_WINDOW.XMLHttpRequest) {
    return;
  }
  const xhrproto = XMLHttpRequest.prototype;
  xhrproto.open = new Proxy(xhrproto.open, {
    apply(originalOpen, xhrOpenThisArg, xhrOpenArgArray) {
      const virtualError = new Error();
      const startTimestamp = time_timestampInSeconds() * 1e3;
      const method = is_isString(xhrOpenArgArray[0]) ? xhrOpenArgArray[0].toUpperCase() : void 0;
      const url = parseXhrUrlArg(xhrOpenArgArray[1]);
      if (!method || !url) {
        return originalOpen.apply(xhrOpenThisArg, xhrOpenArgArray);
      }
      xhrOpenThisArg[SENTRY_XHR_DATA_KEY] = {
        method,
        url,
        request_headers: {}
      };
      if (method === "POST" && url.match(/sentry_key/)) {
        xhrOpenThisArg.__sentry_own_request__ = true;
      }
      const onreadystatechangeHandler = () => {
        const xhrInfo = xhrOpenThisArg[SENTRY_XHR_DATA_KEY];
        if (!xhrInfo) {
          return;
        }
        if (xhrOpenThisArg.readyState === 4) {
          try {
            xhrInfo.status_code = xhrOpenThisArg.status;
          } catch {
          }
          const handlerData = {
            endTimestamp: time_timestampInSeconds() * 1e3,
            startTimestamp,
            xhr: xhrOpenThisArg,
            virtualError
          };
          handlers_triggerHandlers("xhr", handlerData);
          xhrOpenThisArg.removeEventListener("readystatechange", onreadystatechangeHandler);
        }
      };
      if ("onreadystatechange" in xhrOpenThisArg && typeof xhrOpenThisArg.onreadystatechange === "function") {
        xhrOpenThisArg.onreadystatechange = new Proxy(xhrOpenThisArg.onreadystatechange, {
          apply(originalOnreadystatechange, onreadystatechangeThisArg, onreadystatechangeArgArray) {
            onreadystatechangeHandler();
            return originalOnreadystatechange.apply(onreadystatechangeThisArg, onreadystatechangeArgArray);
          }
        });
      } else {
        xhrOpenThisArg.addEventListener("readystatechange", onreadystatechangeHandler);
      }
      xhrOpenThisArg.setRequestHeader = new Proxy(xhrOpenThisArg.setRequestHeader, {
        apply(originalSetRequestHeader, setRequestHeaderThisArg, setRequestHeaderArgArray) {
          const [header, value] = setRequestHeaderArgArray;
          const xhrInfo = setRequestHeaderThisArg[SENTRY_XHR_DATA_KEY];
          if (xhrInfo && is_isString(header) && is_isString(value)) {
            xhrInfo.request_headers[header.toLowerCase()] = value;
          }
          return originalSetRequestHeader.apply(setRequestHeaderThisArg, setRequestHeaderArgArray);
        }
      });
      return originalOpen.apply(xhrOpenThisArg, xhrOpenArgArray);
    }
  });
  xhrproto.send = new Proxy(xhrproto.send, {
    apply(originalSend, sendThisArg, sendArgArray) {
      const sentryXhrData = sendThisArg[SENTRY_XHR_DATA_KEY];
      if (!sentryXhrData) {
        return originalSend.apply(sendThisArg, sendArgArray);
      }
      if (sendArgArray[0] !== void 0) {
        sentryXhrData.body = sendArgArray[0];
      }
      const handlerData = {
        startTimestamp: time_timestampInSeconds() * 1e3,
        xhr: sendThisArg
      };
      handlers_triggerHandlers("xhr", handlerData);
      return originalSend.apply(sendThisArg, sendArgArray);
    }
  });
}
function parseXhrUrlArg(url) {
  if (is_isString(url)) {
    return url;
  }
  try {
    return url.toString();
  } catch {
  }
  return void 0;
}


//# sourceMappingURL=xhr.js.map

;// ./node_modules/@sentry/browser-utils/build/esm/instrument/history.js



let lastHref;
function addHistoryInstrumentationHandler(handler) {
  const type = "history";
  handlers_addHandler(type, handler);
  handlers_maybeInstrument(type, instrumentHistory);
}
function instrumentHistory() {
  types_WINDOW.addEventListener("popstate", () => {
    const to = types_WINDOW.location.href;
    const from = lastHref;
    lastHref = to;
    if (from === to) {
      return;
    }
    const handlerData = { from, to };
    handlers_triggerHandlers("history", handlerData);
  });
  if (!supportsHistory()) {
    return;
  }
  function historyReplacementFunction(originalHistoryFunction) {
    return function(...args) {
      const url = args.length > 2 ? args[2] : void 0;
      if (url) {
        const from = lastHref;
        const to = getAbsoluteUrl(String(url));
        lastHref = to;
        if (from === to) {
          return originalHistoryFunction.apply(this, args);
        }
        const handlerData = { from, to };
        handlers_triggerHandlers("history", handlerData);
      }
      return originalHistoryFunction.apply(this, args);
    };
  }
  fill(types_WINDOW.history, "pushState", historyReplacementFunction);
  fill(types_WINDOW.history, "replaceState", historyReplacementFunction);
}
function getAbsoluteUrl(urlOrPath) {
  try {
    const url = new URL(urlOrPath, types_WINDOW.location.origin);
    return url.toString();
  } catch {
    return urlOrPath;
  }
}


//# sourceMappingURL=history.js.map

;// ./node_modules/@sentry/browser-utils/build/esm/htmlTreeAsString.js


const htmlTreeAsString_DEFAULT_MAX_STRING_LENGTH = 80;
const accessors = {};
try {
  if (typeof Node !== "undefined") {
    accessors.parentNode = Object.getOwnPropertyDescriptor(Node.prototype, "parentNode").get;
  }
  if (typeof Element !== "undefined") {
    accessors.tagName = Object.getOwnPropertyDescriptor(Element.prototype, "tagName").get;
    accessors.id = Object.getOwnPropertyDescriptor(Element.prototype, "id").get;
    accessors.className = Object.getOwnPropertyDescriptor(Element.prototype, "className").get;
    accessors.getAttribute = Element.prototype.getAttribute;
  }
  if (typeof HTMLElement !== "undefined") {
    accessors.dataset = Object.getOwnPropertyDescriptor(HTMLElement.prototype, "dataset").get;
  }
} catch {
}
function _safeRead(el, prop, arg) {
  const fn = accessors[prop];
  if (fn) {
    try {
      return fn.call(el, arg);
    } catch {
    }
  }
  const val = el[prop];
  return typeof val === "function" ? val.call(el, arg) : val;
}
function htmlTreeAsString_htmlTreeAsString(elem, options = {}) {
  if (!elem) {
    return "<unknown>";
  }
  try {
    let currentElem = elem;
    const MAX_TRAVERSE_HEIGHT = 5;
    const out = [];
    let height = 0;
    let len = 0;
    const separator = " > ";
    const sepLength = separator.length;
    let nextStr;
    const keyAttrs = Array.isArray(options) ? options : options.keyAttrs;
    const maxStringLength = !Array.isArray(options) && options.maxStringLength || htmlTreeAsString_DEFAULT_MAX_STRING_LENGTH;
    while (currentElem && height++ < MAX_TRAVERSE_HEIGHT) {
      nextStr = htmlTreeAsString_htmlElementAsString(currentElem, keyAttrs);
      if (nextStr === "html" || height > 1 && len + out.length * sepLength + nextStr.length >= maxStringLength) {
        break;
      }
      out.push(nextStr);
      len += nextStr.length;
      currentElem = _safeRead(currentElem, "parentNode");
    }
    return out.reverse().join(separator);
  } catch {
    return "<unknown>";
  }
}
function htmlTreeAsString_htmlElementAsString(el, keyAttrs) {
  const out = [];
  const tagName = _safeRead(el, "tagName");
  if (!tagName) {
    return "";
  }
  if (typeof HTMLElement !== "undefined") {
    if (el instanceof HTMLElement) {
      const dataset = _safeRead(el, "dataset");
      if (dataset) {
        if (dataset["sentryComponent"]) {
          return dataset["sentryComponent"];
        }
        if (dataset["sentryElement"]) {
          return dataset["sentryElement"];
        }
      }
    }
  }
  out.push(tagName.toLowerCase());
  const keyAttrPairs = keyAttrs?.length ? keyAttrs.filter((keyAttr) => _safeRead(el, "getAttribute", keyAttr)).map((keyAttr) => [keyAttr, _safeRead(el, "getAttribute", keyAttr)]) : null;
  if (keyAttrPairs?.length) {
    keyAttrPairs.forEach((keyAttrPair) => {
      out.push(`[${keyAttrPair[0]}="${keyAttrPair[1]}"]`);
    });
  } else {
    const id = _safeRead(el, "id");
    if (id) {
      out.push(`#${id}`);
    }
    const className = _safeRead(el, "className");
    if (className && is_isString(className)) {
      const classes = className.split(/\s+/);
      for (const c of classes) {
        out.push(`.${c}`);
      }
    }
  }
  for (const k of ["aria-label", "type", "name", "title", "alt"]) {
    const attr = _safeRead(el, "getAttribute", k);
    if (attr) {
      out.push(`[${k}="${attr}"]`);
    }
  }
  return out.join("");
}


//# sourceMappingURL=htmlTreeAsString.js.map

;// ./node_modules/@sentry/browser/build/npm/esm/prod/debug-build.js
const prod_debug_build_DEBUG_BUILD = (typeof __SENTRY_DEBUG__ === 'undefined' || __SENTRY_DEBUG__);


//# sourceMappingURL=debug-build.js.map

;// ./node_modules/@sentry/browser/build/npm/esm/prod/integrations/breadcrumbs.js





const MAX_ALLOWED_STRING_LENGTH = 1024;
const breadcrumbs_INTEGRATION_NAME = "Breadcrumbs";
const _breadcrumbsIntegration = ((options = {}) => {
  const _options = {
    console: true,
    dom: true,
    fetch: true,
    history: true,
    sentry: true,
    xhr: true,
    ...options
  };
  return {
    name: breadcrumbs_INTEGRATION_NAME,
    setup(client) {
      if (_options.console) {
        addConsoleInstrumentationHandler(_getConsoleBreadcrumbHandler(client));
      }
      if (_options.dom) {
        addClickKeypressInstrumentationHandler(_getDomBreadcrumbHandler(client, _options.dom));
      }
      if (_options.xhr) {
        addXhrInstrumentationHandler(_getXhrBreadcrumbHandler(client));
      }
      if (_options.fetch) {
        addFetchInstrumentationHandler(_getFetchBreadcrumbHandler(client));
      }
      if (_options.history) {
        addHistoryInstrumentationHandler(_getHistoryBreadcrumbHandler(client));
      }
      if (_options.sentry) {
        client.on("beforeSendEvent", _getSentryBreadcrumbHandler(client));
      }
    }
  };
});
const breadcrumbsIntegration = defineIntegration(_breadcrumbsIntegration);
function _getSentryBreadcrumbHandler(client) {
  return function addSentryBreadcrumb(event) {
    if (currentScopes_getClient() !== client) {
      return;
    }
    addBreadcrumb(
      {
        category: `sentry.${event.type === "transaction" ? "transaction" : "event"}`,
        event_id: event.event_id,
        level: event.level,
        message: getEventDescription(event)
      },
      {
        event
      }
    );
  };
}
function _getDomBreadcrumbHandler(client, dom) {
  return function _innerDomBreadcrumb(handlerData) {
    if (currentScopes_getClient() !== client) {
      return;
    }
    let target;
    let componentName;
    let keyAttrs = typeof dom === "object" ? dom.serializeAttribute : void 0;
    let maxStringLength = typeof dom === "object" && typeof dom.maxStringLength === "number" ? dom.maxStringLength : void 0;
    if (maxStringLength && maxStringLength > MAX_ALLOWED_STRING_LENGTH) {
      prod_debug_build_DEBUG_BUILD && debug_logger_debug.warn(
        `\`dom.maxStringLength\` cannot exceed ${MAX_ALLOWED_STRING_LENGTH}, but a value of ${maxStringLength} was configured. Sentry will use ${MAX_ALLOWED_STRING_LENGTH} instead.`
      );
      maxStringLength = MAX_ALLOWED_STRING_LENGTH;
    }
    if (typeof keyAttrs === "string") {
      keyAttrs = [keyAttrs];
    }
    try {
      const event = handlerData.event;
      const element = _isEvent(event) ? event.target : event;
      target = htmlTreeAsString_htmlTreeAsString(element, { keyAttrs, maxStringLength });
      componentName = getComponentName(element);
    } catch {
      target = "<unknown>";
    }
    if (target.length === 0) {
      return;
    }
    const breadcrumb = {
      category: `ui.${handlerData.name}`,
      message: target
    };
    if (componentName) {
      breadcrumb.data = { "ui.component_name": componentName };
    }
    addBreadcrumb(breadcrumb, {
      event: handlerData.event,
      name: handlerData.name,
      global: handlerData.global
    });
  };
}
function _getConsoleBreadcrumbHandler(client) {
  return function _consoleBreadcrumb(handlerData) {
    if (currentScopes_getClient() !== client) {
      return;
    }
    const breadcrumb = {
      category: "console",
      data: {
        arguments: handlerData.args,
        logger: "console"
      },
      level: severityLevelFromString(handlerData.level),
      message: safeJoin(handlerData.args, " ")
    };
    if (handlerData.level === "assert") {
      if (handlerData.args[0] === false) {
        breadcrumb.message = `Assertion failed: ${safeJoin(handlerData.args.slice(1), " ") || "console.assert"}`;
        breadcrumb.data.arguments = handlerData.args.slice(1);
      } else {
        return;
      }
    }
    addBreadcrumb(breadcrumb, {
      input: handlerData.args,
      level: handlerData.level
    });
  };
}
function _getXhrBreadcrumbHandler(client) {
  return function _xhrBreadcrumb(handlerData) {
    if (currentScopes_getClient() !== client) {
      return;
    }
    const { startTimestamp, endTimestamp } = handlerData;
    const sentryXhrData = handlerData.xhr[SENTRY_XHR_DATA_KEY];
    if (!startTimestamp || !endTimestamp || !sentryXhrData) {
      return;
    }
    const { method, url, status_code, body } = sentryXhrData;
    const data = {
      method,
      url,
      status_code
    };
    const hint = {
      xhr: handlerData.xhr,
      input: body,
      startTimestamp,
      endTimestamp
    };
    const breadcrumb = {
      category: "xhr",
      data,
      type: "http",
      level: getBreadcrumbLogLevelFromHttpStatusCode(status_code)
    };
    client.emit("beforeOutgoingRequestBreadcrumb", breadcrumb, hint);
    addBreadcrumb(breadcrumb, hint);
  };
}
function _getFetchBreadcrumbHandler(client) {
  return function _fetchBreadcrumb(handlerData) {
    if (currentScopes_getClient() !== client) {
      return;
    }
    const { startTimestamp, endTimestamp } = handlerData;
    if (!endTimestamp) {
      return;
    }
    if (handlerData.fetchData.url.match(/sentry_key/) && handlerData.fetchData.method === "POST") {
      return;
    }
    if (handlerData.error) {
      const hint = {
        data: handlerData.error,
        input: handlerData.args,
        startTimestamp,
        endTimestamp
      };
      const breadcrumb = {
        category: "fetch",
        data: handlerData.fetchData,
        level: "error",
        type: "http"
      };
      client.emit("beforeOutgoingRequestBreadcrumb", breadcrumb, hint);
      addBreadcrumb(breadcrumb, hint);
    } else {
      const response = handlerData.response;
      const data = {
        ...handlerData.fetchData,
        status_code: response?.status
      };
      const hint = {
        input: handlerData.args,
        response,
        startTimestamp,
        endTimestamp
      };
      const breadcrumb = {
        category: "fetch",
        data,
        type: "http",
        level: getBreadcrumbLogLevelFromHttpStatusCode(data.status_code)
      };
      client.emit("beforeOutgoingRequestBreadcrumb", breadcrumb, hint);
      addBreadcrumb(breadcrumb, hint);
    }
  };
}
function _getHistoryBreadcrumbHandler(client) {
  return function _historyBreadcrumb(handlerData) {
    if (currentScopes_getClient() !== client) {
      return;
    }
    let from = handlerData.from;
    let to = handlerData.to;
    const parsedLoc = url_parseUrl(helpers_WINDOW.location.href);
    let parsedFrom = from ? url_parseUrl(from) : void 0;
    const parsedTo = url_parseUrl(to);
    if (!parsedFrom?.path) {
      parsedFrom = parsedLoc;
    }
    if (parsedLoc.protocol === parsedTo.protocol && parsedLoc.host === parsedTo.host) {
      to = parsedTo.relative;
    }
    if (parsedLoc.protocol === parsedFrom.protocol && parsedLoc.host === parsedFrom.host) {
      from = parsedFrom.relative;
    }
    addBreadcrumb({
      category: "navigation",
      data: {
        from,
        to
      }
    });
  };
}
function _isEvent(event) {
  return !!event && !!event.target;
}


//# sourceMappingURL=breadcrumbs.js.map

;// ./node_modules/@sentry/browser/build/npm/esm/prod/integrations/browserapierrors.js



const DEFAULT_EVENT_TARGET = "EventTarget,Window,Node,ApplicationCache,AudioTrackList,BroadcastChannel,ChannelMergerNode,CryptoOperation,EventSource,FileReader,HTMLUnknownElement,IDBDatabase,IDBRequest,IDBTransaction,KeyOperation,MediaController,MessagePort,ModalWindow,Notification,SVGElementInstance,Screen,SharedWorker,TextTrack,TextTrackCue,TextTrackList,WebSocket,WebSocketWorker,Worker,XMLHttpRequest,XMLHttpRequestEventTarget,XMLHttpRequestUpload".split(
  ","
);
const browserapierrors_INTEGRATION_NAME = "BrowserApiErrors";
const _browserApiErrorsIntegration = ((options = {}) => {
  const _options = {
    XMLHttpRequest: true,
    eventTarget: true,
    requestAnimationFrame: true,
    setInterval: true,
    setTimeout: true,
    unregisterOriginalCallbacks: false,
    ...options
  };
  return {
    name: browserapierrors_INTEGRATION_NAME,
    // TODO: This currently only works for the first client this is setup
    // We may want to adjust this to check for client etc.
    setupOnce() {
      if (_options.setTimeout) {
        fill(helpers_WINDOW, "setTimeout", _wrapTimeFunction);
      }
      if (_options.setInterval) {
        fill(helpers_WINDOW, "setInterval", _wrapTimeFunction);
      }
      if (_options.requestAnimationFrame) {
        fill(helpers_WINDOW, "requestAnimationFrame", _wrapRAF);
      }
      if (_options.XMLHttpRequest && "XMLHttpRequest" in helpers_WINDOW) {
        fill(XMLHttpRequest.prototype, "send", _wrapXHR);
      }
      const eventTargetOption = _options.eventTarget;
      if (eventTargetOption) {
        const eventTarget = Array.isArray(eventTargetOption) ? eventTargetOption : DEFAULT_EVENT_TARGET;
        eventTarget.forEach((target) => _wrapEventTarget(target, _options));
      }
    }
  };
});
const browserApiErrorsIntegration = defineIntegration(_browserApiErrorsIntegration);
function _wrapTimeFunction(original) {
  return function(...args) {
    const originalCallback = args[0];
    args[0] = wrap(originalCallback, {
      mechanism: {
        handled: false,
        type: `auto.browser.browserapierrors.${getFunctionName(original)}`
      }
    });
    return original.apply(this, args);
  };
}
function _wrapRAF(original) {
  return function(callback) {
    return original.apply(this, [
      wrap(callback, {
        mechanism: {
          data: {
            handler: getFunctionName(original)
          },
          handled: false,
          type: "auto.browser.browserapierrors.requestAnimationFrame"
        }
      })
    ]);
  };
}
function _wrapXHR(originalSend) {
  return function(...args) {
    const xhr = this;
    const xmlHttpRequestProps = ["onload", "onerror", "onprogress", "onreadystatechange"];
    xmlHttpRequestProps.forEach((prop) => {
      if (prop in xhr && typeof xhr[prop] === "function") {
        fill(xhr, prop, function(original) {
          const wrapOptions = {
            mechanism: {
              data: {
                handler: getFunctionName(original)
              },
              handled: false,
              type: `auto.browser.browserapierrors.xhr.${prop}`
            }
          };
          const originalFunction = getOriginalFunction(original);
          if (originalFunction) {
            wrapOptions.mechanism.data.handler = getFunctionName(originalFunction);
          }
          return wrap(original, wrapOptions);
        });
      }
    });
    return originalSend.apply(this, args);
  };
}
function _wrapEventTarget(target, integrationOptions) {
  const globalObject = helpers_WINDOW;
  const proto = globalObject[target]?.prototype;
  if (!proto?.hasOwnProperty?.("addEventListener")) {
    return;
  }
  fill(proto, "addEventListener", function(original) {
    return function(eventName, fn, options) {
      try {
        if (isEventListenerObject(fn)) {
          fn.handleEvent = wrap(fn.handleEvent, {
            mechanism: {
              data: {
                handler: getFunctionName(fn),
                target
              },
              handled: false,
              type: "auto.browser.browserapierrors.handleEvent"
            }
          });
        }
      } catch {
      }
      if (integrationOptions.unregisterOriginalCallbacks) {
        unregisterOriginalCallback(this, eventName, fn);
      }
      return original.apply(this, [
        eventName,
        wrap(fn, {
          mechanism: {
            data: {
              handler: getFunctionName(fn),
              target
            },
            handled: false,
            type: "auto.browser.browserapierrors.addEventListener"
          }
        }),
        options
      ]);
    };
  });
  fill(proto, "removeEventListener", function(originalRemoveEventListener) {
    return function(eventName, fn, options) {
      try {
        if (Object.prototype.hasOwnProperty.call(fn, "__sentry_wrapped__")) {
          const originalEventHandler = fn.__sentry_wrapped__;
          if (originalEventHandler) {
            originalRemoveEventListener.call(this, eventName, originalEventHandler, options);
          }
        }
      } catch {
      }
      return originalRemoveEventListener.call(this, eventName, fn, options);
    };
  });
}
function isEventListenerObject(obj) {
  return typeof obj.handleEvent === "function";
}
function unregisterOriginalCallback(target, eventName, fn) {
  if (target && typeof target === "object" && "removeEventListener" in target && typeof target.removeEventListener === "function") {
    target.removeEventListener(eventName, fn);
  }
}


//# sourceMappingURL=browserapierrors.js.map

;// ./node_modules/@sentry/browser-utils/build/esm/metrics/web-vitals/lib/globalListeners.js


function addPageListener(type, listener, options) {
  if (types_WINDOW.document) {
    types_WINDOW.addEventListener(type, listener, options);
  }
}
function removePageListener(type, listener, options) {
  if (types_WINDOW.document) {
    types_WINDOW.removeEventListener(type, listener, options);
  }
}


//# sourceMappingURL=globalListeners.js.map

;// ./node_modules/@sentry/browser-utils/build/esm/metrics/web-vitals/lib/runOnce.js
const runOnce = (cb) => {
  let called = false;
  return () => {
    if (!called) {
      cb();
      called = true;
    }
  };
};


//# sourceMappingURL=runOnce.js.map

;// ./node_modules/@sentry/browser-utils/build/esm/metrics/web-vitals/lib/whenIdleOrHidden.js




const whenIdleOrHidden = (cb) => {
  const rIC = types_WINDOW.requestIdleCallback || types_WINDOW.setTimeout;
  if (types_WINDOW.document?.visibilityState === "hidden") {
    cb();
  } else {
    cb = runOnce(cb);
    addPageListener("visibilitychange", cb, { once: true, capture: true });
    addPageListener("pagehide", cb, { once: true, capture: true });
    rIC(() => {
      cb();
      removePageListener("visibilitychange", cb, { capture: true });
      removePageListener("pagehide", cb, { capture: true });
    });
  }
};


//# sourceMappingURL=whenIdleOrHidden.js.map

;// ./node_modules/@sentry/browser/build/npm/esm/prod/integrations/browsersession.js





const browserSessionIntegration = defineIntegration((options = {}) => {
  const lifecycle = options.lifecycle ?? "route";
  return {
    name: "BrowserSession",
    setupOnce() {
      if (typeof helpers_WINDOW.document === "undefined") {
        prod_debug_build_DEBUG_BUILD && debug_logger_debug.warn("Using the `browserSessionIntegration` in non-browser environments is not supported.");
        return;
      }
      startSession({ ignoreDuration: true });
      let initialSessionSent = false;
      whenIdleOrHidden(() => {
        if (!initialSessionSent) {
          captureSession();
          initialSessionSent = true;
        }
      });
      const isolationScope = currentScopes_getIsolationScope();
      let previousUser = isolationScope.getUser();
      isolationScope.addScopeListener((scope) => {
        const maybeNewUser = scope.getUser();
        if (previousUser?.id !== maybeNewUser?.id || previousUser?.ip_address !== maybeNewUser?.ip_address) {
          previousUser = maybeNewUser;
          if (initialSessionSent) {
            captureSession();
          }
        }
      });
      if (lifecycle === "route") {
        addHistoryInstrumentationHandler(({ from, to }) => {
          if (from !== to) {
            startSession({ ignoreDuration: true });
            captureSession();
            initialSessionSent = true;
          }
        });
      }
    }
  };
});


//# sourceMappingURL=browsersession.js.map

;// ./node_modules/@sentry/core/build/esm/tracing/spans/captureSpan.js









function captureSpan(span, client) {
  const spanJSON = spanToStreamedSpanJSON(span);
  const segmentSpan = INTERNAL_getSegmentSpan(span);
  const serializedSegmentSpan = spanToStreamedSpanJSON(segmentSpan);
  const { isolationScope: spanIsolationScope, scope: spanScope } = getCapturedScopesOnSpan(span);
  const finalScopeData = getCombinedScopeData(spanIsolationScope, spanScope);
  applyCommonSpanAttributes(spanJSON, serializedSegmentSpan, client, finalScopeData);
  const spanKind = span.kind;
  client.emit("preprocessSpan", spanJSON, { spanKind });
  if (spanJSON.is_segment) {
    applyScopeToSegmentSpan(spanJSON, finalScopeData);
    applySdkMetadataToSegmentSpan(spanJSON, client);
    client.emit("processSegmentSpan", spanJSON);
  }
  client.emit("processSpan", spanJSON);
  const { beforeSendSpan } = client.getOptions();
  const processedSpan = beforeSendSpan && isStreamedBeforeSendSpanCallback(beforeSendSpan) ? applyBeforeSendSpanCallback(spanJSON, beforeSendSpan) : spanJSON;
  const spanNameSource = processedSpan.attributes?.[SEMANTIC_ATTRIBUTE_SENTRY_SOURCE];
  if (spanJSON.is_segment && spanNameSource) {
    safeSetSpanJSONAttributes(processedSpan, {
      ["sentry.segment.name.source"]: spanNameSource
    });
  }
  return {
    ...streamedSpanJsonToSerializedSpan(processedSpan),
    _segmentSpan: segmentSpan
  };
}
function applyScopeToSegmentSpan(segmentSpanJSON, scopeData) {
  const contextAttributes = scopeContextsToSpanAttributes(scopeData.contexts);
  safeSetSpanJSONAttributes(segmentSpanJSON, contextAttributes);
}
function safeSetSpanJSONAttributes(spanJSON, newAttributes) {
  const originalAttributes = spanJSON.attributes ?? (spanJSON.attributes = {});
  Object.entries(newAttributes).forEach(([key, value]) => {
    if (value != null && !(key in originalAttributes)) {
      originalAttributes[key] = value;
    }
  });
}
function applySdkMetadataToSegmentSpan(segmentSpanJSON, client) {
  const integrationNames = client.getIntegrationNames();
  if (!integrationNames.length) return;
  safeSetSpanJSONAttributes(segmentSpanJSON, {
    [SEMANTIC_ATTRIBUTE_SENTRY_SDK_INTEGRATIONS]: integrationNames
  });
}
function applyCommonSpanAttributes(spanJSON, serializedSegmentSpan, client, scopeData) {
  const sdk = client.getSdkMetadata();
  const { release, environment } = client.getOptions();
  safeSetSpanJSONAttributes(spanJSON, {
    [SENTRY_TRACE_LIFECYCLE]: "stream",
    [SENTRY_SEGMENT_NAME]: serializedSegmentSpan.name,
    [SENTRY_SEGMENT_ID]: serializedSegmentSpan.span_id,
    [SENTRY_SDK_NAME]: sdk?.sdk?.name,
    [SENTRY_SDK_VERSION]: sdk?.sdk?.version,
    [SEMANTIC_ATTRIBUTE_SENTRY_RELEASE]: release,
    [SEMANTIC_ATTRIBUTE_SENTRY_ENVIRONMENT]: environment || DEFAULT_ENVIRONMENT,
    [SEMANTIC_ATTRIBUTE_USER_ID]: scopeData.user?.id,
    [SEMANTIC_ATTRIBUTE_USER_EMAIL]: scopeData.user?.email,
    [SEMANTIC_ATTRIBUTE_USER_IP_ADDRESS]: scopeData.user?.ip_address,
    [SEMANTIC_ATTRIBUTE_USER_USERNAME]: scopeData.user?.username,
    ...scopeData.attributes
  });
}
function applyBeforeSendSpanCallback(span, beforeSendSpan) {
  const modifedSpan = beforeSendSpan(span);
  if (!modifedSpan) {
    showSpanDropWarning();
    return span;
  }
  return modifedSpan;
}


//# sourceMappingURL=captureSpan.js.map

;// ./node_modules/@sentry/browser/build/npm/esm/prod/integrations/culturecontext.js



const culturecontext_INTEGRATION_NAME = "CultureContext";
const _cultureContextIntegration = (() => {
  return {
    name: culturecontext_INTEGRATION_NAME,
    preprocessEvent(event) {
      const culture = getCultureContext();
      if (culture) {
        event.contexts = {
          ...event.contexts,
          culture: { ...culture, ...event.contexts?.culture }
        };
      }
    },
    processSegmentSpan(span) {
      const culture = getCultureContext();
      if (culture) {
        safeSetSpanJSONAttributes(span, {
          "culture.locale": culture.locale,
          "culture.timezone": culture.timezone,
          "culture.calendar": culture.calendar
        });
      }
    }
  };
});
const cultureContextIntegration = defineIntegration(_cultureContextIntegration);
function getCultureContext() {
  try {
    const intl = helpers_WINDOW.Intl;
    if (!intl) {
      return void 0;
    }
    const options = intl.DateTimeFormat().resolvedOptions();
    return {
      locale: options.locale,
      timezone: options.timeZone,
      calendar: options.calendar
    };
  } catch {
    return void 0;
  }
}


//# sourceMappingURL=culturecontext.js.map

;// ./node_modules/@sentry/core/build/esm/instrument/globalError.js



let _oldOnErrorHandler = null;
function addGlobalErrorInstrumentationHandler(handler) {
  const type = "error";
  handlers_addHandler(type, handler);
  handlers_maybeInstrument(type, instrumentError);
}
function instrumentError() {
  _oldOnErrorHandler = worldwide_GLOBAL_OBJ.onerror;
  worldwide_GLOBAL_OBJ.onerror = function(msg, url, line, column, error) {
    const handlerData = {
      column,
      error,
      line,
      msg,
      url
    };
    handlers_triggerHandlers("error", handlerData);
    if (_oldOnErrorHandler) {
      return _oldOnErrorHandler.apply(this, arguments);
    }
    return false;
  };
  worldwide_GLOBAL_OBJ.onerror.__SENTRY_INSTRUMENTED__ = true;
}


//# sourceMappingURL=globalError.js.map

;// ./node_modules/@sentry/core/build/esm/instrument/globalUnhandledRejection.js



let _oldOnUnhandledRejectionHandler = null;
function addGlobalUnhandledRejectionInstrumentationHandler(handler) {
  const type = "unhandledrejection";
  handlers_addHandler(type, handler);
  handlers_maybeInstrument(type, instrumentUnhandledRejection);
}
function instrumentUnhandledRejection() {
  _oldOnUnhandledRejectionHandler = worldwide_GLOBAL_OBJ.onunhandledrejection;
  worldwide_GLOBAL_OBJ.onunhandledrejection = function(e) {
    const handlerData = e;
    handlers_triggerHandlers("unhandledrejection", handlerData);
    if (_oldOnUnhandledRejectionHandler) {
      return _oldOnUnhandledRejectionHandler.apply(this, arguments);
    }
    return true;
  };
  worldwide_GLOBAL_OBJ.onunhandledrejection.__SENTRY_INSTRUMENTED__ = true;
}


//# sourceMappingURL=globalUnhandledRejection.js.map

;// ./node_modules/@sentry/browser/build/npm/esm/prod/integrations/globalhandlers.js





const globalhandlers_INTEGRATION_NAME = "GlobalHandlers";
const _globalHandlersIntegration = ((options = {}) => {
  const _options = {
    onerror: true,
    onunhandledrejection: true,
    ...options
  };
  return {
    name: globalhandlers_INTEGRATION_NAME,
    setupOnce() {
      Error.stackTraceLimit = 50;
    },
    setup(client) {
      if (_options.onerror) {
        _installGlobalOnErrorHandler(client);
        globalHandlerLog("onerror");
      }
      if (_options.onunhandledrejection) {
        _installGlobalOnUnhandledRejectionHandler(client);
        globalHandlerLog("onunhandledrejection");
      }
    }
  };
});
const globalHandlersIntegration = defineIntegration(_globalHandlersIntegration);
function _installGlobalOnErrorHandler(client) {
  addGlobalErrorInstrumentationHandler((data) => {
    const { stackParser, attachStacktrace } = getOptions();
    if (currentScopes_getClient() !== client || shouldIgnoreOnError()) {
      return;
    }
    const { msg, url, line, column, error } = data;
    const event = _enhanceEventWithInitialFrame(
      eventbuilder_eventFromUnknownInput(stackParser, error || msg, void 0, attachStacktrace, false),
      url,
      line,
      column
    );
    event.level = "error";
    captureEvent(event, {
      originalException: error,
      mechanism: {
        handled: false,
        type: "auto.browser.global_handlers.onerror"
      }
    });
  });
}
function _installGlobalOnUnhandledRejectionHandler(client) {
  addGlobalUnhandledRejectionInstrumentationHandler((e) => {
    const { stackParser, attachStacktrace } = getOptions();
    if (currentScopes_getClient() !== client || shouldIgnoreOnError()) {
      return;
    }
    const error = _getUnhandledRejectionError(e);
    const event = is_isPrimitive(error) ? _eventFromRejectionWithPrimitive(error) : eventbuilder_eventFromUnknownInput(stackParser, error, void 0, attachStacktrace, true);
    event.level = "error";
    captureEvent(event, {
      originalException: error,
      mechanism: {
        handled: false,
        type: "auto.browser.global_handlers.onunhandledrejection"
      }
    });
  });
}
function _getUnhandledRejectionError(error) {
  if (is_isPrimitive(error)) {
    return error;
  }
  try {
    if ("reason" in error) {
      return error.reason;
    }
    if ("detail" in error && "reason" in error.detail) {
      return error.detail.reason;
    }
  } catch {
  }
  return error;
}
function _eventFromRejectionWithPrimitive(reason) {
  return {
    exception: {
      values: [
        {
          type: "UnhandledRejection",
          // String() is needed because the Primitive type includes symbols (which can't be automatically stringified)
          value: `Non-Error promise rejection captured with value: ${String(reason)}`
        }
      ]
    }
  };
}
function _enhanceEventWithInitialFrame(event, url, lineno, colno) {
  const e = event.exception = event.exception || {};
  const ev = e.values = e.values || [];
  const ev0 = ev[0] = ev[0] || {};
  const ev0s = ev0.stacktrace = ev0.stacktrace || {};
  const ev0sf = ev0s.frames = ev0s.frames || [];
  if (ev0sf.length === 0) {
    ev0sf.push({
      colno,
      lineno,
      filename: getFilenameFromUrl(url) ?? getLocationHref(),
      function: UNKNOWN_FUNCTION,
      in_app: true
    });
  }
  return event;
}
function globalHandlerLog(type) {
  prod_debug_build_DEBUG_BUILD && debug_logger_debug.log(`Global Handler attached: ${type}`);
}
function getOptions() {
  const client = currentScopes_getClient();
  const options = client?.getOptions() || {
    stackParser: () => [],
    attachStacktrace: false
  };
  return options;
}
function getFilenameFromUrl(url) {
  if (!is_isString(url) || url.length === 0) {
    return void 0;
  }
  if (url.startsWith("data:")) {
    return `<${stripDataUrlContent(url, false)}>`;
  }
  return url;
}


//# sourceMappingURL=globalhandlers.js.map

;// ./node_modules/@sentry/conventions/dist/attributes.mjs
const e="ai.citations",i="ai.completion_tokens.used",t="ai.documents",n="ai.finish_reason",r="ai.frequency_penalty",a="ai.function_call",s="ai.generation_id",o="ai.input_messages",l="ai.is_search_required",p="ai.metadata",c="ai.model_id",u="ai.model.provider",b="ai.pipeline.name",g="ai.preamble",d="ai.presence_penalty",m="ai.prompt_tokens.used",y="ai.raw_prompting",_="ai.responses",h="ai.response_format",v="ai.search_queries",f="ai.search_results",S="ai.seed",E="ai.streaming",T="ai.tags",I="ai.temperature",O="ai.texts",k="ai.tools",A="ai.tool_calls",x="ai.top_k",w="ai.top_p",R="ai.total_cost",N="ai.total_tokens.used",C="ai.warnings",P="angular.version",D="app.app_build",L="app.app_identifier",U="app.app_name",M="app.app_start_time",q="app.app_version",G="app.build",Y="app.identifier",V="app.in_foreground",W="app.name",F="app_start_cold",B="app.start_time",H="app_start_type",z="app_start_warm",K="app.version",j="app.vitals.frames.delay.value",Q="app.vitals.frames.frozen.count",X="app.vitals.frames.slow.count",J="app.vitals.frames.total.count",Z="app.vitals.start.cold.value",$="app.vitals.start.prewarmed",ee="app.vitals.start.reason",ie="app.vitals.start.screen",te="app.vitals.start.type",ne="app.vitals.start.warm.value",re="app.vitals.ttfd.value",ae="app.vitals.ttid.value",se="art.gc.blocking_count",oe="art.gc.blocking_time",le="art.gc.pre_oome_count",pe="art.gc.total_count",ce="art.gc.total_time",ue="art.gc.waiting_time",be="art.memory.free",ge="art.memory.free_until_gc",de="art.memory.free_until_oome",me="art.memory.max",ye="art.memory.total",_e="aws.cloudwatch.logs.log_group",he="aws.cloudwatch.logs.log_stream",ve="aws.cloudwatch.logs.url",fe="aws.dynamodb.attribute_definitions",Se="aws.dynamodb.consistent_read",Ee="aws.dynamodb.consumed_capacity",Te="aws.dynamodb.count",Ie="aws.dynamodb.exclusive_start_table",Oe="aws.dynamodb.global_secondary_indexes",ke="aws.dynamodb.global_secondary_index_updates",Ae="aws.dynamodb.index_name",xe="aws.dynamodb.item_collection_metrics",we="aws.dynamodb.limit",Re="aws.dynamodb.local_secondary_indexes",Ne="aws.dynamodb.projection",Ce="aws.dynamodb.provisioned_read_capacity",Pe="aws.dynamodb.provisioned_write_capacity",De="aws.dynamodb.scanned_count",Le="aws.dynamodb.scan_forward",Ue="aws.dynamodb.segment",Me="aws.dynamodb.select",qe="aws.dynamodb.table_count",Ge="aws.dynamodb.table_names",Ye="aws.dynamodb.total_segments",Ve="aws.extended_request_id",We="aws.kinesis.stream_name",Fe="aws.kinesis.stream.name",Be="aws.lambda.aws_request_id",He="aws.lambda.execution_duration_in_millis",ze="aws.lambda.function_name",Ke="aws.lambda.function_version",je="aws.lambda.invoked_arn",Qe="aws.lambda.invoked_function_arn",Xe="aws.lambda.remaining_time_in_millis",Je="aws.log.group.names",Ze="aws.log.stream.names",$e="aws.request.extended_id",ei="aws.request_id",ii="aws.request.id",ti="aws.s3.bucket",ni="aws.secretsmanager.secret.arn",ri="aws.sns.topic.arn",ai="aws.step_functions.activity.arn",si="aws.step_functions.state_machine.arn",oi="blocked_main_thread",li="browser.name",pi="browser.performance.navigation.activation_start",ci="browser.performance.time_origin",ui="browser.report.type",bi="browser.script.invoker",gi="browser.script.invoker_type",di="browser.script.source_char_position",mi="browser.version",yi="browser.web_vital.cls.report_event",_i="browser.web_vital.cls.source.<key>",hi="browser.web_vital.cls.source",vi="browser.web_vital.cls.value",fi="browser.web_vital.fcp.value",Si="browser.web_vital.fp.value",Ei="browser.web_vital.inp.value",Ti="browser.web_vital.lcp.element",Ii="browser.web_vital.lcp.id",Oi="browser.web_vital.lcp.load_time",ki="browser.web_vital.lcp.render_time",Ai="browser.web_vital.lcp.report_event",xi="browser.web_vital.lcp.size",wi="browser.web_vital.lcp.url",Ri="browser.web_vital.lcp.value",Ni="browser.web_vital.ttfb.request_time",Ci="browser.web_vital.ttfb.value",Pi="cache.hit",Di="cache.item_size",Li="cache.key",Ui="cache.operation",Mi="cache.ttl",qi="cache.write",Gi="channel",Yi="client.address",Vi="client.port",Wi="cloudflare.d1.duration",Fi="cloudflare.d1.query_type",Bi="cloudflare.d1.rows_read",Hi="cloudflare.d1.rows_written",zi="cloudflare.durable_object.query.bindings",Ki="cloudflare.durable_object.response.rows_read",ji="cloudflare.durable_object.response.rows_written",Qi="cloudflare.r2.bucket",Xi="cloudflare.r2.operation",Ji="cloudflare.r2.request.delimiter",Zi="cloudflare.r2.request.key",$i="cloudflare.r2.request.part_number",et="cloudflare.r2.request.prefix",it="cloudflare.workflow.attempt",tt="cloudflare.workflow.retries.backoff",nt="cloudflare.workflow.retries.delay",rt="cloudflare.workflow.retries.limit",at="cloudflare.workflow.timeout",st="cloud.account.id",ot="cloud.availability_zone",lt="cloud.platform",pt="cloud.provider",ct="cloud.region",ut="cloud.resource_id",bt="cls",gt="cls.source.<key>",dt="cls.source",mt="code.filepath",yt="code.file.path",_t="code.function",ht="code.function.name",vt="code.lineno",ft="code.line.number",St="code.namespace",Et="connectionType",Tt="connection.rtt",It="culture.calendar",Ot="culture.display_name",kt="culture.is_24_hour_format",At="culture.locale",xt="culture.timezone",wt="db.collection.name",Rt="db.driver.name",Nt="db.name",Ct="db.namespace",Pt="db.operation",Dt="db.operation.batch.size",Lt="db.operation.name",Ut="db.query.parameter.<key>",Mt="db.query.parameter",qt="db.query.summary",Gt="db.query.text",Yt="db.redis.connection",Vt="db.redis.key",Wt="db.redis.parameters",Ft="db.response.status_code",Bt="db.sql.bindings",Ht="db.statement",zt="db.stored_procedure.name",Kt="db.system",jt="db.system.name",Qt="db.user",Xt="deviceMemory",Jt="device.archs",Zt="device.battery_level",$t="device.battery_temperature",en="device.boot_time",tn="device.brand",nn="device.charging",rn="device.chipset",an="device.class",sn="device.connection_type",on="device.cpu_description",ln="device.external_free_storage",pn="device.external_storage_size",cn="device.family",un="device.free_memory",bn="device.free_storage",gn="device.id",dn="device.locale",mn="device.low_memory",yn="device.low_power_mode",_n="device.manufacturer",hn="device.memory.estimated_capacity",vn="device.memory_size",fn="device.model",Sn="device.model_id",En="device.name",Tn="device.online",In="device.orientation",On="device.processor_count",kn="device.processor_frequency",An="device.screen_density",xn="device.screen_dpi",wn="device.screen_height_pixels",Rn="device.screen_width_pixels",Nn="device.simulator",Cn="device.storage_size",Pn="device.thermal_state",Dn="device.timezone",Ln="device.usable_memory",Un="dist",Mn="effectiveConnectionType",qn="environment",Gn="error.type",Yn="event.id",Vn="event.name",Wn="exception.escaped",Fn="exception.message",Bn="exception.stacktrace",Hn="exception.type",zn="faas.coldstart",Kn="faas.cron",jn="faas.duration_in_ms",Qn="faas.entry_point",Xn="faas.execution",Jn="faas.id",Zn="faas.identity",$n="faas.invocation_id",er="faas.invoked_name",ir="faas.invoked_provider",tr="faas.invoked_region",nr="faas.name",rr="faas.time",ar="faas.trigger",sr="faas.version",or="fcp",lr="flag.evaluation.<key>",pr="flag.evaluation",cr="fp",ur="frames.delay",br="frames.frozen",gr="frames_frozen_rate",dr="frames.slow",mr="frames_slow_rate",yr="frames.total",_r="fs_error",hr="gcp.function.context.event_id",vr="gcp.function.context.event_type",fr="gcp.function.context.id",Sr="gcp.function.context.resource",Er="gcp.function.context.source",Tr="gcp.function.context.specversion",Ir="gcp.function.context.time",Or="gcp.function.context.timestamp",kr="gcp.function.context.type",Ar="gcp.project.id",xr="gen_ai.agent.name",wr="gen_ai.context.utilization",Rr="gen_ai.context.window_size",Nr="gen_ai.conversation.id",Cr="gen_ai.cost.cache_creation.input_tokens",Pr="gen_ai.cost.cache_read.input_tokens",Dr="gen_ai.cost.input_tokens",Lr="gen_ai.cost.output_tokens",Ur="gen_ai.cost.reasoning.output_tokens",Mr="gen_ai.cost.total_tokens",qr="gen_ai.embeddings.input",Gr="gen_ai.function_id",Yr="gen_ai.input.messages",Vr="gen_ai.operation.name",Wr="gen_ai.operation.type",Fr="gen_ai.output.messages",Br="gen_ai.pipeline.name",Hr="gen_ai.prompt",zr="gen_ai.prompt.name",Kr="gen_ai.provider.name",jr="gen_ai.request.available_tools",Qr="gen_ai.request.frequency_penalty",Xr="gen_ai.request.max_tokens",Jr="gen_ai.request.messages",Zr="gen_ai.request.model",$r="gen_ai.request.presence_penalty",ea="gen_ai.request.reasoning_effort",ia="gen_ai.request.seed",ta="gen_ai.request.stop_sequences",na="gen_ai.request.temperature",ra="gen_ai.request.top_k",aa="gen_ai.request.top_p",sa="gen_ai.response.finish_reasons",oa="gen_ai.response.id",la="gen_ai.response.model",pa="gen_ai.response.streaming",ca="gen_ai.response.text",ua="gen_ai.response.time_to_first_chunk",ba="gen_ai.response.time_to_first_token",ga="gen_ai.response.tokens_per_second",da="gen_ai.response.tool_calls",ma="gen_ai.system",ya="gen_ai.system_instructions",_a="gen_ai.system.message",ha="gen_ai.tool.call.arguments",va="gen_ai.tool.call.result",fa="gen_ai.tool.definitions",Sa="gen_ai.tool.description",Ea="gen_ai.tool.input",Ta="gen_ai.tool.message",Ia="gen_ai.tool.name",Oa="gen_ai.tool.output",ka="gen_ai.tool.type",Aa="gen_ai.usage.cache_creation.input_tokens",xa="gen_ai.usage.cache_read.input_tokens",wa="gen_ai.usage.completion_tokens",Ra="gen_ai.usage.input_tokens",Na="gen_ai.usage.input_tokens.cached",Ca="gen_ai.usage.input_tokens.cache_write",Pa="gen_ai.usage.output_tokens",Da="gen_ai.usage.output_tokens.reasoning",La="gen_ai.usage.prompt_tokens",Ua="gen_ai.usage.reasoning.output_tokens",Ma="gen_ai.usage.total_tokens",qa="graphql.document",Ga="graphql.operation.name",Ya="graphql.operation.type",Va="hardwareConcurrency",Wa="http.client_ip",Fa="http.decoded_response_content_length",Ba="http.flavor",Ha="http.fragment",za="http.host",Ka="http.method",ja="http.query",Qa="http.request.body.data",Xa="http.request.connection_end",Ja="http.request.connect_start",Za="http.request.domain_lookup_end",$a="http.request.domain_lookup_start",es="http.request.fetch_start",is="http.request.header.<key>",ts="http.request.header",ns="http.request.method",rs="http.request_method",as="http.request.redirect_end",ss="http.request.redirect_start",os="http.request.request_start",ls="http.request.resend_count",ps="http.request.response_end",cs="http.request.response_start",us="http.request.same_origin",bs="http.request.secure_connection_start",gs="http.request.time_to_first_byte",ds="http.request.worker_start",ms="http.response.body.size",ys="http.response_content_length",_s="http.response.header.content-length",hs="http.response.header.<key>",vs="http.response.header",fs="http.response.size",Ss="http.response.status_code",Es="http.response_transfer_size",Ts="http.route",Is="http.scheme",Os="http.server_name",ks="http.server.request.time_in_queue",As="http.status_code",xs="http.target",ws="http.url",Rs="http.user_agent",Ns="id",Cs="inp",Ps="jsonrpc.protocol.version",Ds="jsonrpc.request.id",Ls="jvm.gc.action",Us="jvm.gc.name",Ms="jvm.memory.pool.name",qs="jvm.memory.type",Gs="jvm.thread.daemon",Ys="jvm.thread.state",Vs="koa.name",Ws="koa.type",Fs="lcp",Bs="lcp.element",Hs="lcp.id",zs="lcp.loadTime",Ks="lcp.renderTime",js="lcp.size",Qs="lcp.url",Xs="logger.name",Js="mcp.cancelled.reason",Zs="mcp.cancelled.request_id",$s="mcp.client.name",eo="mcp.client.title",io="mcp.client.version",to="mcp.lifecycle.phase",no="mcp.logging.data_type",ro="mcp.logging.level",ao="mcp.logging.logger",so="mcp.logging.message",oo="mcp.method.name",lo="mcp.progress.current",po="mcp.progress.message",co="mcp.progress.percentage",uo="mcp.progress.token",bo="mcp.progress.total",go="mcp.prompt.name",mo="mcp.prompt.result.description",yo="mcp.prompt.result.message_content",_o="mcp.prompt.result.message_count",ho="mcp.prompt.result.message_role",vo="mcp.protocol.ready",fo="mcp.protocol.version",So="mcp.request.argument.<key>",Eo="mcp.request.argument",To="mcp.request.argument.name",Io="mcp.request.argument.uri",Oo="mcp.request.id",ko="mcp.resource.protocol",Ao="mcp.resource.uri",xo="mcp.server.name",wo="mcp.server.title",Ro="mcp.server.version",No="mcp.session.id",Co="mcp.tool.name",Po="mcp.tool.result.content",Do="mcp.tool.result.content_count",Lo="mcp.tool.result.is_error",Uo="mcp.transport",Mo="mdc.<key>",qo="mdc",Go="messaging.batch.message_count",Yo="messaging.destination",Vo="messaging.destination.connection",Wo="messaging.destination.name",Fo="messaging.message.body.size",Bo="messaging.message.conversation_id",Ho="messaging.message.envelope.size",zo="messaging.message.id",Ko="messaging.message.receive.latency",jo="messaging.message.retry.count",Qo="messaging.operation.name",Xo="messaging.operation.type",Jo="messaging.rabbitmq.destination.routing_key",Zo="messaging.system",$o="method",el="middleware.name",il="navigation.origin",tl="navigation.route.id",nl="navigation.type",rl="nel.elapsed_time",al="nel.phase",sl="nel.referrer",ol="nel.sampling_function",ll="nel.type",pl="network.connection.effective_type",cl="network.connection.rtt",ul="network.connection.type",bl="network.local.address",gl="network.local.port",dl="network.peer.address",ml="network.peer.port",yl="network.protocol.name",_l="network.protocol.version",hl="network.transport",vl="network.type",fl="net.host.ip",Sl="net.host.name",El="net.host.port",Tl="net.peer.ip",Il="net.peer.name",Ol="net.peer.port",kl="net.protocol.name",Al="net.protocol.version",xl="net.sock.family",wl="net.sock.host.addr",Rl="net.sock.host.port",Nl="net.sock.peer.addr",Cl="net.sock.peer.name",Pl="net.sock.peer.port",Dl="net.transport",Ll="os.build",Ul="os.build_id",Ml="os.description",ql="os.kernel_version",Gl="os.name",Yl="os.raw_description",Vl="os.rooted",Wl="os.theme",Fl="os.type",Bl="os.version",Hl="otel.kind",zl="otel.scope.name",Kl="otel.scope.version",jl="otel.status_code",Ql="otel.status_description",Xl="params.<key>",Jl="params",Zl="performance.activationStart",$l="performance.timeOrigin",ep="previous_route",ip="process.command_args",tp="process.executable.name",np="process.pid",rp="process.runtime.description",ap="process.runtime.engine.name",sp="process.runtime.engine.version",op="process.runtime.name",lp="process.runtime.version",pp="query.<key>",cp="query",up="react.version",bp="release",gp="remix.action_form_data.<key>",dp="remix.action_form_data",mp="replay_id",yp="resource.deployment.environment",_p="resource.deployment.environment.name",hp="resource.render_blocking_status",vp="route",fp="rpc.grpc.status_code",Sp="rpc.method",Ep="rpc.response.status_code",Tp="rpc.service",Ip="rpc.system",Op="rpc.system.name",kp="runtime.build",Ap="runtime.name",xp="runtime.raw_description",wp="runtime.version",Rp="score.<key>",Np="score",Cp="score.ratio.<key>",Pp="score.ratio",Dp="score.total",Lp="score.weight.<key>",Up="score.weight",Mp="sentry.action",qp="sentry.browser.name",Gp="sentry.browser.version",Yp="sentry.cancellation_reason",Vp="sentry.category",Wp="sentry.client_sample_rate",Fp="sentry.description",Bp="sentry.dist",Hp="sentry.domain",zp="sentry.dsc.environment",Kp="sentry.dsc.project_id",jp="sentry.dsc.public_key",Qp="sentry.dsc.release",Xp="sentry.dsc.sampled",Jp="sentry.dsc.sample_rate",Zp="sentry.dsc.trace_id",$p="sentry.dsc.transaction",ec="sentry.environment",ic="sentry.exclusive_time",tc="sentry.graphql.operation",nc="sentry.group",rc="sentry.http.prefetch",ac="sentry.idle_span_finish_reason",sc="sentry.is_remote",oc="sentry.kind",lc="sentry.main_thread",pc="sentry.message.parameter.<key>",cc="sentry.message.template",uc="sentry.metric.source",bc="sentry.mobile",gc="sentry.module.<key>",dc="sentry.module",mc="sentry.nextjs.ssr.function.route",yc="sentry.nextjs.ssr.function.type",_c="sentry.normalized_db_query",hc="sentry.normalized_db_query.hash",vc="sentry.normalized_description",fc="sentry.observed_timestamp_nanos",Sc="sentry.op",Ec="sentry.origin",Tc="sentry.platform",Ic="sentry.profiler_id",Oc="sentry.profile_id",kc="sentry.release",Ac="sentry.replay_id",xc="sentry.replay_is_buffering",wc="sentry.report_event",Rc="sentry.sdk.integrations",Nc="sentry.sdk.name",Cc="sentry.sdk.version",Pc="sentry.segment.id",Dc="sentry.segment_id",Lc="sentry.segment.name",Uc="sentry.server_sample_rate",Mc="sentry.source",qc="sentry.span.source",Gc="sentry.status",Yc="sentry.status_code",Vc="sentry.status.message",Wc="sentry.sveltekit.navigation.from",Fc="sentry.sveltekit.navigation.to",Bc="sentry.sveltekit.navigation.type",Hc="sentry.thread.id",zc="sentry.timestamp.sequence",Kc="sentry.trace_lifecycle",jc="sentry.trace.parent_span_id",Qc="sentry.trace.status",Xc="sentry.transaction",Jc="sentry.user.email",Zc="sentry.user.geo.city",$c="sentry.user.geo.country_code",eu="sentry.user.geo.region",iu="sentry.user.geo.subdivision",tu="sentry.user.id",nu="sentry.user.ip",ru="sentry.user.username",au="server.address",su="server_name",ou="server.port",lu="service.name",pu="service.version",cu="session.id",uu="stall_percentage",bu="stall_total_time",gu="state.type",du="thread.id",mu="thread.name",yu="timber.tag",_u="time_to_full_display",hu="time_to_initial_display",vu="transaction",fu="trpc.procedure_path",Su="trpc.procedure_type",Eu="ttfb",Tu="ttfb.requestTime",Iu="type",Ou="ui.component_name",ku="ui.contributes_to_ttfd",Au="ui.contributes_to_ttid",xu="ui.element.height",wu="ui.element.id",Ru="ui.element.identifier",Nu="ui.element.load_time",Cu="ui.element.paint_type",Pu="ui.element.render_time",Du="ui.element.type",Lu="ui.element.url",Uu="ui.element.width",Mu="url",qu="url.domain",Gu="url.fragment",Yu="url.full",Vu="url.path",Wu="url.path.parameter.<key>",Fu="url.path.parameter",Bu="url.port",Hu="url.query",zu="url.same_origin",Ku="url.scheme",ju="url.template",Qu="user_agent.original",Xu="user.email",Ju="user.full_name",Zu="user.geo.city",$u="user.geo.country_code",eb="user.geo.region",ib="user.geo.subdivision",tb="user.hash",nb="user.id",rb="user.ip_address",ab="user.name",sb="user.roles",ob="vercel.branch",lb="vercel.build_id",pb="vercel.deployment_id",cb="vercel.destination",ub="vercel.edge_type",bb="vercel.entrypoint",gb="vercel.execution_region",db="vercel.id",mb="vercel.ja3_digest",yb="vercel.ja4_digest",_b="vercel.log_type",hb="vercel.path",vb="vercel.project_id",fb="vercel.project_name",Sb="vercel.proxy.cache_id",Eb="vercel.proxy.client_ip",Tb="vercel.proxy.host",Ib="vercel.proxy.lambda_region",Ob="vercel.proxy.method",kb="vercel.proxy.path",Ab="vercel.proxy.path_type",xb="vercel.proxy.path_type_variant",wb="vercel.proxy.referer",Rb="vercel.proxy.region",Nb="vercel.proxy.response_byte_size",Cb="vercel.proxy.scheme",Pb="vercel.proxy.status_code",Db="vercel.proxy.timestamp",Lb="vercel.proxy.user_agent",Ub="vercel.proxy.vercel_cache",Mb="vercel.proxy.vercel_id",qb="vercel.proxy.waf_action",Gb="vercel.proxy.waf_rule_id",Yb="vercel.request_id",Vb="vercel.source",Wb="vercel.status_code",Fb={"ai.citations":"string[]","ai.completion_tokens.used":"integer","ai.documents":"string[]","ai.finish_reason":"string","ai.frequency_penalty":"double","ai.function_call":"string","ai.generation_id":"string","ai.input_messages":"string","ai.is_search_required":"boolean","ai.metadata":"string","ai.model_id":"string","ai.model.provider":"string","ai.pipeline.name":"string","ai.preamble":"string","ai.presence_penalty":"double","ai.prompt_tokens.used":"integer","ai.raw_prompting":"boolean","ai.responses":"string[]","ai.response_format":"string","ai.search_queries":"string[]","ai.search_results":"string[]","ai.seed":"string","ai.streaming":"boolean","ai.tags":"string","ai.temperature":"double","ai.texts":"string[]","ai.tools":"string[]","ai.tool_calls":"string[]","ai.top_k":"integer","ai.top_p":"double","ai.total_cost":"double","ai.total_tokens.used":"integer","ai.warnings":"string[]","angular.version":"string","app.app_build":"string","app.app_identifier":"string","app.app_name":"string","app.app_start_time":"string","app.app_version":"string","app.build":"string","app.identifier":"string","app.in_foreground":"boolean","app.name":"string",app_start_cold:"double","app.start_time":"string",app_start_type:"string",app_start_warm:"double","app.version":"string","app.vitals.frames.delay.value":"integer","app.vitals.frames.frozen.count":"integer","app.vitals.frames.slow.count":"integer","app.vitals.frames.total.count":"integer","app.vitals.start.cold.value":"double","app.vitals.start.prewarmed":"boolean","app.vitals.start.reason":"string","app.vitals.start.screen":"string","app.vitals.start.type":"string","app.vitals.start.warm.value":"double","app.vitals.ttfd.value":"double","app.vitals.ttid.value":"double","art.gc.blocking_count":"integer","art.gc.blocking_time":"double","art.gc.pre_oome_count":"integer","art.gc.total_count":"integer","art.gc.total_time":"double","art.gc.waiting_time":"double","art.memory.free":"integer","art.memory.free_until_gc":"integer","art.memory.free_until_oome":"integer","art.memory.max":"integer","art.memory.total":"integer","aws.cloudwatch.logs.log_group":"string","aws.cloudwatch.logs.log_stream":"string","aws.cloudwatch.logs.url":"string","aws.dynamodb.attribute_definitions":"string[]","aws.dynamodb.consistent_read":"boolean","aws.dynamodb.consumed_capacity":"string[]","aws.dynamodb.count":"integer","aws.dynamodb.exclusive_start_table":"string","aws.dynamodb.global_secondary_indexes":"string[]","aws.dynamodb.global_secondary_index_updates":"string[]","aws.dynamodb.index_name":"string","aws.dynamodb.item_collection_metrics":"string","aws.dynamodb.limit":"integer","aws.dynamodb.local_secondary_indexes":"string[]","aws.dynamodb.projection":"string","aws.dynamodb.provisioned_read_capacity":"double","aws.dynamodb.provisioned_write_capacity":"double","aws.dynamodb.scanned_count":"integer","aws.dynamodb.scan_forward":"boolean","aws.dynamodb.segment":"integer","aws.dynamodb.select":"string","aws.dynamodb.table_count":"integer","aws.dynamodb.table_names":"string[]","aws.dynamodb.total_segments":"integer","aws.extended_request_id":"string","aws.kinesis.stream_name":"string","aws.kinesis.stream.name":"string","aws.lambda.aws_request_id":"string","aws.lambda.execution_duration_in_millis":"double","aws.lambda.function_name":"string","aws.lambda.function_version":"string","aws.lambda.invoked_arn":"string","aws.lambda.invoked_function_arn":"string","aws.lambda.remaining_time_in_millis":"double","aws.log.group.names":"string[]","aws.log.stream.names":"string[]","aws.request.extended_id":"string","aws.request_id":"string","aws.request.id":"string","aws.s3.bucket":"string","aws.secretsmanager.secret.arn":"string","aws.sns.topic.arn":"string","aws.step_functions.activity.arn":"string","aws.step_functions.state_machine.arn":"string",blocked_main_thread:"boolean","browser.name":"string","browser.performance.navigation.activation_start":"double","browser.performance.time_origin":"double","browser.report.type":"string","browser.script.invoker":"string","browser.script.invoker_type":"string","browser.script.source_char_position":"integer","browser.version":"string","browser.web_vital.cls.report_event":"string","browser.web_vital.cls.source.<key>":"string","browser.web_vital.cls.value":"double","browser.web_vital.fcp.value":"double","browser.web_vital.fp.value":"double","browser.web_vital.inp.value":"double","browser.web_vital.lcp.element":"string","browser.web_vital.lcp.id":"string","browser.web_vital.lcp.load_time":"integer","browser.web_vital.lcp.render_time":"integer","browser.web_vital.lcp.report_event":"string","browser.web_vital.lcp.size":"integer","browser.web_vital.lcp.url":"string","browser.web_vital.lcp.value":"double","browser.web_vital.ttfb.request_time":"double","browser.web_vital.ttfb.value":"double","cache.hit":"boolean","cache.item_size":"integer","cache.key":"string[]","cache.operation":"string","cache.ttl":"integer","cache.write":"boolean",channel:"string","client.address":"string","client.port":"integer","cloudflare.d1.duration":"integer","cloudflare.d1.query_type":"string","cloudflare.d1.rows_read":"integer","cloudflare.d1.rows_written":"integer","cloudflare.durable_object.query.bindings":"integer","cloudflare.durable_object.response.rows_read":"integer","cloudflare.durable_object.response.rows_written":"integer","cloudflare.r2.bucket":"string","cloudflare.r2.operation":"string","cloudflare.r2.request.delimiter":"string","cloudflare.r2.request.key":"string","cloudflare.r2.request.part_number":"integer","cloudflare.r2.request.prefix":"string","cloudflare.workflow.attempt":"integer","cloudflare.workflow.retries.backoff":"string","cloudflare.workflow.retries.delay":"string","cloudflare.workflow.retries.limit":"integer","cloudflare.workflow.timeout":"string","cloud.account.id":"string","cloud.availability_zone":"string","cloud.platform":"string","cloud.provider":"string","cloud.region":"string","cloud.resource_id":"string",cls:"double","cls.source.<key>":"string","code.filepath":"string","code.file.path":"string","code.function":"string","code.function.name":"string","code.lineno":"integer","code.line.number":"integer","code.namespace":"string",connectionType:"string","connection.rtt":"integer","culture.calendar":"string","culture.display_name":"string","culture.is_24_hour_format":"boolean","culture.locale":"string","culture.timezone":"string","db.collection.name":"string","db.driver.name":"string","db.name":"string","db.namespace":"string","db.operation":"string","db.operation.batch.size":"integer","db.operation.name":"string","db.query.parameter.<key>":"string","db.query.summary":"string","db.query.text":"string","db.redis.connection":"string","db.redis.key":"string","db.redis.parameters":"string[]","db.response.status_code":"string","db.sql.bindings":"string[]","db.statement":"string","db.stored_procedure.name":"string","db.system":"string","db.system.name":"string","db.user":"string",deviceMemory:"string","device.archs":"string[]","device.battery_level":"double","device.battery_temperature":"double","device.boot_time":"string","device.brand":"string","device.charging":"boolean","device.chipset":"string","device.class":"string","device.connection_type":"string","device.cpu_description":"string","device.external_free_storage":"integer","device.external_storage_size":"integer","device.family":"string","device.free_memory":"integer","device.free_storage":"integer","device.id":"string","device.locale":"string","device.low_memory":"boolean","device.low_power_mode":"boolean","device.manufacturer":"string","device.memory.estimated_capacity":"integer","device.memory_size":"integer","device.model":"string","device.model_id":"string","device.name":"string","device.online":"boolean","device.orientation":"string","device.processor_count":"integer","device.processor_frequency":"double","device.screen_density":"double","device.screen_dpi":"integer","device.screen_height_pixels":"integer","device.screen_width_pixels":"integer","device.simulator":"boolean","device.storage_size":"integer","device.thermal_state":"string","device.timezone":"string","device.usable_memory":"integer",dist:"string",effectiveConnectionType:"string",environment:"string","error.type":"string","event.id":"integer","event.name":"string","exception.escaped":"boolean","exception.message":"string","exception.stacktrace":"string","exception.type":"string","faas.coldstart":"boolean","faas.cron":"string","faas.duration_in_ms":"integer","faas.entry_point":"string","faas.execution":"string","faas.id":"string","faas.identity":"string","faas.invocation_id":"string","faas.invoked_name":"string","faas.invoked_provider":"string","faas.invoked_region":"string","faas.name":"string","faas.time":"string","faas.trigger":"string","faas.version":"string",fcp:"double","flag.evaluation.<key>":"boolean",fp:"double","frames.delay":"integer","frames.frozen":"integer",frames_frozen_rate:"double","frames.slow":"integer",frames_slow_rate:"double","frames.total":"integer",fs_error:"string","gcp.function.context.event_id":"string","gcp.function.context.event_type":"string","gcp.function.context.id":"string","gcp.function.context.resource":"string","gcp.function.context.source":"string","gcp.function.context.specversion":"string","gcp.function.context.time":"string","gcp.function.context.timestamp":"string","gcp.function.context.type":"string","gcp.project.id":"string","gen_ai.agent.name":"string","gen_ai.context.utilization":"double","gen_ai.context.window_size":"integer","gen_ai.conversation.id":"string","gen_ai.cost.cache_creation.input_tokens":"double","gen_ai.cost.cache_read.input_tokens":"double","gen_ai.cost.input_tokens":"double","gen_ai.cost.output_tokens":"double","gen_ai.cost.reasoning.output_tokens":"double","gen_ai.cost.total_tokens":"double","gen_ai.embeddings.input":"string","gen_ai.function_id":"string","gen_ai.input.messages":"string","gen_ai.operation.name":"string","gen_ai.operation.type":"string","gen_ai.output.messages":"string","gen_ai.pipeline.name":"string","gen_ai.prompt":"string","gen_ai.prompt.name":"string","gen_ai.provider.name":"string","gen_ai.request.available_tools":"string","gen_ai.request.frequency_penalty":"double","gen_ai.request.max_tokens":"integer","gen_ai.request.messages":"string","gen_ai.request.model":"string","gen_ai.request.presence_penalty":"double","gen_ai.request.reasoning_effort":"string","gen_ai.request.seed":"string","gen_ai.request.stop_sequences":"string[]","gen_ai.request.temperature":"double","gen_ai.request.top_k":"integer","gen_ai.request.top_p":"double","gen_ai.response.finish_reasons":"string","gen_ai.response.id":"string","gen_ai.response.model":"string","gen_ai.response.streaming":"boolean","gen_ai.response.text":"string","gen_ai.response.time_to_first_chunk":"double","gen_ai.response.time_to_first_token":"double","gen_ai.response.tokens_per_second":"double","gen_ai.response.tool_calls":"string","gen_ai.system":"string","gen_ai.system_instructions":"string","gen_ai.system.message":"string","gen_ai.tool.call.arguments":"string","gen_ai.tool.call.result":"string","gen_ai.tool.definitions":"string","gen_ai.tool.description":"string","gen_ai.tool.input":"string","gen_ai.tool.message":"string","gen_ai.tool.name":"string","gen_ai.tool.output":"string","gen_ai.tool.type":"string","gen_ai.usage.cache_creation.input_tokens":"integer","gen_ai.usage.cache_read.input_tokens":"integer","gen_ai.usage.completion_tokens":"integer","gen_ai.usage.input_tokens":"integer","gen_ai.usage.input_tokens.cached":"integer","gen_ai.usage.input_tokens.cache_write":"integer","gen_ai.usage.output_tokens":"integer","gen_ai.usage.output_tokens.reasoning":"integer","gen_ai.usage.prompt_tokens":"integer","gen_ai.usage.reasoning.output_tokens":"integer","gen_ai.usage.total_tokens":"integer","graphql.document":"string","graphql.operation.name":"string","graphql.operation.type":"string",hardwareConcurrency:"string","http.client_ip":"string","http.decoded_response_content_length":"integer","http.flavor":"string","http.fragment":"string","http.host":"string","http.method":"string","http.query":"string","http.request.body.data":"string","http.request.connection_end":"double","http.request.connect_start":"double","http.request.domain_lookup_end":"double","http.request.domain_lookup_start":"double","http.request.fetch_start":"double","http.request.header.<key>":"string[]","http.request.method":"string","http.request_method":"string","http.request.redirect_end":"double","http.request.redirect_start":"double","http.request.request_start":"double","http.request.resend_count":"integer","http.request.response_end":"double","http.request.response_start":"double","http.request.same_origin":"boolean","http.request.secure_connection_start":"double","http.request.time_to_first_byte":"double","http.request.worker_start":"double","http.response.body.size":"integer","http.response_content_length":"integer","http.response.header.content-length":"string","http.response.header.<key>":"string[]","http.response.size":"integer","http.response.status_code":"integer","http.response_transfer_size":"integer","http.route":"string","http.scheme":"string","http.server_name":"string","http.server.request.time_in_queue":"double","http.status_code":"integer","http.target":"string","http.url":"string","http.user_agent":"string",id:"string",inp:"double","jsonrpc.protocol.version":"string","jsonrpc.request.id":"string","jvm.gc.action":"string","jvm.gc.name":"string","jvm.memory.pool.name":"string","jvm.memory.type":"string","jvm.thread.daemon":"boolean","jvm.thread.state":"string","koa.name":"string","koa.type":"string",lcp:"double","lcp.element":"string","lcp.id":"string","lcp.loadTime":"integer","lcp.renderTime":"integer","lcp.size":"integer","lcp.url":"string","logger.name":"string","mcp.cancelled.reason":"string","mcp.cancelled.request_id":"string","mcp.client.name":"string","mcp.client.title":"string","mcp.client.version":"string","mcp.lifecycle.phase":"string","mcp.logging.data_type":"string","mcp.logging.level":"string","mcp.logging.logger":"string","mcp.logging.message":"string","mcp.method.name":"string","mcp.progress.current":"integer","mcp.progress.message":"string","mcp.progress.percentage":"double","mcp.progress.token":"string","mcp.progress.total":"integer","mcp.prompt.name":"string","mcp.prompt.result.description":"string","mcp.prompt.result.message_content":"string","mcp.prompt.result.message_count":"integer","mcp.prompt.result.message_role":"string","mcp.protocol.ready":"integer","mcp.protocol.version":"string","mcp.request.argument.<key>":"string","mcp.request.argument.name":"string","mcp.request.argument.uri":"string","mcp.request.id":"string","mcp.resource.protocol":"string","mcp.resource.uri":"string","mcp.server.name":"string","mcp.server.title":"string","mcp.server.version":"string","mcp.session.id":"string","mcp.tool.name":"string","mcp.tool.result.content":"string","mcp.tool.result.content_count":"integer","mcp.tool.result.is_error":"boolean","mcp.transport":"string","mdc.<key>":"string","messaging.batch.message_count":"integer","messaging.destination":"string","messaging.destination.connection":"string","messaging.destination.name":"string","messaging.message.body.size":"integer","messaging.message.conversation_id":"string","messaging.message.envelope.size":"integer","messaging.message.id":"string","messaging.message.receive.latency":"integer","messaging.message.retry.count":"integer","messaging.operation.name":"string","messaging.operation.type":"string","messaging.rabbitmq.destination.routing_key":"string","messaging.system":"string",method:"string","middleware.name":"string","navigation.origin":"string","navigation.route.id":"string","navigation.type":"string","nel.elapsed_time":"integer","nel.phase":"string","nel.referrer":"string","nel.sampling_function":"double","nel.type":"string","network.connection.effective_type":"string","network.connection.rtt":"integer","network.connection.type":"string","network.local.address":"string","network.local.port":"integer","network.peer.address":"string","network.peer.port":"integer","network.protocol.name":"string","network.protocol.version":"string","network.transport":"string","network.type":"string","net.host.ip":"string","net.host.name":"string","net.host.port":"integer","net.peer.ip":"string","net.peer.name":"string","net.peer.port":"integer","net.protocol.name":"string","net.protocol.version":"string","net.sock.family":"string","net.sock.host.addr":"string","net.sock.host.port":"integer","net.sock.peer.addr":"string","net.sock.peer.name":"string","net.sock.peer.port":"integer","net.transport":"string","os.build":"string","os.build_id":"string","os.description":"string","os.kernel_version":"string","os.name":"string","os.raw_description":"string","os.rooted":"boolean","os.theme":"string","os.type":"string","os.version":"string","otel.kind":"string","otel.scope.name":"string","otel.scope.version":"string","otel.status_code":"string","otel.status_description":"string","params.<key>":"string","performance.activationStart":"double","performance.timeOrigin":"double",previous_route:"string","process.command_args":"string[]","process.executable.name":"string","process.pid":"integer","process.runtime.description":"string","process.runtime.engine.name":"string","process.runtime.engine.version":"string","process.runtime.name":"string","process.runtime.version":"string","query.<key>":"string","react.version":"string",release:"string","remix.action_form_data.<key>":"string",replay_id:"string","resource.deployment.environment":"string","resource.deployment.environment.name":"string","resource.render_blocking_status":"string",route:"string","rpc.grpc.status_code":"integer","rpc.method":"string","rpc.response.status_code":"string","rpc.service":"string","rpc.system":"string","rpc.system.name":"string","runtime.build":"string","runtime.name":"string","runtime.raw_description":"string","runtime.version":"string","score.<key>":"double","score.ratio.<key>":"double","score.total":"double","score.weight.<key>":"double","sentry.action":"string","sentry.browser.name":"string","sentry.browser.version":"string","sentry.cancellation_reason":"string","sentry.category":"string","sentry.client_sample_rate":"double","sentry.description":"string","sentry.dist":"string","sentry.domain":"string","sentry.dsc.environment":"string","sentry.dsc.project_id":"string","sentry.dsc.public_key":"string","sentry.dsc.release":"string","sentry.dsc.sampled":"boolean","sentry.dsc.sample_rate":"string","sentry.dsc.trace_id":"string","sentry.dsc.transaction":"string","sentry.environment":"string","sentry.exclusive_time":"double","sentry.graphql.operation":"string","sentry.group":"string","sentry.http.prefetch":"boolean","sentry.idle_span_finish_reason":"string","sentry.is_remote":"boolean","sentry.kind":"string","sentry.main_thread":"boolean","sentry.message.parameter.<key>":"string","sentry.message.template":"string","sentry.metric.source":"string","sentry.mobile":"boolean","sentry.module.<key>":"string","sentry.nextjs.ssr.function.route":"string","sentry.nextjs.ssr.function.type":"string","sentry.normalized_db_query":"string","sentry.normalized_db_query.hash":"string","sentry.normalized_description":"string","sentry.observed_timestamp_nanos":"string","sentry.op":"string","sentry.origin":"string","sentry.platform":"string","sentry.profiler_id":"string","sentry.profile_id":"string","sentry.release":"string","sentry.replay_id":"string","sentry.replay_is_buffering":"boolean","sentry.report_event":"string","sentry.sdk.integrations":"string[]","sentry.sdk.name":"string","sentry.sdk.version":"string","sentry.segment.id":"string","sentry.segment_id":"string","sentry.segment.name":"string","sentry.server_sample_rate":"double","sentry.source":"string","sentry.span.source":"string","sentry.status":"string","sentry.status_code":"integer","sentry.status.message":"string","sentry.sveltekit.navigation.from":"string","sentry.sveltekit.navigation.to":"string","sentry.sveltekit.navigation.type":"string","sentry.thread.id":"integer","sentry.timestamp.sequence":"integer","sentry.trace_lifecycle":"string","sentry.trace.parent_span_id":"string","sentry.trace.status":"string","sentry.transaction":"string","sentry.user.email":"string","sentry.user.geo.city":"string","sentry.user.geo.country_code":"string","sentry.user.geo.region":"string","sentry.user.geo.subdivision":"string","sentry.user.id":"string","sentry.user.ip":"string","sentry.user.username":"string","server.address":"string",server_name:"string","server.port":"integer","service.name":"string","service.version":"string","session.id":"string",stall_percentage:"double",stall_total_time:"double","state.type":"string","thread.id":"integer","thread.name":"string","timber.tag":"string",time_to_full_display:"double",time_to_initial_display:"double",transaction:"string","trpc.procedure_path":"string","trpc.procedure_type":"string",ttfb:"double","ttfb.requestTime":"double",type:"string","ui.component_name":"string","ui.contributes_to_ttfd":"boolean","ui.contributes_to_ttid":"boolean","ui.element.height":"integer","ui.element.id":"string","ui.element.identifier":"string","ui.element.load_time":"double","ui.element.paint_type":"string","ui.element.render_time":"double","ui.element.type":"string","ui.element.url":"string","ui.element.width":"integer",url:"string","url.domain":"string","url.fragment":"string","url.full":"string","url.path":"string","url.path.parameter.<key>":"string","url.port":"integer","url.query":"string","url.same_origin":"boolean","url.scheme":"string","url.template":"string","user_agent.original":"string","user.email":"string","user.full_name":"string","user.geo.city":"string","user.geo.country_code":"string","user.geo.region":"string","user.geo.subdivision":"string","user.hash":"string","user.id":"string","user.ip_address":"string","user.name":"string","user.roles":"string[]","vercel.branch":"string","vercel.build_id":"string","vercel.deployment_id":"string","vercel.destination":"string","vercel.edge_type":"string","vercel.entrypoint":"string","vercel.execution_region":"string","vercel.id":"string","vercel.ja3_digest":"string","vercel.ja4_digest":"string","vercel.log_type":"string","vercel.path":"string","vercel.project_id":"string","vercel.project_name":"string","vercel.proxy.cache_id":"string","vercel.proxy.client_ip":"string","vercel.proxy.host":"string","vercel.proxy.lambda_region":"string","vercel.proxy.method":"string","vercel.proxy.path":"string","vercel.proxy.path_type":"string","vercel.proxy.path_type_variant":"string","vercel.proxy.referer":"string","vercel.proxy.region":"string","vercel.proxy.response_byte_size":"integer","vercel.proxy.scheme":"string","vercel.proxy.status_code":"integer","vercel.proxy.timestamp":"integer","vercel.proxy.user_agent":"string[]","vercel.proxy.vercel_cache":"string","vercel.proxy.vercel_id":"string","vercel.proxy.waf_action":"string","vercel.proxy.waf_rule_id":"string","vercel.request_id":"string","vercel.source":"string","vercel.status_code":"integer"},Bb={"ai.citations":{brief:"References or sources cited by the AI model in its response.",type:"string[]",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:["Citation 1","Citation 2"],deprecation:{},changelog:[{version:"0.5.0",prs:[264]},{version:"0.1.0",prs:[55]}]},"ai.completion_tokens.used":{brief:"The number of tokens used to respond to the message.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:10,deprecation:{replacement:"gen_ai.usage.output_tokens"},aliases:["gen_ai.usage.output_tokens","gen_ai.usage.completion_tokens"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[57,61]},{version:"0.0.0"}]},"ai.documents":{brief:"Documents or content chunks used as context for the AI model.",type:"string[]",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:["document1.txt","document2.pdf"],deprecation:{},changelog:[{version:"0.5.0",prs:[264]},{version:"0.1.0",prs:[55]}]},"ai.finish_reason":{brief:"The reason why the model stopped generating.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"COMPLETE",deprecation:{replacement:"gen_ai.response.finish_reasons"},aliases:["gen_ai.response.finish_reasons"],changelog:[{version:"0.1.0",prs:[55,57,61,108,127]}]},"ai.frequency_penalty":{brief:"Used to reduce repetitiveness of generated tokens. The higher the value, the stronger a penalty is applied to previously present tokens, proportional to how many times they have already appeared in the prompt or prior generation.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:.5,deprecation:{replacement:"gen_ai.request.frequency_penalty"},aliases:["gen_ai.request.frequency_penalty"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[55,57,61,108]}]},"ai.function_call":{brief:"For an AI model call, the function that was called. This is deprecated for OpenAI, and replaced by tool_calls",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"function_name",deprecation:{replacement:"gen_ai.tool.name"},aliases:["gen_ai.tool.name","mcp.tool.name"],changelog:[{version:"0.1.0",prs:[55,57,61,108]}]},"ai.generation_id":{brief:"Unique identifier for the completion.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"gen_123abc",deprecation:{replacement:"gen_ai.response.id"},aliases:["gen_ai.response.id"],changelog:[{version:"0.1.0",prs:[55,57,61,108,127]}]},"ai.input_messages":{brief:"The input messages sent to the model",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:'[{"role": "user", "message": "hello"}]',deprecation:{replacement:"gen_ai.input.messages"},aliases:["gen_ai.request.messages"],changelog:[{version:"0.1.0",prs:[65,119]},{version:"0.0.0"}]},"ai.is_search_required":{brief:"Boolean indicating if the model needs to perform a search.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!1,deprecation:{},changelog:[{version:"0.5.0",prs:[264]},{version:"0.1.0",prs:[55]}]},"ai.metadata":{brief:"Extra metadata passed to an AI pipeline step.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:'{"user_id": 123, "session_id": "abc123"}',deprecation:{},changelog:[{version:"0.5.0",prs:[264]},{version:"0.1.0",prs:[55,127]}]},"ai.model_id":{brief:"The vendor-specific ID of the model used.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"gpt-4",deprecation:{replacement:"gen_ai.response.model"},aliases:["gen_ai.response.model"],changelog:[{version:"0.1.0",prs:[57,61,127]},{version:"0.0.0"}]},"ai.model.provider":{brief:"The provider of the model.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"openai",deprecation:{replacement:"gen_ai.provider.name"},aliases:["gen_ai.provider.name","gen_ai.system"],changelog:[{version:"0.4.0",prs:[253]},{version:"0.1.0",prs:[57,61,108,127]}]},"ai.pipeline.name":{brief:"The name of the AI pipeline.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Autofix Pipeline",deprecation:{replacement:"gen_ai.pipeline.name"},aliases:["gen_ai.pipeline.name"],changelog:[{version:"0.1.0",prs:[53,76,108,127]}]},"ai.preamble":{brief:"For an AI model call, the preamble parameter. Preambles are a part of the prompt used to adjust the model's overall behavior and conversation style.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"You are now a clown.",deprecation:{replacement:"gen_ai.system_instructions"},aliases:["gen_ai.system_instructions"],changelog:[{version:"0.5.0",prs:[264]},{version:"0.1.0",prs:[55]}]},"ai.presence_penalty":{brief:"Used to reduce repetitiveness of generated tokens. Similar to frequency_penalty, except that this penalty is applied equally to all tokens that have already appeared, regardless of their exact frequencies.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:.5,deprecation:{replacement:"gen_ai.request.presence_penalty"},aliases:["gen_ai.request.presence_penalty"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[55,57,61,108]}]},"ai.prompt_tokens.used":{brief:"The number of tokens used to process just the prompt.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:20,deprecation:{replacement:"gen_ai.usage.input_tokens"},aliases:["gen_ai.usage.prompt_tokens","gen_ai.usage.input_tokens"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[57,61]},{version:"0.0.0"}]},"ai.raw_prompting":{brief:"When enabled, the user\u2019s prompt will be sent to the model without any pre-processing.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!0,deprecation:{},changelog:[{version:"0.5.0",prs:[264]},{version:"0.1.0",prs:[55]}]},"ai.responses":{brief:"The response messages sent back by the AI model.",type:"string[]",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:["hello","world"],deprecation:{replacement:"gen_ai.output.messages"},changelog:[{version:"0.1.0",prs:[65,127]},{version:"0.0.0"}]},"ai.response_format":{brief:"For an AI model call, the format of the response",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"json_object",deprecation:{},changelog:[{version:"0.5.0",prs:[264]},{version:"0.1.0",prs:[55,127]}]},"ai.search_queries":{brief:"Queries used to search for relevant context or documents.",type:"string[]",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:["climate change effects","renewable energy"],deprecation:{},changelog:[{version:"0.5.0",prs:[264]},{version:"0.1.0",prs:[55]}]},"ai.search_results":{brief:"Results returned from search queries for context.",type:"string[]",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:["search_result_1, search_result_2"],deprecation:{},changelog:[{version:"0.5.0",prs:[264]},{version:"0.1.0",prs:[55]}]},"ai.seed":{brief:"The seed, ideally models given the same seed and same other parameters will produce the exact same output.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"1234567890",deprecation:{replacement:"gen_ai.request.seed"},aliases:["gen_ai.request.seed"],changelog:[{version:"0.1.0",prs:[55,57,61,108,127]}]},"ai.streaming":{brief:"Whether the request was streamed back.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!0,deprecation:{replacement:"gen_ai.response.streaming"},aliases:["gen_ai.response.streaming"],changelog:[{version:"0.1.0",prs:[76,108]},{version:"0.0.0"}]},"ai.tags":{brief:"Tags that describe an AI pipeline step.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:'{"executed_function": "add_integers"}',deprecation:{},changelog:[{version:"0.5.0",prs:[264]},{version:"0.1.0",prs:[55,127]}]},"ai.temperature":{brief:"For an AI model call, the temperature parameter. Temperature essentially means how random the output will be.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:.1,deprecation:{replacement:"gen_ai.request.temperature"},aliases:["gen_ai.request.temperature"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[55,57,61,108]}]},"ai.texts":{brief:"Raw text inputs provided to the model.",type:"string[]",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:["Hello, how are you?","What is the capital of France?"],deprecation:{replacement:"gen_ai.input.messages"},aliases:["gen_ai.input.messages"],changelog:[{version:"0.5.0",prs:[264]},{version:"0.1.0",prs:[55]}]},"ai.tools":{brief:"For an AI model call, the functions that are available",type:"string[]",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:["function_1","function_2"],deprecation:{replacement:"gen_ai.tool.definitions"},changelog:[{version:"0.1.0",prs:[55,65,127]}]},"ai.tool_calls":{brief:"For an AI model call, the tool calls that were made.",type:"string[]",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:["tool_call_1","tool_call_2"],deprecation:{replacement:"gen_ai.output.messages"},changelog:[{version:"0.1.0",prs:[55,65]}]},"ai.top_k":{brief:"Limits the model to only consider the K most likely next tokens, where K is an integer (e.g., top_k=20 means only the 20 highest probability tokens are considered).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:35,deprecation:{replacement:"gen_ai.request.top_k"},aliases:["gen_ai.request.top_k"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[55,57,61,108]}]},"ai.top_p":{brief:"Limits the model to only consider tokens whose cumulative probability mass adds up to p, where p is a float between 0 and 1 (e.g., top_p=0.7 means only tokens that sum up to 70% of the probability mass are considered).",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:.7,deprecation:{replacement:"gen_ai.request.top_p"},aliases:["gen_ai.request.top_p"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[55,57,61,108]}]},"ai.total_cost":{brief:"The total cost for the tokens used.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:12.34,deprecation:{replacement:"gen_ai.cost.total_tokens"},aliases:["gen_ai.cost.total_tokens"],changelog:[{version:"0.5.0",prs:[264]},{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[53]}]},"ai.total_tokens.used":{brief:"The total number of tokens used to process the prompt.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:30,deprecation:{replacement:"gen_ai.usage.total_tokens"},aliases:["gen_ai.usage.total_tokens"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[57,61,108]},{version:"0.0.0"}]},"ai.warnings":{brief:"Warning messages generated during model execution.",type:"string[]",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:["Token limit exceeded"],deprecation:{},changelog:[{version:"0.5.0",prs:[264]},{version:"0.1.0",prs:[55]}]},"angular.version":{brief:"The version of the Angular framework",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"17.1.0",changelog:[{version:"0.7.0",prs:[367],description:"Added angular.version attribute"}]},"app.app_build":{brief:"Internal build identifier, as it appears on the platform.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"1",deprecation:{replacement:"app.build",reason:"Deprecated in favor of app.build"},aliases:["app.build"],changelog:[{version:"0.5.0",prs:[296],description:"Added and deprecated app.app_build in favor of app.build"}]},"app.app_identifier":{brief:"Version-independent application identifier, often a dotted bundle ID.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"com.example.myapp",deprecation:{replacement:"app.identifier",reason:"Deprecated in favor of app.identifier"},aliases:["app.identifier"],changelog:[{version:"0.5.0",prs:[296],description:"Added and deprecated app.app_identifier in favor of app.identifier"}]},"app.app_name":{brief:"Human readable application name, as it appears on the platform.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"My App",deprecation:{replacement:"app.name",reason:"Deprecated in favor of app.name"},aliases:["app.name"],changelog:[{version:"0.5.0",prs:[296],description:"Added and deprecated app.app_name in favor of app.name"}]},"app.app_start_time":{brief:"Formatted UTC timestamp when the user started the application.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"2025-01-01T00:00:00.000Z",deprecation:{replacement:"app.start_time",reason:"Deprecated in favor of app.start_time"},aliases:["app.start_time"],changelog:[{version:"0.5.0",prs:[296],description:"Added and deprecated app.app_start_time in favor of app.start_time"}]},"app.app_version":{brief:"Human readable application version, as it appears on the platform.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"1.0.0",deprecation:{replacement:"app.version",reason:"Deprecated in favor of app.version"},aliases:["app.version"],changelog:[{version:"0.5.0",prs:[296],description:"Added and deprecated app.app_version in favor of app.version"}]},"app.build":{brief:"Internal build identifier, as it appears on the platform.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"1",aliases:["app.app_build"],changelog:[{version:"0.5.0",prs:[296],description:"Added app.build attribute"}]},"app.identifier":{brief:"Version-independent application identifier, often a dotted bundle ID.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"com.example.myapp",aliases:["app.app_identifier"],changelog:[{version:"0.5.0",prs:[296],description:"Added app.identifier attribute"}]},"app.in_foreground":{brief:"Whether the application is currently in the foreground.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!0,changelog:[{version:"0.5.0",prs:[296],description:"Added app.in_foreground attribute"}]},"app.name":{brief:"Human readable application name, as it appears on the platform.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"My App",aliases:["app.app_name"],changelog:[{version:"0.5.0",prs:[296],description:"Added app.name attribute"}]},app_start_cold:{brief:"The duration of a cold app start in milliseconds",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1234.56,deprecation:{replacement:"app.vitals.start.cold.value",reason:"Replaced by app.vitals.start.cold.value to align with the app.vitals.* namespace for mobile performance attributes"},aliases:["app.vitals.start.cold.value"],changelog:[{version:"0.5.0",prs:[323],description:"Added and deprecated in favor of app.vitals.start.cold.value"}]},"app.start_time":{brief:"Formatted UTC timestamp when the user started the application.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"2025-01-01T00:00:00.000Z",aliases:["app.app_start_time"],changelog:[{version:"0.5.0",prs:[296],description:"Added app.start_time attribute"}]},app_start_type:{brief:"Mobile app start variant. Either cold or warm.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"cold",deprecation:{replacement:"app.vitals.start.type",reason:"Replaced by app.vitals.start.type to align with the app.vitals.* namespace for mobile performance attributes"},aliases:["app.vitals.start.type"],changelog:[{version:"0.5.0",prs:[313],description:"Deprecated in favor of app.vitals.start.type"},{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},app_start_warm:{brief:"The duration of a warm app start in milliseconds",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1234.56,deprecation:{replacement:"app.vitals.start.warm.value",reason:"Replaced by app.vitals.start.warm.value to align with the app.vitals.* namespace for mobile performance attributes"},aliases:["app.vitals.start.warm.value"],changelog:[{version:"0.5.0",prs:[323],description:"Added and deprecated in favor of app.vitals.start.warm.value"}]},"app.version":{brief:"Human readable application version, as it appears on the platform.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"1.0.0",aliases:["app.app_version"],changelog:[{version:"0.5.0",prs:[296],description:"Added app.version attribute"}]},"app.vitals.frames.delay.value":{brief:"The sum of all delayed frame durations in seconds during the lifetime of the span. For more information see [frames delay](https://develop.sentry.dev/sdk/performance/frames-delay/).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:5,aliases:["frames.delay"],changelog:[{version:"0.5.0",prs:[313],description:"Added app.vitals.frames.delay.value to replace frames.delay"}]},"app.vitals.frames.frozen.count":{brief:"The number of frozen frames rendered during the lifetime of the span.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:3,aliases:["frames.frozen"],changelog:[{version:"0.5.0",prs:[313],description:"Added app.vitals.frames.frozen.count to replace frames.frozen"}]},"app.vitals.frames.slow.count":{brief:"The number of slow frames rendered during the lifetime of the span.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1,aliases:["frames.slow"],changelog:[{version:"0.5.0",prs:[313],description:"Added app.vitals.frames.slow.count to replace frames.slow"}]},"app.vitals.frames.total.count":{brief:"The number of total frames rendered during the lifetime of the span.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:60,aliases:["frames.total"],changelog:[{version:"0.5.0",prs:[313],description:"Added app.vitals.frames.total.count to replace frames.total"}]},"app.vitals.start.cold.value":{brief:"The duration of a cold app start in milliseconds",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1234.56,aliases:["app_start_cold"],changelog:[{version:"0.5.0",prs:[313],description:"Added app.vitals.start.cold.value attribute"}]},"app.vitals.start.prewarmed":{brief:"Whether the app start was prewarmed.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!0,changelog:[{version:"0.11.0",prs:[379],description:"Added app.vitals.start.prewarmed attribute"}]},"app.vitals.start.reason":{brief:"The reason that triggered the app start.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"push",changelog:[{version:"0.7.0",prs:[353],description:"Added app.vitals.start.reason attribute"}]},"app.vitals.start.screen":{brief:"The screen that is rendered when the app start is complete. This is the screen the user first sees and can interact with after launch. The absence of this attribute on the app start span indicates a background app start where no UI was rendered.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"MainActivity",changelog:[{version:"0.7.0",prs:[353],description:"Added app.vitals.start.screen attribute"}]},"app.vitals.start.type":{brief:"The type of app start, for example `cold` or `warm`",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"cold",aliases:["app_start_type"],changelog:[{version:"0.5.0",prs:[313],description:"Added app.vitals.start.type attribute"}]},"app.vitals.start.warm.value":{brief:"The duration of a warm app start in milliseconds",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1234.56,aliases:["app_start_warm"],changelog:[{version:"0.5.0",prs:[313],description:"Added app.vitals.start.warm.value attribute"}]},"app.vitals.ttfd.value":{brief:"The duration of time to full display in milliseconds",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1234.56,aliases:["time_to_full_display"],changelog:[{version:"0.5.0",prs:[313],description:"Added app.vitals.ttfd.value attribute"}]},"app.vitals.ttid.value":{brief:"The duration of time to initial display in milliseconds",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1234.56,aliases:["time_to_initial_display"],changelog:[{version:"0.5.0",prs:[313],description:"Added app.vitals.ttid.value attribute"}]},"art.gc.blocking_count":{brief:"Total number of blocking (stop-the-world) garbage collections performed by the Android Runtime",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1,changelog:[{version:"0.11.0",prs:[382],description:"Added art.gc.blocking_count attribute"}]},"art.gc.blocking_time":{brief:"Total time spent in blocking (stop-the-world) garbage collections by the Android Runtime, in milliseconds",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:11.873,changelog:[{version:"0.11.0",prs:[382],description:"Added art.gc.blocking_time attribute"}]},"art.gc.pre_oome_count":{brief:"Total number of garbage collections triggered as a last resort before an OutOfMemoryError by the Android Runtime",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:0,changelog:[{version:"0.11.0",prs:[382],description:"Added art.gc.pre_oome_count attribute"}]},"art.gc.total_count":{brief:"Total number of garbage collections performed by the Android Runtime",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1,changelog:[{version:"0.11.0",prs:[382],description:"Added art.gc.total_count attribute"}]},"art.gc.total_time":{brief:"Total time spent in garbage collection by the Android Runtime, in milliseconds",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:11.807,changelog:[{version:"0.11.0",prs:[382],description:"Added art.gc.total_time attribute"}]},"art.gc.waiting_time":{brief:"Total time threads spent waiting for garbage collection to complete in the Android Runtime, in milliseconds",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:8.054,changelog:[{version:"0.11.0",prs:[382],description:"Added art.gc.waiting_time attribute"}]},"art.memory.free":{brief:"Free memory available to the process as reported by the Android Runtime, in bytes",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:3181568,changelog:[{version:"0.11.0",prs:[382],description:"Added art.memory.free attribute"}]},"art.memory.free_until_gc":{brief:"Free memory available before a garbage collection would be triggered by the Android Runtime, in bytes",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:3181568,changelog:[{version:"0.11.0",prs:[382],description:"Added art.memory.free_until_gc attribute"}]},"art.memory.free_until_oome":{brief:"Free memory available before an OutOfMemoryError would be thrown by the Android Runtime, in bytes",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:196083712,changelog:[{version:"0.11.0",prs:[382],description:"Added art.memory.free_until_oome attribute"}]},"art.memory.max":{brief:"Maximum memory the process is allowed to use as reported by the Android Runtime, in bytes",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:201326592,changelog:[{version:"0.11.0",prs:[382],description:"Added art.memory.max attribute"}]},"art.memory.total":{brief:"Total memory currently allocated to the process by the Android Runtime, in bytes",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:7774208,changelog:[{version:"0.11.0",prs:[382],description:"Added art.memory.total attribute"}]},"aws.cloudwatch.logs.log_group":{brief:"The name of the CloudWatch Logs log group",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"/aws/lambda/my-function",changelog:[{version:"0.7.0",prs:[369],description:"Added aws.cloudwatch.logs.log_group attribute"}]},"aws.cloudwatch.logs.log_stream":{brief:"The name of the CloudWatch Logs log stream",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"2024/01/01/[$LATEST]abcdef1234567890",changelog:[{version:"0.7.0",prs:[369],description:"Added aws.cloudwatch.logs.log_stream attribute"}]},"aws.cloudwatch.logs.url":{brief:"The URL to the CloudWatch Logs log group",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/my-log-group",changelog:[{version:"0.7.0",prs:[369],description:"Added aws.cloudwatch.logs.url attribute"}]},"aws.dynamodb.attribute_definitions":{brief:"The JSON-serialized value of each item in the `AttributeDefinitions` request field.",type:"string[]",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:['{ "AttributeName": "string", "AttributeType": "string" }'],changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.attribute_definitions attribute"}]},"aws.dynamodb.consistent_read":{brief:"The value of the `ConsistentRead` request parameter.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:!0,changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.consistent_read attribute"}]},"aws.dynamodb.consumed_capacity":{brief:"The JSON-serialized value of each item in the `ConsumedCapacity` response field.",type:"string[]",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:['{ "CapacityUnits": number, "GlobalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "LocalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "ReadCapacityUnits": number, "Table": { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number }, "TableName": "string", "WriteCapacityUnits": number }'],changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.consumed_capacity attribute"}]},"aws.dynamodb.count":{brief:"The value of the `Count` response parameter.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:10,changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.count attribute"}]},"aws.dynamodb.exclusive_start_table":{brief:"The value of the `ExclusiveStartTableName` request parameter.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"Users",changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.exclusive_start_table attribute"}]},"aws.dynamodb.global_secondary_indexes":{brief:"The JSON-serialized value of each item of the `GlobalSecondaryIndexes` request field.",type:"string[]",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:['{ "IndexName": "string", "KeySchema": [ { "AttributeName": "string", "KeyType": "string" } ], "Projection": { "NonKeyAttributes": [ "string" ], "ProjectionType": "string" }, "ProvisionedThroughput": { "ReadCapacityUnits": number, "WriteCapacityUnits": number } }'],changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.global_secondary_indexes attribute"}]},"aws.dynamodb.global_secondary_index_updates":{brief:"The JSON-serialized value of each item in the `GlobalSecondaryIndexUpdates` request field.",type:"string[]",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:['{ "Create": { "IndexName": "string", "KeySchema": [ { "AttributeName": "string", "KeyType": "string" } ], "Projection": { "NonKeyAttributes": [ "string" ], "ProjectionType": "string" }, "ProvisionedThroughput": { "ReadCapacityUnits": number, "WriteCapacityUnits": number } }'],changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.global_secondary_index_updates attribute"}]},"aws.dynamodb.index_name":{brief:"The value of the `IndexName` request parameter.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"name_to_group",changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.index_name attribute"}]},"aws.dynamodb.item_collection_metrics":{brief:"The JSON-serialized value of the `ItemCollectionMetrics` response field.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:'{ "string" : [ { "ItemCollectionKey": { "string" : { "B": blob, "BOOL": boolean, "BS": [ blob ], "L": [ "AttributeValue" ], "M": { "string" : "AttributeValue" }, "N": "string", "NS": [ "string" ], "NULL": boolean, "S": "string", "SS": [ "string" ] } }, "SizeEstimateRangeGB": [ number ] } ] }',changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.item_collection_metrics attribute"}]},"aws.dynamodb.limit":{brief:"The value of the `Limit` request parameter.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:10,changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.limit attribute"}]},"aws.dynamodb.local_secondary_indexes":{brief:"The JSON-serialized value of each item of the `LocalSecondaryIndexes` request field.",type:"string[]",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:['{ "IndexArn": "string", "IndexName": "string", "IndexSizeBytes": number, "ItemCount": number, "KeySchema": [ { "AttributeName": "string", "KeyType": "string" } ], "Projection": { "NonKeyAttributes": [ "string" ], "ProjectionType": "string" } }'],changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.local_secondary_indexes attribute"}]},"aws.dynamodb.projection":{brief:"The value of the `ProjectionExpression` request parameter.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"Title, Price, Color",changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.projection attribute"}]},"aws.dynamodb.provisioned_read_capacity":{brief:"The value of the `ProvisionedThroughput.ReadCapacityUnits` request parameter.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:1,changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.provisioned_read_capacity attribute"}]},"aws.dynamodb.provisioned_write_capacity":{brief:"The value of the `ProvisionedThroughput.WriteCapacityUnits` request parameter.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:2,changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.provisioned_write_capacity attribute"}]},"aws.dynamodb.scanned_count":{brief:"The value of the `ScannedCount` response parameter.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:50,changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.scanned_count attribute"}]},"aws.dynamodb.scan_forward":{brief:"The value of the `ScanIndexForward` request parameter.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:!0,changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.scan_forward attribute"}]},"aws.dynamodb.segment":{brief:"The value of the `Segment` request parameter.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:10,changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.segment attribute"}]},"aws.dynamodb.select":{brief:"The value of the `Select` request parameter.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"ALL_ATTRIBUTES",changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.select attribute"}]},"aws.dynamodb.table_count":{brief:"The number of items in the `TableNames` response parameter.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:20,changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.table_count attribute"}]},"aws.dynamodb.table_names":{brief:"The keys in the `RequestItems` object field.",type:"string[]",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:["Users","Cats"],changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.table_names attribute"}]},"aws.dynamodb.total_segments":{brief:"The value of the `TotalSegments` request parameter.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:100,changelog:[{version:"0.16.0",prs:[479],description:"Added aws.dynamodb.total_segments attribute"}]},"aws.extended_request_id":{brief:"The AWS extended request ID as returned in the response headers.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"wzHcyEWfmOGDIE5QOhTAqFDoDWP3y8IUvpNINCwL9N4TEHbUw0/gZJ+VZTmCNCWR7fezEN3eCiQ=",aliases:["aws.request.extended_id"],changelog:[{version:"0.16.0",prs:[480],description:"Added aws.extended_request_id attribute"}]},"aws.kinesis.stream_name":{brief:"The name of the AWS Kinesis stream the request refers to.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"some-stream-name",aliases:["aws.kinesis.stream.name"],changelog:[{version:"0.16.0",prs:[480],description:"Added aws.kinesis.stream_name attribute"}]},"aws.kinesis.stream.name":{brief:"The name of the AWS Kinesis stream the request refers to.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"some-stream-name",deprecation:{replacement:"aws.kinesis.stream_name",reason:"This attribute is being deprecated in favor of aws.kinesis.stream_name, which is the OTel-aligned replacement."},aliases:["aws.kinesis.stream_name"],changelog:[{version:"0.16.0",prs:[480],description:"Added aws.kinesis.stream.name attribute, deprecated in favor of aws.kinesis.stream_name"}]},"aws.lambda.aws_request_id":{brief:"The AWS request ID as received by the Lambda function runtime",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"8476a536-e9f4-11e8-9739-2dfe598c3fcd",deprecation:{replacement:"faas.invocation_id",reason:"This attribute is being deprecated in favor of faas.invocation_id"},aliases:["faas.invocation_id","faas.execution"],changelog:[{version:"0.16.0",prs:[473],description:"Added faas.execution as an alias"},{version:"0.11.1",prs:[414,424],description:"Deprecated aws.lambda.aws_request_id in favor of faas.invocation_id"},{version:"0.7.0",prs:[369],description:"Added aws.lambda.aws_request_id attribute"}]},"aws.lambda.execution_duration_in_millis":{brief:"The execution duration of the Lambda function invocation in milliseconds",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1234.56,changelog:[{version:"0.7.0",prs:[369],description:"Added aws.lambda.execution_duration_in_millis attribute"}]},"aws.lambda.function_name":{brief:"The name of the Lambda function",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"my-function",deprecation:{replacement:"faas.name",reason:"Use the OTel-aligned faas.name attribute instead"},aliases:["faas.name"],changelog:[{version:"0.11.1",prs:[414],description:"Deprecated aws.lambda.function_name in favor of faas.name"},{version:"0.7.0",prs:[369],description:"Added aws.lambda.function_name attribute"}]},"aws.lambda.function_version":{brief:"The version of the Lambda function",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"$LATEST",deprecation:{replacement:"faas.version",reason:"Use the OTel-aligned faas.version attribute instead"},aliases:["faas.version"],changelog:[{version:"0.11.1",prs:[414,424],description:"Deprecated aws.lambda.function_version in favor of faas.version"},{version:"0.7.0",prs:[369],description:"Added aws.lambda.function_version attribute"}]},"aws.lambda.invoked_arn":{brief:"The full ARN of the Lambda function that was invoked",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"arn:aws:lambda:us-east-1:123456789012:function:my-function",aliases:["aws.lambda.invoked_function_arn"],changelog:[{version:"0.11.1",prs:[414]}]},"aws.lambda.invoked_function_arn":{brief:"The full ARN of the Lambda function that was invoked",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"arn:aws:lambda:us-east-1:123456789012:function:my-function",deprecation:{replacement:"aws.lambda.invoked_arn",reason:"This attribute is being deprecated in favor of aws.lambda.invoked_arn"},aliases:["aws.lambda.invoked_arn"],changelog:[{version:"0.11.1",prs:[414],description:"Deprecated aws.lambda.invoked_function_arn in favor of aws.lambda.invoked_arn"},{version:"0.7.0",prs:[369],description:"Added aws.lambda.invoked_function_arn attribute"}]},"aws.lambda.remaining_time_in_millis":{brief:"The remaining time in milliseconds before the Lambda function times out",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:5e3,changelog:[{version:"0.7.0",prs:[369],description:"Added aws.lambda.remaining_time_in_millis attribute"}]},"aws.log.group.names":{brief:"The name(s) of the AWS log group(s) an application is writing to.",type:"string[]",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:["/aws/lambda/my-function","opentelemetry-service"],changelog:[{version:"0.11.1",prs:[414]}]},"aws.log.stream.names":{brief:"The name(s) of the AWS log stream(s) an application is writing to.",type:"string[]",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:["logs/main/10838bed-421f-43ef-870a-f43feacbbb5b"],changelog:[{version:"0.11.1",prs:[414]}]},"aws.request.extended_id":{brief:"The AWS extended request ID as returned in the response headers.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"wzHcyEWfmOGDIE5QOhTAqFDoDWP3y8IUvpNINCwL9N4TEHbUw0/gZJ+VZTmCNCWR7fezEN3eCiQ=",deprecation:{replacement:"aws.extended_request_id",reason:"This attribute is being deprecated in favor of aws.extended_request_id, which is the OTel-aligned replacement."},aliases:["aws.extended_request_id"],changelog:[{version:"0.16.0",prs:[480],description:"Added aws.request.extended_id attribute, deprecated in favor of aws.extended_request_id"}]},"aws.request_id":{brief:"The AWS request ID as returned in the response headers.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"79b9da39-b7ae-508a-a6bc-864b2829c622",aliases:["aws.request.id"],changelog:[{version:"0.16.0",prs:[480],description:"Added aws.request_id attribute"}]},"aws.request.id":{brief:"The AWS request ID as returned in the response headers.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"79b9da39-b7ae-508a-a6bc-864b2829c622",deprecation:{replacement:"aws.request_id",reason:"This attribute is being deprecated in favor of aws.request_id, which is the OTel-aligned replacement."},aliases:["aws.request_id"],changelog:[{version:"0.16.0",prs:[480],description:"Added aws.request.id attribute, deprecated in favor of aws.request_id"}]},"aws.s3.bucket":{brief:"The S3 bucket name the request refers to.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"ot-demo-test",changelog:[{version:"0.16.0",prs:[480],description:"Added aws.s3.bucket attribute"}]},"aws.secretsmanager.secret.arn":{brief:"The ARN of the Secret stored in Secrets Manager.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"arn:aws:secretsmanager:us-east-1:123456789012:secret:SecretName-6RandomCharacters",changelog:[{version:"0.16.0",prs:[480],description:"Added aws.secretsmanager.secret.arn attribute"}]},"aws.sns.topic.arn":{brief:"The ARN of the AWS SNS Topic. An Amazon SNS topic is a logical access point that acts as a communication channel.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"arn:aws:sns:us-east-1:123456789012:mystack-mytopic-NZJ5JSMVGFIE",changelog:[{version:"0.16.0",prs:[480],description:"Added aws.sns.topic.arn attribute"}]},"aws.step_functions.activity.arn":{brief:"The ARN of the AWS Step Functions Activity.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"arn:aws:states:us-east-1:123456789012:activity:get-greeting",changelog:[{version:"0.16.0",prs:[480],description:"Added aws.step_functions.activity.arn attribute"}]},"aws.step_functions.state_machine.arn":{brief:"The ARN of the AWS Step Functions State Machine.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"arn:aws:states:us-east-1:123456789012:stateMachine:myStateMachine:1",changelog:[{version:"0.16.0",prs:[480],description:"Added aws.step_functions.state_machine.arn attribute"}]},blocked_main_thread:{brief:"Whether the main thread was blocked by the span.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!0,changelog:[{version:"0.0.0"}]},"browser.name":{brief:"The name of the browser.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Chrome",aliases:["sentry.browser.name"],changelog:[{version:"0.1.0",prs:[127,139]},{version:"0.0.0"}]},"browser.performance.navigation.activation_start":{brief:"The time between initiating a navigation to a page and the browser activating the page",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1.983,aliases:["performance.activationStart"],changelog:[{version:"0.5.0",prs:[321],description:"Added browser.performance.navigation.activation_start attribute"}]},"browser.performance.time_origin":{brief:"The browser's performance.timeOrigin timestamp representing the time when the pageload was initiated",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1776185678886e-3,aliases:["performance.timeOrigin"],changelog:[{version:"0.5.0",prs:[321],description:"Added browser.performance.time_origin attribute attribute"}]},"browser.report.type":{brief:"A browser report sent via reporting API..",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"network-error",changelog:[{version:"0.1.0",prs:[68,127]}]},"browser.script.invoker":{brief:"How a script was called in the browser.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Window.requestAnimationFrame",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"browser.script.invoker_type":{brief:"Browser script entry point type.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"event-listener",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"browser.script.source_char_position":{brief:"A number representing the script character position of the script.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:678,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"browser.version":{brief:"The version of the browser.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"120.0.6099.130",aliases:["sentry.browser.version"],changelog:[{version:"0.1.0",prs:[59,127,139]}]},"browser.web_vital.cls.report_event":{brief:"The event that caused the SDK to report CLS (pagehide or navigation)",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"navigation",changelog:[{version:"0.5.0",prs:[319],description:"Added browser.web_vital.cls.report_event attribute"}]},"browser.web_vital.cls.source.<key>":{brief:"The HTML elements or components responsible for the layout shift. <key> is a numeric index from 1 to N",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",hasDynamicSuffix:!0,example:"body > div#app",aliases:["cls.source.<key>"],changelog:[{version:"0.5.0",prs:[234]}]},"browser.web_vital.cls.value":{brief:"The value of the recorded Cumulative Layout Shift (CLS) web vital",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:.2361,aliases:["cls"],changelog:[{version:"0.5.0",prs:[229],description:"Added browser.web_vital.cls.value attribute"}]},"browser.web_vital.fcp.value":{brief:"The time it takes for the browser to render the first piece of meaningful content on the screen",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:547.6951,aliases:["fcp"],changelog:[{version:"0.5.0",prs:[235]}]},"browser.web_vital.fp.value":{brief:"The time in milliseconds it takes for the browser to render the first pixel on the screen",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:477.1926,aliases:["fp"],changelog:[{version:"0.5.0",prs:[235]}]},"browser.web_vital.inp.value":{brief:"The value of the recorded Interaction to Next Paint (INP) web vital",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:200,aliases:["inp"],changelog:[{version:"0.5.0",prs:[229],description:"Added browser.web_vital.inp.value attribute"}]},"browser.web_vital.lcp.element":{brief:"The HTML element selector or component name for which LCP was reported",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"body > div#app > div#container > div",aliases:["lcp.element"],changelog:[{version:"0.5.0",prs:[233]}]},"browser.web_vital.lcp.id":{brief:"The id of the dom element responsible for the largest contentful paint",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"#gero",aliases:["lcp.id"],changelog:[{version:"0.5.0",prs:[233]}]},"browser.web_vital.lcp.load_time":{brief:"The time it took for the LCP element to be loaded",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1402,aliases:["lcp.loadTime"],changelog:[{version:"0.5.0",prs:[233]}]},"browser.web_vital.lcp.render_time":{brief:"The time it took for the LCP element to be rendered",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1685,aliases:["lcp.renderTime"],changelog:[{version:"0.5.0",prs:[233]}]},"browser.web_vital.lcp.report_event":{brief:"The event that caused the SDK to report LCP (pagehide or navigation)",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"pagehide",changelog:[{version:"0.5.0",prs:[319],description:"Added browser.web_vital.lcp.report_event attribute"}]},"browser.web_vital.lcp.size":{brief:"The size of the largest contentful paint element",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1024,aliases:["lcp.size"],changelog:[{version:"0.5.0",prs:[233]}]},"browser.web_vital.lcp.url":{brief:"The url of the dom element responsible for the largest contentful paint",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"https://example.com/static/img.png",aliases:["lcp.url"],changelog:[{version:"0.5.0",prs:[233]}]},"browser.web_vital.lcp.value":{brief:"The value of the recorded Largest Contentful Paint (LCP) web vital",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:2500,aliases:["lcp"],changelog:[{version:"0.5.0",prs:[229],description:"Added browser.web_vital.lcp.value attribute"}]},"browser.web_vital.ttfb.request_time":{brief:"The time it takes for the server to process the initial request and send the first byte of a response to the user's browser",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1554.5814,aliases:["ttfb.requestTime"],changelog:[{version:"0.5.0",prs:[235]}]},"browser.web_vital.ttfb.value":{brief:"The value of the recorded Time To First Byte (TTFB) web vital in Milliseconds",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:194.3322,aliases:["ttfb"],changelog:[{version:"0.5.0",prs:[235]}]},"cache.hit":{brief:"If the cache was hit during this span.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!0,changelog:[{version:"0.0.0"}]},"cache.item_size":{brief:"The size of the requested item in the cache. In bytes.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:58,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"cache.key":{brief:"The key of the cache accessed.",type:"string[]",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:["my-cache-key","my-other-cache-key"],changelog:[{version:"0.0.0"}]},"cache.operation":{brief:"The operation being performed on the cache.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"get",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"cache.ttl":{brief:"The ttl of the cache in seconds",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:120,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"cache.write":{brief:"If the cache operation resulted in a write to the cache.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!0,changelog:[{version:"0.5.0"}]},channel:{brief:"The channel name that is being used.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"mail",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"client.address":{brief:"Client address - domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"example.com",aliases:["http.client_ip"],changelog:[{version:"0.1.0",prs:[106,127]},{version:"0.0.0"}]},"client.port":{brief:"Client port number.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:5432,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"cloudflare.d1.duration":{brief:"The duration of a Cloudflare D1 operation.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:543,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"cloudflare.d1.query_type":{brief:"The type of query executed in a Cloudflare D1 operation",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"run",deprecation:{replacement:"db.operation.name"},aliases:["db.operation.name","db.operation"],changelog:[{version:"0.11.0",prs:[392],description:"Added cloudflare.d1.query_type attribute"}]},"cloudflare.d1.rows_read":{brief:"The number of rows read in a Cloudflare D1 operation.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:12,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"cloudflare.d1.rows_written":{brief:"The number of rows written in a Cloudflare D1 operation.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:12,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"cloudflare.durable_object.query.bindings":{brief:"The number of bound parameters passed to the SQL exec call.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:2,changelog:[{version:"0.13.0",prs:[435],description:"Added cloudflare.durable_object.query.bindings attribute"}]},"cloudflare.durable_object.response.rows_read":{brief:"The number of rows read by a Cloudflare Durable Object SQL operation.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:12,changelog:[{version:"0.13.0",prs:[435],description:"Added cloudflare.durable_object.response.rows_read attribute"}]},"cloudflare.durable_object.response.rows_written":{brief:"The number of rows written by a Cloudflare Durable Object SQL operation.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1,changelog:[{version:"0.13.0",prs:[435],description:"Added cloudflare.durable_object.response.rows_written attribute"}]},"cloudflare.r2.bucket":{brief:"The name of the Cloudflare R2 bucket binding",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"MY_BUCKET",changelog:[{version:"0.11.1",prs:[413],description:"Added cloudflare.r2.bucket attribute"}]},"cloudflare.r2.operation":{brief:"The R2 API operation being performed",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"GetObject",changelog:[{version:"0.11.1",prs:[413],description:"Added cloudflare.r2.operation attribute"}]},"cloudflare.r2.request.delimiter":{brief:"The delimiter used to group objects in an R2 list operation",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"/",changelog:[{version:"0.11.1",prs:[413],description:"Added cloudflare.r2.request.delimiter attribute"}]},"cloudflare.r2.request.key":{brief:"The object key used in the R2 operation",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"my-file.txt",changelog:[{version:"0.11.1",prs:[413],description:"Added cloudflare.r2.request.key attribute"}]},"cloudflare.r2.request.part_number":{brief:"The part number in a multipart upload operation",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1,changelog:[{version:"0.11.1",prs:[413],description:"Added cloudflare.r2.request.part_number attribute"}]},"cloudflare.r2.request.prefix":{brief:"The prefix used to filter objects in an R2 list operation",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"images/",changelog:[{version:"0.11.1",prs:[413],description:"Added cloudflare.r2.request.prefix attribute"}]},"cloudflare.workflow.attempt":{brief:"The current attempt number for a Cloudflare Workflow step",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1,changelog:[{version:"0.11.0",prs:[392],description:"Added cloudflare.workflow.attempt attribute"}]},"cloudflare.workflow.retries.backoff":{brief:"The backoff strategy for Cloudflare Workflow step retries",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"exponential",changelog:[{version:"0.11.0",prs:[392],description:"Added cloudflare.workflow.retries.backoff attribute"}]},"cloudflare.workflow.retries.delay":{brief:"The delay between Cloudflare Workflow step retries",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"5 seconds",changelog:[{version:"0.11.0",prs:[392],description:"Added cloudflare.workflow.retries.delay attribute"}]},"cloudflare.workflow.retries.limit":{brief:"The maximum number of retries for a Cloudflare Workflow step",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:3,changelog:[{version:"0.11.0",prs:[392],description:"Added cloudflare.workflow.retries.limit attribute"}]},"cloudflare.workflow.timeout":{brief:"The timeout duration for a Cloudflare Workflow step",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"1 minute",changelog:[{version:"0.11.0",prs:[392],description:"Added cloudflare.workflow.timeout attribute"}]},"cloud.account.id":{brief:"The cloud account ID the resource is assigned to",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"123456789012",changelog:[{version:"0.7.0",prs:[364],description:"Added cloud.account.id attribute"}]},"cloud.availability_zone":{brief:"Cloud regions often have multiple, isolated locations known as zones to increase availability",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"us-east-1c",changelog:[{version:"0.7.0",prs:[364],description:"Added cloud.availability_zone attribute"}]},"cloud.platform":{brief:"The cloud platform in use",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"aws_lambda",changelog:[{version:"0.7.0",prs:[364],description:"Added cloud.platform attribute"}]},"cloud.provider":{brief:"Name of the cloud provider",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"aws",changelog:[{version:"0.7.0",prs:[364],description:"Added cloud.provider attribute"}]},"cloud.region":{brief:"The geographical region the resource is running",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"us-east-1",changelog:[{version:"0.7.0",prs:[364],description:"Added cloud.region attribute"}]},"cloud.resource_id":{brief:"Cloud provider-specific native identifier of the monitored cloud resource",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"arn:aws:lambda:REGION:ACCOUNT_ID:function:my-function",aliases:["faas.id"],changelog:[{version:"0.16.0",prs:[475],description:"Added faas.id as an alias"},{version:"0.11.1",prs:[414]}],additionalContext:["This can be an identifier for a resource in AWS, GCP, or Azure. There may be some overlap in values found here with other attributes. For instance, an AWS lambda ARN may be found here as well as in `aws.lambda.invoked_arn`. OTEL recommends setting them alongside each other."]},cls:{brief:"The value of the recorded Cumulative Layout Shift (CLS) web vital",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:.2361,deprecation:{replacement:"browser.web_vital.cls.value",reason:"The CLS web vital is now recorded as a browser.web_vital.cls.value attribute."},aliases:["browser.web_vital.cls.value"],changelog:[{version:"0.5.0",prs:[229],description:"Added and deprecated attribute to document JS SDK's current behaviour"}]},"cls.source.<key>":{brief:"The HTML elements or components responsible for the layout shift. <key> is a numeric index from 1 to N",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",hasDynamicSuffix:!0,example:"body > div#app",deprecation:{replacement:"browser.web_vital.cls.source.<key>",reason:"The CLS source is now recorded as a browser.web_vital.cls.source.<key> attribute."},aliases:["browser.web_vital.cls.source.<key>"],changelog:[{version:"0.5.0",prs:[234]}]},"code.filepath":{brief:"The source code file name that identifies the code unit as uniquely as possible (preferably an absolute file path).",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"/app/myapplication/http/handler/server.py",deprecation:{replacement:"code.file.path"},aliases:["code.file.path"],changelog:[{version:"0.1.0",prs:[61]},{version:"0.0.0"}]},"code.file.path":{brief:"The source code file name that identifies the code unit as uniquely as possible (preferably an absolute file path).",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"/app/myapplication/http/handler/server.py",aliases:["code.filepath"],changelog:[{version:"0.0.0"}]},"code.function":{brief:"The method or function name, or equivalent (usually rightmost part of the code unit's name).",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"server_request",aliases:["code.function.name"],changelog:[{version:"0.1.0",prs:[61,74]},{version:"0.0.0"}]},"code.function.name":{brief:"The method or function fully-qualified name without arguments.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"server_request",aliases:["code.function"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"code.lineno":{brief:"The line number in code.filepath best representing the operation. It SHOULD point within the code unit named in code.function",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:42,deprecation:{replacement:"code.line.number"},aliases:["code.line.number"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[61,108]},{version:"0.0.0"}]},"code.line.number":{brief:"The line number in code.filepath best representing the operation. It SHOULD point within the code unit named in code.function",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:42,aliases:["code.lineno"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"code.namespace":{brief:"The 'namespace' within which code.function is defined. Usually the qualified class or module name, such that code.namespace + some separator + code.function form a unique identifier for the code unit.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"http.handler",changelog:[{version:"0.1.0",prs:[61,74]},{version:"0.0.0"}]},connectionType:{brief:"Specifies the type of the current connection (e.g. wifi, ethernet, cellular , etc).",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"wifi",deprecation:{replacement:"network.connection.type",reason:"Old namespace-less attribute, to be replaced with network.connection.type for span-first future"},aliases:["network.connection.type","device.connection_type"],changelog:[{version:"0.5.0",prs:[279],description:"Added and deprecated attribute to document JS SDK's current behaviour"}]},"connection.rtt":{brief:"Specifies the estimated effective round-trip time of the current connection, in milliseconds.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:100,deprecation:{replacement:"network.connection.rtt",reason:"Old attribute name (no official namespace), to be replaced with network.connection.rtt for span-first future"},aliases:["network.connection.rtt"],changelog:[{version:"0.5.0",prs:[279],description:"Added and deprecated attribute to document JS SDK's current behaviour"}]},"culture.calendar":{brief:"The calendar system used by the culture.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"GregorianCalendar",changelog:[{version:"0.4.0",prs:[243]}]},"culture.display_name":{brief:"Human readable name of the culture.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"English (United States)",changelog:[{version:"0.4.0",prs:[243]}]},"culture.is_24_hour_format":{brief:"Whether the culture uses 24-hour time format.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!0,changelog:[{version:"0.4.0",prs:[243]}]},"culture.locale":{brief:"The locale identifier following RFC 4646.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"en-US",changelog:[{version:"0.4.0",prs:[243]}]},"culture.timezone":{brief:"The timezone of the culture, as a geographic timezone identifier.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Europe/Vienna",changelog:[{version:"0.4.0",prs:[243]}]},"db.collection.name":{brief:"The name of a collection (table, container) within the database.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"users",changelog:[{version:"0.1.0",prs:[106,127]},{version:"0.0.0"}]},"db.driver.name":{brief:"The name of the driver used for the database connection.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"psycopg2",changelog:[{version:"0.5.0",prs:[297],description:"Added db.driver.name attribute"}]},"db.name":{brief:"The name of the database being accessed.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"customers",deprecation:{replacement:"db.namespace"},aliases:["db.namespace"],changelog:[{version:"0.1.0",prs:[61,127]},{version:"0.0.0"}]},"db.namespace":{brief:"The name of the database being accessed.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"customers",aliases:["db.name"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"db.operation":{brief:"The name of the operation being executed.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"SELECT",deprecation:{replacement:"db.operation.name"},aliases:["db.operation.name","cloudflare.d1.query_type"],changelog:[{version:"0.4.0",prs:[199]},{version:"0.1.0",prs:[61,127]},{version:"0.0.0"}]},"db.operation.batch.size":{brief:"The number of queries included in a batch operation. Operations are only considered batches when they contain two or more operations, and so db.operation.batch.size SHOULD never be 1.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:3,changelog:[{version:"0.11.0",prs:[407],description:"Added db.operation.batch.size attribute"}]},"db.operation.name":{brief:"The name of the operation being executed.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"SELECT",aliases:["db.operation","cloudflare.d1.query_type"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"db.query.parameter.<key>":{brief:"A query parameter used in db.query.text, with <key> being the parameter name, and the attribute value being a string representation of the parameter value.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",hasDynamicSuffix:!0,example:"db.query.parameter.foo='123'",changelog:[{version:"0.1.0",prs:[103,127]}]},"db.query.summary":{brief:"A shortened representation of operation(s) in the full query. This attribute must be low-cardinality and should only contain the operation table names.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"SELECT users",changelog:[{version:"0.4.0",prs:[208]},{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"db.query.text":{brief:"The database parameterized query being executed. Any parameter values (filters, insertion values, etc) should be replaced with parameter placeholders. If applicable, use `db.query.parameter.<key>` to add the parameter value.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"SELECT * FROM users WHERE id = $1",aliases:["db.statement"],changelog:[{version:"0.4.0",prs:[208]},{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"db.redis.connection":{brief:"The redis connection name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"my-redis-instance",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"db.redis.key":{brief:"The key the Redis command is operating on.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"user:2047:city",changelog:[{version:"0.6.0",prs:[326],description:"Added db.redis.key attribute"}]},"db.redis.parameters":{brief:"The array of command parameters given to a redis command.",type:"string[]",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:["test","*"],changelog:[{version:"0.0.0"}]},"db.response.status_code":{brief:"Database response status code. The status code returned by the database. Usually it represents an error code, but may also represent partial success, warning, or differentiate between various types of successful outcomes.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"ORA-17002",changelog:[{version:"0.16.0",prs:[462],description:"Added db.response.status_code attribute"}]},"db.sql.bindings":{brief:"The array of query bindings.",type:"string[]",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:["1","foo"],deprecation:{replacement:"db.query.parameter.<key>",reason:"Instead of adding every binding in the db.sql.bindings attribute, add them as individual entires with db.query.parameter.<key>."},changelog:[{version:"0.1.0",prs:[61]},{version:"0.0.0"}]},"db.statement":{brief:"The database statement being executed.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"SELECT * FROM users",deprecation:{replacement:"db.query.text"},aliases:["db.query.text"],changelog:[{version:"0.4.0",prs:[199]},{version:"0.1.0",prs:[61,127]},{version:"0.0.0"}]},"db.stored_procedure.name":{brief:"The name of a stored procedure being called.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"GetUserById",changelog:[{version:"0.11.0",prs:[398]}]},"db.system":{brief:"An identifier for the database management system (DBMS) product being used. See [OpenTelemetry docs](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/database/database-spans.md#notes-and-well-known-identifiers-for-dbsystem) for a list of well-known identifiers.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"postgresql",deprecation:{replacement:"db.system.name"},aliases:["db.system.name"],changelog:[{version:"0.4.0",prs:[199,224]},{version:"0.1.0",prs:[61,127]},{version:"0.0.0"}]},"db.system.name":{brief:"An identifier for the database management system (DBMS) product being used. See [OpenTelemetry docs](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/database/database-spans.md#notes-and-well-known-identifiers-for-dbsystem) for a list of well-known identifiers.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"postgresql",aliases:["db.system"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"db.user":{brief:"The database user.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"fancy_user",changelog:[{version:"0.0.0"}]},deviceMemory:{brief:"The estimated total memory capacity of the device, only a rough estimation in gigabytes.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"8 GB",deprecation:{replacement:"device.memory.estimated_capacity",reason:"Old namespace-less attribute, to be replaced with device.memory.estimated_capacity for span-first future"},aliases:["device.memory.estimated_capacity"],changelog:[{version:"0.5.0",prs:[281],description:"Added and deprecated attribute to document JS SDK's current behaviour"}]},"device.archs":{brief:"The CPU architectures of the device.",type:"string[]",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:["arm64-v8a","armeabi-v7a","armeabi"],changelog:[{version:"0.5.0",prs:[303],description:"Added device.archs attribute"}]},"device.battery_level":{brief:"The battery level of the device as a percentage (0-100).",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:100,changelog:[{version:"0.5.0",prs:[303],description:"Added device.battery_level attribute"}]},"device.battery_temperature":{brief:"The battery temperature of the device in Celsius.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:25,changelog:[{version:"0.5.0",prs:[303],description:"Added device.battery_temperature attribute"}]},"device.boot_time":{brief:"A formatted UTC timestamp when the system was booted.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"2018-02-08T12:52:12Z",changelog:[{version:"0.5.0",prs:[303],description:"Added device.boot_time attribute"}]},"device.brand":{brief:"The brand of the device.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Apple",changelog:[{version:"0.1.0",prs:[116,127]}]},"device.charging":{brief:"Whether the device was charging or not.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!1,changelog:[{version:"0.5.0",prs:[303],description:"Added device.charging attribute"}]},"device.chipset":{brief:"The chipset of the device.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Qualcomm SM8550",changelog:[{version:"0.5.0",prs:[303],description:"Added device.chipset attribute"}]},"device.class":{brief:"The classification of the device. For example, `low`, `medium`, or `high`. Typically inferred by Relay - SDKs generally do not need to set this directly.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"medium",changelog:[{version:"0.5.0",prs:[300],description:"Added device.class attribute"}]},"device.connection_type":{brief:"The internet connection type currently being used by the device.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"wifi",deprecation:{replacement:"network.connection.type",reason:"This attribute is being deprecated in favor of network.connection.type"},aliases:["network.connection.type","connectionType"],changelog:[{version:"0.5.0",prs:[303],description:"Added and deprecated device.connection_type in favor of network.connection.type"}]},"device.cpu_description":{brief:"A description of the CPU of the device.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Intel(R) Core(TM)2 Quad CPU Q6600 @ 2.40GHz",changelog:[{version:"0.5.0",prs:[303],description:"Added device.cpu_description attribute"}]},"device.external_free_storage":{brief:"External storage free size in bytes.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:67108864e3,changelog:[{version:"0.5.0",prs:[303],description:"Added device.external_free_storage attribute"}]},"device.external_storage_size":{brief:"External storage total size in bytes.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:134217728e3,changelog:[{version:"0.5.0",prs:[303],description:"Added device.external_storage_size attribute"}]},"device.family":{brief:"The family of the device.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"iPhone",changelog:[{version:"0.1.0",prs:[116,127]}]},"device.free_memory":{brief:"Free system memory in bytes.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:2147483648,changelog:[{version:"0.5.0",prs:[300],description:"Added device.free_memory attribute"}]},"device.free_storage":{brief:"Free device storage in bytes.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:107374182400,changelog:[{version:"0.5.0",prs:[303],description:"Added device.free_storage attribute"}]},"device.id":{brief:"Unique device identifier.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"a1b2c3d4-e5f6-7890-abcd-ef1234567890",changelog:[{version:"0.5.0",prs:[303],description:"Added device.id attribute"}]},"device.locale":{brief:"The locale of the device.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"en-US",changelog:[{version:"0.5.0",prs:[303],description:"Added device.locale attribute"}]},"device.low_memory":{brief:"Whether the device was low on memory.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!1,changelog:[{version:"0.5.0",prs:[303],description:"Added device.low_memory attribute"}]},"device.low_power_mode":{brief:"Whether the device is in Low Power Mode.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!0,changelog:[{version:"0.6.0",prs:[314],description:"Added device.low_power_mode attribute"}]},"device.manufacturer":{brief:"The manufacturer of the device.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"Google",changelog:[{version:"0.5.0",prs:[303],description:"Added device.manufacturer attribute"}]},"device.memory.estimated_capacity":{brief:"The estimated total memory capacity of the device, only a rough estimation in gigabytes. Browsers report estimations in buckets of powers of 2, mostly capped at 8 GB",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:8,aliases:["deviceMemory"],changelog:[{version:"0.5.0",prs:[281],description:"Added attribute device.memory.estimated_capacity to be used instead of deviceMemory"}]},"device.memory_size":{brief:"Total system memory available in bytes.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:17179869184,changelog:[{version:"0.5.0",prs:[300],description:"Added device.memory_size attribute"}]},"device.model":{brief:"The model of the device.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"iPhone 15 Pro Max",changelog:[{version:"0.1.0",prs:[116,127]}]},"device.model_id":{brief:"An internal hardware revision to identify the device exactly.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"N861AP",changelog:[{version:"0.5.0",prs:[300],description:"Added device.model_id attribute"}]},"device.name":{brief:"The name of the device. On mobile, this is the user-assigned device name. On servers and desktops, this is typically the hostname.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"localhost",changelog:[{version:"0.5.0",prs:[303],description:"Added device.name attribute"}]},"device.online":{brief:"Whether the device was online or not.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!0,changelog:[{version:"0.5.0",prs:[303],description:"Added device.online attribute"}]},"device.orientation":{brief:'The orientation of the device, either "portrait" or "landscape".',type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"portrait",changelog:[{version:"0.5.0",prs:[303],description:"Added device.orientation attribute"}]},"device.processor_count":{brief:'Number of "logical processors".',type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:8,aliases:["hardwareConcurrency"],changelog:[{version:"0.5.0",prs:[300],description:"Added and deprecated attribute device.processor_count in favor of device.cpu.logical_core_count"}]},"device.processor_frequency":{brief:"Processor frequency in MHz.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:2400,changelog:[{version:"0.5.0",prs:[303],description:"Added device.processor_frequency attribute"}]},"device.screen_density":{brief:"The screen density of the device.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:2.625,changelog:[{version:"0.5.0",prs:[303],description:"Added device.screen_density attribute"}]},"device.screen_dpi":{brief:"The screen density in dots-per-inch (DPI) of the device.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:420,changelog:[{version:"0.5.0",prs:[303],description:"Added device.screen_dpi attribute"}]},"device.screen_height_pixels":{brief:"The height of the device screen in pixels.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:2400,changelog:[{version:"0.5.0",prs:[303],description:"Added device.screen_height_pixels attribute"}]},"device.screen_width_pixels":{brief:"The width of the device screen in pixels.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1080,changelog:[{version:"0.5.0",prs:[303],description:"Added device.screen_width_pixels attribute"}]},"device.simulator":{brief:"Whether the device is a simulator or an actual device.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!1,changelog:[{version:"0.5.0",prs:[300],description:"Added device.simulator attribute"}]},"device.storage_size":{brief:"Total device storage in bytes.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:274877906944,changelog:[{version:"0.5.0",prs:[303],description:"Added device.storage_size attribute"}]},"device.thermal_state":{brief:"The thermal state of the device. Based on Apple's `ProcessInfo.ThermalState` enum: `nominal`, `fair`, `serious`, or `critical`.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"nominal",changelog:[{version:"0.5.0",prs:[303],description:"Added device.thermal_state attribute"}]},"device.timezone":{brief:"The timezone of the device.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Europe/Vienna",changelog:[{version:"0.5.0",prs:[303],description:"Added device.timezone attribute"}]},"device.usable_memory":{brief:"Memory usable for the app in bytes.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:2147483648,changelog:[{version:"0.5.0",prs:[303],description:"Added device.usable_memory attribute"}]},dist:{brief:"The sentry dist.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"1.0",deprecation:{replacement:"sentry.dist",reason:"This attribute is being deprecated in favor of sentry.dist."},aliases:["sentry.dist"],changelog:[{version:"0.16.0",prs:[489],description:"Added dist attribute"}]},effectiveConnectionType:{brief:"Specifies the estimated effective type of the current connection (e.g. slow-2g, 2g, 3g, 4g).",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"4g",deprecation:{replacement:"network.connection.effective_type",reason:"Old namespace-less attribute, to be replaced with network.connection.effective_type for span-first future"},aliases:["network.connection.effective_type"],changelog:[{version:"0.5.0",prs:[279],description:"Added and deprecated attribute to document JS SDK's current behaviour"}]},environment:{brief:"The sentry environment.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"production",deprecation:{replacement:"sentry.environment"},aliases:["sentry.environment"],changelog:[{version:"0.1.0",prs:[61,127]},{version:"0.0.0"}]},"error.type":{brief:"Describes a class of error the operation ended with.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"timeout",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"event.id":{brief:"The unique identifier for this event (log record)",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1234567890,changelog:[{version:"0.1.0",prs:[101]}]},"event.name":{brief:"The name that uniquely identifies this event (log record)",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Process Payload",changelog:[{version:"0.1.0",prs:[101,127]}]},"exception.escaped":{brief:"SHOULD be set to true if the exception event is recorded at a point where it is known that the exception is escaping the scope of the span.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:!0,changelog:[{version:"0.0.0"}]},"exception.message":{brief:"The error message.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"ENOENT: no such file or directory",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"exception.stacktrace":{brief:"A stacktrace as a string in the natural representation for the language runtime. The representation is to be determined and documented by each language SIG.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:`Exception in thread "main" java.lang.RuntimeException: Test exception
 at com.example.GenerateTrace.methodB(GenerateTrace.java:13)
 at com.example.GenerateTrace.methodA(GenerateTrace.java:9)
 at com.example.GenerateTrace.main(GenerateTrace.java:5)`,changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"exception.type":{brief:"The type of the exception (its fully-qualified class name, if applicable). The dynamic type of the exception should be preferred over the static type in languages that support it.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"OSError",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"faas.coldstart":{brief:"A boolean that is true if the serverless function is executed for the first time (aka cold-start).",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:!0,changelog:[{version:"0.0.0"}]},"faas.cron":{brief:"A string containing the schedule period as Cron Expression.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"0/5 * * * ? *",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"faas.duration_in_ms":{brief:"The duration a function took to run, in milliseconds.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:120,changelog:[{version:"0.11.0",prs:[403]}]},"faas.entry_point":{brief:"The code that's run when the cloud provider invokes your function.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"my_main_function",changelog:[{version:"0.11.0",prs:[403,415]}]},"faas.execution":{brief:"The execution ID of the current function execution.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"af9d5aa4-a685-4c5f-a22b-444f80b3cc28",deprecation:{replacement:"faas.invocation_id",reason:"This attribute is being deprecated in favor of faas.invocation_id, which is the OTel-aligned replacement."},aliases:["faas.invocation_id","aws.lambda.aws_request_id"],changelog:[{version:"0.16.0",prs:[473],description:"Added faas.execution attribute, deprecated in favor of faas.invocation_id"}]},"faas.id":{brief:"The unique ID of the single function that this runtime instance executes.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"arn:aws:lambda:REGION:ACCOUNT_ID:function:my-function",deprecation:{replacement:"cloud.resource_id",reason:"This attribute is being deprecated in favor of cloud.resource_id, which is the OTel-aligned replacement (renamed in OTel semantic conventions v1.19.0)."},aliases:["cloud.resource_id"],changelog:[{version:"0.16.0",prs:[475],description:"Added faas.id attribute, deprecated in favor of cloud.resource_id"}]},"faas.identity":{brief:"The Service Account (GCP), IAM Execution Role (AWS), or Managed Identity (Azure) used by the serverless function when interacting with other cloud services",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"name@project.iam.gserviceaccount.com (GCP), arn:aws:iam::123456789012:role/role-name (AWS), 00000000-0000-0000-0000-000000000000 (Azure)",changelog:[{version:"0.11.0",prs:[403]}]},"faas.invocation_id":{brief:"The invocation ID of the current function invocation.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"af9d5aa4-a685-4c5f-a22b-444f80b3cc28",aliases:["aws.lambda.aws_request_id","faas.execution"],changelog:[{version:"0.16.0",prs:[473],description:"Added faas.execution as an alias"},{version:"0.11.1",prs:[414,424]}]},"faas.invoked_name":{brief:"The name of the invoked function.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"my-function",changelog:[{version:"0.16.0",prs:[481],description:"Added faas.invoked_name attribute"}]},"faas.invoked_provider":{brief:"The cloud provider of the invoked function.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"aws",changelog:[{version:"0.16.0",prs:[481],description:"Added faas.invoked_provider attribute"}]},"faas.invoked_region":{brief:"The cloud region of the invoked function.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"eu-central-1",changelog:[{version:"0.16.0",prs:[481],description:"Added faas.invoked_region attribute"}]},"faas.name":{brief:"The name of the serverless function",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"my_function",aliases:["aws.lambda.function_name"],changelog:[{version:"0.11.0",prs:[403,415]}]},"faas.time":{brief:"A string containing the function invocation time in the ISO 8601 format expressed in UTC.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"2020-01-23T13:47:06Z",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"faas.trigger":{brief:"Type of the trigger which caused this function invocation.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"timer",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"faas.version":{brief:"The version of the function that was invoked",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"$LATEST",aliases:["aws.lambda.function_version"],changelog:[{version:"0.11.1",prs:[414,424]}]},fcp:{brief:"The time it takes for the browser to render the first piece of meaningful content on the screen",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:547.6951,deprecation:{replacement:"browser.web_vital.fcp.value",reason:"This attribute is being deprecated in favor of browser.web_vital.fcp.value"},aliases:["browser.web_vital.fcp.value"],changelog:[{version:"0.5.0",prs:[235]}]},"flag.evaluation.<key>":{brief:"An instance of a feature flag evaluation. The value of this attribute is the boolean representing the evaluation result. The <key> suffix is the name of the feature flag.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",hasDynamicSuffix:!0,example:"flag.evaluation.is_new_ui=true",changelog:[{version:"0.1.0",prs:[103]}]},fp:{brief:"The time it takes for the browser to render the first pixel on the screen",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:477.1926,deprecation:{replacement:"browser.web_vital.fp.value",reason:"This attribute is being deprecated in favor of browser.web_vital.fp.value"},aliases:["browser.web_vital.fp.value"],changelog:[{version:"0.5.0",prs:[235]}]},"frames.delay":{brief:"The sum of all delayed frame durations in seconds during the lifetime of the span. For more information see [frames delay](https://develop.sentry.dev/sdk/performance/frames-delay/).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:5,deprecation:{replacement:"app.vitals.frames.delay.value",reason:"Replaced by app.vitals.frames.delay.value to align with the app.vitals.* namespace for mobile performance attributes"},aliases:["app.vitals.frames.delay.value"],changelog:[{version:"0.5.0",prs:[313],description:"Deprecated in favor of app.vitals.frames.delay.value"},{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"frames.frozen":{brief:"The number of frozen frames rendered during the lifetime of the span.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:3,deprecation:{replacement:"app.vitals.frames.frozen.count",reason:"Replaced by app.vitals.frames.frozen.count to align with the app.vitals.* namespace for mobile performance attributes"},aliases:["app.vitals.frames.frozen.count"],changelog:[{version:"0.5.0",prs:[313],description:"Deprecated in favor of app.vitals.frames.frozen.count"},{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},frames_frozen_rate:{brief:"The rate of frozen frames, or `app_vitals.frames.frozen.count` divided by `app_vitals.frames.total.count`. This is computed by Relay.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",changelog:[{version:"0.7.0",prs:[362],description:"Added frames_frozen_rate attribute"}]},"frames.slow":{brief:"The number of slow frames rendered during the lifetime of the span.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1,deprecation:{replacement:"app.vitals.frames.slow.count",reason:"Replaced by app.vitals.frames.slow.count to align with the app.vitals.* namespace for mobile performance attributes"},aliases:["app.vitals.frames.slow.count"],changelog:[{version:"0.5.0",prs:[313],description:"Deprecated in favor of app.vitals.frames.slow.count"},{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},frames_slow_rate:{brief:"The rate of slow frames, or `app_vitals.frames.slow.count` divided by `app_vitals.frames.total.count`. This is computed by Relay.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",changelog:[{version:"0.7.0",prs:[362],description:"Added frames_slow_rate attribute"}]},"frames.total":{brief:"The number of total frames rendered during the lifetime of the span.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:60,deprecation:{replacement:"app.vitals.frames.total.count",reason:"Replaced by app.vitals.frames.total.count to align with the app.vitals.* namespace for mobile performance attributes"},aliases:["app.vitals.frames.total.count"],changelog:[{version:"0.5.0",prs:[313],description:"Deprecated in favor of app.vitals.frames.total.count"},{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},fs_error:{brief:"The error message of a file system error.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"ENOENT: no such file or directory",deprecation:{replacement:"error.type",reason:"This attribute is not part of the OpenTelemetry specification and error.type fits much better."},changelog:[{version:"0.1.0",prs:[61,127]},{version:"0.0.0"}]},"gcp.function.context.event_id":{brief:"The event ID from the legacy GCP Cloud Function context (1st gen)",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"1234567890",changelog:[{version:"0.7.0",prs:[371],description:"Added gcp.function.context.event_id attribute"}]},"gcp.function.context.event_type":{brief:"The type of the GCP Cloud Function event",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"google.pubsub.topic.publish",changelog:[{version:"0.7.0",prs:[371],description:"Added gcp.function.context.event_type attribute"}]},"gcp.function.context.id":{brief:"The unique event ID from the GCP CloudEvents context (2nd gen Cloud Functions)",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"1234567890",changelog:[{version:"0.7.0",prs:[371],description:"Added gcp.function.context.id attribute"}]},"gcp.function.context.resource":{brief:"The resource that triggered the GCP Cloud Function event",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"projects/my-project/topics/my-topic",changelog:[{version:"0.7.0",prs:[371],description:"Added gcp.function.context.resource attribute"}]},"gcp.function.context.source":{brief:"The source of the GCP Cloud Function event",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"//pubsub.googleapis.com/projects/my-project/topics/my-topic",changelog:[{version:"0.7.0",prs:[371],description:"Added gcp.function.context.source attribute"}]},"gcp.function.context.specversion":{brief:"The CloudEvents specification version of the GCP Cloud Function event",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"1.0",changelog:[{version:"0.7.0",prs:[371],description:"Added gcp.function.context.specversion attribute"}]},"gcp.function.context.time":{brief:"The timestamp of the GCP Cloud Function event",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"2024-01-01T00:00:00.000Z",changelog:[{version:"0.7.0",prs:[371],description:"Added gcp.function.context.time attribute"}]},"gcp.function.context.timestamp":{brief:"The legacy timestamp of the GCP Cloud Function event",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"2024-01-01T00:00:00.000Z",changelog:[{version:"0.7.0",prs:[371],description:"Added gcp.function.context.timestamp attribute"}]},"gcp.function.context.type":{brief:"The type of the GCP Cloud Function event context",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"cloud_functions.context",changelog:[{version:"0.7.0",prs:[371],description:"Added gcp.function.context.type attribute"}]},"gcp.project.id":{brief:"The ID of the project in GCP that this resource is associated with",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"my-project-123",changelog:[{version:"0.11.0",prs:[403]}]},"gen_ai.agent.name":{brief:"The name of the agent being used.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"ResearchAssistant",changelog:[{version:"0.1.0",prs:[62,127]}]},"gen_ai.context.utilization":{brief:"The fraction of the model context window utilized by this generation.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:.75,changelog:[{version:"0.5.0",prs:[315],description:"Added gen_ai.context.utilization attribute"}]},"gen_ai.context.window_size":{brief:"The maximum context window size supported by the model for this generation.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:128e3,changelog:[{version:"0.5.0",prs:[315],description:"Added gen_ai.context.window_size attribute"}]},"gen_ai.conversation.id":{brief:"The unique identifier for a conversation (session, thread), used to store and correlate messages within this conversation.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"conv_5j66UpCpwteGg4YSxUnt7lPY",changelog:[{version:"0.4.0",prs:[250]}]},"gen_ai.cost.cache_creation.input_tokens":{brief:"The cost of input tokens written to cache in USD.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:12.34,changelog:[{version:"0.16.0",description:"Added gen_ai.cost.cache_creation.input_tokens attribute"}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to calculate total cost, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans.","Despite the name 'cost.cache_creation.input_tokens', this value is cost in USD, not a token count. For token counts, use gen_ai.usage.cache_creation.input_tokens.","This is a subset of gen_ai.cost.input_tokens, not an independent cost. Do not sum this with gen_ai.cost.input_tokens \u2014 it is already included."]},"gen_ai.cost.cache_read.input_tokens":{brief:"The cost of cached input tokens in USD.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:12.34,changelog:[{version:"0.16.0",description:"Added gen_ai.cost.cache_read.input_tokens attribute"}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to calculate total cost, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans.","Despite the name 'cost.cache_read.input_tokens', this value is cost in USD, not a token count. For token counts, use gen_ai.usage.cache_read.input_tokens.","This is a subset of gen_ai.cost.input_tokens, not an independent cost. Do not sum this with gen_ai.cost.input_tokens \u2014 it is already included."]},"gen_ai.cost.input_tokens":{brief:"The total cost of all input tokens in USD (includes cached and cache creation tokens).",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:123.45,changelog:[{version:"0.9.0",prs:[397],description:"Add additional_context"},{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[112]}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to calculate total cost, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans.","Despite the name 'cost.input_tokens', this value is cost in USD, not a token count. For token counts, use gen_ai.usage.input_tokens.","This is the total cost of all input tokens, including cached and cache creation tokens at their respective rates. For the cached portion, see gen_ai.cost.cache_read.input_tokens. For the cache creation portion, see gen_ai.cost.cache_creation.input_tokens."]},"gen_ai.cost.output_tokens":{brief:"The total cost of all output tokens in USD (includes reasoning tokens).",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:123.45,changelog:[{version:"0.9.0",prs:[397],description:"Add additional_context"},{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[112]}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to calculate total cost, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans.","Despite the name 'cost.output_tokens', this value is cost in USD, not a token count. For token counts, use gen_ai.usage.output_tokens.","This is the total cost of all output tokens, including reasoning tokens at their respective rate. For the reasoning portion, see gen_ai.cost.reasoning.output_tokens."]},"gen_ai.cost.reasoning.output_tokens":{brief:"The cost of reasoning output tokens in USD.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:12.34,changelog:[{version:"0.16.0",description:"Added gen_ai.cost.reasoning.output_tokens attribute"}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to calculate total cost, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans.","Despite the name 'cost.reasoning.output_tokens', this value is cost in USD, not a token count. For token counts, use gen_ai.usage.reasoning.output_tokens.","This is a subset of gen_ai.cost.output_tokens, not an independent cost. Do not sum this with gen_ai.cost.output_tokens \u2014 it is already included."]},"gen_ai.cost.total_tokens":{brief:"The total cost for the tokens used.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:12.34,aliases:["ai.total_cost"],changelog:[{version:"0.9.0",prs:[397],description:"Add additional_context"},{version:"0.5.0",prs:[264]},{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[126]}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to calculate total cost, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans.","Despite the name 'cost.total_tokens', this value is cost in USD, not a token count. For token counts, use gen_ai.usage.total_tokens."]},"gen_ai.embeddings.input":{brief:"The input to the embeddings model.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"What's the weather in Paris?",changelog:[{version:"0.3.1",prs:[195]}]},"gen_ai.function_id":{brief:"Framework-specific tracing label for the execution of a function or other unit of execution in a generative AI system.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"my-awesome-function",changelog:[{version:"0.5.0",prs:[308],description:"Added gen_ai.function_id attribute"}]},"gen_ai.input.messages":{brief:'The messages passed to the model. It has to be a stringified version of an array of objects. The `role` attribute of each object must be `"user"`, `"assistant"`, `"tool"`, or `"system"`. For messages of the role `"tool"`, the `content` can be a string or an arbitrary object with information about the tool call. For other messages the `content` can be either a string or a list of objects in the format `{type: "text", text:"..."}`.',type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:'[{"role": "user", "parts": [{"type": "text", "content": "Weather in Paris?"}]}, {"role": "assistant", "parts": [{"type": "tool_call", "id": "call_VSPygqKTWdrhaFErNvMV18Yl", "name": "get_weather", "arguments": {"location": "Paris"}}]}, {"role": "tool", "parts": [{"type": "tool_call_response", "id": "call_VSPygqKTWdrhaFErNvMV18Yl", "result": "rainy, 57\xB0F"}]}]',aliases:["ai.texts"],changelog:[{version:"0.5.0",prs:[264]},{version:"0.4.0",prs:[221]}]},"gen_ai.operation.name":{brief:"The name of the operation being performed. It has the following list of well-known values: 'chat', 'create_agent', 'embeddings', 'execute_tool', 'generate_content', 'invoke_agent', 'text_completion'. If one of them applies, then that value MUST be used. Otherwise a custom value MAY be used.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"chat",changelog:[{version:"0.4.0",prs:[225]},{version:"0.1.0",prs:[62,127]}]},"gen_ai.operation.type":{brief:"The type of AI operation. Must be one of 'agent' (invoke_agent and create_agent spans), 'ai_client' (any LLM call), 'tool' (execute_tool spans), 'handoff' (handoff spans), 'other' (input and output processors, skill loading, guardrails etc.) . Added during ingestion based on span.op and gen_ai.operation.type. Used to filter and aggregate data in the UI",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"tool",changelog:[{version:"0.4.0",prs:[257]},{version:"0.1.0",prs:[113,127]}]},"gen_ai.output.messages":{brief:"The model's response messages. It has to be a stringified version of an array of message objects, which can include text responses and tool calls.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:'[{"role": "assistant", "parts": [{"type": "text", "content": "The weather in Paris is currently rainy with a temperature of 57\xB0F."}], "finish_reason": "stop"}]',changelog:[{version:"0.4.0",prs:[221]}]},"gen_ai.pipeline.name":{brief:"Name of the AI pipeline or chain being executed.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Autofix Pipeline",aliases:["ai.pipeline.name"],changelog:[{version:"0.1.0",prs:[76,127]}]},"gen_ai.prompt":{brief:"The input messages sent to the model",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:'[{"role": "user", "message": "hello"}]',deprecation:{reason:"Deprecated from OTEL, use gen_ai.input.messages with the new format instead."},changelog:[{version:"0.1.0",prs:[74,108,119]},{version:"0.0.0"}]},"gen_ai.prompt.name":{brief:"The name of the prompt that uniquely identifies it.",type:"string",applyScrubbing:{key:"manual",reason:"Prompt names may reveal user behavior patterns or sensitive operations"},isInOtel:!0,visibility:"public",example:"summarize_text",aliases:["mcp.prompt.name"],changelog:[{version:"0.12.0",prs:[420],description:"Added gen_ai.prompt.name attribute"}]},"gen_ai.provider.name":{brief:"The Generative AI provider as identified by the client or server instrumentation.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"openai",aliases:["ai.model.provider","gen_ai.system"],changelog:[{version:"0.4.0",prs:[253]}]},"gen_ai.request.available_tools":{brief:"The available tools for the model. It has to be a stringified version of an array of objects.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:'[{"name": "get_weather", "description": "Get the weather for a given location"}, {"name": "get_news", "description": "Get the news for a given topic"}]',deprecation:{replacement:"gen_ai.tool.definitions"},changelog:[{version:"0.4.0",prs:[221]},{version:"0.1.0",prs:[63,127]}]},"gen_ai.request.frequency_penalty":{brief:"Used to reduce repetitiveness of generated tokens. The higher the value, the stronger a penalty is applied to previously present tokens, proportional to how many times they have already appeared in the prompt or prior generation.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:.5,aliases:["ai.frequency_penalty"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[57]}]},"gen_ai.request.max_tokens":{brief:"The maximum number of tokens to generate in the response.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:2048,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[62]}]},"gen_ai.request.messages":{brief:'The messages passed to the model. It has to be a stringified version of an array of objects. The `role` attribute of each object must be `"user"`, `"assistant"`, `"tool"`, or `"system"`. For messages of the role `"tool"`, the `content` can be a string or an arbitrary object with information about the tool call. For other messages the `content` can be either a string or a list of objects in the format `{type: "text", text:"..."}`.',type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:'[{"role": "system", "content": "Generate a random number."}, {"role": "user", "content": [{"text": "Generate a random number between 0 and 10.", "type": "text"}]}, {"role": "tool", "content": {"toolCallId": "1", "toolName": "Weather", "output": "rainy"}}]',deprecation:{replacement:"gen_ai.input.messages"},aliases:["ai.input_messages"],changelog:[{version:"0.4.0",prs:[221]},{version:"0.1.0",prs:[63,74,108,119,122]}]},"gen_ai.request.model":{brief:"The model identifier being used for the request.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"gpt-4-turbo-preview",changelog:[{version:"0.1.0",prs:[62,127]}]},"gen_ai.request.presence_penalty":{brief:"Used to reduce repetitiveness of generated tokens. Similar to frequency_penalty, except that this penalty is applied equally to all tokens that have already appeared, regardless of their exact frequencies.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:.5,aliases:["ai.presence_penalty"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[57]}]},"gen_ai.request.reasoning_effort":{brief:"Constrains the effort on reasoning for reasoning models. Supported values vary by provider.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"high",changelog:[{version:"0.13.0",prs:[334],description:"Added gen_ai.request.reasoning_effort attribute"}]},"gen_ai.request.seed":{brief:"The seed, ideally models given the same seed and same other parameters will produce the exact same output.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"1234567890",aliases:["ai.seed"],changelog:[{version:"0.1.0",prs:[57,127]}]},"gen_ai.request.stop_sequences":{brief:"List of sequences that the model will use to stop generating further tokens.",type:"string[]",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:["forest","lived"],changelog:[{version:"0.16.0",prs:[482],description:"Added gen_ai.request.stop_sequences attribute"}]},"gen_ai.request.temperature":{brief:"For an AI model call, the temperature parameter. Temperature essentially means how random the output will be.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:.1,aliases:["ai.temperature"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[57]}]},"gen_ai.request.top_k":{brief:"Limits the model to only consider the K most likely next tokens, where K is an integer (e.g., top_k=20 means only the 20 highest probability tokens are considered).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:35,aliases:["ai.top_k"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[57]}]},"gen_ai.request.top_p":{brief:"Limits the model to only consider tokens whose cumulative probability mass adds up to p, where p is a float between 0 and 1 (e.g., top_p=0.7 means only tokens that sum up to 70% of the probability mass are considered).",type:"double",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:.7,aliases:["ai.top_p"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[57]}]},"gen_ai.response.finish_reasons":{brief:"The reason why the model stopped generating.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"COMPLETE",aliases:["ai.finish_reason"],changelog:[{version:"0.1.0",prs:[57,127]}]},"gen_ai.response.id":{brief:"Unique identifier for the completion.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"gen_123abc",aliases:["ai.generation_id"],changelog:[{version:"0.1.0",prs:[57,127]}]},"gen_ai.response.model":{brief:"The vendor-specific ID of the model used.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"gpt-4",aliases:["ai.model_id"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"gen_ai.response.streaming":{brief:"Whether or not the AI model call's response was streamed back asynchronously",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!0,aliases:["ai.streaming"],changelog:[{version:"0.1.0",prs:[76]}]},"gen_ai.response.text":{brief:"The model's response text messages. It has to be a stringified version of an array of response text messages.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:'["The weather in Paris is rainy and overcast, with temperatures around 57\xB0F", "The weather in London is sunny and warm, with temperatures around 65\xB0F"]',deprecation:{replacement:"gen_ai.output.messages"},changelog:[{version:"0.4.0",prs:[221]},{version:"0.1.0",prs:[63,74]}]},"gen_ai.response.time_to_first_chunk":{brief:"Time in seconds when the first response content chunk arrived in streaming responses.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:.6853435,aliases:["gen_ai.response.time_to_first_token"],changelog:[{version:"0.11.0",prs:[418],description:"Added gen_ai.response.time_to_first_chunk attribute"}]},"gen_ai.response.time_to_first_token":{brief:"Time in seconds when the first response content chunk arrived in streaming responses.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:.6853435,deprecation:{replacement:"gen_ai.response.time_to_first_chunk"},aliases:["gen_ai.response.time_to_first_chunk"],changelog:[{version:"0.11.0",prs:[418],description:"Deprecate in favor of gen_ai.response.time_to_first_chunk"},{version:"0.4.0",prs:[227]}]},"gen_ai.response.tokens_per_second":{brief:"The total output tokens per seconds throughput",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:12345.67,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[66]}]},"gen_ai.response.tool_calls":{brief:"The tool calls in the model's response. It has to be a stringified version of an array of objects.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:'[{"name": "get_weather", "arguments": {"location": "Paris"}}]',deprecation:{replacement:"gen_ai.output.messages"},changelog:[{version:"0.4.0",prs:[221]},{version:"0.1.0",prs:[63,74]}]},"gen_ai.system":{brief:"The provider of the model.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"openai",deprecation:{replacement:"gen_ai.provider.name"},aliases:["ai.model.provider","gen_ai.provider.name"],changelog:[{version:"0.4.0",prs:[253]},{version:"0.1.0",prs:[57,127]}]},"gen_ai.system_instructions":{brief:"The system instructions passed to the model.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"You are a helpful assistant",aliases:["ai.preamble"],changelog:[{version:"0.5.0",prs:[264]},{version:"0.4.0",prs:[221]}]},"gen_ai.system.message":{brief:"The system instructions passed to the model.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"You are a helpful assistant",deprecation:{replacement:"gen_ai.system_instructions"},changelog:[{version:"0.4.0",prs:[221]},{version:"0.1.0",prs:[62]}]},"gen_ai.tool.call.arguments":{brief:"The arguments of the tool call. It has to be a stringified version of the arguments to the tool.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:'{"location": "Paris"}',aliases:["gen_ai.tool.input"],changelog:[{version:"0.5.0",prs:[265]},{version:"0.4.0",prs:[221]}]},"gen_ai.tool.call.result":{brief:"The result of the tool call. It has to be a stringified version of the result of the tool.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"rainy, 57\xB0F",aliases:["gen_ai.tool.output","gen_ai.tool.message","mcp.tool.result.content"],changelog:[{version:"0.5.0",prs:[265]},{version:"0.4.0",prs:[221]}]},"gen_ai.tool.definitions":{brief:"The list of source system tool definitions available to the GenAI agent or model.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:'[{"type": "function", "name": "get_current_weather", "description": "Get the current weather in a given location", "parameters": {"type": "object", "properties": {"location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"}, "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}}, "required": ["location", "unit"]}}]',changelog:[{version:"0.4.0",prs:[221]}]},"gen_ai.tool.description":{brief:"The description of the tool being used.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"Searches the web for current information about a topic",changelog:[{version:"0.1.0",prs:[62,127]}]},"gen_ai.tool.input":{brief:"The input of the tool being used. It has to be a stringified version of the input to the tool.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:'{"location": "Paris"}',deprecation:{replacement:"gen_ai.tool.call.arguments"},aliases:["gen_ai.tool.call.arguments"],changelog:[{version:"0.5.0",prs:[265]},{version:"0.1.0",prs:[63,74]}]},"gen_ai.tool.message":{brief:"The response from a tool or function call passed to the model.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"rainy, 57\xB0F",deprecation:{replacement:"gen_ai.tool.call.result"},aliases:["gen_ai.tool.call.result","gen_ai.tool.output","mcp.tool.result.content"],changelog:[{version:"0.5.0",prs:[265]},{version:"0.1.0",prs:[62]}]},"gen_ai.tool.name":{brief:"Name of the tool utilized by the agent.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"Flights",aliases:["ai.function_call","mcp.tool.name"],changelog:[{version:"0.1.0",prs:[57,127]}]},"gen_ai.tool.output":{brief:"The output of the tool being used. It has to be a stringified version of the output of the tool.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"rainy, 57\xB0F",deprecation:{replacement:"gen_ai.tool.call.result"},aliases:["gen_ai.tool.call.result","gen_ai.tool.message","mcp.tool.result.content"],changelog:[{version:"0.5.0",prs:[265]},{version:"0.1.0",prs:[63,74]}]},"gen_ai.tool.type":{brief:"The type of tool being used.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"function",deprecation:{reason:"The gen_ai.tool.type attribute is deprecated and should no longer be set."},changelog:[{version:"0.1.0",prs:[62,127]}]},"gen_ai.usage.cache_creation.input_tokens":{brief:"The number of tokens written to the cache when processing the AI input (prompt).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:100,aliases:["gen_ai.usage.input_tokens.cache_write"],changelog:[{version:"0.11.0",prs:[418],description:"Added gen_ai.usage.cache_creation.input_tokens attribute"}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to count tokens, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans."]},"gen_ai.usage.cache_read.input_tokens":{brief:"The number of cached tokens used to process the AI input (prompt).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:50,aliases:["gen_ai.usage.input_tokens.cached"],changelog:[{version:"0.11.0",prs:[418],description:"Added gen_ai.usage.cache_read.input_tokens attribute"}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to count tokens, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans.","This is a subset of gen_ai.usage.input_tokens, not an independent count. Do not sum this with gen_ai.usage.input_tokens \u2014 it is already included."]},"gen_ai.usage.completion_tokens":{brief:"The number of tokens used in the GenAI response (completion).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:10,deprecation:{replacement:"gen_ai.usage.output_tokens"},aliases:["ai.completion_tokens.used","gen_ai.usage.output_tokens"],changelog:[{version:"0.9.0",prs:[397],description:"Add additional_context"},{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[61]},{version:"0.0.0"}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to count tokens, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans."]},"gen_ai.usage.input_tokens":{brief:"The number of tokens used to process the AI input (prompt) including cached input tokens.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:10,aliases:["ai.prompt_tokens.used","gen_ai.usage.prompt_tokens"],changelog:[{version:"0.11.0",prs:[418],description:"Update additional_context to reference gen_ai.usage.cache_read.input_tokens"},{version:"0.9.0",prs:[397],description:"Add additional_context"},{version:"0.5.0",prs:[261]},{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[112]},{version:"0.0.0"}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to count tokens, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans.","This count includes cached input tokens. gen_ai.usage.cache_read.input_tokens is a subset of this value, not an independent count \u2014 do not sum them together."]},"gen_ai.usage.input_tokens.cached":{brief:"The number of cached tokens used to process the AI input (prompt).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:50,deprecation:{replacement:"gen_ai.usage.cache_read.input_tokens"},aliases:["gen_ai.usage.cache_read.input_tokens"],changelog:[{version:"0.11.0",prs:[418],description:"Deprecate in favor of gen_ai.usage.cache_read.input_tokens"},{version:"0.9.0",prs:[397],description:"Add additional_context"},{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[62,112]}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to count tokens, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans.","This is a subset of gen_ai.usage.input_tokens, not an independent count. Do not sum this with gen_ai.usage.input_tokens \u2014 it is already included."]},"gen_ai.usage.input_tokens.cache_write":{brief:"The number of tokens written to the cache when processing the AI input (prompt).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:100,deprecation:{replacement:"gen_ai.usage.cache_creation.input_tokens"},aliases:["gen_ai.usage.cache_creation.input_tokens"],changelog:[{version:"0.11.0",prs:[418],description:"Deprecate in favor of gen_ai.usage.cache_creation.input_tokens"},{version:"0.9.0",prs:[397],description:"Add additional_context"},{version:"0.4.0",prs:[217,228]}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to count tokens, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans."]},"gen_ai.usage.output_tokens":{brief:"The number of tokens used for creating the AI output (including reasoning tokens).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:10,aliases:["ai.completion_tokens.used","gen_ai.usage.completion_tokens"],changelog:[{version:"0.11.0",prs:[418],description:"Update additional_context to reference gen_ai.usage.reasoning.output_tokens"},{version:"0.9.0",prs:[397],description:"Add additional_context"},{version:"0.5.0",prs:[261]},{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[112]},{version:"0.0.0"}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to count tokens, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans.","This count includes reasoning tokens. gen_ai.usage.reasoning.output_tokens is a subset of this value, not an independent count \u2014 do not sum them together."]},"gen_ai.usage.output_tokens.reasoning":{brief:"The number of tokens used for reasoning to create the AI output.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:75,deprecation:{replacement:"gen_ai.usage.reasoning.output_tokens"},aliases:["gen_ai.usage.reasoning.output_tokens"],changelog:[{version:"0.11.0",prs:[418],description:"Deprecate in favor of gen_ai.usage.reasoning.output_tokens"},{version:"0.9.0",prs:[397],description:"Add additional_context"},{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[62,112]}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to count tokens, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans.","This is a subset of gen_ai.usage.output_tokens, not an independent count. Do not sum this with gen_ai.usage.output_tokens \u2014 it is already included."]},"gen_ai.usage.prompt_tokens":{brief:"The number of tokens used in the GenAI input (prompt).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:20,deprecation:{replacement:"gen_ai.usage.input_tokens"},aliases:["ai.prompt_tokens.used","gen_ai.usage.input_tokens"],changelog:[{version:"0.9.0",prs:[397],description:"Add additional_context"},{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[61]},{version:"0.0.0"}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to count tokens, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans."]},"gen_ai.usage.reasoning.output_tokens":{brief:"The number of tokens used for reasoning to create the AI output.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:75,aliases:["gen_ai.usage.output_tokens.reasoning"],changelog:[{version:"0.11.0",prs:[418],description:"Added gen_ai.usage.reasoning.output_tokens attribute"}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to count tokens, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans.","This is a subset of gen_ai.usage.output_tokens, not an independent count. Do not sum this with gen_ai.usage.output_tokens \u2014 it is already included."]},"gen_ai.usage.total_tokens":{brief:"The total number of tokens used to process the prompt. (input tokens plus output todkens)",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:20,aliases:["ai.total_tokens.used"],changelog:[{version:"0.9.0",prs:[397],description:"Add additional_context"},{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[57]}],additionalContext:["This attribute appears on both agent parent spans (aggregated totals) and LLM child spans (per-call values). When using sum() to count tokens, filter to gen_ai.operation.type:ai_client to avoid double-counting hierarchical spans.","This is the sum of gen_ai.usage.input_tokens and gen_ai.usage.output_tokens. Do not sum this with either of them \u2014 they are already included."]},"graphql.document":{brief:"The GraphQL document being executed.",type:"string",applyScrubbing:{key:"auto",reason:"The document may contain sensitive information in arguments or variables. Instrumentation should redact sensitive information when possible."},isInOtel:!0,visibility:"public",example:"query findBookById { bookById(id: ?) { name } }",changelog:[{version:"0.7.0",description:"Adds the `graphql.document` attribute to track the GraphQL document being executed."}]},"graphql.operation.name":{brief:"The name of the operation being executed.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"findBookById",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"graphql.operation.type":{brief:"The type of the operation being executed.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"query",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},hardwareConcurrency:{brief:"The number of logical CPU cores available.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"14",deprecation:{replacement:"device.processor_count",reason:"Old namespace-less attribute, to be replaced with device.processor_count for span-first future"},aliases:["device.processor_count"],changelog:[{version:"0.5.0",prs:[281,300],description:"Added and deprecated attribute to document JS SDK's current behaviour"}]},"http.client_ip":{brief:"Client address - domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"example.com",deprecation:{replacement:"client.address"},aliases:["client.address"],changelog:[{version:"0.1.0",prs:[61,106,127]},{version:"0.0.0"}]},"http.decoded_response_content_length":{brief:"The decoded body size of the response (in bytes).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:456,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"http.flavor":{brief:"The actual version of the protocol used for network communication.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"1.1",deprecation:{replacement:"network.protocol.version"},aliases:["network.protocol.version","net.protocol.version"],changelog:[{version:"0.1.0",prs:[61,108,127]},{version:"0.0.0"}]},"http.fragment":{brief:"The fragments present in the URI. Note that this contains the leading # character, while the `url.fragment` attribute does not.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"#details",changelog:[{version:"0.0.0"}]},"http.host":{brief:"The domain name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"example.com",deprecation:{replacement:"server.address",reason:"Deprecated, use one of `server.address` or `client.address`, depending on the usage"},aliases:["server.address","client.address","http.server_name","net.host.name","server_name"],changelog:[{version:"0.1.0",prs:[61,108,127]},{version:"0.0.0"}]},"http.method":{brief:"The HTTP method used.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"GET",deprecation:{replacement:"http.request.method"},aliases:["http.request.method","http.request_method","method"],changelog:[{version:"0.1.0",prs:[61,127]},{version:"0.0.0"}]},"http.query":{brief:"The query string present in the URL. Note that this contains the leading ? character, while the `url.query` attribute does not.",type:"string",applyScrubbing:{key:"auto",reason:"Query string values can contain sensitive information. Clients should attempt to scrub parameters that might contain sensitive information."},isInOtel:!1,visibility:"public",example:"?foo=bar&bar=baz",changelog:[{version:"0.0.0"}]},"http.request.body.data":{brief:"HTTP request body data. Can be given as string or structural data of any format.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:'[{"role": "user", "message": "hello"}]',changelog:[{version:"0.6.0",prs:[336],description:"Added http.request.body.data attribute"}]},"http.request.connection_end":{brief:"The UNIX timestamp representing the time immediately after the browser finishes establishing the connection to the server to retrieve the resource. The timestamp value includes the time interval to establish the transport connection, as well as other time intervals such as TLS handshake and SOCKS authentication.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:173282955515e-2,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[134]},{version:"0.0.0"}]},"http.request.connect_start":{brief:"The UNIX timestamp representing the time immediately before the user agent starts establishing the connection to the server to retrieve the resource.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1732829555111e-3,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[134]},{version:"0.0.0"}]},"http.request.domain_lookup_end":{brief:"The UNIX timestamp representing the time immediately after the browser finishes the domain-name lookup for the resource.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1732829555201e-3,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[134]},{version:"0.0.0"}]},"http.request.domain_lookup_start":{brief:"The UNIX timestamp representing the time immediately before the browser starts the domain name lookup for the resource.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1732829555322e-3,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[134]},{version:"0.0.0"}]},"http.request.fetch_start":{brief:"The UNIX timestamp representing the time immediately before the browser starts to fetch the resource.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1732829555389e-3,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[134]},{version:"0.0.0"}]},"http.request.header.<key>":{brief:"HTTP request headers, <key> being the normalized HTTP Header name (lowercase), the value being the header values.",type:"string[]",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",hasDynamicSuffix:!0,example:"http.request.header.custom-header=['foo', 'bar']",changelog:[{version:"0.4.0",prs:[201,204]},{version:"0.1.0",prs:[103]}]},"http.request.method":{brief:"The HTTP method used.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"GET",aliases:["method","http.method","http.request_method"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"http.request_method":{brief:"The HTTP method used.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"GET",deprecation:{replacement:"http.request.method"},aliases:["method","http.method","http.request.method"],changelog:[{version:"0.6.0",prs:[343],description:"Added http.request_method attribute"}]},"http.request.redirect_end":{brief:"The UNIX timestamp representing the timestamp immediately after receiving the last byte of the response of the last redirect",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1732829558502e-3,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[130,134]}]},"http.request.redirect_start":{brief:"The UNIX timestamp representing the start time of the fetch which that initiates the redirect.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1732829555495e-3,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[134]},{version:"0.0.0"}]},"http.request.request_start":{brief:"The UNIX timestamp representing the time immediately before the browser starts requesting the resource from the server, cache, or local resource. If the transport connection fails and the browser retires the request, the value returned will be the start of the retry request.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:173282955551e-2,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[134]},{version:"0.0.0"}]},"http.request.resend_count":{brief:"The ordinal number of request resending attempt (for any reason, including redirects).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:2,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"http.request.response_end":{brief:"The UNIX timestamp representing the time immediately after the browser receives the last byte of the resource or immediately before the transport connection is closed, whichever comes first.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:173282955589e-2,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[134]},{version:"0.0.0"}]},"http.request.response_start":{brief:"The UNIX timestamp representing the time immediately before the browser starts requesting the resource from the server, cache, or local resource. If the transport connection fails and the browser retires the request, the value returned will be the start of the retry request.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:17328295557e-1,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[134]},{version:"0.0.0"}]},"http.request.same_origin":{brief:"Indicates that a URL has the same origin as the current page's origin in the browser.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!0,aliases:["url.same_origin"],changelog:[{version:"0.16.0",prs:[456],description:"Added http.request.same_origin attribute"}]},"http.request.secure_connection_start":{brief:"The UNIX timestamp representing the time immediately before the browser starts the handshake process to secure the current connection. If a secure connection is not used, the property returns zero.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:173282955573e-2,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[134]},{version:"0.0.0"}]},"http.request.time_to_first_byte":{brief:"The time in seconds from the browser's timeorigin to when the first byte of the request's response was received. See https://web.dev/articles/ttfb#measure-resource-requests",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1.032,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[131]}]},"http.request.worker_start":{brief:"The UNIX timestamp representing the timestamp immediately before dispatching the FetchEvent if a Service Worker thread is already running, or immediately before starting the Service Worker thread if it is not already running.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:173282955368e-2,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[130,134]}]},"http.response.body.size":{brief:"The encoded body size of the response (in bytes).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:123,aliases:["http.response_content_length","http.response.header.content-length"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[106]},{version:"0.0.0"}]},"http.response_content_length":{brief:"The encoded body size of the response (in bytes).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:123,deprecation:{replacement:"http.response.body.size"},aliases:["http.response.body.size","http.response.header.content-length"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[61,106]},{version:"0.0.0"}]},"http.response.header.content-length":{brief:"The size of the message body sent to the recipient (in bytes)",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"http.response.header.custom-header=['foo', 'bar']",aliases:["http.response_content_length","http.response.body.size"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"http.response.header.<key>":{brief:"HTTP response headers, <key> being the normalized HTTP Header name (lowercase), the value being the header values.",type:"string[]",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",hasDynamicSuffix:!0,example:"http.response.header.custom-header=['foo', 'bar']",changelog:[{version:"0.4.0",prs:[201,204]},{version:"0.1.0",prs:[103]}]},"http.response.size":{brief:"The transfer size of the response (in bytes).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:456,aliases:["http.response_transfer_size"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"http.response.status_code":{brief:"The status code of the HTTP response.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:404,aliases:["http.status_code"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"http.response_transfer_size":{brief:"The transfer size of the response (in bytes).",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:456,deprecation:{replacement:"http.response.size"},aliases:["http.response.size"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[61]},{version:"0.0.0"}]},"http.route":{brief:"The matched route, that is, the path template in the format used by the respective server framework.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"/users/:id",aliases:["url.template"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"http.scheme":{brief:"The URI scheme component identifying the used protocol.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"https",deprecation:{replacement:"url.scheme"},aliases:["url.scheme"],changelog:[{version:"0.1.0",prs:[61,127]},{version:"0.0.0"}]},"http.server_name":{brief:"The server domain name",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"example.com",deprecation:{replacement:"server.address"},aliases:["server.address","net.host.name","http.host","server_name"],changelog:[{version:"0.1.0",prs:[61,108,127]},{version:"0.0.0"}]},"http.server.request.time_in_queue":{brief:"The time in milliseconds the request spent in the server queue before processing began. Measured from the X-Request-Start header set by reverse proxies (e.g., Nginx, HAProxy, Heroku) to when the application started handling the request.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:50,changelog:[{version:"0.5.0",prs:[267]}]},"http.status_code":{brief:"The status code of the HTTP response.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:404,deprecation:{replacement:"http.response.status_code"},aliases:["http.response.status_code"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[61]},{version:"0.0.0"}]},"http.target":{brief:"The pathname and query string of the URL.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"/test?foo=bar#buzz",deprecation:{replacement:"url.path",reason:"This attribute is being deprecated in favor of url.path and url.query"},changelog:[{version:"0.1.0",prs:[61]},{version:"0.0.0"}]},"http.url":{brief:"The URL of the resource that was fetched.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"https://example.com/test?foo=bar#buzz",deprecation:{replacement:"url.full"},aliases:["url.full","url"],changelog:[{version:"0.1.0",prs:[61,108]},{version:"0.0.0"}]},"http.user_agent":{brief:"Value of the HTTP User-Agent header sent by the client.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",deprecation:{replacement:"user_agent.original"},aliases:["user_agent.original"],changelog:[{version:"0.1.0",prs:[61,127]},{version:"0.0.0"}]},id:{brief:"A unique identifier for the span.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"f47ac10b58cc4372a5670e02b2c3d479",changelog:[{version:"0.0.0"}]},inp:{brief:"The value of the recorded Interaction to Next Paint (INP) web vital",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:200,deprecation:{replacement:"browser.web_vital.inp.value",reason:"The INP web vital is now recorded as a browser.web_vital.inp.value attribute."},aliases:["browser.web_vital.inp.value"],changelog:[{version:"0.5.0",prs:[229],description:"Added and deprecated attribute to document JS SDK's current behaviour"}]},"jsonrpc.protocol.version":{brief:"The version of the JSON-RPC protocol used.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"2.0",changelog:[{version:"0.12.0",prs:[420],description:"Added jsonrpc.protocol.version attribute"}]},"jsonrpc.request.id":{brief:"The JSON-RPC request identifier. Unique within the session.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"1",aliases:["mcp.request.id"],changelog:[{version:"0.12.0",prs:[420],description:"Added jsonrpc.request.id attribute"}]},"jvm.gc.action":{brief:"Name of the garbage collector action.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"end of minor GC",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"jvm.gc.name":{brief:"Name of the garbage collector.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"G1 Young Generation",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"jvm.memory.pool.name":{brief:"Name of the memory pool.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"G1 Old Gen",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"jvm.memory.type":{brief:"Name of the memory pool.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"G1 Old Gen",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"jvm.thread.daemon":{brief:"Whether the thread is daemon or not.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:!0,changelog:[{version:"0.0.0"}]},"jvm.thread.state":{brief:"State of the thread.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"blocked",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"koa.name":{brief:"The name of the Koa middleware or matched route that handled the request.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"/users/:id",deprecation:{reason:"No single replacement. SDKs should use http.route for router layers and code.function.name for middleware layers instead."},changelog:[{version:"0.16.0",prs:[490],description:"Added koa.name attribute as deprecated"}]},"koa.type":{brief:"The type of the Koa layer that handled the request.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"router",changelog:[{version:"0.16.0",prs:[471],description:"Added koa.type attribute"}]},lcp:{brief:"The value of the recorded Largest Contentful Paint (LCP) web vital",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:2500,deprecation:{replacement:"browser.web_vital.lcp.value",reason:"The LCP web vital is now recorded as a browser.web_vital.lcp.value attribute."},aliases:["browser.web_vital.lcp.value"],changelog:[{version:"0.5.0",prs:[229],description:"Added and deprecated attribute to document JS SDK's current behaviour"}]},"lcp.element":{brief:"The dom element responsible for the largest contentful paint.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"img",deprecation:{replacement:"browser.web_vital.lcp.element",reason:"The LCP element is now recorded as a browser.web_vital.lcp.element attribute."},aliases:["browser.web_vital.lcp.element"],changelog:[{version:"0.5.0",prs:[233]},{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"lcp.id":{brief:"The id of the dom element responsible for the largest contentful paint.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"#hero",deprecation:{replacement:"browser.web_vital.lcp.id",reason:"The LCP id is now recorded as a browser.web_vital.lcp.id attribute."},aliases:["browser.web_vital.lcp.id"],changelog:[{version:"0.5.0",prs:[233]},{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"lcp.loadTime":{brief:"The time it took for the LCP element to be loaded",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1402,deprecation:{replacement:"browser.web_vital.lcp.load_time",reason:"The LCP load time is now recorded as a browser.web_vital.lcp.load_time attribute."},aliases:["browser.web_vital.lcp.load_time"],changelog:[{version:"0.5.0",prs:[233]}]},"lcp.renderTime":{brief:"The time it took for the LCP element to be rendered",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1685,deprecation:{replacement:"browser.web_vital.lcp.render_time",reason:"The LCP render time is now recorded as a browser.web_vital.lcp.render_time attribute."},aliases:["browser.web_vital.lcp.render_time"],changelog:[{version:"0.5.0",prs:[233]}]},"lcp.size":{brief:"The size of the largest contentful paint element.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1234,deprecation:{replacement:"browser.web_vital.lcp.size",reason:"The LCP size is now recorded as a browser.web_vital.lcp.size attribute."},aliases:["browser.web_vital.lcp.size"],changelog:[{version:"0.5.0",prs:[233]},{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"lcp.url":{brief:"The url of the dom element responsible for the largest contentful paint.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"https://example.com",deprecation:{replacement:"browser.web_vital.lcp.url",reason:"The LCP url is now recorded as a browser.web_vital.lcp.url attribute."},aliases:["browser.web_vital.lcp.url"],changelog:[{version:"0.5.0",prs:[233]},{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"logger.name":{brief:"The name of the logger that generated this event.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"myLogger",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"mcp.cancelled.reason":{brief:"Reason for the cancellation of an MCP operation.",type:"string",applyScrubbing:{key:"manual",reason:"Cancellation reasons may contain user-specific or sensitive information"},isInOtel:!1,visibility:"public",example:"User cancelled the request",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.cancelled.request_id":{brief:"Request ID of the cancelled MCP operation.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"123",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.client.name":{brief:"Name of the MCP client application.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"claude-desktop",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.client.title":{brief:"Display title of the MCP client application.",type:"string",applyScrubbing:{key:"manual",reason:"Client titles may reveal user-specific application configurations or custom setups"},isInOtel:!1,visibility:"public",example:"Claude Desktop",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.client.version":{brief:"Version of the MCP client application.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"1.0.0",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.lifecycle.phase":{brief:"Lifecycle phase indicator for MCP operations.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"initialization_complete",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.logging.data_type":{brief:"Data type of the logged message content.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"string",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.logging.level":{brief:"Log level for MCP logging operations.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"info",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.logging.logger":{brief:"Logger name for MCP logging operations.",type:"string",applyScrubbing:{key:"manual",reason:"Logger names may be user-defined and could contain sensitive information"},isInOtel:!1,visibility:"public",example:"mcp_server",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.logging.message":{brief:"Log message content from MCP logging operations.",type:"string",applyScrubbing:{key:"auto",reason:"Log messages can contain user data"},isInOtel:!1,visibility:"public",example:"Tool execution completed successfully",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.method.name":{brief:"The name of the MCP request or notification method being called.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"tools/call",changelog:[{version:"0.12.0",prs:[420],description:"Set is_in_otel=true, attribute exists in OTel MCP registry"},{version:"0.3.0",prs:[171]}]},"mcp.progress.current":{brief:"Current progress value of an MCP operation.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:50,changelog:[{version:"0.4.0",prs:[228]},{version:"0.3.0",prs:[171]}]},"mcp.progress.message":{brief:"Progress message describing the current state of an MCP operation.",type:"string",applyScrubbing:{key:"manual",reason:"Progress messages may contain user-specific or sensitive information"},isInOtel:!1,visibility:"public",example:"Processing 50 of 100 items",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.progress.percentage":{brief:"Calculated progress percentage of an MCP operation. Computed from current/total * 100.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:50,changelog:[{version:"0.4.0",prs:[228]},{version:"0.3.0",prs:[171]}]},"mcp.progress.token":{brief:"Token for tracking progress of an MCP operation.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"progress-token-123",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.progress.total":{brief:"Total progress target value of an MCP operation.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:100,changelog:[{version:"0.4.0",prs:[228]},{version:"0.3.0",prs:[171]}]},"mcp.prompt.name":{brief:"Name of the MCP prompt template being used.",type:"string",applyScrubbing:{key:"manual",reason:"Prompt names may reveal user behavior patterns or sensitive operations"},isInOtel:!1,visibility:"public",example:"summarize",deprecation:{replacement:"gen_ai.prompt.name",reason:"OTel uses gen_ai.prompt.name for MCP prompt names"},aliases:["gen_ai.prompt.name"],changelog:[{version:"0.12.0",prs:[420],description:"Deprecated in favor of gen_ai.prompt.name"},{version:"0.3.0",prs:[171]}]},"mcp.prompt.result.description":{brief:"Description of the prompt result.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"A summary of the requested information",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.prompt.result.message_content":{brief:"Content of the message in the prompt result. Used for single message results only.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"Please provide a summary of the document",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.prompt.result.message_count":{brief:"Number of messages in the prompt result.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:3,changelog:[{version:"0.4.0",prs:[228]},{version:"0.3.0",prs:[171]}]},"mcp.prompt.result.message_role":{brief:"Role of the message in the prompt result. Used for single message results only.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"user",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.protocol.ready":{brief:"Protocol readiness indicator for MCP session. Non-zero value indicates the protocol is ready.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1,changelog:[{version:"0.4.0",prs:[228]},{version:"0.3.0",prs:[171]}]},"mcp.protocol.version":{brief:"MCP protocol version used in the session.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"2024-11-05",changelog:[{version:"0.12.0",prs:[420],description:"Set is_in_otel=true, attribute exists in OTel MCP registry"},{version:"0.3.0",prs:[171]}]},"mcp.request.argument.<key>":{brief:"MCP request argument with dynamic key suffix. The <key> is replaced with the actual argument name. The value is a JSON-stringified representation of the argument value.",type:"string",applyScrubbing:{key:"auto",reason:"Arguments contain user input"},isInOtel:!1,visibility:"public",hasDynamicSuffix:!0,example:"mcp.request.argument.query='weather in Paris'",changelog:[{version:"0.3.0",prs:[176]}]},"mcp.request.argument.name":{brief:"Name argument from prompts/get MCP request.",type:"string",applyScrubbing:{key:"auto",reason:"Prompt names can contain user input"},isInOtel:!1,visibility:"public",example:"summarize",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.request.argument.uri":{brief:"URI argument from resources/read MCP request.",type:"string",applyScrubbing:{key:"auto",reason:"URIs can contain user file paths"},isInOtel:!1,visibility:"public",example:"file:///path/to/resource",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.request.id":{brief:"JSON-RPC request identifier for the MCP request. Unique within the MCP session.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"1",deprecation:{replacement:"jsonrpc.request.id",reason:"OTel models MCP as JSON-RPC, uses jsonrpc.request.id"},aliases:["jsonrpc.request.id"],changelog:[{version:"0.12.0",prs:[420],description:"Deprecated in favor of jsonrpc.request.id"},{version:"0.3.0",prs:[171]}]},"mcp.resource.protocol":{brief:"Protocol of the resource URI being accessed, extracted from the URI.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"file",deprecation:{replacement:"network.protocol.name",reason:"OTel uses the generic network.protocol.name attribute"},aliases:["network.protocol.name","net.protocol.name"],changelog:[{version:"0.12.0",prs:[420],description:"Deprecated in favor of network.protocol.name"},{version:"0.3.0",prs:[171]}]},"mcp.resource.uri":{brief:"The resource URI being accessed in an MCP operation.",type:"string",applyScrubbing:{key:"auto",reason:"URIs can contain sensitive file paths"},isInOtel:!0,visibility:"public",example:"file:///path/to/file.txt",changelog:[{version:"0.12.0",prs:[420],description:"Set is_in_otel=true, attribute exists in OTel MCP registry"},{version:"0.3.0",prs:[171]}]},"mcp.server.name":{brief:"Name of the MCP server application.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"sentry-mcp-server",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.server.title":{brief:"Display title of the MCP server application.",type:"string",applyScrubbing:{key:"manual",reason:"Server titles may reveal user-specific application configurations or custom setups"},isInOtel:!1,visibility:"public",example:"Sentry MCP Server",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.server.version":{brief:"Version of the MCP server application.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"0.1.0",changelog:[{version:"0.3.0",prs:[171]}]},"mcp.session.id":{brief:"Identifier for the MCP session.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"550e8400-e29b-41d4-a716-446655440000",changelog:[{version:"0.12.0",prs:[420],description:"Set is_in_otel=true, attribute exists in OTel MCP registry"},{version:"0.3.0",prs:[171]}]},"mcp.tool.name":{brief:"Name of the MCP tool being called.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"calculator",deprecation:{replacement:"gen_ai.tool.name",reason:"OTel uses gen_ai.tool.name for MCP tool names"},aliases:["gen_ai.tool.name","ai.function_call"],changelog:[{version:"0.12.0",prs:[420],description:"Deprecated in favor of gen_ai.tool.name"},{version:"0.3.0",prs:[171]}]},"mcp.tool.result.content":{brief:"The content of the tool result.",type:"string",applyScrubbing:{key:"auto",reason:"Tool results can contain user data"},isInOtel:!1,visibility:"public",example:'{"output": "rainy", "toolCallId": "1"}',deprecation:{replacement:"gen_ai.tool.call.result",reason:"OTel uses gen_ai.tool.call.result for MCP tool results"},aliases:["gen_ai.tool.call.result","gen_ai.tool.message","gen_ai.tool.output"],changelog:[{version:"0.12.0",prs:[420],description:"Deprecated in favor of gen_ai.tool.call.result"},{version:"0.3.0",prs:[171]},{version:"0.2.0",prs:[164]}]},"mcp.tool.result.content_count":{brief:"Number of content items in the tool result.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1,changelog:[{version:"0.4.0",prs:[228]},{version:"0.3.0",prs:[171]}]},"mcp.tool.result.is_error":{brief:"Whether a tool execution resulted in an error.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!1,deprecation:{replacement:"error.type",reason:"OTel uses error.type set to 'tool_error' when isError is true. Cannot be automatically backfilled due to type mismatch (boolean vs string)."},changelog:[{version:"0.12.0",prs:[420],description:"Deprecated in favor of error.type"},{version:"0.3.0",prs:[171]}]},"mcp.transport":{brief:"Transport method used for MCP communication.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"stdio",deprecation:{replacement:"network.transport",reason:"OTel uses the generic network.transport attribute"},aliases:["network.transport","net.transport"],changelog:[{version:"0.12.0",prs:[420],description:"Deprecated in favor of network.transport"},{version:"0.3.0",prs:[171]}]},"mdc.<key>":{brief:"Attributes from the Mapped Diagnostic Context (MDC) present at the moment the log record was created. The MDC is supported by all the most popular logging solutions in the Java ecosystem, and it's usually implemented as a thread-local map that stores context for e.g. a specific request.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",hasDynamicSuffix:!0,example:"mdc.some_key='some_value'",changelog:[{version:"0.3.0",prs:[176]}]},"messaging.batch.message_count":{brief:"The number of messages sent, received, or processed in the scope of the batching operation.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:10,changelog:[{version:"0.6.0",prs:[341],description:"Added messaging.batch.message_count attribute"}]},"messaging.destination":{brief:"The message destination name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"BestTopic",deprecation:{replacement:"messaging.destination.name",reason:"This attribute is being deprecated in favor of messaging.destination.name, which is the OTel-aligned replacement."},aliases:["messaging.destination.name"],changelog:[{version:"0.16.0",prs:[482],description:"Added messaging.destination attribute, deprecated in favor of messaging.destination.name"}]},"messaging.destination.connection":{brief:"The message destination connection.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"BestTopic",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"messaging.destination.name":{brief:"The message destination name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"BestTopic",aliases:["messaging.destination"],changelog:[{version:"0.16.0",prs:[482],description:"Added messaging.destination as an alias"},{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"messaging.message.body.size":{brief:"The size of the message body in bytes.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:839,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"messaging.message.conversation_id":{brief:'The conversation ID identifying the conversation to which the message belongs, represented as a string. Sometimes called "Correlation ID".',type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"MyConversationId",changelog:[{version:"0.16.0",prs:[468],description:"Added messaging.message.conversation_id attribute"}]},"messaging.message.envelope.size":{brief:"The size of the message body and metadata in bytes.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:1045,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"messaging.message.id":{brief:"A value used by the messaging system as an identifier for the message, represented as a string.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"f47ac10b58cc4372a5670e02b2c3d479",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"messaging.message.receive.latency":{brief:"The latency between when the message was published and received.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1732847252,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"messaging.message.retry.count":{brief:"The amount of attempts to send the message.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:2,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"messaging.operation.name":{brief:"The name of the messaging operation being performed",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"send",changelog:[{version:"0.11.0",prs:[392],description:"Added messaging.operation.name attribute"}]},"messaging.operation.type":{brief:"A string identifying the type of the messaging operation",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"create",changelog:[{version:"0.1.0",prs:[51,127]}]},"messaging.rabbitmq.destination.routing_key":{brief:"RabbitMQ message routing key.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"myKey",changelog:[{version:"0.16.0",prs:[468],description:"Added messaging.rabbitmq.destination.routing_key attribute"}]},"messaging.system":{brief:"The messaging system as identified by the client instrumentation.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"activemq",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},method:{brief:"The HTTP method used.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"GET",deprecation:{replacement:"http.request.method"},aliases:["http.request.method","http.request_method","http.method"],changelog:[{version:"0.1.0",prs:[61,127]},{version:"0.0.0"}]},"middleware.name":{brief:"The name of the middleware.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"AuthenticationMiddleware",changelog:[{version:"0.6.0",prs:[336],description:"Added middleware.name attribute"}]},"navigation.origin":{brief:"The origin of the navigation (usually client side router navigations). Should preferrably parameterized template (like url.template) or a URL path otherwise.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"/users/:id",aliases:["sentry.sveltekit.navigation.from"],changelog:[{version:"0.16.0",prs:[467],description:"Added navigation.origin attribute"}]},"navigation.route.id":{brief:"The identifier of the matched client-side route, as assigned by the routing framework (e.g., vue-router name, react-router id).",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"AboutView",changelog:[{version:"0.16.0",prs:[468],description:"Added navigation.route.id attribute"}]},"navigation.type":{brief:"The type of navigation done by a client-side router.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"router.push",aliases:["sentry.sveltekit.navigation.type"],changelog:[{version:"0.16.0",prs:[467],description:"Added new deprecated alias"},{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"nel.elapsed_time":{brief:"The elapsed number of milliseconds between the start of the resource fetch and when it was completed or aborted by the user agent.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:100,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[68]}]},"nel.phase":{brief:'If request failed, the phase of its network error. If request succeeded, "application".',type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"application",changelog:[{version:"0.1.0",prs:[68,127]}]},"nel.referrer":{brief:"request's referrer, as determined by the referrer policy associated with its client.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"https://example.com/foo?bar=baz",changelog:[{version:"0.1.0",prs:[68,127]}]},"nel.sampling_function":{brief:"The sampling function used to determine if the request should be sampled.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:.5,changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[68]}]},"nel.type":{brief:'If request failed, the type of its network error. If request succeeded, "ok".',type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"dns.unreachable",changelog:[{version:"0.1.0",prs:[68,127]}]},"network.connection.effective_type":{brief:"Specifies the effective type of the current connection (e.g. slow-2g, 2g, 3g, 4g).",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"4g",aliases:["effectiveConnectionType"],changelog:[{version:"0.5.0",prs:[279],description:"Added attribute network.connection.effective_type to be used instead of effectiveConnectionType"}]},"network.connection.rtt":{brief:"Specifies the estimated effective round-trip time of the current connection, in milliseconds.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:100,aliases:["connection.rtt"],changelog:[{version:"0.5.0",prs:[279],description:"Added attribute network.connection.rtt to be used instead of connection.rtt"}]},"network.connection.type":{brief:"Specifies the type of the current connection (e.g. wifi, ethernet, cellular , etc).",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"wifi",aliases:["device.connection_type","connectionType"],changelog:[{version:"0.5.0",prs:[279],description:"Added attribute network.connection.type to be used instead of connectionType"}]},"network.local.address":{brief:"Local address of the network connection - IP address or Unix domain socket name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"10.1.2.80",aliases:["net.host.ip","net.sock.host.addr"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"network.local.port":{brief:"Local port number of the network connection.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:65400,aliases:["net.sock.host.port"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"network.peer.address":{brief:"Peer address of the network connection - IP address or Unix domain socket name.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"10.1.2.80",aliases:["net.peer.ip","net.sock.peer.addr"],changelog:[{version:"0.1.0",prs:[108,127]},{version:"0.0.0"}]},"network.peer.port":{brief:"Peer port number of the network connection.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:65400,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"network.protocol.name":{brief:"OSI application layer or non-OSI equivalent.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"http",aliases:["net.protocol.name","mcp.resource.protocol"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"network.protocol.version":{brief:"The actual version of the protocol used for network communication.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"1.1",aliases:["http.flavor","net.protocol.version"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"network.transport":{brief:"OSI transport layer or inter-process communication method.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"tcp",aliases:["net.transport","mcp.transport"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"network.type":{brief:"OSI network layer or non-OSI equivalent.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"ipv4",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"net.host.ip":{brief:"Local address of the network connection - IP address or Unix domain socket name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"192.168.0.1",deprecation:{replacement:"network.local.address"},aliases:["network.local.address","net.sock.host.addr"],changelog:[{version:"0.1.0",prs:[61,108,127]},{version:"0.0.0"}]},"net.host.name":{brief:"Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"example.com",deprecation:{replacement:"server.address"},aliases:["server.address","http.server_name","http.host","server_name"],changelog:[{version:"0.1.0",prs:[61,108,127]},{version:"0.0.0"}]},"net.host.port":{brief:"Server port number.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:1337,deprecation:{replacement:"server.port"},aliases:["server.port"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[61]},{version:"0.0.0"}]},"net.peer.ip":{brief:"Peer address of the network connection - IP address or Unix domain socket name.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"192.168.0.1",deprecation:{replacement:"network.peer.address"},aliases:["network.peer.address","net.sock.peer.addr"],changelog:[{version:"0.1.0",prs:[61,108,127]},{version:"0.0.0"}]},"net.peer.name":{brief:"Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"example.com",deprecation:{replacement:"server.address",reason:"Deprecated, use server.address on client spans and client.address on server spans."},changelog:[{version:"0.1.0",prs:[61,127]},{version:"0.0.0"}]},"net.peer.port":{brief:"Peer port number.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:1337,deprecation:{replacement:"server.port",reason:"Deprecated, use server.port on client spans and client.port on server spans."},changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[61]},{version:"0.0.0"}]},"net.protocol.name":{brief:"OSI application layer or non-OSI equivalent.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"http",deprecation:{replacement:"network.protocol.name"},aliases:["network.protocol.name","mcp.resource.protocol"],changelog:[{version:"0.1.0",prs:[61,127]},{version:"0.0.0"}]},"net.protocol.version":{brief:"The actual version of the protocol used for network communication.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"1.1",deprecation:{replacement:"network.protocol.version"},aliases:["network.protocol.version","http.flavor"],changelog:[{version:"0.1.0",prs:[61,108,127]},{version:"0.0.0"}]},"net.sock.family":{brief:"OSI transport and network layer",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"inet",deprecation:{replacement:"network.transport",reason:"Deprecated, use network.transport and network.type."},changelog:[{version:"0.1.0",prs:[61,127]},{version:"0.0.0"}]},"net.sock.host.addr":{brief:"Local address of the network connection mapping to Unix domain socket name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"/var/my.sock",deprecation:{replacement:"network.local.address"},aliases:["network.local.address","net.host.ip"],changelog:[{version:"0.1.0",prs:[61,108,127]},{version:"0.0.0"}]},"net.sock.host.port":{brief:"Local port number of the network connection.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:8080,deprecation:{replacement:"network.local.port"},aliases:["network.local.port"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[61]},{version:"0.0.0"}]},"net.sock.peer.addr":{brief:"Peer address of the network connection - IP address",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"192.168.0.1",deprecation:{replacement:"network.peer.address"},aliases:["network.peer.address","net.peer.ip"],changelog:[{version:"0.1.0",prs:[61,108,127]},{version:"0.0.0"}]},"net.sock.peer.name":{brief:"Peer address of the network connection - Unix domain socket name",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"/var/my.sock",deprecation:{reason:"Deprecated from OTEL, no replacement at this time"},changelog:[{version:"0.1.0",prs:[61,119,127]},{version:"0.0.0"}]},"net.sock.peer.port":{brief:"Peer port number of the network connection.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:8080,deprecation:{replacement:"network.peer.port"},changelog:[{version:"0.4.0",prs:[228]},{version:"0.1.0",prs:[61]},{version:"0.0.0"}]},"net.transport":{brief:"OSI transport layer or inter-process communication method.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"tcp",deprecation:{replacement:"network.transport"},aliases:["network.transport","mcp.transport"],changelog:[{version:"0.1.0",prs:[61,127]},{version:"0.0.0"}]},"os.build":{brief:"The build ID of the operating system.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"1234567890",deprecation:{replacement:"os.build_id"},aliases:["os.build_id"],changelog:[{version:"0.5.0",prs:[301],description:"Added os.build attribute, deprecated in favor of os.build_id"}]},"os.build_id":{brief:"The build ID of the operating system.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"1234567890",aliases:["os.build"],changelog:[{version:"0.5.0",prs:[301],description:"Added os.build as alias"},{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"os.description":{brief:"Human readable (not intended to be parsed) OS version information, like e.g. reported by ver or lsb_release -a commands.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"Ubuntu 18.04.1 LTS",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"os.kernel_version":{brief:"An independent kernel version string. Typically the entire output of the `uname` syscall.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"20.2.0",changelog:[{version:"0.5.0",prs:[301],description:"Added os.kernel_version attribute"}]},"os.name":{brief:"Human readable operating system name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"Ubuntu",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"os.raw_description":{brief:"An unprocessed description string obtained by the operating system. For some well-known runtimes, Sentry will attempt to parse `name` and `version` from this string, if they are not explicitly given.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Ubuntu 22.04.4 LTS (Jammy Jellyfish)",changelog:[{version:"0.5.0",prs:[301],description:"Added os.raw_description attribute"}]},"os.rooted":{brief:"Whether the operating system has been jailbroken or rooted.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!0,changelog:[{version:"0.5.0",prs:[301],description:"Added os.rooted attribute"}]},"os.theme":{brief:"Whether the OS runs in dark mode or light mode.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"dark",changelog:[{version:"0.5.0",prs:[301],description:"Added os.theme attribute"}]},"os.type":{brief:"The operating system type.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"linux",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"os.version":{brief:"The version of the operating system.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"18.04.2",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"otel.kind":{brief:"The span kind (https://opentelemetry.io/docs/concepts/signals/traces/#span-kind). Deprecated, use `sentry.kind` instead.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"SERVER",deprecation:{replacement:"sentry.kind",reason:"Deprecated in favor of sentry.kind"},aliases:["sentry.kind"],changelog:[{version:"0.13.0",prs:[440],description:"Added otel.kind attribute"}]},"otel.scope.name":{brief:"The name of the instrumentation scope - (InstrumentationScope.Name in OTLP).",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"io.opentelemetry.contrib.mongodb",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"otel.scope.version":{brief:"The version of the instrumentation scope - (InstrumentationScope.Version in OTLP).",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"2.4.5",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"otel.status_code":{brief:"Name of the code, either \u201COK\u201D or \u201CERROR\u201D. MUST NOT be set if the status code is UNSET.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"OK",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"otel.status_description":{brief:"Description of the Status if it has a value, otherwise not set.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"resource not found",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"params.<key>":{brief:"Decoded parameters extracted from a URL path. Usually added by client-side routing frameworks like vue-router.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",hasDynamicSuffix:!0,example:"params.id='123'",aliases:["url.path.parameter.<key>"],changelog:[{version:"0.1.0",prs:[103]}]},"performance.activationStart":{brief:"The time between initiating a navigation to a page and the browser activating the page",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1.983,deprecation:{replacement:"browser.performance.navigation.activation_start",reason:"The activationStart is now recorded as the browser.performance.navigation.activation_start attribute."},aliases:["browser.performance.navigation.activation_start"],changelog:[{version:"0.5.0",prs:[321],description:"Added performance.activationStart attribute"}]},"performance.timeOrigin":{brief:"The browser's performance.timeOrigin timestamp representing the time when the pageload was initiated",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1776185678886e-3,deprecation:{replacement:"browser.performance.time_origin",reason:"The timeOrigin is now recorded as the browser.performance.time_origin attribute."},aliases:["browser.performance.time_origin"],changelog:[{version:"0.5.0",prs:[321],description:"Added performance.timeOrigin attribute"}]},previous_route:{brief:"Also used by mobile SDKs to indicate the previous route in the application.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"HomeScreen",changelog:[{version:"0.1.0",prs:[74]},{version:"0.0.0"}]},"process.command_args":{brief:"All the command arguments (including the command/executable itself) as received by the process.",type:"string[]",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:["cmd/otecol","--config=config.yaml"],changelog:[{version:"0.6.0",prs:[327],description:"Added process.command_args attribute"}]},"process.executable.name":{brief:"The name of the executable that started the process.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"getsentry",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"process.pid":{brief:"The process ID of the running process.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:12345,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"process.runtime.description":{brief:"An additional description about the runtime of the process, for example a specific vendor customization of the runtime environment. Equivalent to `raw_description` in the Sentry runtime context.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"Eclipse OpenJ9 VM openj9-0.21.0",aliases:["runtime.raw_description"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"process.runtime.engine.name":{brief:"The name of the runtime engine.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"v8",changelog:[{version:"0.0.0"}]},"process.runtime.engine.version":{brief:"The version of the runtime engine.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"12.9.202.13-rusty",changelog:[{version:"0.0.0"}]},"process.runtime.name":{brief:"The name of the runtime. Equivalent to `name` in the Sentry runtime context.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"node",aliases:["runtime.name"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"process.runtime.version":{brief:"The version of the runtime of this process, as returned by the runtime without modification. Equivalent to `version` in the Sentry runtime context.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"18.04.2",aliases:["runtime.version"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"query.<key>":{brief:"An item in a query string. Usually added by client-side routing frameworks like vue-router.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",hasDynamicSuffix:!0,example:"query.id='123'",deprecation:{replacement:"url.query",reason:"Instead of sending items individually in query.<key>, they should be sent all together with url.query."},changelog:[{version:"0.1.0",prs:[103]}]},"react.version":{brief:"The version of the React framework",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"18.2.0",changelog:[{version:"0.7.0",prs:[368],description:"Added react.version attribute"}]},release:{brief:"The sentry release.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"production",deprecation:{replacement:"sentry.release"},aliases:["sentry.release"],changelog:[{version:"0.1.0",prs:[61,127]},{version:"0.0.0"}]},"remix.action_form_data.<key>":{brief:"Remix form data, <key> being the form data key, the value being the form data value.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",hasDynamicSuffix:!0,example:"http.response.header.text='test'",changelog:[{version:"0.1.0",prs:[103]}]},replay_id:{brief:"The id of the sentry replay.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"123e4567e89b12d3a456426614174000",deprecation:{replacement:"sentry.replay_id"},aliases:["sentry.replay_id"],changelog:[{version:"0.1.0",prs:[61]},{version:"0.0.0"}]},"resource.deployment.environment":{brief:"The software deployment environment name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"production",deprecation:{replacement:"sentry.environment"},changelog:[{version:"0.5.0",prs:[266]}]},"resource.deployment.environment.name":{brief:"The software deployment environment name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"production",deprecation:{replacement:"sentry.environment"},changelog:[{version:"0.3.1",prs:[196]}]},"resource.render_blocking_status":{brief:"The render blocking status of the resource.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"non-blocking",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},route:{brief:"The matched route, that is, the path template in the format used by the respective server framework. Also used by mobile SDKs to indicate the current route in the application.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"App\\Controller::indexAction",deprecation:{replacement:"http.route"},aliases:["http.route"],changelog:[{version:"0.1.0",prs:[61,74]},{version:"0.0.0"}]},"rpc.grpc.status_code":{brief:"The numeric status code of the gRPC request.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:2,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"rpc.method":{brief:"The fully-qualified logical name of the method from the RPC interface perspective.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"com.example.ExampleService/exampleMethod",changelog:[{version:"0.7.0",prs:[351],description:"Added rpc.method attribute"}]},"rpc.response.status_code":{brief:"Status code of the RPC returned by the RPC server or generated by the client.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"DEADLINE_EXCEEDED",changelog:[{version:"0.7.0",prs:[352],description:"Added rpc.response.status_code attribute"}]},"rpc.service":{brief:"The full (logical) name of the service being called, including its package name, if applicable.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"myService.BestService",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"rpc.system":{brief:"A string identifying the remoting system.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"aws-api",deprecation:{replacement:"rpc.system.name",reason:"This attribute is being deprecated in favor of rpc.system.name, which is the OTel-aligned replacement."},aliases:["rpc.system.name"],changelog:[{version:"0.16.0",prs:[482],description:"Added rpc.system attribute, deprecated in favor of rpc.system.name"}]},"rpc.system.name":{brief:"A string identifying the remoting system.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"aws-api",aliases:["rpc.system"],changelog:[{version:"0.16.0",prs:[482],description:"Added rpc.system.name attribute"}]},"runtime.build":{brief:"The application build string, when it is separate from the version.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"stable",deprecation:{reason:"The runtime.* namespace is deprecated in favor of process.runtime.*. No direct OTel equivalent exists for this attribute."},changelog:[{version:"0.11.0",prs:[383],description:"Added and deprecated runtime.build attribute"}]},"runtime.name":{brief:"The name of the runtime. For example node, CPython, or rustc.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"node",deprecation:{replacement:"process.runtime.name",reason:"Prefer OTel-aligned process.runtime.name"},aliases:["process.runtime.name"],changelog:[{version:"0.11.0",prs:[383],description:"Added and deprecated runtime.name attribute in favor of process.runtime.name"}]},"runtime.raw_description":{brief:"Unprocessed description string as obtained from the runtime. Used to extract name and version for well-known runtimes.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Eclipse OpenJ9 VM openj9-0.21.0",deprecation:{replacement:"process.runtime.description",reason:"Prefer OTel-aligned process.runtime.description"},aliases:["process.runtime.description"],changelog:[{version:"0.11.0",prs:[383],description:"Added and deprecated runtime.raw_description attribute in favor of process.runtime.description"}]},"runtime.version":{brief:"The version of the runtime.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"18.04.2",deprecation:{replacement:"process.runtime.version",reason:"Prefer OTel-aligned process.runtime.version"},aliases:["process.runtime.version"],changelog:[{version:"0.11.0",prs:[383],description:"Added and deprecated runtime.version attribute in favor of process.runtime.version"}]},"score.<key>":{brief:"The weighted performance score for a web vital. This is defined as `score.weight.<key>` * `score.ratio.<key>`.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",hasDynamicSuffix:!0,example:"score.cls=0.1723",changelog:[{version:"0.7.0",prs:[355],description:"Added score.<key> attribute"}]},"score.ratio.<key>":{brief:"The score for a web vital, normalized to a number between 0 and 1.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",hasDynamicSuffix:!0,example:"score.ratio.inp=0.7748",changelog:[{version:"0.7.0",prs:[355],description:"Added score.ratio.<key> attribute"}]},"score.total":{brief:"The total performance score of a span. This is the sum of individual weighted web vital scores (see `score.<key>`).",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",changelog:[{version:"0.7.0",prs:[355],description:"Added score.total attribute"}]},"score.weight.<key>":{brief:"The relative weight of a web vital in a span's performance score.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",hasDynamicSuffix:!0,example:"score.weight.fcp=0.25",changelog:[{version:"0.7.0",prs:[355],description:"Added score.weight.<key> attribute"}]},"sentry.action":{brief:"Used as a generic attribute representing the action depending on the type of span. For instance, this is the database query operation for DB spans, and the request method for HTTP spans.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"SELECT",changelog:[{version:"0.4.0",prs:[212]}]},"sentry.browser.name":{brief:"The name of the browser.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Chrome",deprecation:{replacement:"browser.name"},aliases:["browser.name"],changelog:[{version:"0.1.0",prs:[139]}]},"sentry.browser.version":{brief:"The version of the browser.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"120.0.6099.130",deprecation:{replacement:"browser.version"},aliases:["browser.version"],changelog:[{version:"0.1.0",prs:[139]}]},"sentry.cancellation_reason":{brief:"The reason why a span ended early.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"document.hidden",changelog:[{version:"0.0.0"}]},"sentry.category":{brief:"The high-level category of a span, derived from the span operation or span attributes. This categorizes spans by their general purpose (e.g., database, HTTP, UI). Known values include: 'ai', 'ai.pipeline', 'app', 'browser', 'cache', 'console', 'db', 'event', 'file', 'function.aws', 'function.azure', 'function.gcp', 'function.nextjs', 'function.remix', 'graphql', 'grpc', 'http', 'measure', 'middleware', 'navigation', 'pageload', 'queue', 'resource', 'rpc', 'serialize', 'subprocess', 'template', 'topic', 'ui', 'ui.angular', 'ui.ember', 'ui.react', 'ui.svelte', 'ui.vue', 'view', 'websocket'.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"db",changelog:[{version:"0.4.0",prs:[218]}]},"sentry.client_sample_rate":{brief:"Rate at which a span was sampled in the SDK.",type:"double",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:.5,changelog:[{version:"0.1.0",prs:[102]}]},"sentry.description":{brief:"The human-readable description of a span.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"index view query",changelog:[{version:"0.1.0",prs:[135]}]},"sentry.dist":{brief:"The sentry dist.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"1.0",aliases:["dist"],changelog:[{version:"0.16.0",prs:[489],description:"Added dist as an alias"},{version:"0.0.0"}]},"sentry.domain":{brief:"Used as a generic attribute representing the domain depending on the type of span. For instance, this is the collection/table name for database spans, and the server address for HTTP spans.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"example.com",changelog:[{version:"0.4.0",prs:[212]}]},"sentry.dsc.environment":{brief:"The environment from the dynamic sampling context.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"internal",example:"prod",changelog:[{version:"0.3.0",prs:[185]}]},"sentry.dsc.project_id":{brief:"The ID of the project where the trace originated (i.e. the project of the SDK that started the trace). Propagated through the dynamic sampling context and set by Relay during ingestion.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"internal",example:"12345",changelog:[{version:"0.7.0",prs:[358],description:"Add sentry.dsc.project_id as an attribute"}]},"sentry.dsc.public_key":{brief:"The public key from the dynamic sampling context.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"internal",example:"c51734c603c4430eb57cb0a5728a479d",changelog:[{version:"0.3.0",prs:[185]}]},"sentry.dsc.release":{brief:"The release identifier from the dynamic sampling context.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"internal",example:"frontend@e8211be71b214afab5b85de4b4c54be3714952bb",changelog:[{version:"0.3.0",prs:[185]}]},"sentry.dsc.sampled":{brief:"Whether the event was sampled according to the dynamic sampling context.",type:"boolean",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"internal",example:!0,changelog:[{version:"0.3.0",prs:[185]}]},"sentry.dsc.sample_rate":{brief:"The sample rate from the dynamic sampling context.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"internal",example:"1.0",changelog:[{version:"0.3.0",prs:[185]}]},"sentry.dsc.trace_id":{brief:"The trace ID from the dynamic sampling context.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"internal",example:"047372980460430cbc78d9779df33a46",changelog:[{version:"0.3.0",prs:[185]}]},"sentry.dsc.transaction":{brief:"The transaction name from the dynamic sampling context.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"internal",example:"/issues/errors-outages/",changelog:[{version:"0.3.0",prs:[185]}]},"sentry.environment":{brief:"The sentry environment.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"production",aliases:["environment"],changelog:[{version:"0.0.0"}]},"sentry.exclusive_time":{brief:"The exclusive time duration of the span in milliseconds.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1234,changelog:[{version:"0.4.0",prs:[228]},{version:"0.3.0",prs:[160]},{version:"0.0.0"}]},"sentry.graphql.operation":{brief:"Indicates the type of graphql operation, emitted by the Javascript SDK.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"getUserById",changelog:[{version:"0.3.1",prs:[190]}]},"sentry.group":{brief:"Stores the hash of `sentry.normalized_description`. This is primarily used for grouping spans in the product end.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",changelog:[{version:"0.4.0",prs:[212]}]},"sentry.http.prefetch":{brief:"If an http request was a prefetch request.",type:"boolean",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:!0,changelog:[{version:"0.0.0"}]},"sentry.idle_span_finish_reason":{brief:"The reason why an idle span ended early.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"idleTimeout",changelog:[{version:"0.0.0"}]},"sentry.is_remote":{brief:"Indicates whether a span's parent is remote.",type:"boolean",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:!0,changelog:[{version:"0.3.1",prs:[190]}]},"sentry.kind":{brief:"Used to clarify the relationship between parents and children, or to distinguish between spans, e.g. a `server` and `client` span with the same name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"server",aliases:["otel.kind"],changelog:[{version:"0.3.1",prs:[190]}]},"sentry.main_thread":{brief:"Whether the span or event occurred on the main thread. Computed by Relay and should not be set by SDKs.",type:"boolean",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:!0,changelog:[{version:"0.5.0"}]},"sentry.message.parameter.<key>":{brief:"A parameter used in the message template. <key> can either be the number that represent the parameter's position in the template string (sentry.message.parameter.0, sentry.message.parameter.1, etc) or the parameter's name (sentry.message.parameter.item_id, sentry.message.parameter.user_id, etc)",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"sentry.message.parameter.0='123'",changelog:[{version:"0.1.0",prs:[116]}]},"sentry.message.template":{brief:"The parameterized template string.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Hello, {name}!",changelog:[{version:"0.1.0",prs:[116]}]},"sentry.metric.source":{brief:"The provenance of a metric.  For example, this can be set to indicate if a metric was generated by Relay from a span.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"span",changelog:[{version:"0.16.0",prs:[476],description:"Added sentry.metric.source attribute"}]},"sentry.mobile":{brief:"Whether the application is using a mobile SDK. Computed by Relay and should not be set by SDKs.",type:"boolean",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:!0,changelog:[{version:"0.5.0"}]},"sentry.module.<key>":{brief:"A module that was loaded in the process. The key is the name of the module.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",hasDynamicSuffix:!0,example:"sentry.module.brianium/paratest='v7.7.0'",changelog:[{version:"0.1.0",prs:[103]}]},"sentry.nextjs.ssr.function.route":{brief:"A parameterized route for a function in Next.js that contributes to Server-Side Rendering. Should be present on spans that track such functions when the file location of the function is known.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"/posts/[id]/layout",changelog:[{version:"0.1.0",prs:[54,106]}]},"sentry.nextjs.ssr.function.type":{brief:"A descriptor for a for a function in Next.js that contributes to Server-Side Rendering. Should be present on spans that track such functions.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"generateMetadata",changelog:[{version:"0.1.0",prs:[54,106]}]},"sentry.normalized_db_query":{brief:"The normalized version of `db.query.text`.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"SELECT .. FROM sentry_project WHERE (project_id = %s)",changelog:[{version:"0.3.1",prs:[194]}]},"sentry.normalized_db_query.hash":{brief:"The hash of `sentry.normalized_db_query`.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",changelog:[{version:"0.4.0",prs:[200]}]},"sentry.normalized_description":{brief:"Used as a generic attribute representing the normalized `sentry.description`. This refers to the legacy use case of `sentry.description` where it holds relevant data depending on the type of span (e.g. database query, resource url, http request description, etc).",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"SELECT .. FROM sentry_project WHERE (project_id = %s)",changelog:[{version:"0.4.0",prs:[212]}]},"sentry.observed_timestamp_nanos":{brief:"The timestamp at which an envelope was received by Relay, in nanoseconds.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"1544712660300000000",changelog:[{version:"0.3.0",prs:[174]},{version:"0.2.0",prs:[137]}]},"sentry.op":{brief:"The operation of a span.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"http.client",changelog:[{version:"0.0.0"}]},"sentry.origin":{brief:"The origin of the instrumentation (e.g. span, log, etc.)",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"auto.http.otel.fastify",changelog:[{version:"0.1.0",prs:[68]},{version:"0.0.0"}]},"sentry.platform":{brief:"The sdk platform that generated the event.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"php",changelog:[{version:"0.0.0"}]},"sentry.profiler_id":{brief:"The id of the currently running profiler (continuous profiling)",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"18779b64dd35d1a538e7ce2dd2d3fad3",changelog:[{version:"0.4.0",prs:[242]}]},"sentry.profile_id":{brief:"The ID of the Sentry profile the span is associated with. This is only meaningful for transaction-based profiling.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"123e4567e89b12d3a456426614174000",changelog:[{version:"0.6.0",prs:[344],description:"Added sentry.profile_id attribute"}]},"sentry.release":{brief:"The sentry release.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"7.0.0",aliases:["service.version","release"],changelog:[{version:"0.0.0"}]},"sentry.replay_id":{brief:"The id of the sentry replay.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"123e4567e89b12d3a456426614174000",aliases:["replay_id"],changelog:[{version:"0.0.0"}]},"sentry.replay_is_buffering":{brief:"A sentinel attribute on log events indicating whether the current Session Replay is being buffered (onErrorSampleRate).",type:"boolean",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:!0,changelog:[{version:"0.3.0",prs:[185]}]},"sentry.report_event":{brief:"(Deprecated) The event that caused the SDK to report CLS or LCP (pagehide or navigation)",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"pagehide",deprecation:{reason:"The report event is now recorded as a browser.web_vital.lcp.report_event or browser.web_vital.cls.report_event attribute. No backfill required."},changelog:[{version:"0.5.0",prs:[320],description:"Added sentry.report_event attribute"}]},"sentry.sdk.integrations":{brief:"A list of names identifying enabled integrations. The list shouldhave all enabled integrations, including default integrations. Defaultintegrations are included because different SDK releases may contain differentdefault integrations.",type:"string[]",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:["InboundFilters","FunctionToString","BrowserApiErrors","Breadcrumbs"],changelog:[{version:"0.0.0",prs:[42]}]},"sentry.sdk.name":{brief:"The sentry sdk name.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"@sentry/react",changelog:[{version:"0.0.0"}]},"sentry.sdk.version":{brief:"The sentry sdk version.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"7.0.0",changelog:[{version:"0.0.0"}]},"sentry.segment.id":{brief:"The segment ID of a span",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"051581bf3cb55c13",aliases:["sentry.segment_id"],changelog:[{version:"0.1.0",prs:[107,124]}]},"sentry.segment_id":{brief:"The segment ID of a span",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"051581bf3cb55c13",deprecation:{replacement:"sentry.segment.id"},aliases:["sentry.segment.id"],changelog:[{version:"0.1.0",prs:[124]}]},"sentry.segment.name":{brief:"The segment name of a span",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"GET /user",aliases:["sentry.transaction","transaction"],changelog:[{version:"0.6.0",prs:[345],description:"Added sentry.transaction and transaction aliases"},{version:"0.1.0",prs:[104]}]},"sentry.server_sample_rate":{brief:"Rate at which a span was sampled in Relay.",type:"double",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:.5,changelog:[{version:"0.1.0",prs:[102]}]},"sentry.source":{brief:"The source of a span, also referred to as transaction source. Known values are:  `'custom'`, `'url'`, `'route'`, `'component'`, `'view'`, `'task'`. '`source`' describes a parametrized route, while `'url'` describes the full URL, potentially containing identifiers.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"route",deprecation:{replacement:"sentry.span.source",reason:"This attribute is being deprecated in favor of sentry.span.source"},changelog:[{version:"0.5.0"}]},"sentry.span.source":{brief:"The source of a span, also referred to as transaction source. Known values are:  `'custom'`, `'url'`, `'route'`, `'component'`, `'view'`, `'task'`. '`source`' describes a parametrized route, while `'url'` describes the full URL, potentially containing identifiers.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"route",changelog:[{version:"0.4.0",prs:[214]},{version:"0.0.0"}]},"sentry.status":{brief:`The span's status (either "ok" or "error"). Older SDKs may set this to a more specific error, but this behaviour is deprecated.`,type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"ok",changelog:[{version:"0.14.0",prs:[453]}]},"sentry.status_code":{brief:"The HTTP status code used in Sentry Insights. Typically set by Sentry during ingestion, rather than by clients.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:200,changelog:[{version:"0.4.0",prs:[223,228]}]},"sentry.status.message":{brief:"The from OTLP extracted status message.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"foobar",changelog:[{version:"0.3.1",prs:[190]}]},"sentry.sveltekit.navigation.from":{brief:"the navigation origin (sveltekit router)",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"/home",deprecation:{replacement:"navigation.origin",reason:"Use the more generic attribute instead"},aliases:["navigation.origin"],changelog:[{version:"0.16.0",prs:[467],description:"Added sentry.sveltekit.navigation.from attribute"}]},"sentry.sveltekit.navigation.to":{brief:"the navigation destination",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"/users/:id",deprecation:{reason:"the navigation destination is already covered by url.* attributes"},changelog:[{version:"0.16.0",prs:[467],description:"Added sentry.sveltekit.navigation.to attribute"}]},"sentry.sveltekit.navigation.type":{brief:"The type of navigation event emitted from the sveltekit client router",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"link",deprecation:{replacement:"navigation.type",reason:"Use the more generic attribute instead"},aliases:["navigation.type"],changelog:[{version:"0.16.0",prs:[467],description:"Added sentry.sveltekit.navigation.type attribute"}]},"sentry.thread.id":{brief:"Current \u201Cmanaged\u201D thread ID.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:56,deprecation:{replacement:"thread.id",reason:"This attribute is being deprecated in favor of the OTel-standard thread.id"},changelog:[{version:"0.13.0",prs:[451]}]},"sentry.timestamp.sequence":{brief:"A sequencing counter for deterministic ordering of logs or metrics when timestamps share the same integer millisecond. Starts at 0 on SDK initialization, increments by 1 for each captured item, and resets to 0 when the integer millisecond of the current item differs from the previous one.",type:"integer",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:0,changelog:[{version:"0.5.0",prs:[262]}]},"sentry.trace_lifecycle":{brief:"Indicates the chosen trace lifecycle mode of the SDK (stream or static)",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"stream",changelog:[{version:"0.13.0",prs:[442],description:"Added sentry.trace_lifecycle attribute"}]},"sentry.trace.parent_span_id":{brief:"The span id of the span that was active when the log was collected. This should not be set if there was no active span.",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"b0e6f15b45c36b12",deprecation:{},changelog:[{version:"0.5.0",prs:[287],description:"Deprecate `sentry.trace.parent_span_id`"},{version:"0.1.0",prs:[116]}]},"sentry.trace.status":{brief:`The segment's status (either "ok" or "error"). Older SDKs may set this to a more specific error, but this behaviour is deprecated.`,type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"ok",changelog:[{version:"0.14.0",prs:[453]}]},"sentry.transaction":{brief:"The sentry transaction (segment name).",type:"string",applyScrubbing:{key:"never"},isInOtel:!1,visibility:"public",example:"GET /",deprecation:{replacement:"sentry.segment.name",reason:"This attribute is being deprecated in favor of sentry.segment.name"},aliases:["sentry.segment.name","transaction"],changelog:[{version:"0.6.0",prs:[345],description:"Deprecated sentry.transaction in favor of sentry.segment.name"},{version:"0.0.0"}]},"sentry.user.email":{brief:"User email address.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",deprecation:{replacement:"user.email"},aliases:["user.email"],changelog:[{version:"0.10.0",prs:[406]}]},"sentry.user.geo.city":{brief:"Human readable city name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",deprecation:{replacement:"user.geo.city"},aliases:["user.geo.city"],changelog:[{version:"0.10.0",prs:[406]}]},"sentry.user.geo.country_code":{brief:"Two-letter country code (ISO 3166-1 alpha-2).",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",deprecation:{replacement:"user.geo.country_code"},aliases:["user.geo.country_code"],changelog:[{version:"0.10.0",prs:[406]}]},"sentry.user.geo.region":{brief:"Human readable region name or code.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",deprecation:{replacement:"user.geo.region"},aliases:["user.geo.region"],changelog:[{version:"0.10.0",prs:[406]}]},"sentry.user.geo.subdivision":{brief:"Human readable subdivision name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",deprecation:{replacement:"user.geo.subdivision"},aliases:["user.geo.subdivision"],changelog:[{version:"0.10.0",prs:[406]}]},"sentry.user.id":{brief:"Unique identifier of the user.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",deprecation:{replacement:"user.id"},aliases:["user.id"],changelog:[{version:"0.10.0",prs:[406]}]},"sentry.user.ip":{brief:"The IP address of the user.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",deprecation:{replacement:"user.ip_address"},aliases:["user.ip_address"],changelog:[{version:"0.10.0",prs:[406]}]},"sentry.user.username":{brief:"Short name or login/username of the user.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",deprecation:{replacement:"user.name"},aliases:["user.name"],changelog:[{version:"0.10.0",prs:[406]}]},"server.address":{brief:"Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"example.com",aliases:["http.server_name","net.host.name","http.host","server_name"],changelog:[{version:"0.1.0",prs:[108,127]},{version:"0.0.0"}]},server_name:{brief:"Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"example.com",deprecation:{replacement:"server.address",reason:"This attribute is being deprecated in favor of server.address, which is the OTel-aligned replacement."},aliases:["server.address","http.server_name","net.host.name","http.host"],changelog:[{version:"0.16.0",prs:[477],description:"Added server_name attribute, deprecated in favor of server.address"}]},"server.port":{brief:"Server port number.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:1337,aliases:["net.host.port"],changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"service.name":{brief:"Logical name of the service.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"omegastar",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"service.version":{brief:"The version string of the service API or implementation. The format is not defined by these conventions.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"5.0.0",aliases:["sentry.release"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"session.id":{brief:"A unique id identifying the active session at the time of setting this attribute",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"00112233-4455-6677-8899-aabbccddeeff",changelog:[{version:"0.11.0",prs:[412],description:"Added session.id attribute"}]},stall_percentage:{brief:"The fraction of time the app was stalled. Only applies to React Native. This is computed by Relay.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",changelog:[{version:"0.7.0",prs:[362],description:"Added stall_percentage attribute"}]},stall_total_time:{brief:"The combined duration of all stalls in milliseconds. Only applies to React Native. This is computed by Relay.",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",changelog:[{version:"0.7.0",prs:[362],description:"Added stall_total_time attribute"}]},"state.type":{brief:"The type of state management library",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"redux",changelog:[{version:"0.7.0",prs:[365],description:"Added state.type attribute"}]},"thread.id":{brief:"Current \u201Cmanaged\u201D thread ID.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:56,changelog:[{version:"0.0.0"}]},"thread.name":{brief:"Current thread name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"main",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"timber.tag":{brief:"The log tag provided by the timber logging framework.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"MyTag",changelog:[{version:"0.3.0",prs:[183]}]},time_to_full_display:{brief:"The duration of time to full display in milliseconds",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1234.56,deprecation:{replacement:"app.vitals.ttfd.value",reason:"Replaced by app.vitals.ttfd.value to align with the app.vitals.* namespace for mobile performance attributes"},aliases:["app.vitals.ttfd.value"],changelog:[{version:"0.5.0",prs:[313],description:"Added and deprecated in favor of app.vitals.ttfd.value"}]},time_to_initial_display:{brief:"The duration of time to initial display in milliseconds",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1234.56,deprecation:{replacement:"app.vitals.ttid.value",reason:"Replaced by app.vitals.ttid.value to align with the app.vitals.* namespace for mobile performance attributes"},aliases:["app.vitals.ttid.value"],changelog:[{version:"0.5.0",prs:[313],description:"Added and deprecated in favor of app.vitals.ttid.value"}]},transaction:{brief:"The sentry transaction (segment name).",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"GET /",deprecation:{replacement:"sentry.segment.name"},aliases:["sentry.segment.name","sentry.transaction"],changelog:[{version:"0.6.0",prs:[345],description:"Updated transaction deprecation replacement to sentry.segment.name"},{version:"0.1.0",prs:[61,127]},{version:"0.0.0"}]},"trpc.procedure_path":{brief:"The path of the tRPC procedure being called",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"user.getById",changelog:[{version:"0.7.0",prs:[370],description:"Added trpc.procedure_path attribute"}]},"trpc.procedure_type":{brief:"The type of the tRPC procedure",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"query",changelog:[{version:"0.7.0",prs:[370],description:"Added trpc.procedure_type attribute"}]},ttfb:{brief:"The value of the recorded Time To First Byte (TTFB) web vital in milliseconds",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:194,deprecation:{replacement:"browser.web_vital.ttfb.value",reason:"This attribute is being deprecated in favor of browser.web_vital.ttfb.value"},aliases:["browser.web_vital.ttfb.value"],changelog:[{version:"0.5.0",prs:[235]}]},"ttfb.requestTime":{brief:"The time it takes for the server to process the initial request and send the first byte of a response to the user's browser",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1554.5814,deprecation:{replacement:"browser.web_vital.ttfb.request_time",reason:"This attribute is being deprecated in favor of browser.web_vital.ttfb.request_time"},aliases:["browser.web_vital.ttfb.request_time"],changelog:[{version:"0.5.0",prs:[235]}]},type:{brief:"More granular type of the operation happening.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"fetch",changelog:[{version:"0.0.0"}]},"ui.component_name":{brief:"The name of the associated component.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"HomeButton",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"ui.contributes_to_ttfd":{brief:"Whether the span execution contributed to the TTFD (time to fully drawn) metric.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!0,changelog:[{version:"0.0.0"}]},"ui.contributes_to_ttid":{brief:"Whether the span execution contributed to the TTID (time to initial display) metric.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!0,changelog:[{version:"0.0.0"}]},"ui.element.height":{brief:"The height of the UI element (for Html in pixels)",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:256,changelog:[{version:"0.5.0",prs:[284],description:"Added ui.element.height attribute"}]},"ui.element.id":{brief:"The id of the UI element",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"btn-login",changelog:[{version:"0.5.0",prs:[284],description:"Added ui.element.id attribute"}]},"ui.element.identifier":{brief:"The identifier used to measure the UI element timing",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"heroImage",changelog:[{version:"0.5.0",prs:[284],description:"Added ui.element.identifier attribute"}]},"ui.element.load_time":{brief:"The loading time of a UI element (from time origin to finished loading)",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:998.2234,changelog:[{version:"0.5.0",prs:[284],description:"Added ui.element.load_time attribute"}]},"ui.element.paint_type":{brief:"The type of element paint. Can either be 'image-paint' or 'text-paint'",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"image-paint",changelog:[{version:"0.5.0",prs:[284],description:"Added ui.element.paint_type attribute"}]},"ui.element.render_time":{brief:"The rendering time of the UI element (from time origin to finished rendering)",type:"double",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1023.1124,changelog:[{version:"0.5.0",prs:[284],description:"Added ui.element.render_time attribute"}]},"ui.element.type":{brief:"type of the UI element",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"img",changelog:[{version:"0.5.0",prs:[284],description:"Added ui.element.type attribute"}]},"ui.element.url":{brief:"The URL of the UI element (e.g. an img src)",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"https://assets.myapp.com/hero.png",changelog:[{version:"0.5.0",prs:[284],description:"Added ui.element.url attribute"}]},"ui.element.width":{brief:"The width of the UI element (for HTML in pixels)",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:512,changelog:[{version:"0.5.0",prs:[284],description:"Added ui.element.width attribute"}]},url:{brief:"The URL of the resource that was fetched.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"https://example.com/test?foo=bar#buzz",deprecation:{replacement:"url.full"},aliases:["url.full","http.url"],changelog:[{version:"0.1.0",prs:[61]},{version:"0.0.0"}]},"url.domain":{brief:"Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"example.com",changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"url.fragment":{brief:"The fragments present in the URI. Note that this does not contain the leading # character, while the `http.fragment` attribute does.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"details",changelog:[{version:"0.0.0"}]},"url.full":{brief:"The URL of the resource that was fetched.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"https://example.com/test?foo=bar#buzz",aliases:["http.url","url"],changelog:[{version:"0.1.0",prs:[108]},{version:"0.0.0"}]},"url.path":{brief:"The URI path component.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"/foo",changelog:[{version:"0.0.0"}]},"url.path.parameter.<key>":{brief:"Decoded parameters extracted from a URL path. Usually added by client-side routing frameworks like vue-router.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",hasDynamicSuffix:!0,example:"url.path.parameter.id='123'",aliases:["params.<key>"],changelog:[{version:"0.1.0",prs:[103]}]},"url.port":{brief:"Server port number.",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:1337,changelog:[{version:"0.4.0",prs:[228]},{version:"0.0.0"}]},"url.query":{brief:"The query string present in the URL. Note that this does not contain the leading ? character, while the `http.query` attribute does.",type:"string",applyScrubbing:{key:"auto",reason:"Query string values can contain sensitive information. Clients should attempt to scrub parameters that might contain sensitive information."},isInOtel:!0,visibility:"public",example:"foo=bar&bar=baz",changelog:[{version:"0.0.0"}]},"url.same_origin":{brief:"Indicates that a URL has the same origin as the current page's origin in the browser.",type:"boolean",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:!0,deprecation:{replacement:"http.request.same_origin",reason:"This attribute is being deprecated in favor of http.request.same_origin."},aliases:["http.request.same_origin"],changelog:[{version:"0.16.0",prs:[456],description:"Added url.same_origin attribute, deprecated in favor of http.request.same_origin"}]},"url.scheme":{brief:"The URI scheme component identifying the used protocol.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"https",aliases:["http.scheme"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"url.template":{brief:"The low-cardinality template of an absolute path reference.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"/users/:id",aliases:["http.route"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"user_agent.original":{brief:"Value of the HTTP User-Agent header sent by the client.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!0,visibility:"public",example:"Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",aliases:["http.user_agent"],changelog:[{version:"0.1.0",prs:[127]},{version:"0.0.0"}]},"user.email":{brief:"User email address.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"test@example.com",aliases:["sentry.user.email"],changelog:[{version:"0.0.0"}]},"user.full_name":{brief:"User's full name.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"John Smith",changelog:[{version:"0.0.0"}]},"user.geo.city":{brief:"Human readable city name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Toronto",aliases:["sentry.user.geo.city"],changelog:[{version:"0.0.0"}]},"user.geo.country_code":{brief:"Two-letter country code (ISO 3166-1 alpha-2).",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"CA",aliases:["sentry.user.geo.country_code"],changelog:[{version:"0.0.0"}]},"user.geo.region":{brief:"Human readable region name or code.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Canada",aliases:["sentry.user.geo.region"],changelog:[{version:"0.0.0"}]},"user.geo.subdivision":{brief:"Human readable subdivision name.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"Ontario",aliases:["sentry.user.geo.subdivision"],changelog:[{version:"0.0.0"}]},"user.hash":{brief:"Unique user hash to correlate information for a user in anonymized form.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"8ae4c2993e0f4f3b8b2d1b1f3b5e8f4d",changelog:[{version:"0.0.0"}]},"user.id":{brief:"Unique identifier of the user.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"S-1-5-21-202424912787-2692429404-2351956786-1000",aliases:["sentry.user.id"],changelog:[{version:"0.0.0"}]},"user.ip_address":{brief:"The IP address of the user.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"192.168.1.1",aliases:["sentry.user.ip"],changelog:[{version:"0.1.0",prs:[75]}]},"user.name":{brief:"Short name or login/username of the user.",type:"string",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:"j.smith",aliases:["sentry.user.username"],changelog:[{version:"0.0.0"}]},"user.roles":{brief:"Array of user roles at the time of the event.",type:"string[]",applyScrubbing:{key:"auto"},isInOtel:!0,visibility:"public",example:["admin","editor"],changelog:[{version:"0.0.0"}]},"vercel.branch":{brief:"Git branch name for Vercel project",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"main",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.build_id":{brief:"Identifier for the Vercel build (only present on build logs)",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"bld_cotnkcr76",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.deployment_id":{brief:"Identifier for the Vercel deployment",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"dpl_233NRGRjVZX1caZrXWtz5g1TAksD",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.destination":{brief:"Origin of the external content in Vercel (only on external logs)",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"https://vitals.vercel-insights.com/v1",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.edge_type":{brief:"Type of edge runtime in Vercel",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"edge-function",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.entrypoint":{brief:"Entrypoint for the request in Vercel",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"api/index.js",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.execution_region":{brief:"Region where the request is executed",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"sfo1",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.id":{brief:"Unique identifier for the log entry in Vercel",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"1573817187330377061717300000",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.ja3_digest":{brief:"JA3 fingerprint digest of Vercel request",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"769,47-53-5-10-49161-49162-49171-49172-50-56-19-4,0-10-11,23-24-25,0",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.ja4_digest":{brief:"JA4 fingerprint digest",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"t13d1516h2_8daaf6152771_02713d6af862",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.log_type":{brief:"Vercel log output type",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"stdout",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.path":{brief:"Function or dynamic path of the request in Vercel.",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"/dynamic/[route].json",changelog:[{version:"0.6.0",prs:[349],description:"Added vercel.path attribute"}]},"vercel.project_id":{brief:"Identifier for the Vercel project",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"gdufoJxB6b9b1fEqr1jUtFkyavUU",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.project_name":{brief:"Name of the Vercel project",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"my-app",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.proxy.cache_id":{brief:"Original request ID when request is served from cache",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"pdx1::v8g4b-1744143786684-93dafbc0f70d",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.proxy.client_ip":{brief:"Client IP address",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"120.75.16.101",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.proxy.host":{brief:"Hostname of the request",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"test.vercel.app",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.proxy.lambda_region":{brief:"Region where lambda function executed",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"sfo1",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.proxy.method":{brief:"HTTP method of the request",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"GET",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.proxy.path":{brief:"Request path with query parameters",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"/dynamic/some-value.json?route=some-value",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.proxy.path_type":{brief:"How the request was served based on its path and project configuration",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"func",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.proxy.path_type_variant":{brief:"Variant of the path type",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"api",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.proxy.referer":{brief:"Referer of the request",type:"string",applyScrubbing:{key:"auto"},isInOtel:!1,visibility:"public",example:"*.vercel.app",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.proxy.region":{brief:"Region where the request is processed",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"sfo1",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.proxy.response_byte_size":{brief:"Size of the response in bytes",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1024,changelog:[{version:"0.4.0",prs:[228]},{version:"0.2.0",prs:[163]}]},"vercel.proxy.scheme":{brief:"Protocol of the request",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"https",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.proxy.status_code":{brief:"HTTP status code of the proxy request",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:200,changelog:[{version:"0.4.0",prs:[228]},{version:"0.2.0",prs:[163]}]},"vercel.proxy.timestamp":{brief:"Unix timestamp when the proxy request was made",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:1573817250172,changelog:[{version:"0.4.0",prs:[228]},{version:"0.2.0",prs:[163]}]},"vercel.proxy.user_agent":{brief:"User agent strings of the request",type:"string[]",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:["Mozilla/5.0..."],changelog:[{version:"0.2.0",prs:[163]}]},"vercel.proxy.vercel_cache":{brief:"Cache status sent to the browser",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"REVALIDATED",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.proxy.vercel_id":{brief:"Vercel-specific identifier",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"sfo1::abc123",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.proxy.waf_action":{brief:"Action taken by firewall rules",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"deny",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.proxy.waf_rule_id":{brief:"ID of the firewall rule that matched",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"rule_gAHz8jtSB1Gy",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.request_id":{brief:"Identifier of the Vercel request",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"643af4e3-975a-4cc7-9e7a-1eda11539d90",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.source":{brief:"Origin of the Vercel log (build, edge, lambda, static, external, or firewall)",type:"string",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:"build",changelog:[{version:"0.2.0",prs:[163]}]},"vercel.status_code":{brief:"HTTP status code of the request (-1 means no response returned and the lambda crashed)",type:"integer",applyScrubbing:{key:"manual"},isInOtel:!1,visibility:"public",example:200,changelog:[{version:"0.4.0",prs:[228]},{version:"0.2.0",prs:[163]}]}};
//# sourceMappingURL=attributes.mjs.map

;// ./node_modules/@sentry/browser/build/npm/esm/prod/integrations/httpcontext.js




const httpContextIntegration = defineIntegration(() => {
  return {
    name: "HttpContext",
    preprocessEvent(event) {
      if (!helpers_WINDOW.navigator && !helpers_WINDOW.location && !helpers_WINDOW.document) {
        return;
      }
      const reqData = getHttpRequestData();
      const headers = {
        ...reqData.headers,
        ...event.request?.headers
      };
      event.request = {
        ...reqData,
        ...event.request,
        headers
      };
    },
    processSegmentSpan(span) {
      const spanOp = span.attributes?.[SEMANTIC_ATTRIBUTE_SENTRY_OP];
      if (!helpers_WINDOW.navigator && !helpers_WINDOW.location && !helpers_WINDOW.document) {
        return;
      }
      const reqData = getHttpRequestData();
      safeSetSpanJSONAttributes(span, {
        // Coerce empty string to undefined so the helper's nullish check drops it,
        // rather than writing an empty `url.full` attribute onto the span.
        [Yu]: spanOp !== "http.client" ? reqData.url : void 0,
        "http.request.header.user_agent": reqData.headers["User-Agent"],
        "http.request.header.referer": reqData.headers["Referer"]
      });
    }
  };
});


//# sourceMappingURL=httpcontext.js.map

;// ./node_modules/@sentry/core/build/esm/utils/aggregate-errors.js


function applyAggregateErrorsToEvent(exceptionFromErrorImplementation, parser, key, limit, event, hint) {
  if (!event.exception?.values || !hint || !is_isError(hint.originalException)) {
    return;
  }
  const originalException = event.exception.values.length > 0 ? event.exception.values[event.exception.values.length - 1] : void 0;
  if (originalException) {
    event.exception.values = aggregateExceptionsFromError(
      exceptionFromErrorImplementation,
      parser,
      limit,
      hint.originalException,
      key,
      event.exception.values,
      originalException,
      0
    );
  }
}
function aggregateExceptionsFromError(exceptionFromErrorImplementation, parser, limit, error, key, prevExceptions, exception, exceptionId) {
  if (prevExceptions.length >= limit + 1) {
    return prevExceptions;
  }
  let newExceptions = [...prevExceptions];
  if (is_isError(error[key])) {
    applyExceptionGroupFieldsForParentException(exception, exceptionId, error);
    const newException = exceptionFromErrorImplementation(parser, error[key]);
    const newExceptionId = newExceptions.length;
    applyExceptionGroupFieldsForChildException(newException, key, newExceptionId, exceptionId);
    newExceptions = aggregateExceptionsFromError(
      exceptionFromErrorImplementation,
      parser,
      limit,
      error[key],
      key,
      [newException, ...newExceptions],
      newException,
      newExceptionId
    );
  }
  if (isExceptionGroup(error)) {
    error.errors.forEach((childError, i) => {
      if (is_isError(childError)) {
        applyExceptionGroupFieldsForParentException(exception, exceptionId, error);
        const newException = exceptionFromErrorImplementation(parser, childError);
        const newExceptionId = newExceptions.length;
        applyExceptionGroupFieldsForChildException(newException, `errors[${i}]`, newExceptionId, exceptionId);
        newExceptions = aggregateExceptionsFromError(
          exceptionFromErrorImplementation,
          parser,
          limit,
          childError,
          key,
          [newException, ...newExceptions],
          newException,
          newExceptionId
        );
      }
    });
  }
  return newExceptions;
}
function isExceptionGroup(error) {
  return Array.isArray(error.errors);
}
function applyExceptionGroupFieldsForParentException(exception, exceptionId, error) {
  exception.mechanism = {
    handled: true,
    type: "auto.core.linked_errors",
    ...isExceptionGroup(error) && { is_exception_group: true },
    ...exception.mechanism,
    exception_id: exceptionId
  };
}
function applyExceptionGroupFieldsForChildException(exception, source, exceptionId, parentId) {
  exception.mechanism = {
    handled: true,
    ...exception.mechanism,
    type: "chained",
    source,
    exception_id: exceptionId,
    parent_id: parentId
  };
}


//# sourceMappingURL=aggregate-errors.js.map

;// ./node_modules/@sentry/browser/build/npm/esm/prod/integrations/linkederrors.js



const DEFAULT_KEY = "cause";
const DEFAULT_LIMIT = 5;
const linkederrors_INTEGRATION_NAME = "LinkedErrors";
const _linkedErrorsIntegration = ((options = {}) => {
  const limit = options.limit || DEFAULT_LIMIT;
  const key = options.key || DEFAULT_KEY;
  return {
    name: linkederrors_INTEGRATION_NAME,
    preprocessEvent(event, hint, client) {
      const options2 = client.getOptions();
      applyAggregateErrorsToEvent(
        // This differs from the LinkedErrors integration in core by using a different exceptionFromError function
        eventbuilder_exceptionFromError,
        options2.stackParser,
        key,
        limit,
        event,
        hint
      );
    }
  };
});
const linkedErrorsIntegration = defineIntegration(_linkedErrorsIntegration);


//# sourceMappingURL=linkederrors.js.map

;// ./node_modules/@sentry/browser/build/npm/esm/prod/stack-parsers.js


const OPERA10_PRIORITY = 10;
const OPERA11_PRIORITY = 20;
const CHROME_PRIORITY = 30;
const WINJS_PRIORITY = 40;
const GECKO_PRIORITY = 50;
function createFrame(filename, func, lineno, colno) {
  const frame = {
    filename,
    function: func === "<anonymous>" ? UNKNOWN_FUNCTION : func,
    in_app: true
    // All browser frames are considered in_app
  };
  if (lineno !== void 0) {
    frame.lineno = lineno;
  }
  if (colno !== void 0) {
    frame.colno = colno;
  }
  return frame;
}
const chromeRegexNoFnName = /^\s*at (\S+?)(?::(\d+))(?::(\d+))\s*$/i;
const chromeRegex = /^\s*at (?:(.+?\)(?: \[.+\])?|.*?) ?\((?:address at )?)?(?:async )?((?:<anonymous>|[-a-z]+:|.*bundle|\/)?.*?)(?::(\d+))?(?::(\d+))?\)?\s*$/i;
const chromeEvalRegex = /\((\S*)(?::(\d+))(?::(\d+))\)/;
const chromeDataUriRegex = /at (.+?) ?\(data:(.+?),/;
const chromeStackParserFn = (line) => {
  const dataUriMatch = line.match(chromeDataUriRegex);
  if (dataUriMatch) {
    return {
      filename: `<data:${dataUriMatch[2]}>`,
      function: dataUriMatch[1]
    };
  }
  const noFnParts = chromeRegexNoFnName.exec(line);
  if (noFnParts) {
    const [, filename, line2, col] = noFnParts;
    return createFrame(filename, UNKNOWN_FUNCTION, +line2, +col);
  }
  const parts = chromeRegex.exec(line);
  if (parts) {
    const isEval = parts[2]?.indexOf("eval") === 0;
    if (isEval) {
      const subMatch = chromeEvalRegex.exec(parts[2]);
      if (subMatch) {
        parts[2] = subMatch[1];
        parts[3] = subMatch[2];
        parts[4] = subMatch[3];
      }
    }
    const [func, filename] = extractSafariExtensionDetails(parts[1] || UNKNOWN_FUNCTION, parts[2]);
    return createFrame(filename, func, parts[3] ? +parts[3] : void 0, parts[4] ? +parts[4] : void 0);
  }
  return;
};
const chromeStackLineParser = [CHROME_PRIORITY, chromeStackParserFn];
const geckoREgex = /^\s*(.*?)(?:\((.*?)\))?(?:^|@)?((?:[-a-z]+)?:\/.*?|\[native code\]|[^@]*(?:bundle|\d+\.js)|\/[\w\-. /=]+)(?::(\d+))?(?::(\d+))?\s*$/i;
const geckoEvalRegex = /(\S+) line (\d+)(?: > eval line \d+)* > eval/i;
const gecko = (line) => {
  const parts = geckoREgex.exec(line);
  if (parts) {
    const isEval = parts[3] && parts[3].indexOf(" > eval") > -1;
    if (isEval) {
      const subMatch = geckoEvalRegex.exec(parts[3]);
      if (subMatch) {
        parts[1] = parts[1] || "eval";
        parts[3] = subMatch[1];
        parts[4] = subMatch[2];
        parts[5] = "";
      }
    }
    let filename = parts[3];
    let func = parts[1] || UNKNOWN_FUNCTION;
    [func, filename] = extractSafariExtensionDetails(func, filename);
    return createFrame(filename, func, parts[4] ? +parts[4] : void 0, parts[5] ? +parts[5] : void 0);
  }
  return;
};
const geckoStackLineParser = [GECKO_PRIORITY, gecko];
const winjsRegex = /^\s*at (?:((?:\[object object\])?.+) )?\(?((?:[-a-z]+):.*?):(\d+)(?::(\d+))?\)?\s*$/i;
const winjs = (line) => {
  const parts = winjsRegex.exec(line);
  return parts ? createFrame(parts[2], parts[1] || UNKNOWN_FUNCTION, +parts[3], parts[4] ? +parts[4] : void 0) : void 0;
};
const winjsStackLineParser = [WINJS_PRIORITY, winjs];
const opera10Regex = / line (\d+).*script (?:in )?(\S+)(?:: in function (\S+))?$/i;
const opera10 = (line) => {
  const parts = opera10Regex.exec(line);
  return parts ? createFrame(parts[2], parts[3] || UNKNOWN_FUNCTION, +parts[1]) : void 0;
};
const opera10StackLineParser = [OPERA10_PRIORITY, opera10];
const opera11Regex = / line (\d+), column (\d+)\s*(?:in (?:<anonymous function: ([^>]+)>|([^)]+))\(.*\))? in (.*):\s*$/i;
const opera11 = (line) => {
  const parts = opera11Regex.exec(line);
  return parts ? createFrame(parts[5], parts[3] || parts[4] || UNKNOWN_FUNCTION, +parts[1], +parts[2]) : void 0;
};
const opera11StackLineParser = [OPERA11_PRIORITY, opera11];
const defaultStackLineParsers = [chromeStackLineParser, geckoStackLineParser];
const defaultStackParser = createStackParser(...defaultStackLineParsers);
const extractSafariExtensionDetails = (func, filename) => {
  const isSafariExtension = func.indexOf("safari-extension") !== -1;
  const isSafariWebExtension = func.indexOf("safari-web-extension") !== -1;
  return isSafariExtension || isSafariWebExtension ? [
    func.indexOf("@") !== -1 ? func.split("@")[0] : UNKNOWN_FUNCTION,
    isSafariExtension ? `safari-extension:${filename}` : `safari-web-extension:${filename}`
  ] : [func, filename];
};


//# sourceMappingURL=stack-parsers.js.map

;// ./node_modules/@sentry/browser-utils/build/esm/debug-build.js
const esm_debug_build_DEBUG_BUILD = (typeof __SENTRY_DEBUG__ === 'undefined' || __SENTRY_DEBUG__);


//# sourceMappingURL=debug-build.js.map

;// ./node_modules/@sentry/browser-utils/build/esm/getNativeImplementation.js




const cachedImplementations = {};
function getNativeImplementation(name) {
  const cached = cachedImplementations[name];
  if (cached) {
    return cached;
  }
  let impl = types_WINDOW[name];
  if (isNativeFunction(impl)) {
    return cachedImplementations[name] = impl.bind(types_WINDOW);
  }
  const document = types_WINDOW.document;
  if (document && typeof document.createElement === "function") {
    try {
      const sandbox = document.createElement("iframe");
      sandbox.hidden = true;
      document.head.appendChild(sandbox);
      const contentWindow = sandbox.contentWindow;
      if (contentWindow?.[name]) {
        impl = contentWindow[name];
      }
      document.head.removeChild(sandbox);
    } catch (e) {
      esm_debug_build_DEBUG_BUILD && debug_logger_debug.warn(`Could not create sandbox iframe for ${name} check, bailing to window.${name}: `, e);
    }
  }
  if (!impl) {
    return impl;
  }
  return cachedImplementations[name] = impl.bind(types_WINDOW);
}
function clearCachedImplementation(name) {
  cachedImplementations[name] = void 0;
}
function getNativeImplementation_fetch(...rest) {
  return getNativeImplementation("fetch")(...rest);
}
function getNativeImplementation_setTimeout(...rest) {
  return getNativeImplementation("setTimeout")(...rest);
}


//# sourceMappingURL=getNativeImplementation.js.map

;// ./node_modules/@sentry/browser/build/npm/esm/prod/transports/fetch.js



const DEFAULT_BROWSER_TRANSPORT_BUFFER_SIZE = 40;
function makeFetchTransport(options, nativeFetch = getNativeImplementation("fetch")) {
  let pendingBodySize = 0;
  let pendingCount = 0;
  async function makeRequest(request) {
    const requestSize = request.body.length;
    pendingBodySize += requestSize;
    pendingCount++;
    const requestOptions = {
      body: request.body,
      method: "POST",
      referrerPolicy: "strict-origin",
      headers: options.headers,
      // Outgoing requests are usually cancelled when navigating to a different page, causing a "TypeError: Failed to
      // fetch" error and sending a "network_error" client-outcome - in Chrome, the request status shows "(cancelled)".
      // The `keepalive` flag keeps outgoing requests alive, even when switching pages. We want this since we're
      // frequently sending events right before the user is switching pages (eg. when finishing navigation transactions).
      // Gotchas:
      // - `keepalive` isn't supported by Firefox
      // - As per spec (https://fetch.spec.whatwg.org/#http-network-or-cache-fetch):
      //   If the sum of contentLength and inflightKeepaliveBytes is greater than 64 kibibytes, then return a network error.
      //   We will therefore only activate the flag when we're below that limit.
      // There is also a limit of requests that can be open at the same time, so we also limit this to 15
      // See https://github.com/getsentry/sentry-javascript/pull/7553 for details
      keepalive: pendingBodySize <= 6e4 && pendingCount < 15,
      ...options.fetchOptions
    };
    try {
      const response = await nativeFetch(options.url, requestOptions);
      return {
        statusCode: response.status,
        headers: {
          "x-sentry-rate-limits": response.headers.get("X-Sentry-Rate-Limits"),
          "retry-after": response.headers.get("Retry-After")
        }
      };
    } catch (e) {
      clearCachedImplementation("fetch");
      throw e;
    } finally {
      pendingBodySize -= requestSize;
      pendingCount--;
    }
  }
  return createTransport(
    options,
    makeRequest,
    makePromiseBuffer(options.bufferSize || DEFAULT_BROWSER_TRANSPORT_BUFFER_SIZE)
  );
}


//# sourceMappingURL=fetch.js.map

;// ./node_modules/@sentry/browser-utils/build/esm/is.js
function is_isElement(wat) {
  if (typeof Element === "undefined") {
    return false;
  }
  try {
    return wat instanceof Element;
  } catch {
    return false;
  }
}


//# sourceMappingURL=is.js.map

;// ./node_modules/@sentry/browser/build/npm/esm/prod/normalizeStringifyValue.js


const HTML_ELEMENT_CONSTRUCTOR_NAME_REGEX = /^HTML(\w*)Element$/;
function normalizeStringifyValue(value) {
  if (typeof window !== "undefined" && value === window) {
    return "[Window]";
  }
  if (typeof document !== "undefined" && value === document) {
    return "[Document]";
  }
  if (is_isElement(value)) {
    const objName = normalizeStringifyValue_getConstructorName(value);
    if (HTML_ELEMENT_CONSTRUCTOR_NAME_REGEX.test(objName)) {
      return `[HTMLElement: ${htmlTreeAsString_htmlTreeAsString(value)}]`;
    }
  }
  return void 0;
}
function normalizeStringifyValue_getConstructorName(value) {
  const prototype = Object.getPrototypeOf(value);
  return prototype?.constructor ? prototype.constructor.name : "null prototype";
}


//# sourceMappingURL=normalizeStringifyValue.js.map

;// ./node_modules/@sentry/browser/build/npm/esm/prod/utils/detectBrowserExtension.js




function checkAndWarnIfIsEmbeddedBrowserExtension() {
  if (_isEmbeddedBrowserExtension()) {
    if (prod_debug_build_DEBUG_BUILD) {
      debug_logger_consoleSandbox(() => {
        console.error(
          "[Sentry] You cannot use Sentry.init() in a browser extension, see: https://docs.sentry.io/platforms/javascript/best-practices/browser-extensions/"
        );
      });
    }
    return true;
  }
  return false;
}
function _isEmbeddedBrowserExtension() {
  if (typeof helpers_WINDOW.window === "undefined") {
    return false;
  }
  const _window = helpers_WINDOW;
  if (_window.nw) {
    return false;
  }
  const extensionObject = _window["chrome"] || _window["browser"];
  if (!extensionObject?.runtime?.id) {
    return false;
  }
  const href = getLocationHref();
  const isDedicatedExtensionPage = helpers_WINDOW === helpers_WINDOW.top && /^(?:chrome-extension|moz-extension|ms-browser-extension|safari-web-extension):\/\//.test(href);
  return !isDedicatedExtensionPage;
}


//# sourceMappingURL=detectBrowserExtension.js.map

;// ./node_modules/@sentry/browser/build/npm/esm/prod/sdk.js














function getDefaultIntegrations(_options) {
  return [
    // TODO(v11): Replace with `eventFiltersIntegration` once we remove the deprecated `inboundFiltersIntegration`
    // eslint-disable-next-line typescript/no-deprecated
    inboundFiltersIntegration(),
    functionToStringIntegration(),
    conversationIdIntegration(),
    browserApiErrorsIntegration(),
    breadcrumbsIntegration(),
    globalHandlersIntegration(),
    linkedErrorsIntegration(),
    dedupeIntegration(),
    httpContextIntegration(),
    cultureContextIntegration(),
    browserSessionIntegration()
  ];
}
function init(options = {}) {
  const shouldDisableBecauseIsBrowserExtenstion = !options.skipBrowserExtensionCheck && checkAndWarnIfIsEmbeddedBrowserExtension();
  let defaultIntegrations = options.defaultIntegrations == null ? getDefaultIntegrations() : options.defaultIntegrations;
  const clientOptions = {
    ...options,
    enabled: shouldDisableBecauseIsBrowserExtenstion ? false : options.enabled,
    stackParser: stackParserFromStackParserOptions(options.stackParser || defaultStackParser),
    integrations: getIntegrationsToSetup({
      integrations: options.integrations,
      defaultIntegrations
    }),
    transport: options.transport || makeFetchTransport
  };
  setNormalizeStringifier(normalizeStringifyValue);
  return initAndBind(BrowserClient, clientOptions);
}
function forceLoad() {
}
function onLoad(callback) {
  callback();
}


//# sourceMappingURL=sdk.js.map

;// ./src/main.js









function sentryBeforeSend(event, hint) {
  let regExp = new RegExp("[a-z]+-extension\:\/\/[^\/]+\/", 'gi');
  event = replaceStringInObjectProperties(event, regExp, "extension://antitracker/");
  if (false) // removed by dead control flow
{}
  return event;
}
function initSentry() {
  init({
    dsn: 'https://fc16e67b5548432e9f9d7ffa71bb6846@o4504802466004992.ingest.sentry.io/4504995704537088',
    debug: "production" === 'development',
    environment: "production",
    release: "anti-tracker@1.6.0.44",
    beforeSend: sentryBeforeSend,
    //error reports only, like the previous SDK: no session pings on popup
    //open, no client reports, no page/request URLs in breadcrumbs
    sendClientReports: false,
    integrations: defaults => defaults.filter(integration => 'BrowserSession' !== integration.name).map(integration => 'Breadcrumbs' === integration.name ? breadcrumbsIntegration({
      console: false,
      fetch: false,
      xhr: false,
      history: false
    }) : integration)
  });
}

//error reports are declared in the manifest as optional data collection
//("technicalAndInteraction"): on Firefox 140+ the user can decline them at
//install time or in about:addons, so only start Sentry when granted.
//Browsers without the data_collection permission keep the previous behavior.
try {
  browser.permissions.contains({
    data_collection: ['technicalAndInteraction']
  }).then(granted => {
    if (granted) {
      initSentry();
    }
  }).catch(() => {
    initSentry();
  });
} catch (ex) {
  initSentry();
}

//Chrome imposes a limit of 800x600 for Extension popup windows
//https://ayastreb.me/chrome-extension-with-react/
//https://code.visualstudio.com/blogs/2016/02/23/introducing-chrome-debugger-for-vs-code
//https://developer.chrome.com/webstore/i18n

let startExtension = rulesMatchedDetails => {
  log.warn('[dnr] startExtension rulesMatchedDetails: ' + JSON.stringify(rulesMatchedDetails, null, 4));
  loadAndInitStoredState(storedState => {
    chrome.tabs.query({
      currentWindow: true,
      lastFocusedWindow: true,
      active: true
    }, tabs => {
      if (!tabs || !tabs.length) {
        return;
      }
      const [activeTab] = tabs;
      if (!activeTab) {
        return;
      }
      let homeElement = /*#__PURE__*/react.createElement(Home, {
        "rulesMatchedDetails": rulesMatchedDetails,
        "currentTab": activeTab,
        ...storedState
      });
      let container = document.getElementById('root');
      let root = (0,client/* createRoot */.H)(container);
      root.render(homeElement);
    });
  });
};
if (scripts_compat.dnr.available) {
  scripts_compat.dnr.declarativeNetRequest.getMatchedRules(null, rulesMatchedDetails => {
    startExtension(rulesMatchedDetails);
  });
} else {
  startExtension(null);
}
})();

/******/ })()
;