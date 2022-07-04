from rest_framework import serializers
from blogapi.models import Blogs,UserProfile,Comments
from django.contrib.auth.models import User


class BlogSerializers(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)

    likes = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="username"
    )
    class Meta:
        model=Blogs
        fields=['id','user','title','content','blog_img','likes']


    def create(self, validated_data):
        user=self.context.get('user')
        return Blogs.objects.create(**validated_data,user=user)


class UserSerializers(serializers.ModelSerializer):
    # bio=serializers.CharField(read_only=True)
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    class Meta:
         model = UserProfile
         fields = ['user', 'bio', 'phone']

    def create(self, validated_data):
         user = self.context.get('user')
         return UserProfile.objects.create(**validated_data, user=user)





class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()




class CommentSerializer(serializers.ModelSerializer):
    blog=serializers.CharField(read_only=True)

    user = serializers.CharField(read_only=True)
    class Meta:
        model=Comments
        fields=['blog','comments','user']
    def create(self, validated_data):
        user= self.context.get('user')
        blog= self.context.get('blog')
        return Comments.objects.create( **validated_data,blog=blog, user=user)