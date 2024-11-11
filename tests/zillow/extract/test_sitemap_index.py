import pytest

from zillow.extract.site_map_index import collect_sitemap_partitions


@pytest.mark.parametrize(
    "grab_html",
    [("sitemap-index.html")],
    indirect=True,
)
def test_collect_sitemap_partitions(grab_html: bytes):

    collect_sitemap_partitions.fn(grab_html)

    # assert False
