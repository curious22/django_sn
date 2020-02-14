from rest_framework.routers import SimpleRouter

from .views import PostResource

router = SimpleRouter()
router.register('posts', PostResource, basename='posts')
urlpatterns = router.urls
