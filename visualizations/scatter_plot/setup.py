from setuptools import setup, find_packages

setup(
    name='webviz_scatter_plot',
    version='0.1.0',
    packages=find_packages("."),
    package_dir={"": "."},
    package_data={
        'webviz_scatter_plot': []},
    test_suite="setup.discover_test_suite",
    install_requires=['jinja2', 'webviz', 'webviz_plotly', 'pandas'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'mock', 'pycodestyle', 'selenium'],
    entry_points={
        'webviz_page_elements': [
            'ScatterPlot = webviz_scatter_plot:ScatterPlot'
        ]
    },
    zip_safe=False
)
