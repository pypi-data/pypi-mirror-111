from setuptools import setup, find_packages


def readme():
	with open('README.md') as f:
		info = f.read()
	return info


setup(
	name='speedo',
	version='1.0.6',
	description='analyse and illustrate data and equation',
	long_description=readme(),
	long_description_content_type='text/markdown',
	url='https://github.com/messizqin/speedo/',
	author='Messiz YiQi Qin',
	author_email='messizqin@gmail.com',
	license='MIT',
	classifiers=[
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.8",
	],
	packages=find_packages(),
	include_package_data=True,
	install_requires=[],
)
