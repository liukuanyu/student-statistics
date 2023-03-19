from setuptools import setup, find_packages

setup(
    name='task',
    version='1.0.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        "flask",
        "requests",
        "prometheus_client"
    ],
)
