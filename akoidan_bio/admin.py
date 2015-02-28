from akoidan_bio.models import UserProfile

__author__ = 'andrew'

class MovieAdmin(UserProfile):
    readonly_fields = ( 'image_tag',)