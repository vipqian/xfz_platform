function CourseDetail() {
}

CourseDetail.prototype.initPlayer = function () {
    var videoInfoSpan = $("#video-info");
    var video_url = videoInfoSpan.attr("data-video-url");
    var cover_url = videoInfoSpan.attr("data-cover-url");
    var course_id = videoInfoSpan.attr('data-course-id');
    var price = videoInfoSpan.attr('data-course-price');

    console.log(video_url);
    console.log(cover_url);
    console.log(course_id);
    console.log(price);



    var player = cyberplayer("playercontainer").setup({
            width: '100%',
            height: '100%',
            file: video_url,
            image: cover_url,
            autostart: false,
            stretching: "uniform",
            repeat: false,
            volume: 100,
            controls: true,
            tokenEncrypt: true,
            // AccessKey
            ak: 'd6d83bc2e0d449ef932514eaec2c0876'
        });

        player.on('beforePlay',function (e) {
            if(!/m3u8/.test(e.file)){
                return;
            }
            xfzajax.get({
                'url': '/course/course_token/',
                'data': {
                    'video': video_url,
                    'course_id': course_id,
                    'price': price
                },
                'success': function (result) {
                    if(result['code'] === 200){
                        var token = result['data']['token'];
                        player.setToken(e.file,token);
                    }else{
                        player.stop();
                        window.messageBox.show(result['message']);

                    }

                },
                'fail': function (error) {
                    console.log(error);
                }
            });
        });
};

CourseDetail.prototype.run = function () {
    this.initPlayer();
};


$(function () {
    var courseDetail = new CourseDetail();
    courseDetail.run();
});
