from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='GoogleWalletPassGenerator',
    version='1.0.4',
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
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gianlucapirro/GoogleWalletPassGenerator',
    download_url='https://github.com/gianlucapirro/GoogleWalletPassGenerator/archive/refs/tags/v1.0.4.tar.gz'
)
