from setuptools import setup, find_packages

setup(
    name='GoogleWalletPassGenerator',
    version='0.1',
    license='MIT',
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
    url='https://github.com/gianlucapirro/GoogleWalletPassGenerator',
    download_url='https://github.com/gianlucapirro/GoogleWalletPassGenerator/archive/refs/tags/GoogleWalletGenerator.tar.gz'
)
