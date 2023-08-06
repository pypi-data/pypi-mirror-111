import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "borgor",
	version = "0.1.0",
	author = "coverosu",
	author_email = 'coverosu@gmail.com',
	description = "An osu! python package.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/coverosu/borgor",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.9',
)
