

function Course() {
    
}

Course.prototype.listenStart = function(){


};


Course.prototype.initUEditor = function () {
    window.ue = UE.getEditor('editor',{
        // 编辑器高度
        'initialFrameHeight': 400,
        // 使用图片上传
        'serverUrl': '/ueditor/upload/'
    });
};

Course.prototype.run = function(){
    this.listenStart();
    this.initUEditor();
};


$(function () {
    var course = new Course();
    course.run();
});

