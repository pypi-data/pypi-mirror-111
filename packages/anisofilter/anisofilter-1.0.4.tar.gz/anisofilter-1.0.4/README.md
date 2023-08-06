# Python Wrapper for Anisotropic Denoising of 3D Point Clouds

![Image of Result noisy](http://www.cs.tut.fi/~foi/PointCloudFiltering/arma_n.jpg)
![Image of Result denoised](http://www.cs.tut.fi/~foi/PointCloudFiltering/arma_d.jpg)

A python implementation for denosing 3D point clouds with Gaussian noise, where the anisotropic neighborhoods were computed to both denoise the smooth regions and to preserve the sharp features, i.e. edges and corners.
 
The implementation is based on *Z. Xu and A. Foi, "Anisotropic Denoising of 3D Point Clouds by Aggregation of Multiple Surface-Adaptive Estimates," in IEEE Transactions on Visualization and Computer Graphics, vol. 27, no. 6, pp. 2851-2868, 1 June 2021, doi: 10.1109/TVCG.2019.2959761.*

The package contains the Anisotropic Denoising binaries compiled for:

* Windows (Win10, MinGW-64)
* Linux (Ubuntu 20.04.2 LTS, 64bit)
* Mac OSX (Big Sur, 64-bit)

The binaries are available for non-commercial use only (please see LICENSE for more details).

For the demo, see the demo folder of the full source zip, which also includes the example noisy and noise-free point clouds demonstrated in the paper. You can also download the demo from http://www.cs.tut.fi/~foi/PointCloudFiltering/pcd_anisotropic_denoi_py_demo.zip

Authors:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Zhongwei Xu [xu@noiselessimaging.com](mailto:xu@noiselessimaging.com)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Alessandro Foi
