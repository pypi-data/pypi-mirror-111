from setuptools import setup

setup(
    name='deprogressapi',
    packages=['deprogressapi'],
    version='0.1.0',
    description='basic back-end progress api for the data analytics software framework dasf',
    license='Apache-2.0',
    author='Daniel Eggert <daniel.eggert@gfz-potsdam.de>, Adam Sasin <sasin@hu-potsdam.de>',
    author_email = 'daniel.eggert@gfz-potsdam.de',
    keywords=['dasf', 'digital-earth', 'pulsar', 'gfz', 'progress reporting', 'api'],
    url='https://git.geomar.de/digital-earth/dasf/dasf-progress-api',
    download_url='https://git.geomar.de/digital-earth/dasf/dasf-progress-api/-/archive/v0.1.0/dasf-progress-api-v0.1.0.tar.gz',
    install_requires=[
    ],
    setup_requires=[
        'wheel'
    ]
)
