from django.db import models
from django.contrib.auth.models import User

class KYC(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    document_type = models.CharField(max_length=50)
    document_file = models.FileField(upload_to='kyc_docs/')

    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"
