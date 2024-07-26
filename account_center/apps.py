from django.apps import AppConfig


class AccountCenterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account_center'

    def ready(self):
        import account_center.signals  # 确保信号处理器在 Django 启动时被导入