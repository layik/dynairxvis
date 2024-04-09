from dynairxvis.main import greet


def test_main():
    w = "Welcome to DynAirXVis!"
    assert greet() == w
