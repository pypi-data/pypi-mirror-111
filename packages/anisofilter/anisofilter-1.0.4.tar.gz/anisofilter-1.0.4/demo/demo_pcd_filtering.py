"""
This is a demo programme to implement the algorithm proposed in:  

Z. Xu and A. Foi, "Anisotropic Denoising of 3D Point Clouds by Aggregation of Multiple 
Surface-Adaptive Estimates," in IEEE Transactions on Visualization and Computer Graphics, 
vol. 27, no. 6, pp. 2851-2868, 1 June 2021, doi: 10.1109/TVCG.2019.2959761.    

Copyright (c) 2019-2021 Noiseless Imaging Oy (Ltd).
All rights reserved.
This work (software, material, and documentation) shall only
be used for nonprofit noncommercial purposes.
Any unauthorized use of this work for commercial or for-profit purposes
is prohibited.
"""

import sys
import time
import numpy as np
from anisofilter import utilities as UTI
from anisofilter import anisofilter 
from mayavi import mlab


def demo():
    print("========== System Info ==========")
    print("Python version: "+sys.version)
    print("Numpy version: "+np.__version__)
    print("=================================")

    ###############  noisy and noise-free pcds  ###############
    #pcd_ori = UTI.read_ply_single_class("Fandisk_ori.ply")
    #pcd = UTI.read_ply_single_class("Fandisk_noisy0_2delta.ply")

    #pcd_ori = UTI.read_ply_single_class("Bunny_ori.ply")
    #pcd = UTI.read_ply_single_class("Bunny_noisy0_2delta.ply")

    #pcd_ori = UTI.read_ply_single_class("Armadillo_ori.ply")
    #pcd = UTI.read_ply_single_class("Armadillo_noisy0_2delta.ply")

    #pcd_ori = UTI.read_ply_single_class("Cube49_ori.ply")
    #pcd = UTI.read_ply_single_class("cube49_noisy0_4delta.ply")

    #pcd_ori = UTI.read_ply_single_class("Sphere_ori.ply")
    #pcd = UTI.read_ply_single_class("Sphere_noisy0_4delta.ply")

    pcd_ori = UTI.read_ply_single_class("Dodecahedron_ori.ply")
    pcd = UTI.read_ply_single_class("Dodecahedron_noi.ply")
    print("Number of points = " + str(len(pcd)))

    start_time = time.time()
    sigma_pcd, dens_pcd = UTI.pcd_std_est(pcd)
    print("sigma_pcd = " + str(sigma_pcd))
    print("dens_pcd = " + str(dens_pcd))
    print("--- pcd std estimation took %.5f seconds ---" % (time.time() - start_time))

    start_time = time.time()
    pcd_de_m2c = anisofilter.anisofilter(pcd, sigma_pcd, dens_pcd)
    print(">>> Total filtering time is %.5f seconds <<<" % (time.time() - start_time))

    # compute Mean squared point-to-surface distance (not compiled)
    RSMSE_p2s = UTI.square_root_mean_point2surf_error(pcd_de_m2c, pcd_ori)
    print('>>> Root mean squared point-to-surface distance = %.5f <<<' % RSMSE_p2s)

    # write to ply file
    UTI.write_ply_only_pos(pcd_de_m2c, "pcd_denoi.ply")
    print(">>> Denoised point cloud is SAVED in PLY format in current file directory. <<<")

    fig1 = mlab.figure(bgcolor=(0, 0, 0), size=(512, 512))
    mlab.points3d(pcd[:, 0], pcd[:, 1], pcd[:, 2],
                  mode="point",
                  color=(0, 1, 0),
                  figure=fig1)
    fig2 = mlab.figure(bgcolor=(0, 0, 0), size=(512, 512))
    mlab.points3d(pcd_de_m2c[:, 0], pcd_de_m2c[:, 1], pcd_de_m2c[:, 2],
                  mode="point",
                  color=(0, 1, 0),
                  figure=fig2)
    mlab.show()

    #return pcd_de_m2c, RSMSE_p2s

demo()
