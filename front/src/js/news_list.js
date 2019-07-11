
function CmsNewsList() {

}


CmsNewsList.prototype.run = function () {
    this.initDatePicker()
};


CmsNewsList.prototype.initDatePicker = function(){
    var startPicker = $('#start-picker');
    var endPicker = $('#end-picker');

    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth()+1) + '/' + todayDate.getDate();
    var options = {
        // 显示底部按钮
        'showButtonPanel': true,
        // 选择后的时间格式
        'format': 'yyyy/mm/dd',
        // 开始时间
        'startDate': '2018/6/18',
        // 结束时间
        'endDate': todayStr,
        // 语言
        'language': 'zh-CN',
        // 是否显示今天按钮
        'todayBtn': 'linked',
        // 今天高亮
        'todayHighlight': true,
        // 清除按钮
        'clearBtn': true,
        // 自动关闭
        'autoclose': true
    };

    startPicker.datepicker(options);
    endPicker.datepicker(options);
};

$(function () {
   var cmsNewsList = new CmsNewsList();
   cmsNewsList.run();
});