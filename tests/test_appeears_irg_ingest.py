from datetime import datetime

import pytest

from src.appeears_irg_ingest import (
    AppEEARSReflectanceRow,
    AppEEARSSnowRow,
    convert_appeears_v061_to_irg,
    mod09q1_v061_quality_good,
    ndvi_from_scaled_reflectance,
    parse_appeears_date,
    resolve_column,
    snow_free_from_mod10a2_v061,
)


GOOD_QC = 1 << 12  # atmospheric correction, all quality nibbles zero
GOOD_STATE = 0


def test_strict_mod09_v061_quality_good():
    assert mod09q1_v061_quality_good(
        GOOD_QC,
        GOOD_STATE,
    )


@pytest.mark.parametrize(
    "qc,state",
    [
        (GOOD_QC | 0b01, GOOD_STATE),  # less-than-ideal MODLAND
        (GOOD_QC | (1 << 4), GOOD_STATE),  # band 1 not highest
        (GOOD_QC | (1 << 8), GOOD_STATE),  # band 2 not highest
        (0, GOOD_STATE),  # no atmospheric correction flag
        (GOOD_QC, 0b01),  # cloudy state
        (GOOD_QC, 1 << 2),  # cloud shadow
        (GOOD_QC, 3 << 6),  # high aerosol
        (GOOD_QC, 1 << 10),  # internal cloud
        (GOOD_QC, 1 << 13),  # adjacent cloud
        (65535, GOOD_STATE),
        (GOOD_QC, 65535),
    ],
)
def test_strict_mod09_v061_quality_rejects_bad_flags(qc, state):
    assert not mod09q1_v061_quality_good(qc, state)


def test_mod10a2_snow_extent_decode():
    assert snow_free_from_mod10a2_v061(25) is True
    assert snow_free_from_mod10a2_v061(200) is False
    assert snow_free_from_mod10a2_v061(50) is None
    assert snow_free_from_mod10a2_v061(255) is None


def test_scaled_reflectance_ndvi():
    assert ndvi_from_scaled_reflectance(
        0.2,
        0.6,
    ) == pytest.approx(0.5)
    assert ndvi_from_scaled_reflectance(
        float("nan"),
        0.6,
    ) is None
    assert ndvi_from_scaled_reflectance(
        2.0,
        0.6,
    ) is None
    assert ndvi_from_scaled_reflectance(
        0.0,
        0.0,
    ) is None


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("2020-01-17", datetime(2020, 1, 17)),
        ("01/17/2020", datetime(2020, 1, 17)),
        ("01-17-2020", datetime(2020, 1, 17)),
        ("2020/01/17", datetime(2020, 1, 17)),
    ],
)
def test_parse_appeears_date(text, expected):
    assert parse_appeears_date(text) == expected


def test_column_resolver_accepts_product_prefixed_suffix():
    headers = [
        "Category",
        "ID",
        "Date",
        "MOD09Q1_061_sur_refl_b01",
    ]
    assert resolve_column(
        headers,
        suffix_aliases=(
            "sur_refl_b01",
        ),
    ) == "MOD09Q1_061_sur_refl_b01"
    assert resolve_column(
        headers,
        exact_aliases=("ID",),
    ) == "ID"


def test_conversion_joins_exact_pixel_date_and_preserves_bad_quality_flag():
    date1 = datetime(2020, 1, 1)
    date2 = datetime(2020, 1, 9)
    reflectance = (
        AppEEARSReflectanceRow(
            pixel_id="cell1",
            date=date1,
            red_reflectance=0.2,
            nir_reflectance=0.6,
            qc_250m=GOOD_QC,
            state_250m=GOOD_STATE,
        ),
        AppEEARSReflectanceRow(
            pixel_id="cell1",
            date=date2,
            red_reflectance=0.25,
            nir_reflectance=0.5,
            qc_250m=GOOD_QC,
            state_250m=1,  # cloudy
        ),
    )
    snow = (
        AppEEARSSnowRow(
            pixel_id="cell1",
            date=date1,
            maximum_snow_extent=25,
        ),
        AppEEARSSnowRow(
            pixel_id="cell1",
            date=date2,
            maximum_snow_extent=200,
        ),
    )
    result = convert_appeears_v061_to_irg(
        reflectance,
        snow,
    )

    assert result.matched_rows == 2
    assert result.output_rows == 2
    assert result.rows[0].doy == 1
    assert result.rows[0].snow_free is True
    assert result.rows[0].quality_good is True
    assert result.rows[0].ndvi == pytest.approx(0.5)
    assert result.rows[1].doy == 9
    assert result.rows[1].snow_free is False
    assert result.rows[1].quality_good is False


def test_unknown_snow_is_omitted_not_relabelled():
    date = datetime(2020, 1, 1)
    result = convert_appeears_v061_to_irg(
        (
            AppEEARSReflectanceRow(
                pixel_id="cell1",
                date=date,
                red_reflectance=0.2,
                nir_reflectance=0.6,
                qc_250m=GOOD_QC,
                state_250m=GOOD_STATE,
            ),
        ),
        (
            AppEEARSSnowRow(
                pixel_id="cell1",
                date=date,
                maximum_snow_extent=50,
            ),
        ),
    )

    assert result.matched_rows == 1
    assert result.unknown_snow_rows == 1
    assert result.output_rows == 0


def test_unmatched_dates_are_not_force_matched():
    result = convert_appeears_v061_to_irg(
        (
            AppEEARSReflectanceRow(
                pixel_id="cell1",
                date=datetime(2020, 1, 1),
                red_reflectance=0.2,
                nir_reflectance=0.6,
                qc_250m=GOOD_QC,
                state_250m=GOOD_STATE,
            ),
        ),
        (
            AppEEARSSnowRow(
                pixel_id="cell1",
                date=datetime(2020, 1, 2),
                maximum_snow_extent=25,
            ),
        ),
    )
    assert result.matched_rows == 0
    assert result.output_rows == 0


def test_duplicate_keys_are_counted_for_cli_rejection():
    date = datetime(2020, 1, 1)
    refl = AppEEARSReflectanceRow(
        pixel_id="cell1",
        date=date,
        red_reflectance=0.2,
        nir_reflectance=0.6,
        qc_250m=GOOD_QC,
        state_250m=GOOD_STATE,
    )
    snow = AppEEARSSnowRow(
        pixel_id="cell1",
        date=date,
        maximum_snow_extent=25,
    )
    result = convert_appeears_v061_to_irg(
        (refl, refl),
        (snow, snow),
    )

    assert result.duplicate_reflectance_keys == 1
    assert result.duplicate_snow_keys == 1
    assert result.output_rows == 1
