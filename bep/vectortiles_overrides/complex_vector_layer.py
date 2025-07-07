from django.contrib.gis.db.models.functions import Transform, PointOnSurface, GeoFunc, Area
from django.contrib.gis.measure import Area as AreaMeasure
from django.db.models.expressions import RawSQL
from django.db import connections
from vectortiles.backends.postgis.functions import AsMVTGeom, MakeEnvelope
from vectortiles.backends.postgis import VectorLayer

class DumpGeom(GeoFunc):
    function='ST_Dump'
    template = "(%(function)s(%(expressions)s)).geom"

# Hack: to get center labels for Diocese
class ComplexCenterPointsVectorLayer(VectorLayer):
    def get_tile(self, x, y, z):
        if not self.check_in_zoom_levels(z):
            return b""
        features = self.get_vector_tile_queryset(z, x, y)
        # get tile coordinates from x, y and z
        xmin, ymin, xmax, ymax = self.get_bounds(x, y, z)
        # keep features intersecting tile
        filters = {
            # GeoFuncMixin implicitly transforms to SRID of geom
            f"{self.geom_field}__intersects": MakeEnvelope(xmin, ymin, xmax, ymax, 3857),
        }
        features = features.filter(**filters)
        # annotate prepared geometry for MVT
        features = features.annotate(
            geom_area=Area(DumpGeom(self.geom_field)),
            geom_prepared=AsMVTGeom(
                Transform(PointOnSurface(DumpGeom(self.geom_field)), 3857),
                MakeEnvelope(xmin, ymin, xmax, ymax, 3857),
                self.tile_extent,
                self.tile_buffer,
                self.clip_geom,
            ),
        )
        fields = (
            self.get_tile_fields() + ("geom_prepared", "geom_area",)
            if self.get_tile_fields()
            else ("geom_prepared", "geom_area",)
        )
        # limit feature number if limit provided
        limit = self.get_queryset_limit()
        if limit:
            features = features[:limit]
        # keep values to include in tile (extra included_fields + geometry)
        features = features.values(*fields)
        # generate MVT
        sql, params = features.query.sql_with_params()
        with connections[features.db].cursor() as cursor:
            # Hack: WHERE clause is to make sure that small islands don't show up in the labels
            cursor.execute('''
                    SELECT ST_ASMVT(subquery.*, %s, %s, %s)
                    FROM ({}) as subquery
                    WHERE subquery.geom_area >= 0.01
                '''.format(
                    sql
                ),
                params=[
                    self.get_id(),
                    self.tile_extent,
                    "geom_prepared",
                    *params,
                ],
            )
            row = cursor.fetchone()[0]
            # psycopg2 returns memoryview, psycopg returns bytes
            return row.tobytes() if isinstance(row, memoryview) else row or b""