from rest_framework.pagination import CursorPagination

class Customcursor(CursorPagination):
    page_size = 5
    ordering='created_at'