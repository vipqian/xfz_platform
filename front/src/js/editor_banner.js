function EditorBanner() {
    this.imageGroup = $('#banner-group')
}


EditorBanner.prototype.initBanner = function(){
    var self = this;
};


EditorBanner.prototype.listenQnUploadFileEvent = function () {
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

EditorBanner.prototype.updateUploadProgress = function (response) {
    // 上传过程中做的事情
    var total = response.total;
    var percent = total.percent;
    var progressGroup = EditorBanner.progressGroup;
    progressGroup.show();
    var progressBar = $('.progress-bar');
    var progressText = percent.toFixed(0) + '%';
    progressBar.css({'width': progressText});
    progressBar.text(progressText);

};


EditorBanner.prototype.uploadErrorEvent = function (error) {
    var progressGroup = EditorBanner.progressGroup;
    progressGroup.hide();
    if (error.message === 'file type doesn\'t match with what you specify'){
        window.messageBox.show('上传的文件不匹配');
    }

};

EditorBanner.prototype.complateUploadEvent = function (response) {
    var progressGroup = EditorBanner.progressGroup;
    progressGroup.hide();
    var progressBar = $('.progress-bar');
    progressBar.css({'width': 0});
    progressBar.text('0%');

    var imgUrl = 'http://ps9lpfh8q.bkt.clouddn.com/'+ response.key;
    var thumbnailFrom = $('#thumbnail-form');
    thumbnailFrom.val(imgUrl);
    var imageGroup = $('#banner-group');
    document.getElementById('banner-group').src = imgUrl;
    imageGroup.show();

};


EditorBanner.prototype.run = function(){
    this.initBanner();
    this.listenUploadFileEvent()
};




EditorBanner.prototype.listenSubBtn = function(){
    var subBtn = $('#sub-btn');
    subBtn.click(function (event) {
        event.preventDefault();
        var banner_id = subBtn.attr('data-banner-id');
        var image_url = $("input[name='image-url']").val();
        var priority = $("input[name='priority']").val();
        var link_to = $("input[name='link-to']").val();
        console.log(banner_id);

        xfzajax.post({
           'url': '/cms/edit_banner/',
            'data': {
               'banner_id': banner_id,
               'image_url': image_url,
                'priority': priority,
                'link_to': link_to
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    window.messageBox.show('编辑成功');
                    setTimeout(function () {
                        window.location.href="http://129.28.158.195:8000/cms/banners/";
                    }, 2000)
                } else {
                    window.messageBox.show(result['message']);
                }
            }
        });
    });
};

EditorBanner.prototype.listenUploadFileEvent = function () {
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
                    thumbnailFrom.val(url);
                    var imageGroup = $('#banner-group');
                    document.getElementById('banner-group').src = url;
                    imageGroup.show();
                }

            }
        })

    })
};

$(function () {
    var editorBanner = new EditorBanner();
    editorBanner.run();
    editorBanner.listenSubBtn();
    EditorBanner.progressGroup = $('#progress-group');
});