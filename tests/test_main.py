from dynairxvis import main, plot


def test_main():
    w = "Welcome to DynAirXVis!"
    assert main.greet() == w
    assert 'plot' in dir(plot)
