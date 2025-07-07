from vectortiles.backends.postgis import VectorLayer
from .models import Diocese
from.vectortiles_overrides.complex_vector_layer import ComplexCenterPointsVectorLayer

class DiocesePre1541VectorLayer(VectorLayer):
    model = Diocese
    id = 'dioceses_pre_1541'
    tile_fields = ('id',)
    geom_field = 'geom_pre_1541'

class DiocesePre1541LabelVectorLayer(ComplexCenterPointsVectorLayer):
    model = Diocese
    id = 'dioceses_pre_1541_labels'
    tile_fields = ('id', 'label',)
    geom_field = 'geom_pre_1541'

class DiocesePost1541VectorLayer(VectorLayer):
    model = Diocese
    id = 'dioceses_post_1541'
    tile_fields = ('id',)
    geom_field = 'geom_post_1541'

class DiocesePost1541LabelVectorLayer(ComplexCenterPointsVectorLayer):
    model = Diocese
    id = 'dioceses_post_1541_labels'
    tile_fields = ('id', 'label',)
    geom_field = 'geom_post_1541'
