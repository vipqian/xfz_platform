

function CourseTab(){

}

CourseTab.prototype.run = function(){
    this.listenTableClick();
    this.initTable()
};


CourseTab.prototype.initTable = function(){
    var table = $('.nav-list');
    table.children('li').eq(0).addClass('active');
};

CourseTab.prototype.listenTableClick = function(){
     var table = $('.nav-list');
     table.children('li').eq(0).addClass('active');
    table.children('li').each(function (index, obj) {
        $(obj).click(function () {
            table.children('li').eq(index).addClass('active').siblings().removeClass('active');
        });
    })
};

$(function () {
    var courseIndex = new CourseTab();
    courseIndex.run();
});