from distutils.core import setup
import os

readme_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')
try:
    from m2r import parse_from_file
    readme = parse_from_file(readme_file)
except ImportError:
    # m2r may not be installed in user environment
    print('m2r not installed, using fallback README.rst')
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.rst')) as f:
        readme = f.read()

print(readme)

setup(
    name='deprogressapi',
    packages=['deprogressapi'],
    version='0.1.1',
    description='basic back-end progress api for the data analytics software framework dasf',
    long_description=readme,
    license='Apache-2.0',
    author='Daniel Eggert <daniel.eggert@gfz-potsdam.de>, Adam Sasin <sasin@hu-potsdam.de>',
    author_email = 'daniel.eggert@gfz-potsdam.de',
    keywords=['dasf', 'digital-earth', 'pulsar', 'gfz', 'progress reporting', 'api'],
    url='https://git.geomar.de/digital-earth/dasf/dasf-progress-api',
    download_url='https://git.geomar.de/digital-earth/dasf/dasf-progress-api/-/archive/v0.1.1/dasf-progress-api-v0.1.1.tar.gz',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
    ],
)
