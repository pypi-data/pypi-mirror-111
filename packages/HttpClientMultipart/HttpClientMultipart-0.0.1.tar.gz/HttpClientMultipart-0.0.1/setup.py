from setuptools import setup
import HttpClientMultipart as package

setup(
    name=package.__name__,
    version=package.__version__,

    py_modules=[package.__name__],

    author=package.__author__,
    author_email=package.__author_email__,
    maintainer=package.__maintainer__,
    maintainer_email=package.__maintainer_email__,
 
    description=package.__description__,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url=package.__url__,
    project_urls={
        "Executable": f"https://mauricelambert.github.io/info/python/code/{package.__name__}.pyz",
        "Documentation": f"https://mauricelambert.github.io/info/python/code/{package.__name__}.html",
    },
    download_url=f"https://mauricelambert.github.io/python/code/{package.__name__}.pyz",
 
    include_package_data=True,
 
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
    ],
 
    keywords=["Multipart", "HTTP", "form-data", "http.client", "urllib"],
    platforms=['Windows', 'Linux', "MacOS"],
    license=package.__license__,

    entry_points = {
        'console_scripts': [
            'HttpMultipart = HttpClientMultipart:main'
        ],
    },
    python_requires='>=3.6',
)