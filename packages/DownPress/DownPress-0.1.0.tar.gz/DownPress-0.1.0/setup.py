from distutils.core import setup

setup(
    name='DownPress',
    version='0.1.0',
    description='Exctract Markdwon posts and pages from WordPress export',
    packages=['downpress', ],
    license='BSD-3-Clause',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    author='Daniel Terhorst-North',
    author_email='daniel@dannorth.net',
    keywords='wordpress markdown convert',
    install_requires=[
        'lxml>=4.6.3',
        'markdownify>=0.9.0',
    ],
    python_requires='>=3.8',
)
