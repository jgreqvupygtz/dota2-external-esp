from pipeline.world_to_screen import WorldToScreen


IDENTITY = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]


def test_project_origin_center():
    w2s = WorldToScreen(IDENTITY, 1920, 1080)
    pt = w2s.project((0.0, 0.0, 0.0))
    assert pt is not None
    assert abs(pt[0] - 960) < 1e-6
    assert abs(pt[1] - 540) < 1e-6


def test_box_requires_positive_w():
    w2s = WorldToScreen(IDENTITY, 1920, 1080)
    box = w2s.box_for((10.0, 10.0, 10.0))
    assert box is None or box.w > 0