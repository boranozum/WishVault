from django.db import models
from django.utils.translation import gettext as _

from base.models import CachedModelBase


class Product(CachedModelBase):
    ProductCategoryElectronics = "electronics"
    ProductCategoryHomeKitchen = "home_kitchen"
    ProductCategoryFashion = "fashion"
    ProductCategoryBeautyPersonalCare = "beauty_personal_care"
    ProductCategoryHealthWellness = "health_wellness"
    ProductCategorySportsOutdoors = "sports_outdoors"
    ProductCategoryToysGames = "toys_games"
    ProductCategoryBooks = "books"
    ProductCategoryMusicMovies = "music_movies"
    ProductCategoryOfficeSupplies = "office_supplies"
    ProductCategoryAutomotive = "automotive"
    ProductCategoryGroceries = "groceries"
    ProductCategoryFurniture = "furniture"
    ProductCategoryJewelryAccessories = "jewelry_accessories"
    ProductCategoryToolsHomeImprovement = "tools_home_improvement"
    ProductCategoryTravelLuggage = "travel_luggage"
    ProductCategoryUnknown = "unknown"
    ProductCategoryChoices = (
        (ProductCategoryElectronics, "Electronics"),
        (ProductCategoryHomeKitchen, "Home & Kitchen"),
        (ProductCategoryFashion, "Fashion"),
        (ProductCategoryBeautyPersonalCare, "Beauty & Personal Care"),
        (ProductCategoryHealthWellness, "Health & Wellness"),
        (ProductCategorySportsOutdoors, "Sports & Outdoors"),
        (ProductCategoryToysGames, "Toys & Games"),
        (ProductCategoryBooks, "Books"),
        (ProductCategoryMusicMovies, "Music & Movies"),
        (ProductCategoryOfficeSupplies, "Office Supplies"),
        (ProductCategoryAutomotive, "Automotive"),
        (ProductCategoryGroceries, "Groceries"),
        (ProductCategoryFurniture, "Furniture"),
        (ProductCategoryJewelryAccessories, "Jewelry & Accessories"),
        (ProductCategoryToolsHomeImprovement, "Tools & Home Improvement"),
        (ProductCategoryTravelLuggage, "Travel & Luggage"),
        (ProductCategoryUnknown, "Unknown")
    )

    CURRENCY_TL = "TL"
    CURRENCY_USD = "USD"
    CURRENCY_EUR = "EUR"
    CURRENCY_CHOICES = (
        (CURRENCY_TL, "Turkish Lira"),
        (CURRENCY_USD, "United States Dollar"),
        (CURRENCY_EUR, "Euro")
    )

    name = models.CharField(max_length=255, verbose_name=_("Product Name"))
    category = models.CharField(max_length=100, choices=ProductCategoryChoices, default=ProductCategoryUnknown)
    url = models.URLField(null=True)
    price = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=CURRENCY_TL)
    sold_at = models.ForeignKey("product.ECommerceSite", on_delete=models.CASCADE, related_name="product_sold_at",
                                null=True, verbose_name=_("E-Commerce Site"))
    rating = models.FloatField(null=True)
    cover_photo = models.ImageField(upload_to="product/cover_photos", null=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        unique_together = ['name', 'sold_at']

    def __str__(self):
        return f"{self.name} - {self.category} - {self.price}"
