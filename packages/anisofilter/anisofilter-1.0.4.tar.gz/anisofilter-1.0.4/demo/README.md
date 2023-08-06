# Python demo to denoise a 3D point cloud, and visualize the noisy and denoised clouds

It is recommended to do all the following in a Conda virtual environment, with Python3:
	1. $ conda create -n YOUR-ENV-NAME python=3
	2. $ conda activate YOUR-ENV-NAME	

To use our anisotropic filter, simply do:
	1. $ pip install anisofilter

For efficiently visualize and interact with the point cloud with many points, we use Mayavi.
Due to the dependecies issue, please do the installation with the following order:
	1. $ pip install vtk	(for MacOS and Linux platforms) , 
	   $ conda install -c conda-forge vtk	(for Windows platform)
	2. $ pip install mayavi
	3. $ pip install PyQt5

For Windows platform, you may need to reinstall Anisofilter, due to the change of python version 
during installing VTK:
	1. $ pip install anisofilter

Then simply run: python demo_pcd_filtering.py

The denoised point cloud is saved under current directory. Thus, you can also use the Meshlab software to directly 
check the noisy and denoised PLY files.

Authors:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Zhongwei Xu [xu@noiselessimaging.com](mailto:xu@noiselessimaging.com)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Alessandro Foi 

	 
