from django import forms
from .models import DataPost
from PIL import Image
from django.core.exceptions import ValidationError

class DataPostForm(forms.ModelForm):
    uploaded_image_path = forms.CharField(widget=forms.HiddenInput(), required=False)
    PostImage = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'id': 'image_uploader'})
    )
    class Meta:
        model = DataPost
        fields = ['Title', 'PostImage', 'Description', 'buttonColor', 'category', 'priority']
        widgets = {
            'buttonColor': forms.TextInput(attrs={'type': 'color', 'value':'#ffffff' }),
            'Title': forms.TextInput(attrs={'id': 'field_text','placeholder':'Best cities in Qatar' }),
            'Description': forms.Textarea(attrs={'id': 'field_description','placeholder':'Best cities in Qatar . . . .','cols':80}),
            
                    
        }
        
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['PostImage'].widget = forms.HiddenInput()

    def clean_PostImage(self):
        image = self.cleaned_data.get("PostImage")

        if image:
            # ✅ Check file size (e.g., 100KB min, 2MB max)
            max_size = 2 * 1024 * 1024  # 2 MB
            min_size = 100 * 1024       # 100 KB
            if image.size > max_size:
                raise ValidationError("Image file too large (max 2MB).")
            if image.size < min_size:
                raise ValidationError("Image file too small (min 100KB).")

            # ✅ Check filename length
            if len(image.name) > 100:
                raise ValidationError("Image filename is too long (max 100 characters).")

            # ✅ Check image dimensions
            try:
                img = Image.open(image)
                width, height = img.size
                if width < 600 or height < 400:
                    raise ValidationError("Image dimensions too small (min 600x400 pixels).")
                if width > 5000 or height > 5000:
                    raise ValidationError("Image dimensions too large (max 5000x5000 pixels).")
            except Exception:
                raise ValidationError("Invalid image file.")

        return image