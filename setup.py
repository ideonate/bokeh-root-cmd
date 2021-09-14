import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

# read requirements.txt
with open('requirements.txt', 'r') as f:
    content = f.read()
li_req = content.split('\n')
install_requires = [e.strip() for e in li_req if len(e)]

setuptools.setup(
    name="bokeh-root-cmd",
    version="0.1.2",
    author="Dan Lester",
    author_email="dan@ideonate.com",
    description="Command line wrapper to run a Bokeh script/folder at the root URL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ideonate/bokeh-root-cmd",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
    entry_points={"console_scripts": ["bokeh-root-cmd = bokeh_root_cmd.main:run"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


