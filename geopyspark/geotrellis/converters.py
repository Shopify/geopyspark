# pylint: skip-file
from py4j.java_gateway import JavaClass
from py4j.protocol import register_input_converter

from geopyspark.geotrellis import RasterizerOptions, GlobalLayout, LocalLayout, CellType

class CellTypeConverter(object):
    def can_convert(self, obj):
        return isinstance(obj, CellType)

    def convert(self, obj, gateway_client):
        JavaCellType = JavaClass("geotrellis.raster.CellType", gateway_client)
        return JavaCellType.fromName(obj.value)

class RasterizerOptionsConverter(object):
    def can_convert(self, object):
        return isinstance(object, RasterizerOptions)

    def convert(self, object, gateway_client):
        JavaRasterizerOptions = JavaClass("geotrellis.raster.rasterize.Rasterizer$Options$", gateway_client)
        if (object.sampleType == 'PixelIsPoint'):
            sample = JavaClass("geotrellis.raster.PixelIsPoint$", gateway_client)
        elif (object.sampleType == 'PixelIsArea'):
            sample = JavaClass("geotrellis.raster.PixelIsArea$", gateway_client)
        else:
            raise TypeError("Could not convert {} to geotrellis.raster.PixelSampleType".format(object.sampleType))

        sample_instance = sample.__getattr__("MODULE$")
        return JavaRasterizerOptions().apply(object.includePartial, sample_instance)


class LayoutTypeConverter(object):
    def can_convert(self, object):
        return isinstance(object, GlobalLayout) or isinstance(object, LocalLayout)

    def convert(self, obj, gateway_client):
        if isinstance(obj, GlobalLayout):
            JavaGlobalLayout = JavaClass("geopyspark.geotrellis.GlobalLayout", gateway_client)
            return JavaGlobalLayout(obj.tile_size, obj.zoom, float(obj.threshold))
        elif isinstance(obj, LocalLayout):
            JavaLocalLayout = JavaClass("geopyspark.geotrellis.LocalLayout", gateway_client)
            return JavaLocalLayout(obj.tile_size)
        else:
            raise TypeError("Could not convert {} to geotrellis.raster.LayoutType".format(obj.sampleType))


register_input_converter(CellTypeConverter(), prepend=True)
register_input_converter(RasterizerOptionsConverter(), prepend=True)
register_input_converter(LayoutTypeConverter(), prepend=True)
