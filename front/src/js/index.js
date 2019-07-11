
function Banner() {
    this.bannerWidth = 798;
    this.index = 1;

    this.bannerUl = $('#banner-ul');
    this.liList = this.bannerUl.children('li');
    this.bannerCount = this.liList.length;
    this.bannerGroup = $('#banner-group');
    this.rightArrow = $('.right-arrow');
    this.leftArrow = $('.left-arrow');
    this.pageControl = $('.page-control');


}


Banner.prototype.run = function(){

    this.initBanner();
    this.initPageControl();
    this.loop();

    this.listenBannerHover();
    this.listenArrowClick();
    this.listenPageControlClick();

};



// 初始化banner
Banner.prototype.initBanner = function(){
    var self = this;
    var firstbanner = self.liList.eq(0).clone();
    var lastbanner = self.liList.eq(self.bannerCount-1).clone();
    self.bannerUl.append(firstbanner);
    self.bannerUl.prepend(lastbanner);

    self.bannerUl.css({'width': self.bannerWidth*(self.bannerCount+2)});
    self.bannerUl.css({'left': -self.bannerWidth})

};

// 滑动banner
Banner.prototype.animates = function(){
    var self = this;
    var index = self.index;
    if (index === self.bannerCount+1){
        index = 0;
    }else if (index === 0){
        index = self.bannerCount - 1;
    } else {
        index = self.index - 1;
    }

    self.bannerUl.stop().animate({'left': -self.bannerWidth*self.index}, 500);
    self.pageControl.children('li').eq(index).addClass('active').siblings().removeClass('active')

};

//定时执行轮播
Banner.prototype.loop = function(){
    var self = this;
    this.items = setInterval(function () {
        if (self.index < self.bannerCount+1){
            self.index++;
        }else {
            self.bannerUl.css({'left': -self.bannerWidth});
            self.index = 2;

        }
        self.animates();


    }, 2000)
};

//鼠标移入监听
Banner.prototype.listenBannerHover = function(){
    var self = this;
    self.bannerGroup.hover(function () {
        self.toggleArrow(true);
        clearInterval(self.items)
    }, function () {
        self.toggleArrow(false);
        self.loop()
    })
};

// 是否显示箭头
Banner.prototype.toggleArrow = function(isShow){
    var self = this;
    if(isShow){
        self.rightArrow.show();
        self.leftArrow.show();
    }else {
        self.rightArrow.hide();
        self.leftArrow.hide();
    }
};

// 箭头点击事件
Banner.prototype.listenArrowClick = function(){
    var self = this;
    self.rightArrow.click(function () {
        if (self.index >= self.bannerCount){
            self.index = 1;
            self.bannerUl.css({'left': 0});
        }else {
            self.index++;
        }
        self.animates();
    });
    self.leftArrow.click(function () {
        if (self.index === 0){
            self.index = self.bannerCount-1;

            self.bannerUl.css({'left': -self.bannerCount*self.bannerWidth})
        }else {
            self.index--;
        };
        self.animates();
    });

};

// 自动生成小圆点
Banner.prototype.initPageControl = function(){
    var self = this;
    self.pageControl.css({'width': self.bannerCount*26});
    for (var i=0; i<self.bannerCount; i++){
        var circle = $('<li></li>');
        self.pageControl.append(circle);

        if (i === 0 ){
            circle.addClass('active')
        }
    }

};

// 小圆点点击事件
Banner.prototype.listenPageControlClick = function(){
    var self = this;
    self.pageControl.children('li').each(function (index, obj) {
        $(obj).click(function () {
            self.index = index + 1;
            self.animates()
        });
    });
};






// 细纹小导航条
function NewsTab(){

};

NewsTab.prototype.run = function(){
    this.listenTableClick();
    this.initTable()
};


NewsTab.prototype.initTable = function(){
    var table = $('.list-tab');
    table.children('li').eq(0).addClass('active');
};

NewsTab.prototype.listenTableClick = function(){
     var table = $('.list-tab');
     table.children('li').eq(0).addClass('active');
    table.children('li').each(function (index, obj) {
        $(obj).click(function () {
            table.children('li').eq(index).addClass('active').siblings().removeClass('active');
        });
    })
};




function Index(){
    this.page = 2;
    this.category_id = 0;

    this.loadBtn = $('#load-more-btn');

    template.defaults.imports.timeSince = function (dateValue) {
        var date = new Date(dateValue);
        var datets = date.getTime();
        var nowsts = (new Date()).getTime();
        var timestamp = (nowsts - datets) / 1000;
        if (timestamp < 60) {
            return '刚刚'
        }else if (timestamp >= 60 && timestamp < 60*60){
            minutes = parseInt(timestamp/60);
            return minutes+'分钟前'
        }else if (timestamp >= 60*60 && timestamp < 60*60*24) {
            hours = parseInt(timestamp / 60 / 60);
            return hours+'小时前'
        }else if (timestamp >= 60*60*24 && timestamp < 60*60*24*30) {
            days = parseInt(timestamp / 60 / 60 / 24);
            return days + '天前'
        }else{
            var year = date.getFullYear();
            var month = date.getMonth() + 1;
            var day = date.getDate();
            var hour = date.getHours();
            var min = date.getMinutes();
            if (month>0 && month < 10) {
                month = '0'+month
            }
            if (day>0 && day < 10) {
                day = '0'+day
            }
            if (hour>0 && hour < 10) {
                hour = '0'+hour
            }
            if (min>0 && min < 10) {
                min = '0'+min
            }
            return year + '/' + month + '/' + day + ' ' + hour + ':' + min
            }

    }
};



Index.prototype.loadMoreBtn = function(){
    var self =this;

    self.loadBtn.click(function () {
        xfzajax.get({
            'url': '/news/list/',
            'data': {
                'page': self.page,
                'category_id': self.category_id
            },
            'success':function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    if (data.length > 0){
                        var tpl = template('news-item', {'newses': data});
                        var ul = $('.list-inner-group');
                        ul.append(tpl);
                        self.page++;
                    } else {
                        self.loadBtn.hide();
                    }
                }
            }
        })
    });
};


Index.prototype.listenCategorySwitchEvent = function(){
    var self = this;
    var ul = $('.list-tab');
    ul.children().click(function () {
        var li = $(this);
        var category_id = li.attr('data-category');
        var page = 1;
        self.loadBtn.show();
        xfzajax.get({
            'url': '/news/list/',
            'data': {
                'page': page,
                'category_id': category_id
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var tpl = template('news-item', {'newses': data});
                    var ul = $('.list-inner-group');
                    ul.empty();
                    ul.append(tpl);
                    self.page = 2;
                    self.category_id = category_id
                }
            }
        });
    });

};

Index.prototype.run = function(){
    this.loadMoreBtn();
    this.listenCategorySwitchEvent();
};




$(function () {
   var banner = new Banner();
   var table = new NewsTab();
   var index = new Index();
   table.run();
   banner.run();
   index.run();
});