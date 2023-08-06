import setuptools


setuptools.setup(
    name='libvarya',
    version='0.0.4',
    author='Alexander Sakharuk',
    author_email='saharuk.alexander@gmail.com',
    url='https://github.com/caxapyk/libvarya',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)