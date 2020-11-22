from django.contrib import admin
from ecommerce import models


admin.site.register([models.Category, models.Subcategory, models.Product])