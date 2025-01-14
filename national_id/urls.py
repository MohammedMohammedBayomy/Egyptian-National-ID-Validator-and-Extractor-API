# Importing Django's path function to define URL patterns.
from django.urls import path

# Importing the NationalIDView class from the views module.
from .views import NationalIDView

# Defining the URL patterns for the app.
urlpatterns = [
    # Route for the National ID validation API endpoint.
    # The endpoint is accessible via "validate-id/".
    # The `as_view()` method is used to convert the class-based view into a callable view function.
    # The `name="validate-id"` allows referencing this route by name in other parts of the project.
    path("validate-id/", NationalIDView.as_view(), name="validate-id"),
]
