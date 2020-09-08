from django.contrib import admin
from blog.models import Blog, Contact

# Register your models here.
# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    class Media:
        js = ("js/editor.js",)

admin.site.register(Blog, BlogAdmin)
admin.site.register(Contact)