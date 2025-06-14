# Generated by Django 4.2.7 on 2025-05-23 14:03

from django.db import migrations

def create_default_projects(apps, schema_editor):
    """Create default projects for existing pages"""
    Page = apps.get_model('api', 'Page')
    Project = apps.get_model('api', 'Project')
    User = apps.get_model('auth', 'User')
    
    # Get all users who have pages but no projects
    users_with_pages = User.objects.filter(pages__isnull=False).distinct()
    
    for user in users_with_pages:
        # Create a default project for each user
        default_project, created = Project.objects.get_or_create(
            name="Default Project",
            owner=user,
            defaults={
                'description': 'Default project for existing pages'
            }
        )
        
        # Assign all pages without a project to the default project
        Page.objects.filter(owner=user, project__isnull=True).update(project=default_project)

def reverse_create_default_projects(apps, schema_editor):
    """Reverse the migration by removing project assignments"""
    Page = apps.get_model('api', 'Page')
    Project = apps.get_model('api', 'Project')
    
    # Remove project assignments from pages
    Page.objects.filter(project__name="Default Project").update(project=None)
    
    # Delete default projects
    Project.objects.filter(name="Default Project").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_page_unique_together_project_page_project'),
    ]

    operations = [
        migrations.RunPython(create_default_projects, reverse_create_default_projects),
    ]
