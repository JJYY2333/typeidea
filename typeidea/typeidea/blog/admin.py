from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


class PostInline(admin.TabularInline):
    """  
    可选择继承自admin.StackedInline以获取不同的展示样式
    """
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category, site = custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline,]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()
    
    post_count.short_description="文章数量"


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('id','name', 'status', 'created_time')
    fields = ('id', 'name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner = request.user).values_list('id', 'name')
        
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id = category_id)
        return queryset


@admin.register(Post, site = custom_site)
class PostAdmin(BaseOwnerAdmin):
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operater'
    ]
    list_display_links = []
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True
    # 编辑页面
    save_on_top = True
    
    form = PostAdminForm

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    fieldsets = (
        ("基础配置", {
            'description':'基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),

        ('内容', {
            'fields':('desc', 'content')
        }),

        ('额外信息', {
            'classes': ('collapse'),
            'fields': ('tag',),
        })
    )

    def operater(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operater.short_description = '操作'

    def post_count(self, obj):
        return obj.post_set.count()
    
    post_count.short_description = '文章数量'

    # class Media:
    #     # 我们可以通过定义media类来往页面上增加想要添加的JS以及CSS资源
    #     css = {
    #         'all': (
                
    #         )
    #     }
    #     js = ('') """


@admin.register(LogEntry, site=custom_site)
class LogEnrtyAdmin(admin.ModelAdmin):
    list_display = ('object_repr', 'object_id', 'action_flag', 'user',
                    'change_message')


""" 
# 原始版本
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time')
    field = ('name', 'status', 'is_nav')
    # list_filter = [CategoryOwnerFilter]

    def save_model(self,request, obj, form, change):
        obj.owner = request.owner
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self,request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)



class CategoryOwnerFilter(admin.SimpleListFilter):
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner = request.user).values_list('id', 'name')
        
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id = category_id)
        return queryset


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operater'
    ]
    list_display_links = []
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True
    # 编辑页面
    save_on_top = True
    
    form = PostAdminForm

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    fieldsets = (
        ("基础配置", {
            'description':'基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),

        ('内容', {
            'fields':('desc', 'content')
        }),

        ('额外信息', {
            'classes': ('collapse'),
            'fields': ('tag',),
        })
    )

    def operater(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operater.short_description = '操作'

    def post_count(self, obj):
        return obj.post_set.count()
    
    post_count.short_description = '文章数量'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        queryset = super(PostAdmin, self).get_queryset(request)
        return queryset.filter(owner = request.user)

    # class Media:
    #     # 我们可以通过定义media类来往页面上增加想要添加的JS以及CSS资源
    #     css = {
    #         'all': (
                
    #         )
    #     }
    #     js = ('') """