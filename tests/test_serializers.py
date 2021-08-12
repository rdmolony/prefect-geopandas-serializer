import pytest
from shapely.geometry import Point

from prefect_geopandas_serializer.serializers import GeoPandasSerializer


class TestPandasSerializer:
    @pytest.fixture(scope="function")
    def input_geodataframe(self):
        gpd = pytest.importorskip("geopandas", reason="GeoPandas not installed")
        return gpd.GeoDataFrame(
            {
                "one": [1, 2, 3],
                "two": [4, 5, 6],
                "geometry": [Point([0, 0]), Point([0, 0]), Point([0, 0])],
            }
        )

    def test_complains_when_unavailable_file_type_specified(self):
        gpd = pytest.importorskip("geopandas", reason="GeoPandas not installed")
        with pytest.raises(ValueError):
            GeoPandasSerializer("blerg")

    @pytest.mark.parametrize("file_type", ["parquet"])
    def test_serialize_returns_bytes(self, file_type, input_geodataframe):
        gpd = pytest.importorskip("geopandas", reason="GeoPandas not installed")
        serialized = GeoPandasSerializer(file_type).serialize(input_geodataframe)
        assert isinstance(serialized, bytes)

    def test_serialize_deserialize_is_invariant(self, input_geodataframe):
        file_type = "parquet"
        gpd = pytest.importorskip("geopandas", reason="GeoPandas not installed")
        from geopandas.testing import assert_geodataframe_equal

        serializer = GeoPandasSerializer(file_type)
        serialized = serializer.serialize(input_geodataframe)
        deserialized = serializer.deserialize(serialized)

        assert_geodataframe_equal(input_geodataframe, deserialized)
