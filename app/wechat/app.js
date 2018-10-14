App({
    globalData: {
        userInfo: null,
        hasLogin: false,
        token: null,
    },
    onLaunch: function() {
        console.log('App Launch')
        // 展示本地存储能力
        var logs = wx.getStorageSync('logs') || []
        logs.unshift(Date.now())
        wx.setStorageSync('logs', logs)
        // wx.login({
        //   success: res => {
        //     // 发送 res.code 到后台换取 openId, sessionKey, unionId
        //   }
        // })
        wx.login({
            success: function(res) {
                var code = res.code;
                if (code) {
                    console.log('获取用户登录凭证：' + code);
                    // --------- 发送凭证 ------------------
                    wx.request({
                        url: 'https://anwensf.com/api/wxlogin',
                        data: {
                            appname: 'anwen',
                            code: code
                        },
                        header: {
                            'content-type': 'application/json' // 默认值
                        },
                        success: function(res) {
                            console.log(res.data);
                            console.log(getApp().globalData);
                            getApp().globalData.token = res.data.token;
                        }
                    })
                    // ------------------------------------
                } else {
                    console.log('获取用户登录态失败：' + res.errMsg);
                }
            }
        });
        // 获取用户信息
        wx.getSetting({
            success: res => {
                if (res.authSetting['scope.userInfo']) {
                    // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
                    wx.getUserInfo({
                        success: res => {
                            // 可以将 res 发送给后台解码出 unionId
                            this.globalData.userInfo = res.userInfo
                            // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
                            // 所以此处加入 callback 以防止这种情况
                            if (this.userInfoReadyCallback) {
                                this.userInfoReadyCallback(res)
                            }
                        }
                    })
                }
            }
        })
    },
    onShow: function() {
        console.log('App Show')
    },
    onHide: function() {
        console.log('App Hide')
    },
});
