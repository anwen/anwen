var WxParse = require('../../wxParse/wxParse.js');
const app = getApp()

Page({
    data: {
        userInfo: {},
        hasUserInfo: false,
        canIUse: wx.canIUse('button.open-type.getUserInfo')
    },
    ramdonArticle: function(url) {
        if (typeof(url) !== 'string') {
            var url = 'https://anwensf.com/api/shares/random';
        }
        var that = this;
        // var url = 'http://localhost:8888/api/preview?url=https://www.ifanr.com/1080409'
        wx.request({
            url: url,
            success: function(res) {
                if (res.data.success === true) {
                    var data = res.data.data;
                    WxParse.wxParse('title', 'md', data.title, that);
                    WxParse.wxParse('content', 'md', data.markdown, that);
                    if (data.url) {
                        WxParse.wxParse('url', 'html', data.url, that);
                    } else {
                        WxParse.wxParse('url', 'html', '', that);
                    };
                    // WxParse.wxParse('content', 'html', res.data, that);
                }
            }
        })
    },
    onLoad: function(options) {
        var url = 'https://anwensf.com/api/shares/random';
        this.ramdonArticle(url);

        if (app.globalData.userInfo) {
            this.setData({
                userInfo: app.globalData.userInfo,
                hasUserInfo: true
            })
        }

    },

    onGotUserInfo: function(e) {
        var that = this;
        console.log(e.detail)
        // console.log(e.detail.rawData)
        console.log(e.detail.errMsg)
        console.log(e.detail.userInfo)
        if (e.detail.userInfo) {
            app.globalData.userInfo = e.detail.userInfo
            // update info to server
            var info = e.detail.userInfo
            if (e.detail.iv) {
                info.iv = e.detail.iv
                info.isignaturev = e.detail.signature
                info.encryptedData = e.detail.encryptedData
                console.log(info)
                console.log(app.globalData.token)

                // app.globalData.token
                // --------- 发送凭证 ------------------
                wx.request({
                    url: 'https://anwensf.com/api/me',
                    method: 'POST',
                    data: info,
                    header: {
                        'content-type': 'application/json', // 默认值
                        'Authorization': 'token ' + app.globalData.token
                    },
                    success: function(res) {
                        console.log(res.data);
                        app.globalData.userInfo = e.detail.userInfo
                        app.globalData.hasUserInfo = true
                        that.setData({
                            userInfo: e.detail.userInfo,
                            hasUserInfo: true
                        })


                    }
                })
                // ------------------------------------

            }

        }
    },

    wxParseTagATap: function(e) {
        var href = e.currentTarget.dataset.src;
        console.log(href);
        if (href.indexOf('anwensf.com') < 0) {
            var url = 'https://anwensf.com/api/preview?url=' + href;
            console.log(url);
            this.ramdonArticle(url);
            // wx.redirectTo({
            //     // url: '../index/index'
            //     url: '../article/article?url=https://anwensf.com/api/preview?url='+href
            // })
        }
    },

    onReady: function() {},
    onShow: function() {},
    onHide: function() {},
    onUnload: function() {}

})
