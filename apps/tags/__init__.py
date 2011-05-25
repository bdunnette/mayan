from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_menu, \
    register_model_list_columns, register_multi_item_links
from permissions.api import register_permission
from navigation.api import register_sidebar_template

from taggit.models import Tag

PERMISSION_TAG_CREATE = {'namespace': 'tags', 'name': 'tag_create', 'label': _(u'Create new tags')}
PERMISSION_TAG_ATTACH = {'namespace': 'tags', 'name': 'tag_attach', 'label': _(u'Attach exising tags')}
PERMISSION_TAG_REMOVE = {'namespace': 'tags', 'name': 'tag_remove', 'label': _(u'Remove tags from documents')}
PERMISSION_TAG_DELETE = {'namespace': 'tags', 'name': 'tag_delete', 'label': _(u'Delete global tags')}
PERMISSION_TAG_EDIT = {'namespace': 'tags', 'name': 'tag_edit', 'label': _(u'Edit global tags')}

register_permission(PERMISSION_TAG_CREATE)
register_permission(PERMISSION_TAG_ATTACH)
register_permission(PERMISSION_TAG_REMOVE)
register_permission(PERMISSION_TAG_DELETE)
register_permission(PERMISSION_TAG_EDIT)

tag_list = {'text': _(u'tags'), 'view': 'tag_list', 'famfam': 'tag_blue'}
tag_document_remove = {'text': _(u'remove'), 'view': 'tag_remove', 'args': ['object.id', 'document.id'], 'famfam': 'tag_blue_delete', 'permissions': [PERMISSION_TAG_REMOVE]}
tag_delete = {'text': _(u'delete'), 'view': 'tag_delete', 'args': 'object.id', 'famfam': 'tag_blue_delete', 'permissions': [PERMISSION_TAG_DELETE]}
tag_edit = {'text': _(u'edit'), 'view': 'tag_edit', 'args': 'object.id', 'famfam': 'tag_blue_edit', 'permissions': [PERMISSION_TAG_EDIT]}
tag_tagged_item_list = {'text': _(u'tagged documents'), 'view': 'tag_tagged_item_list', 'args': 'object.id', 'famfam': 'tag_blue'}
tag_multiple_delete = {'text': _(u'delete'), 'view': 'tag_multiple_delete', 'famfam': 'tag_blue_delete', 'permissions': [PERMISSION_TAG_DELETE]}

register_model_list_columns(Tag, [
    {
        'name': _(u'color'),
        'attribute': lambda x: u'<div style="width: 20px; height: 20px; border: 1px solid black; background: %s;"></div>' %
            x.tagproperties_set.get().get_color_code(),
    },
    {
        'name': _(u'color name'),
        'attribute': lambda x: x.tagproperties_set.get().get_color_display(),
    }
])

register_links(Tag, [tag_tagged_item_list, tag_edit])

register_multi_item_links(['tag_list'], [tag_multiple_delete])

register_sidebar_template(['document_view_advanced', 'document_view_simple'], 'tags_sidebar_template.html')

tags_menu = [
    {
        'text': _(u'tags'), 'view': 'tag_list', 'famfam': 'tag_blue', 'position': 4, 'links': [
            tag_list
        ]
    },
]
register_menu(tags_menu)
