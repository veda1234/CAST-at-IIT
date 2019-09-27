import os

import flopy
import matplotlib.pyplot as plt
import numpy as np


def numerical_model(Lx, Ly, ztop, zbot, ncol, nrow, nlay, prsity, al, trpt, Gamma, Cd, Ca, h1, h2, hk, perlen,
                    flow_bound_1, flow_bound_2, tran_bound_1, tran_bound_2, tran_bound_3, tran_bound_4):
    # Domain

    Lx = Lx
    Ly = Ly
    ztop = ztop
    zbot = zbot
    ncol = ncol
    nrow = nrow
    nlay = nlay
    delx = Lx / ncol
    dely = Ly / nrow
    delv = (ztop - zbot) / nlay

    # Parameter

    prsity = prsity
    al = al
    trpt = trpt
    Gamma = Gamma
    Cd = Cd
    Ca = Ca
    h1 = h1
    h2 = h2
    hk = hk
    perlen = perlen

    # Flow Calculation

    mf = flopy.modflow.Modflow(modelname='T02_mf')
    dis = flopy.modflow.ModflowDis(mf, nlay=nlay, nrow=nrow, ncol=ncol, delr=delx, delc=dely, top=0, botm=[0 - delv],
                                   perlen=perlen)

    ibound = np.ones((nlay, nrow, ncol), dtype=np.int32)
    ibound[:, :, 0] = flow_bound_1
    ibound[:, :, -1] = flow_bound_2
    strt = np.ones((nlay, nrow, ncol), dtype=np.float32)
    strt[:, :, 0] = h1
    strt[:, :, -1] = h2

    bas = flopy.modflow.ModflowBas(mf, ibound=ibound, strt=strt)
    lpf = flopy.modflow.ModflowLpf(mf, hk=hk, laytyp=0)
    gmg = flopy.modflow.ModflowGmg(mf)
    lmt = flopy.modflow.ModflowLmt(mf)

    mf.write_input()
    mf.run_model(silent=True)

    # Transport Calculation

    mt = flopy.mt3d.Mt3dms(modelname='T02_mt', exe_name='mt3dms5b', modflowmodel=mf)

    icbund = np.ones((nlay, nrow, ncol), dtype=np.int32)
    icbund[:, :, 0] = tran_bound_1  # first column
    icbund[:, :, -1] = tran_bound_2  # last column
    icbund[:, 0, :] = tran_bound_3  # first row
    icbund[:, 0, 0] = tran_bound_4  # first cell
    sconc = np.zeros((nlay, nrow, ncol), dtype=np.float32)
    sconc[:, :, 0] = (Gamma * Cd) + 2 * abs(Ca)
    sconc[:, :, -1] = Ca + 2 * abs(Ca)
    sconc[:, 0, :] = Ca + 2 * abs(Ca)
    sconc[:, 0, 0] = 2 * abs(Ca)

    btn = flopy.mt3d.Mt3dBtn(mt, icbund=icbund, prsity=prsity, sconc=sconc)
    adv = flopy.mt3d.Mt3dAdv(mt, mixelm=-1)
    dsp = flopy.mt3d.Mt3dDsp(mt, al=al, trpt=trpt)
    gcg = flopy.mt3d.Mt3dGcg(mt)
    ssm = flopy.mt3d.Mt3dSsm(mt)

    mt.write_input()
    mt.run_model(silent=True)

    ucnobj = flopy.utils.UcnFile('MT3D001.UCN')
    conc = ucnobj.get_alldata()
    mvt = mt.load_mas('MT3D001.MAS')

    plt.figure(figsize=(10, 10))
    mm = flopy.plot.map.PlotMapView(model=mf)
    mm.plot_grid(color='.5', alpha=0.2)
    conc = conc[0, :, :]
    cs = mm.contour_array(conc, levels=[16.], colors=['k'])
    mm.plot_ibound()
    plt.clabel(cs)
    plt.xlabel('DISTANCE ALONG X-AXIS, IN METERS')
    plt.ylabel('DISTANCE ALONG Y-AXIS, IN METERS')
    plt.title('ULTIMATE')

    # Plume length

    p1 = cs.collections[0].get_paths()[0]
    coor_p1 = p1.vertices
    plume_length = np.max(coor_p1[:, 0])

    # clear up all memory
    ucnobj.close()
    os.remove("T02_mf.bas")
    os.remove("T02_mf.dis")
    os.remove("T02_mf.gmg")
    os.remove("T02_mf.list")
    os.remove("T02_mf.lmt6")
    os.remove("T02_mf.lpf")
    os.remove("T02_mf.nam")
    os.remove("T02_mt.adv")
    os.remove("T02_mt.btn")
    os.remove("T02_mt.dsp")
    os.remove("T02_mt.gcg")
    os.remove("T02_mt.list")
    os.remove("T02_mt.nam")
    os.remove("T02_mt.ssm")
    os.remove("MT3D001.UCN")
    os.remove("MT3D001.MAS")
    os.remove("MT3D.CNF")
    os.remove("mt3d_link.ftl")
    return plume_length


lmax = numerical_model()
print(lmax)
