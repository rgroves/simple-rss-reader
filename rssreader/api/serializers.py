from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from api.models import Feed

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # The fields coming in via the user/register endpoint.
        fields = ('username', 'password')
        # Mark passord write_only so it is not returned in resonse.
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('id', 'title', 'url')
        # Removing the url unique validator, handled with special
        # logic in create
        extra_kwargs = {
            'url': {'validators': []},
        }

    def create(self, validated_data):
        user_id = self.context['user_id']
        feed_title = self.context['feed_title']

        try:
            feed = Feed.objects.get(**validated_data)
        except ObjectDoesNotExist:
            feed = Feed.objects.create(**validated_data)
            feed.title = feed_title
            feed.save()

        # Add the user requesting the feed regardless if it already exists.
        feed.users.add(user_id)

        return feed
