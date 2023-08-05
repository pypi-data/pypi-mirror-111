import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask_doclever",
    version="0.0.1",
    author="liuxu",
    author_email="liuxu@dlyunzhi.com",
    description="auto generate flask_restful interface document to doclever",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.dlyunzhi.com",
    project_urls={
        "Bug Tracker": "https://www.dlyunzhi.com",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "flask_doclever"},
    packages=setuptools.find_packages(where="flask_restful"),
    python_requires=">=3.6",
)
