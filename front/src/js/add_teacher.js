
function AddTeacher() {

}


AddTeacher.prototype.listenUploadFileEvent = function () {
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        var fromData = new FormData();
        fromData.append('file', file);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': fromData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200) {
                    url = result['data']['url'];
                   var thumbnailFrom = $('#thumbnail-form');
                   thumbnailFrom.val(url)
                }

            }
        })

    })
};

AddTeacher.prototype.initUEditor = function () {
    window.ue = UE.getEditor('editor',{
        // 编辑器高度
        'initialFrameHeight': 400,
        // 使用图片上传
        'serverUrl': '/ueditor/upload/'
    });
};

AddTeacher.prototype.listenQnUploadFileEvent = function () {
    var self = this;
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        xfzajax.get({
            'url': '/cms/qntoken',
            'success': function (result) {
                if (result['code'] === 200){
                    var token = result['data']['token'];
                    var key = (new Date().getTime()) + '.' + file.name.split('.')[1];
                    var putExtra = {
                        // 文件名
                        fname: key,
                        // 其他参数
                        params: {},
                        // 限制的文件类型
                        mimeType: ['image/png','video/x-ms-wmv','image/jpeg']
                    };
                    var config = {
                        // 是否加速
                        useCdnDomain: true,
                        // 失败后从新上传的次数
                        retryCount: 6,
                        // 七牛地区
                        region: qiniu.region.z2
                    };
                    var observable = qiniu.upload(file, key, token, putExtra,config);
                    observable.subscribe({
                        // 上传文件过程中告诉你上传多少
                        "next":self.updateUploadProgress,
                        // 上传文件出现错误
                        "error":self.uploadErrorEvent,
                        // 文件上传成功的回调函数
                        "complete": self.complateUploadEvent
                 });

                }
            }
        })
    })
};

AddTeacher.prototype.updateUploadProgress = function (response) {
    // 上传过程中做的事情
    var self = this;
    var total = response.total;
    var percent = total.percent;
    var progressGroup = AddTeacher.progressGroup;
    progressGroup.show();
    var progressBar = $('.progress-bar');
    var progressText = percent.toFixed(0) + '%';
    progressBar.css({'width': progressText});
    progressBar.text(progressText);

};

AddTeacher.prototype.uploadErrorEvent = function (error) {
    var progressGroup = AddTeacher.progressGroup;
    progressGroup.hide();
    if (error.message === 'file type doesn\'t match with what you specify'){
        window.messageBox.show('上传的文件不匹配');
    }

};

AddTeacher.prototype.complateUploadEvent = function (response) {
    var progressGroup = AddTeacher.progressGroup;
    progressGroup.hide();
    var progressBar = $('.progress-bar');
    progressBar.css({'width': 0});
    progressBar.text('0%');

    var imgUrl = 'http://ps9lpfh8q.bkt.clouddn.com/'+ response.key;
    var thumbnailFrom = $('#thumbnail-form');
    thumbnailFrom.val(imgUrl);
};

AddTeacher.prototype.listenSumbitEvent = function () {
    var subBtn = $('#sub-btn');
    subBtn.click(function (event) {
        event.preventDefault();
        var name = $("input[name='name']").val();
        var jobtitle = $("input[name='jobtitle']").val();
        var avatar = $("input[name='avatar']").val();
        var content = window.ue.getContent();

        console.log(name, jobtitle, avatar, content);

        xfzajax.post({
            'url': '/cms/add_teacher/',
            'data': {
                'name': name,
                'jobtitle': jobtitle,
                'avatar':  avatar,
                'profile': content,
            },
            'success': function (result) {
                console.log(result);
                if (result['code'] === 200) {
                    window.messageBox.show('发布成功');
                    setTimeout(function(){window.location.href="http://129.28.158.195:8000/cms/teacher_list/";},3000)
                }else {
                    var messageObject = result['message'];
                    //判断是不是字符串
                    if (typeof messageObject == "string" || messageObject.constructor == 'String') {
                        window.messageBox.show(result['message']);
                    } else {
                        for (var key in messageObject) {
                            var messages = messageObject[key];
                            var message = messages[0];
                            window.messageBox.show(message);
                        }
                    }
                }
            }
        })
    });
};



AddTeacher.prototype.run = function () {
    this.initUEditor();
    // this.listenQnUploadFileEvent();
    this.listenUploadFileEvent();
    this.listenSumbitEvent();
};


$(function () {
    var addTeacher = new AddTeacher();
    addTeacher.run();
    AddTeacher.progressGroup = $('#progress-group');
});
