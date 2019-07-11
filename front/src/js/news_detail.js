function NewsDetails() {

}

NewsDetails.prototype.listenSbuEvent = function(){
    var submitBtn = $('.submit-btn');
    var textarea = $("textarea[name='comment']");
    submitBtn.click(function () {
        var content = textarea.val();
        var news_id = textarea.attr('data-news-id');
        xfzajax.get({
            'url':'/news/comment_list/',
            'data': {
                'content': content,
                'news_id': news_id
            },
            'success': function (result) {
                if (result['code'] === 200){
                    var comment = result['data'];
                    var tpl = template('comment-item',{"comment":comment});
                    var commentListGroup = $(".comment-list");
                    commentListGroup.prepend(tpl);
                    window.messageBox.show('评论发表成功！');
                    textarea.val("");
                    document.getElementById('comment-title').innerText = '文章评论（'+ result['data']['count']['count']+'）';
                }else {
                    window.messageBox.show(result['message']);
                }
            }
        });
    });
};


NewsDetails.prototype.run  = function () {
    this.listenSbuEvent();
};


$(function () {
    var newsDetails= new NewsDetails();
    newsDetails.run();
});