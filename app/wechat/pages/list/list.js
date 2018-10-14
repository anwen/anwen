// pages/list/list.js
const app = getApp()

var pageObject = {
  data:{
    list:[],
    hidden:false,
    page: 1,
    size: 20,
    hasMore:true,
    hasRefesh:false,

    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },


  onLoad:function(options){
    var that = this;
    var url = 'http://v.juhe.cn/weixin/query?key=f16af393a63364b729fd81ed9fdd4b7d&pno=1&ps=10';
          wx.request({
            url: url,
            success: function(res) {
              console.log(res.data);
              that.setData({
                 list:res.data.result.list,
                 hidden: true,
              });
            }
          })
  },
  //点击事件处理
  bindViewTap: function(e) {
    console.log(e.currentTarget.dataset.title);
  },
  onPullDownRefresh: function () {
    wx.showNavigationBarLoading() //在标题栏中显示加载
    console.log('refresh');
  },

  onReachBottom: function () {
    console.log('onReachBottom');
  },

  onReady: function () {
    console.log(app.globalData.hasUserInfo);
  },
  onShow: function () {
  },
  onHide: function () {
  },
  onUnload: function () {
  },

  onShareAppMessage: function () {
  }


}

Page(pageObject)
