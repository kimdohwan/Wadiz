from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from members.token import account_activation_token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.SlugField(max_length=12, min_length=1, allow_blank=False, write_only=True)
    nickname = serializers.CharField(max_length=20, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User

        fields = (
            'pk',
            'username',
            'password',
            'nickname',
            'img_profile',
            'funding_set'
        )

    def validate_password(self, value):
        if value == self.initial_data.get('password1'):
            return value
        raise ValidationError('(password, password1) 불일치')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            nickname=validated_data['nickname'],
            # img_profile=validated_data['img_profile'],
        )
        user.is_active = False
        user.save()

        message = render_to_string('user/account_activate_email.html', {
            'user': user,
            'domain': 'localhost:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
            'token': account_activation_token.make_token(user),
        })

        mail_subject = 'test'
        to_email = user.username
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return validated_data
