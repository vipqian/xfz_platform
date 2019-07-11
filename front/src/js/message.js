
function Message() {
    var self = this;
    self.isAppended = false;
    self.wrapperHeight = 48;
    self.wrapperWidth = 300;
    self.initElement();
    self.listenCloseEvent();

}


Message.prototype.initElement = function () {
    var self = this;
    self.wrapper = $('<div></div>');
    self.wrapper.css({
        'background': '#f2dede',
        'padding': '10px',
        'font-size': '10px',
        'color': '#993d3d',
        'width': '300px',
        'position': 'fixed',
        'z-index': '999',
        'left': '50%',
        'top': '-48px',
        'margin-left': '-150px',
        'height': '48px',
        'box-sizing': 'border-box',
        'border': '1px solid #edccd1',
        'border-radius': '4px',
        'line-height': '24px',
        'text-align': 'center'
    });
    self.closeBtn = $('<span></span>');
    self.closeBtn.css({
        'font-family': 'core_sans_n45_regular, "Avenir Next", "Helvetica Neue", Helvetica, Arial, "PingFang SC", "Source Han Sans SC", "Hiragion Sans GB", "Microsoft YaHei", "WenQuanYi MicroHei", sans-serif;',
        'color': '#993d3d',
        'font-weight': 'right',
        'cursor': 'pointer',
        'font-size': '22px',
    });
    self.messageSpan = $('<span class="xfz-message-group"></span>');
    self.wrapper.append(self.messageSpan);
    self.wrapper.append(self.coloseBtn);
};


Message.prototype.listenCloseEvent = function () {
    var self = this;
    self.closeBtn.click(function () {
         self.wrapper.annotation({'top': -self.wrapperHeight})
    });
};

Message.prototype.show  = function (message) {
    var self = this;
    if (!self.isAppended) {
        $(document.body).append(self.wrapper);
        self.isAppended = true;
    }
    self.messageSpan.text(message);
    self.wrapper.animate({'top': 0}, function () {
        setTimeout(function () {
            self.wrapper.animate({'top': -self.wrapperHeight});
        }, 3000)
    })
};


window.messageBox = new Message();