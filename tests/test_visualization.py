import numpy
from matplotlib.testing.decorators import image_comparison
from SLIX import toolbox, io, visualization
import matplotlib
from matplotlib import pyplot as plt
import pytest
import shutil
import os

matplotlib.use('agg')


class TestVisualization:
    @image_comparison(baseline_images=['parameter_map'], remove_text=True, extensions=['png'])
    def test_visualize_parameter_map(self):
        example = io.imread('tests/files/demo.nii')
        prominence = toolbox.mean_peak_prominence(example, kind_of_normalization=1, use_gpu=False)
        visualization.visualize_parameter_map(prominence, colorbar=False)

    @image_comparison(baseline_images=['unit_vectors'], remove_text=True, extensions=['png'])
    def test_visualize_unit_vectors(self):
        example = io.imread('tests/files/demo.nii')
        peaks = toolbox.significant_peaks(example, use_gpu=False)
        centroid = toolbox.centroid_correction(example, peaks, use_gpu=False)
        direction = toolbox.direction(peaks, centroid, use_gpu=False)
        unit_x, unit_y = toolbox.unit_vectors(direction, use_gpu=False)
        visualization.visualize_unit_vectors(unit_x, unit_y, thinout=10)

    def test_visualize_direction_one_dir(self):
        image = numpy.arange(0, 180)
        hsv_image = visualization.visualize_direction(image)
        assert numpy.all(hsv_image[0, :] == [1, 0, 0])
        assert numpy.all(hsv_image[30, :] == [1, 1, 0])
        assert numpy.all(hsv_image[60, :] == [0, 1, 0])
        assert numpy.all(hsv_image[90, :] == [0, 1, 1])
        assert numpy.all(hsv_image[120, :] == [0, 0, 1])
        assert numpy.all(hsv_image[150, :] == [1, 0, 1])

    def test_visualize_direction_multiple_dir(self):
        image = numpy.arange(0, 180)[..., numpy.newaxis, numpy.newaxis]
        stack_direction = numpy.concatenate((image,
                                             image + 90 % 180,
                                             numpy.full(image.shape, -1)),
                                            axis=-1)
        hsv_image = visualization.visualize_direction(stack_direction)

        assert numpy.all(hsv_image[0, 0, :] == [1, 0, 0])
        assert numpy.all(hsv_image[1, 1, :] == [1, 0, 0])
        # One check should be enough
        assert numpy.all(hsv_image[0, 1, :] == [0, 1, 1])
        assert numpy.all(hsv_image[1, 0, :] == [0, 1, 1])
        assert numpy.all(hsv_image[60, 0, :] == [1, 1, 0])
        assert numpy.all(hsv_image[61, 1, :] == [1, 1, 0])
        assert numpy.all(hsv_image[120, 0, :] == [0, 1, 0])
        assert numpy.all(hsv_image[121, 1, :] == [0, 1, 0])
        assert numpy.all(hsv_image[180, 0, :] == [0, 1, 1])
        assert numpy.all(hsv_image[181, 1, :] == [0, 1, 1])
        assert numpy.all(hsv_image[240, 0, :] == [0, 0, 1])
        assert numpy.all(hsv_image[241, 1, :] == [0, 0, 1])
        assert numpy.all(hsv_image[300, 0, :] == [1, 0, 1])
        assert numpy.all(hsv_image[301, 1, :] == [1, 0, 1])


@pytest.fixture(scope="session", autouse=True)
def run_around_tests(request):
    # A test function will be run at this point
    yield

    # Clear pyplot for next test
    plt.clf()

    # Code that will run after your test, for example:
    def remove_test_dir():
        if os.path.isdir('result_images'):
            # shutil.rmtree('result_images')
            pass

    request.addfinalizer(remove_test_dir)
