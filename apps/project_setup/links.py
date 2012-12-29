from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.classes import Link

from .icons import icon_setup

setup_menu_link = Link(text=_(u'setup'), view='setup_list', icon=icon_setup)
