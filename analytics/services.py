from collections import Counter

from recruitment.models import Application


def get_dashboard_metrics(user):
    """Return summary metrics for recruiters and admins."""
    if not getattr(user, "is_authenticated", False):
        return {}
 
    pk = getattr(user, "pk", None) or getattr(user, "id", None)
    if pk is None:
        return {
            "total_applications": 0,
            "shortlisted": 0,
            "rejected": 0,
            "pending": 0,
            "status_breakdown": {},
        }

    applications = Application.objects.filter(job__created_by__pk=pk)
    total = applications.count()
    shortlisted = applications.filter(status="shortlisted").count()
    rejected = applications.filter(status="rejected").count()
    pending = applications.filter(status__in=["submitted", "reviewed"]).count()
    statuses = Counter(applications.values_list("status", flat=True))

    return {
        "total_applications": total,
        "shortlisted": shortlisted,
        "rejected": rejected,
        "pending": pending,
        "status_breakdown": dict(statuses),
    }
