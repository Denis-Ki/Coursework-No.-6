from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        moderator_group, _ = Group.objects.get_or_create(name='Модераторы')

        can_unpublish_product = Permission.objects.get(codename='can_unpublish_product')
        change_product_description = Permission.objects.get(codename='change_product_description')
        change_product_category = Permission.objects.get(codename='change_product_category')

        # Назначение разрешений группе
        moderator_group.permissions.add(can_unpublish_product, change_product_description, change_product_category)

        self.stdout.write(self.style.SUCCESS('Группа "Модераторы" и необходимые разрешения созданы успешно.'))
        self.stdout.write(self.style.SUCCESS('Добавьте пользователей группе "Модераторы".'))