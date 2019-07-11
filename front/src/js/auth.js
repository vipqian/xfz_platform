
function Author() {
    this.scrrolWrapper = $('.scroll-wrapper');
    this.index = 1;
    this.maskWrapper = $('.mask-wrapper');
    this.signoutGroup = $('.signup-group');
    this.sendBtn = $('.sms-captcha-btn');




    
}

Author.prototype.run = function () {
    this.initSign();
    this.listenShow();
    this.listenClick();
    this.listenSigninEvent();
    this.listenImageCaptcha();
    this.listenPhoneCodeSend();
    this.listenRegisterClick()
};

Author.prototype.initSign = function(){
    var self = this;
    self.scrrolWrapper.css({'width': 1200});
    var firstDiv = self.scrrolWrapper.children('div').eq(0).clone();
    self.scrrolWrapper.append(firstDiv);

};

Author.prototype.listenShow = function(){
    var self = this;
    $('#login').click(function () {
        self.maskWrapper.show();
    });
    $('#signin').click(function () {
        self.scrrolWrapper.css({'left': -400});
        self.maskWrapper.show();
    });
    $('.close-btn').click(function () {
        self.maskWrapper.hide();
    });
};

Author.prototype.animates = function(){
    var self = this;
    self.scrrolWrapper.animate({'left': -400* self.index}, 500);
};

Author.prototype.listenClick = function(){
    var self = this;
    $('.signup-btn').click(function () {
        if (self.index === 2){
            self.index = 1;
            self.scrrolWrapper.css({'left': 0})
        }
        self.animates();


    });
    $('.signin-btn').click(function () {
        self.index++;
        self.animates();
    });
};

Author.prototype.listenSigninEvent = function(){
    var signinGroup = $('.signin-group');
    var telephoneInput = signinGroup.find("input[name='telephone']");
    var passwordInput = signinGroup.find("input[name='password']");
    var rememberInput = signinGroup.find("input[name='remember']");

    var submitBtn = signinGroup.find('.submit-btn');

    submitBtn.click(function () {
        var self = this;
        var telephone = telephoneInput.val();
        var password = passwordInput.val();
        var remember = rememberInput.prop('checked');

        xfzajax.post({
            'url': '/account/login/',
            'data': {
                'telephone': telephone,
                'password': password,
                'remember': remember?0:1,
            },
            'success': function (result) {
                if (result['code'] === 200){
                    $('.mask-wrapper').hide();
                    // 刷新页面
                    window.location.reload();
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
            },
            'fail': function (error) {
                console.log(error);

            }
        });

    });
};

Author.prototype.listenImageCaptcha = function(){
    image = $('.image_captcha');

    image.click(function () {
        image.attr("src", '/account/image/' + '?random' + Math.random())
    })
};

Author.prototype.smsSuccessEvent = function(){
    var self = this;
    self.sendBtn.addClass('disabled');
    var count = 60;
    // 取消点击事情
    self.sendBtn.unbind('click');
    var timer =setInterval(function () {
        self.sendBtn.text(count + 's再次点击');
        count--;
        if (count < 0) {
            clearInterval(timer);
            self.sendBtn.removeClass('disabled');
            self.sendBtn.text('发送验证码');
            self.listenPhoneCodeSend();
        }
    }, 1000)

};

Author.prototype.listenPhoneCodeSend = function(){
    var self = this;

    var telephoneInput = self.signoutGroup.find("input[name='telephone']");


    self.sendBtn.click(function () {
        var telephone = telephoneInput.val();
        if (!telephone) {
            window.messageBox.show("请输入手机号码");
        } else {
            if (!(/^1[3|4|5|7|8][0-9]\d{8}$/.test(telephone))){
                window.messageBox.show("不是正确的手机号码");
            }else {
                xfzajax.get({
            'url': '/account/sms_captcha/',
            'data': {
                'telephone': telephone
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    window.messageBox.show('短信发送成功');
                    self.smsSuccessEvent();
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
            },
            'fail': function (error) {
                console.log(error)
            }


        })
            }
        }

    })
};


Author.prototype.listenRegisterClick = function(){
    console.log('注册~~~~~~~~~~');
    var self = this;
    var telephoneInput = self.signoutGroup.find("input[name='telephone']");
    var usernameInput = self.signoutGroup.find("input[name='username']");
    var img_captchaInput = self.signoutGroup.find("input[name='img_captcha']");
    var password1Input = self.signoutGroup.find("input[name='password1']");
    var password2Input = self.signoutGroup.find("input[name='password2']");
    var sms_captchaInput = self.signoutGroup.find("input[name='sms_captcha']");
    var registerSubmit = self.signoutGroup.find('.submit-btn');

    registerSubmit.click(function () {
        console.log('register button');
        var telephone = telephoneInput.val();
        var username = usernameInput.val();
        var img_captcha = img_captchaInput.val();
        var password1 = password1Input.val();
        var password2 = password2Input.val();
        var sms_captcha = sms_captchaInput.val();

        console.log(telephone);
        xfzajax.post({
            'url': '/account/register/',
            'data': {
                'telephone': telephone,
                'password1': password1,
                'password2': password2,
                'username': username,
                'img_captcha': img_captcha,
                'sms_captcha': sms_captcha,
            },
            'success': function (result) {
                if (result['code'] === 200){
                    $('.mask-wrapper').hide();
                    // 刷新页面
                    window.location.reload();
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
            },
            'fail': function (error) {
                console.log(error)
            }
        })

    })
};


function Nav(){
    this.navTable = $('.nav');

};

Nav.prototype.run = function(){
    this.listenNavClick();
};

Nav.prototype.navColor = function(index){
    var self = this;
    self.navTable.children('li').eq(index).addClass('active').siblings().removeClass('active')
};

Nav.prototype.listenNavClick = function(){
    var self = this;
    var index = 0;
    var url = window.location.pathname;
    if (url == '/news/index/'){
        index = 0;
    } else if (url === '/course/index/') {
        index = 1;
    } else if (url === '/payinfo/index/') {
        index = 2;
    } else if (url === '/news/search/') {
        index = 3;
    }
    self.navColor(index);
};



$(function () {
    var author = new Author();
    var nav = new Nav();
    nav.run();
    author.run();

});
