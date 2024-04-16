from setuptools import setup

setup(
    name='crop',
    version='0.2',
    py_modules=['crop'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        crop=croppdf.crop:crop_pdf
    ''',
)