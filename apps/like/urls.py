from rest_framework.routers import SimpleRouter

from .views import LikeResource

router = SimpleRouter()
router.register('likes', LikeResource, basename='posts')
urlpatterns = router.urls
