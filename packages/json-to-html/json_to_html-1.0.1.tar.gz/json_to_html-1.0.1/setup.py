import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="json_to_html",
    version="1.0.1",
    description="show JSON in HTML",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/laowangv5/json2html",
    author="Yonghang Wang",
    author_email="wyhang@gmail.com",
    license="Apache 2",
    classifiers=["License :: OSI Approved :: Apache Software License"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[ ""],
    keywords=[ "json2html","html","json", ],
    entry_points={ "console_scripts": 
        [ 
            "json2html=json2html:json2html_main", 
        ] 
    },
)
