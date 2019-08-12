function EditorNews() {

}

EditorNews.prototype.run = function () {
    this.listenSumbitEvent();
    // this.listenQnUploadFileEvent();
    this.listenUploadFileEvent();
};


// 上传文件到七牛云
EditorNews.prototype.listenQnUploadFileEvent = function () {
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

EditorNews.prototype.updateUploadProgress = function (response) {
    // 上传过程中做的事情
    var self = this;
    var total = response.total;
    var percent = total.percent;
    var progressGroup = EditorNews.progressGroup;
    progressGroup.show();
    var progressBar = $('.progress-bar');
    var progressText = percent.toFixed(0) + '%';
    progressBar.css({'width': progressText});
    progressBar.text(progressText);

};

EditorNews.prototype.uploadErrorEvent = function (error) {
    var progressGroup = EditorNews.progressGroup;
    progressGroup.hide();
    if (error.message === 'file type doesn\'t match with what you specify'){
        window.messageBox.show('上传的文件不匹配');
    }

};

EditorNews.prototype.complateUploadEvent = function (response) {
    var progressGroup = EditorNews.progressGroup;
    progressGroup.hide();
    var progressBar = $('.progress-bar');
    progressBar.css({'width': 0});
    progressBar.text('0%');

    var imgUrl = 'http://ps9lpfh8q.bkt.clouddn.com/'+ response.key;
    var thumbnailFrom = $('#thumbnail-form');
    thumbnailFrom.val(imgUrl);
};

// 上传文件到自己的服务器
EditorNews.prototype.listenUploadFileEvent = function () {
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

EditorNews.prototype.listenSumbitEvent = function () {
    var subBtn = $('#sub-btn');
    subBtn.click(function (event) {
        event.preventDefault();
        var news_id = subBtn.attr('data-news-id');
        var title = $("input[name='title']").val();
        var desc = $("input[name='desc']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var category = $("select[name='category']").val();
        var author = $("input[name='author']").val();
        var content = window.ue.getContent();

        xfzajax.post({
            'url': '/cms/editor_news/',
            'data': {
                'news_id': news_id,
                'title': title,
                'desc': desc,
                'thumbnail':  thumbnail,
                'category': category,
                'content': content,
                'author': author
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    window.messageBox.show('编辑成功');

                    setTimeout(function(){window.location.href="http://127.0.0.1:8000/cms/newsList/";},3000)
                }
            }
        })
    });
};


$(function () {
    var editorNews = new EditorNews();
    editorNews.run();
    EditorNews.progressGroup = $('#progress-group');
});
