function EditorCourse() {

}

EditorCourse.prototype.run = function () {
    this.listenSumbitEvent();
    this.listenQnUploadFileEvent()
};


// 上传文件到七牛云
EditorCourse.prototype.listenQnUploadFileEvent = function () {
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

EditorCourse.prototype.updateUploadProgress = function (response) {
    // 上传过程中做的事情
    var self = this;
    var total = response.total;
    var percent = total.percent;
    var progressGroup = EditorCourse.progressGroup;
    progressGroup.show();
    var progressBar = $('.progress-bar');
    var progressText = percent.toFixed(0) + '%';
    progressBar.css({'width': progressText});
    progressBar.text(progressText);

};

EditorCourse.prototype.uploadErrorEvent = function (error) {
    var progressGroup = EditorCourse.progressGroup;
    progressGroup.hide();
    if (error.message === 'file type doesn\'t match with what you specify'){
        window.messageBox.show('上传的文件不匹配');
    }

};

EditorCourse.prototype.complateUploadEvent = function (response) {
    var progressGroup = EditorCourse.progressGroup;
    progressGroup.hide();
    var progressBar = $('.progress-bar');
    progressBar.css({'width': 0});
    progressBar.text('0%');

    var imgUrl = 'http://ps9lpfh8q.bkt.clouddn.com/'+ response.key;
    var thumbnailFrom = $('#thumbnail-form');
    thumbnailFrom.val(imgUrl);
};

EditorCourse.prototype.listenSumbitEvent = function () {
    var subBtn = $('#sub-btn');
    subBtn.click(function (event) {
        event.preventDefault();
        var course_id = subBtn.attr('data-course-id');
        var title = $("input[name='title']").val();
        var category = $("select[name='category']").val();
        var teacher = $("select[name='teacher']").val();
        var video_url = $("input[name='voideUrl']").val();
        var cover_url = $("input[name='coverUrl']").val();
        var price = $("input[name='price']").val();
        var duration = $("input[name='duration']").val();
        var profile = window.ue.getContent();


        xfzajax.post({
            'url': '/cms/editor_course/',
            'data': {
                'course_id': course_id,
                'title': title,
                'category': category,
                'teacher':  teacher,
                'video_url': video_url,
                'cover_url': cover_url,
                'price': price,
                'duration': duration,
                'profile': profile
            },

            'success': function (result) {
                if (result['code'] === 200) {
                    window.messageBox.show('编辑成功');

                    setTimeout(function(){window.location.href="http://129.28.158.195:8000/cms/course_list/";},3000)
                } else {
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


$(function () {
    var editorCourse = new EditorCourse();
    editorCourse.run();
    EditorCourse.progressGroup = $('#progress-group');
});
