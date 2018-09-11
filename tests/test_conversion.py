from pytest import approx


def test_round_trip():
    from all_sky_cloud_detection.cameras import cta_la_palma

    rows = 0, 400, 0, -400
    cols = 400, 0, -400, 0

    for row, col in zip(rows, cols):
        row += cta_la_palma.zenith_row
        col += cta_la_palma.zenith_col

        coord = cta_la_palma.pixel2horizontal(row, col)

        row_trafo, col_trafo = cta_la_palma.horizontal2pixel(coord)
        print(row_trafo, col_trafo)

        assert row == approx(row_trafo.value)
        assert col == approx(col_trafo.value)
