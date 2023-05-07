from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Article, Tag, Comment, Like
from .serializers  import ArticleListSerializer, ArticleSerializer, TagSerializer, CommentSerializer, RatingSerializer, LikeSerializer
from .permissions import IsAuthor
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response

# 
"""
@api_vieww - вьюшки на функуиях

rest_framework.views.APIView - вышки на классах без функционала

rest_framework.generics - вышки на готовых классах

rest_framework.viewsets - классах для обработки всех операций CRUD

rest_framework.views.APIView - вьюшки на классах без функционала

rest_framework.generics - вьюшки на готовых классах

rest_framework.viewsets - класс для обработки всех операций СRUD
"""
# 

class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['tag', 'status']
    searche = ['title', 'tag__title']
    # permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_permissions(self):
        if self.action in ['create', 'update', 'delete']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'delete']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action == 'comment':
            return CommentSerializer
        elif self.action == 'rate_article':
            return RatingSerializer
        return super().get_serializer_class()
    
    @action(methods=['POST', 'DELETE'], detail=True)
    def comment(self, request, pk=None):
        article = self.get_object()
        # Article.objects.get(pk=pk)
        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, article=article)
            return Response(serializer.data)
        return Response({'TODO': 'ДОБАВИТЬ УДАЛЕНИЕ КОММЕНТА'}) 

    @action(methods=['POST'], detail=True, url_path='rate')
    def rate_article(self, request, pk=None):
        article = self.get_object()
        serializer = RatingSerializer(data=request.data, context={'request': request, 'article': article})
        serializer.is_valid(raise_exception=True)
        serializer.save(article=article)
        return Response(serializer.data)   
    
    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        article = self.get_object()
        like = Like.objects.filter(user=request.user, article=article)
        if like.exists():
            like.delete()
            return Response({'liked': False})
        else:
            Like.objects.create(user=request.user, article=article).save()
            return Response({'liked': True})


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'destroy']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

"""
actions - действия пользователя.
list
retrieve
create
update
delete
"""


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer





# Create your views here.
