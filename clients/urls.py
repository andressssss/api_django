from rest_framework.routers import DefaultRouter
from clients.views.cliente import ClienteViewSet
from clients.views.portafolio import PortafolioViewSet
from clients.views.deuda import DeudaViewSet

router = DefaultRouter()
router.register("clientes", ClienteViewSet)
router.register("portafolios", PortafolioViewSet)
router.register("deudas", DeudaViewSet)

urlpatterns = router.urls
