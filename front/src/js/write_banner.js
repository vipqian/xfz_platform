function Banner() {
    this.imageGroup = $('#banner-group')
}


Banner.prototype.initBanner = function(){
    var self = this;
    self.imageGroup.hide();
};


Banner.prototype.listenQnUploadFileEvent = function () {
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

Banner.prototype.updateUploadProgress = function (response) {
    // 上传过程中做的事情
    var self = this;
    var total = response.total;
    var percent = total.percent;
    var progressGroup = Banner.progressGroup;
    progressGroup.show();
    var progressBar = $('.progress-bar');
    var progressText = percent.toFixed(0) + '%';
    progressBar.css({'width': progressText});
    progressBar.text(progressText);

};


Banner.prototype.uploadErrorEvent = function (error) {
    var progressGroup = Banner.progressGroup;
    progressGroup.hide();
    if (error.message === 'file type doesn\'t match with what you specify'){
        window.messageBox.show('上传的文件不匹配');
    }

};

Banner.prototype.complateUploadEvent = function (response) {
    var progressGroup = Banner.progressGroup;
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


Banner.prototype.listenUploadFileEvent = function () {
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


Banner.prototype.run = function(){
    this.initBanner();
    // this.listenQnUploadFileEvent()
    this.listenUploadFileEvent();
};




Banner.prototype.listenSubBtn = function(){
    var subBtn = $('#sub-btn');
    subBtn.click(function (event) {
        event.preventDefault();
        var image_url = $("input[name='image-url']").val();
        var priority = $("input[name='priority']").val();
        var link_to = $("input[name='link-to']").val();

        xfzajax.post({
           'url': '/cms/write_banner/',
            'data': {
               'image_url': image_url,
                'priority': priority,
                'link_to': link_to
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    window.messageBox.show('发布成功');
                    setTimeout(function () {
                        // window.location.href="http://129.28.158.195:8000/cms/banners/";
                        window.location.href="http://127.0.0.0:8000/cms/banners/";
                    }, 2000)
                } else {
                    window.messageBox.show(result['message']);
                }
            }
        });
    });
};

$(function () {
    var banner = new Banner();
    banner.run();
    banner.listenSubBtn();
    Banner.progressGroup = $('#progress-group');
});