from django.db import models

class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_experience = models.PositiveSmallIntegerField()
    breed_id = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.breed_id})"


class Mission(models.Model):
    cat = models.ForeignKey(
        SpyCat,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="missions"
    )
    is_complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mission {self.pk} - {'Complete' if self.is_complete else 'Active'}"


class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="targets")
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=2)
    notes = models.TextField(blank=True)
    is_complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("mission", "name") # Possible to achieve that with constraints too

    def __str__(self):
        return f"{self.name} ({self.country})"