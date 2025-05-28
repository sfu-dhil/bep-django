# from vectortiles import VectorLayer
from vectortiles.backends.postgis import VectorLayer
from .models import Diocese

class DiocesePre1541VL(VectorLayer):
    model = Diocese
    id = 'dioceses_pre_1541'
    tile_fields = ('pk', 'label',)
    geom_field = 'geom_pre_1541'

class DiocesePost1541VL(VectorLayer):
    model = Diocese
    id = 'dioceses_post_1541'
    tile_fields = ('pk', 'label',)
    geom_field = 'geom_post_1541'