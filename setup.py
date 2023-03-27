from setuptools import setup

setup(
    name="james",
    version="0.1",
    py_modules=["james"],
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        james=james:cli
    """,
)