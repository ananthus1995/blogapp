from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from blogapi.models import Blogs, User,UserProfile
from rest_framework import status
from blogapi.serializers import BlogSerializers , UserSerializers, LoginSerializer,UserProfileSerializer,CommentSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from rest_framework import permissions,authentication



class BlogView(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        # res=Blogs.objects.get(user=request.user)
        res = Blogs.objects.all()
        blog_ser=BlogSerializers(res,many=True)
        # print(blog_ser)
        # for users in blog_ser:

        return Response(blog_ser.data)

    def post(self,request,*args,**kwargs):
        res=BlogSerializers(data=request.data,context={'user':request.user})
        if res.is_valid():
            res.save()
            return Response(res.data)

class BlogDetails(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,*args,**kwargs):
        blogid=kwargs.get('blog_id')
        blog_detail=Blogs.objects.get(id=blogid)
        res=BlogSerializers(blog_detail)
        return Response(res.data)
    def patch(self,request,*args,**kwargs):
        blogid = kwargs.get('blog_id')
        blog_detail = Blogs.objects.get(id=blogid)
        res = BlogSerializers(instance=blog_detail,data=request.data)
        if res.is_valid():
            res.save()
            return Response(res.data)
    def delete(self,request,*args,**kwargs):
        blogid = kwargs.get('blog_id')
        res=Blogs.objects.get(id=blogid).delete()
        return Response({"msg":"deleted"})


class UserSignup(generics.CreateAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializers
        permission_classes = (AllowAny,)

# class UserSignup(APIView):
#     def post(self,request,*args,**kwargs):
#         usr_ser=UserSerializers(data=request.data)
#         if usr_ser.is_valid():
#             usr_ser.save()
#             return Response(usr_ser.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(usr_ser.errors,status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self,request,*args,**kwargs):
        login_serializer=LoginSerializer(data=request.data)
        if login_serializer.is_valid():
            uname=login_serializer.validated_data.get('username')
            pwd=login_serializer.validated_data.get('password')
            user=authenticate(request, username=uname, password=pwd)
            if user:
                login(request, user)
                return Response({'msg':'loggedIn'})
            else:
                return Response({'msg': 'invalid'})


class AddUserProfile(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):
        # print(request.data)
        user_data=UserProfileSerializer(data=request.data,context={'user':request.user})
        if user_data.is_valid():
            user_data.save()
            return Response(user_data.data,status=status.HTTP_201_CREATED)
        else:
            return Response(user_data.errors)


class ProfileDetails(APIView):

    def get(self,request,*args,**kwargs):
        # print(self.request.user)
        userdata = User.objects.get(id=request.user.id)
        userprofiledata = UserProfile.objects.get(user=request.user)
        bio=userprofiledata.bio
        phone=userprofiledata.phone
        udata=UserSerializers(userdata)
        return Response(udata.data)


    # def put(self,request,*args,**kwargs):
    #     userid=kwargs.get('uesr_id')
    #     user=User.objects.get(id=userid)
    #     usrdt=UserProfileSerializer(data=request.data,context={'user':request.user})


class BlogLikes(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,*args,**kwargs):

        blog_id=kwargs.get('blog_id')
        blog=Blogs.objects.get(id=blog_id)
        blog.likes.add(request.user)
        likes_count= blog.likes.all().count()
        liked_users= blog.likes.all()
        return Response({"likecount": likes_count})


class Comments(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,*args,**kwargs):
        blogid= kwargs.get('blog_id')
        blog=Blogs.objects.get(id=blogid)
        # print(blog)
        comment= CommentSerializer(data= request.data, context={"user": request.user, "blog": blog})
        # print(comment)
        if comment.is_valid():
            comment.save()
            return Response(comment.data)
        else:
            return Response(comment.errors)




# Create your views here.
