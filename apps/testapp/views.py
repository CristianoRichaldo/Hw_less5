from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer

CACHE_KEY = "posts_list"


class PostListCreateAPIView(APIView):
    def get(self, request):

        cached_posts = cache.get(CACHE_KEY)

        if cached_posts is not None:
        
            return Response(cached_posts, status=status.HTTP_200_OK)

     
        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        data = serializer.data

      
        cache.set(CACHE_KEY, data, timeout=60)

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            cache.delete(CACHE_KEY)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)