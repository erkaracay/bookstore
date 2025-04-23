from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Book(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    published_date = models.DateField()
    seller = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='books_sold'
)

    def __init__(self, *args, **kwargs):
        """
        When a Book object is created or loaded from the database,
        store the original title so we can detect changes before saving.
        """
        super().__init__(*args, **kwargs)
        self._original_title = self.title  # Store the initial title

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to:
        - Generate a slug only if it doesn’t exist
        - Update the slug if the title changes
        - Ensure slugs remain unique by appending a number if necessary
        """
        if not self.slug or self.title != self._original_title:  # Check if title has changed
            base_slug = slugify(self.title)  # Convert title to a URL-safe slug
            slug = base_slug
            count = 1

            # Ensure the slug is unique (if a book with the same slug exists, append a number)
            while Book.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1

            self.slug = slug  # Set the new unique slug

        super().save(*args, **kwargs)  # Call the default save method

    def __str__(self):
        return self.title
