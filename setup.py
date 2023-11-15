from setuptools import setup, find_packages

setup(
    name='Google Wallet Pass Generator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
    ],
    author='Gian Luca Pirro',
    author_email='gianlucap2003@gmail.com',
    description='A useful package to help you create Google Wallet Passes.',
)
