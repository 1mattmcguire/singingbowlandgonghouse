from django.contrib import admin
from django import forms
from django.db.models import Count
from django.utils.html import format_html
from .models import Booking, Inquiry, InstrumentCategory, InstrumentSubcategory, Instrument, InstrumentImage


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'service', 'booking_date', 'session_type', 'created_at']
    list_filter = ['service', 'session_type', 'booking_date', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message', 'course_selection']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'age')
        }),
        ('Booking Details', {
            'fields': ('service', 'booking_date', 'session_type', 'course_selection')
        }),
        ('Additional Information', {
            'fields': ('medical_condition', 'message')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'created_at']
    list_filter = ['created_at', 'subject']
    search_fields = ['name', 'email', 'phone', 'subject', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('subject', 'message')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs


class InstrumentInline(admin.TabularInline):
    model = Instrument
    extra = 1
    fields = ['name', 'description', 'image', 'material', 'size', 'weight', 'note', 'created_at']
    readonly_fields = ['created_at', 'image_preview']

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 80px; object-fit: contain;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Image'


@admin.register(InstrumentCategory)
class InstrumentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(InstrumentSubcategory)
class InstrumentSubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug']
    list_filter = ['category']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [InstrumentInline]


class InstrumentImageInline(admin.TabularInline):
    model = InstrumentImage
    extra = 5
    min_num = 1
    fields = ['image', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 80px; object-fit: contain;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Preview'


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultiFileField(forms.FileField):
    widget = MultiFileInput

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data if d]
        if data:
            return [single_file_clean(data, initial)]
        return []


class InstrumentAdminForm(forms.ModelForm):
    bulk_gallery_images = MultiFileField(
        required=False,
        widget=MultiFileInput(attrs={'multiple': True}),
        help_text='Select multiple files to add them as InstrumentImage entries.'
    )

    class Meta:
        model = Instrument
        fields = '__all__'


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    form = InstrumentAdminForm
    list_display = ['name', 'subcategory', 'get_category', 'gallery_image_count', 'image_preview', 'created_at']
    inlines = [InstrumentImageInline]
    list_filter = ['subcategory__category', 'subcategory']
    search_fields = ['name']
    readonly_fields = ['created_at', 'image_preview_large']
    fields = ['subcategory', 'name', 'description', 'image', 'bulk_gallery_images', 'material', 'size', 'weight', 'note', 'image_preview_large', 'created_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('subcategory__category').annotate(_gallery_count=Count('images'))

    def get_category(self, obj):
        return obj.subcategory.category
    get_category.short_description = 'Category'
    get_category.admin_order_field = 'subcategory__category'

    def gallery_image_count(self, obj):
        return getattr(obj, '_gallery_count', obj.images.count())
    gallery_image_count.short_description = 'Gallery Images'

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 80px; object-fit: contain;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Image'

    def image_preview_large(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px; object-fit: contain;" />',
                obj.image.url
            )
        return '-'
    image_preview_large.short_description = 'Image Preview'

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        uploaded_files = form.cleaned_data.get('bulk_gallery_images', [])
        for uploaded_file in uploaded_files:
            InstrumentImage.objects.create(
                instrument=form.instance,
                image=uploaded_file
            )


@admin.register(InstrumentImage)
class InstrumentImageAdmin(admin.ModelAdmin):
    list_display = ['instrument', 'file_name', 'image_preview']
    search_fields = ['instrument__name']
    list_select_related = ['instrument']

    def file_name(self, obj):
        return obj.image.name.split('/')[-1] if obj.image else '-'
    file_name.short_description = 'File'

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 80px; object-fit: contain;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Preview'
 