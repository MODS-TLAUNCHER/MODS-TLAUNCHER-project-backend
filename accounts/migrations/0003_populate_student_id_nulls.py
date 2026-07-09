from django.db import migrations
from django.db.models import Q

def fill_student_ids(apps, schema_editor):
    User = apps.get_model('accounts', 'User')

    used = set(
        User.objects
        .exclude(student_id__isnull=True)
        .exclude(student_id__exact='')
        .values_list('student_id', flat=True)
    )

    users = User.objects.filter(Q(student_id__isnull=True) | Q(student_id=''))

    for user in users:
        base = user.username or f"user{user.pk}"
        candidate = f"{base}-{user.pk}"

        counter = 1
        while candidate in used:
            candidate = f"{base}-{user.pk}-{counter}"
            counter += 1

        user.student_id = candidate
        user.save(update_fields=['student_id'])
        used.add(candidate)


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_student_id'),  # ✅ ESTA ES LA CLAVE
    ]

    operations = [
        migrations.RunPython(fill_student_ids),
    ]
