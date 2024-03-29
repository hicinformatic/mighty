from mighty import fields
from mighty.admin.site import OverAdmin
from mighty import  _

class NationalityAdmin(OverAdmin):
    fieldsets = (((None, {'fields': ('country', 'alpha2', 'alpha3', 'numeric', 'image')})),
                (_.f_infos, {'fields': fields.base + fields.signhash + fields.disable}),)
    list_display = ('country', 'alpha2', 'alpha3', 'numeric', 'image_html') + fields.disable
    list_filter = fields.disable
    readonly_fields = fields.base + fields.signhash + fields.disable