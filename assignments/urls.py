from django.urls import include, path
from rest_framework.routers import SimpleRouter

from assignments.views import (
    AssignmentDetails,
    CategoryViewSet,
    ListAssignments,
    status_check,
)

app_name = "assignments"

category_router = SimpleRouter()
category_router.register("category", CategoryViewSet)

urlpatterns = [
    path("", status_check, name="check"),
    path("list_assignments/", ListAssignments.as_view(), name="assignmentList"),
    path(
        "assignment_details/<int:id>/",
        AssignmentDetails.as_view(),
        name="assignmentDetails",
    ),
    path("", include(category_router.urls)),
]
