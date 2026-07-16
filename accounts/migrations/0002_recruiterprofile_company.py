from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("accounts", "0001_initial"), ("jobs", "0001_initial")]

    operations = [
        migrations.RemoveField(model_name="recruiterprofile", name="company_name"),
        migrations.RemoveField(model_name="recruiterprofile", name="company_website"),
        migrations.RemoveField(model_name="recruiterprofile", name="company_description"),
        migrations.AddField(
            model_name="recruiterprofile",
            name="company",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="recruiters", to="jobs.company"),
        ),
    ]
