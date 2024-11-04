from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import RegisterForm

class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('account_center:register')  # 註冊頁面的 URL 名稱

    def test_register_with_invalid_phone_number(self):
        invalid_phone_number = 'invalid_phone'
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'testuser@example.com',
            'cell_phone': invalid_phone_number,
        }
        response = self.client.post(self.url, data)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('cell_phone', form.errors)
        self.assertIn('手機號碼格式錯誤', form.errors['cell_phone'])
        User = get_user_model()
        self.assertFalse(User.objects.filter(username='testuser').exists())