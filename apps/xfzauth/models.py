

from django.db import models
from shortuuidfield import ShortUUIDField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.


class UserManager(BaseUserManager):

    def _create_user(self, telephone, username, password, **kwargs):
        if not telephone:
            raise ValueError('请传入手机号码')
        if not username:
            raise ValueError('请传入用户名')
        if not password:
            raise ValueError('请传入密码')

        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone, username, password, **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone, username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):

    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=100)
    # 是否有效
    is_active = models.BooleanField(default=True)
    # 是否为公司员工
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # 唯一认证需要字段
    USERNAME_FIELD = 'telephone'
    # 创建超级用户需要填写的字段 默认认证字段和密码是不需要设置的
    REQUIRED_FIELDS = ['username']
    # 发邮件的字段
    EMAIL_FIELD = 'email'

    object = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username






