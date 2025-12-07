from rest_framework.routers import DefaultRouter

from clients.views.cliente import ClienteViewSet
from clients.views.deuda import DeudaViewSet
from clients.views.portafolio import PortafolioViewSet

router = DefaultRouter()
router.register("clientes", ClienteViewSet)
router.register("portafolios", PortafolioViewSet)
router.register("deudas", DeudaViewSet)

urlpatterns = router.urls
