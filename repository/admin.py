from django.contrib import admin
from repository.models import *
# Register your models here.

admin.site.register(Server)
admin.site.register(IDC)
admin.site.register(Asset)
admin.site.register(Disk_info)
admin.site.register(Team)

admin.site.register(Account)
admin.site.register(Domain)
