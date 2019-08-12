# -*- coding: utf-8 -*-#

"""
Name:           initgroup
# Author:       wangyunfei
# Date:         2019-08-12
# Description:  
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('hello world'))