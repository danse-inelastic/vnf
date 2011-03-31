# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


Fermi_nu = 600
T0_nu = 120
nrad = 0.5801
nchans = 31
T0_off = 0
Edes = 60



SE2V = 437.3949

#/*set lengths defined above */
LT0=8.77;LF=11.61;LM1=11.82;LM2=18.50;LS=13.61;L3=3.5;

from math import *
ch_x=log10(Edes*1e-3);
ch_y=-0.4420*ch_x*(1+tanh((ch_x+1.1197)/0.4042))/2-0.1235*ch_x*(1-tanh((ch_x+1.1197)/0.4042))/2-0.4189*tanh((ch_x+1.1197)/0.4042)+0.5612;
# toffset=0.0;
toffset=pow(10,ch_y)/1.0e6;
#  /*set phases for the critical lengths */
phasefc1=(LF)/(sqrt(Edes)*SE2V)+toffset;
phase_T0=(LT0)/(sqrt(Edes)*SE2V)+toffset;
phase_sam=(LS)/(sqrt(Edes)*SE2V)+toffset;
phase_det=(LS+L3)/(sqrt(Edes)*SE2V)+toffset;
phase_m1=(LM1)/(sqrt(Edes)*SE2V)+toffset;
phase_m2=(LM2)/(sqrt(Edes)*SE2V)+toffset;
# /* set parameters for guide reflectivity profile */
Gu_R=0.98;Gu_alpha=5.5;Gu_m=3.6;Gu_Qc=0.02;Gu_W=2e-3;
#  /* set energy range to examine  set to +/- 20% of Edes value*/
Emin=Edes*0.8;Emax=Edes*1.2;
#//tplotw=((0.06-0.0005)/nchans-0.0005)/(4.0*PI*Fermi_nu*0.05)*4.0;
tplotmin=LM1/(sqrt(Emax)*SE2V)+toffset;
tplotmax=LM1/(sqrt(Emin)*SE2V)+toffset;



from vnfb.dom.neutron_experiment_simulations.neutron_components.SNSModeratorMCSimulatedData\
     import SNSModeratorMCSimulatedData


from vnfb.dom.neutron_experiment_simulations.neutron_components.SNSModerator import SNSModerator
from vnfb.dom.neutron_experiment_simulations.neutron_components.TofMonitor import TofMonitor
from vnfb.dom.neutron_experiment_simulations.neutron_components.ChanneledGuide import ChanneledGuide
from vnfb.dom.neutron_experiment_simulations.neutron_components.NeutronRecorder import NeutronRecorder
from vnfb.dom.neutron_experiment_simulations.neutron_components.T0Chopper import T0Chopper
from vnfb.dom.neutron_experiment_simulations.neutron_components.FermiChopper import FermiChopper

def moderator():
    c = SNSModerator()
    c.short_description = 'Moderator for ARCS'
    c.width=0.1
    c.height=0.12
    c.dist=2.5
    c.xw=0.1
    c.yh=0.12
    c.Emin=Emin
    c.Emax=Emax
    # c.neutronprofile = moderator_data
    return c


def core_ves():
    c = ChanneledGuide()
    c.short_description = 'Core vessel insert'
    c.w1=0.094285
    c.h1=0.11323
    c.w2=0.084684
    c.h2=0.102362
    c.l=1.2444
    c.R0=0.0
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def shutter_guide():
    c = ChanneledGuide()
    c.short_description = 'shutter guide'
    c.w1=0.074930
    c.h1=.094040
    c.w2=0.070880
    c.h2=0.086880
    c.l=1.853
    c.R0=Gu_R
    c.mx=2.5
    c.my=2.5
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def guide_1_1_1():
    c = ChanneledGuide()
    c.short_description = 'guide 1_1_1'
    c.w1=0.07088
    c.h1=0.08688
    c.w2=0.07019
    c.h2=0.08573
    c.l=0.48354
    R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def guide_1_1_2():
    c = ChanneledGuide()
    c.short_description = 'guide 1_1_2'
    c.w1=0.07019
    c.h1=0.08573
    c.w2=0.06947
    c.h2=0.08454
    c.l=0.48354
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def guide_1_1_3():
    c = ChanneledGuide()
    c.short_description = 'guide 1_1_3'
    c.w1=0.06947
    c.h1=0.08454
    c.w2=0.06871
    c.h2=0.08329
    c.l=0.48354
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def guide_1_2_1():
    c = ChanneledGuide()
    c.short_description = 'guide 1_2_1'
    c.w1=0.06871
    c.h1=0.08329
    c.w2=0.06792
    c.h2=0.08197
    c.l=0.48354
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def guide_1_2_2():
    c = ChanneledGuide()
    c.short_description = 'guide 1_2_2'
    c.w1=0.06792
    c.h1=0.08197
    c.w2=0.06710
    c.h2=0.08060
    c.l=0.48354
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def guide_1_2_3():
    c = ChanneledGuide()
    c.short_description = 'guide 1_2_3'
    c.w1=0.06710
    c.h1=0.08060
    c.w2=0.06624
    c.h2=0.07917
    c.l=0.48354
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def guide_1_3_1():
    c = ChanneledGuide()
    c.short_description = 'guide 1_3_1'
    c.w1=0.06624
    c.h1=0.07917
    c.w2=0.06534
    c.h2=0.07766
    c.l=0.48354
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def guide_1_3_2():
    c = ChanneledGuide()
    c.short_description = 'guide 1_3_2'
    c.w1=0.06534
    c.h1=0.07766
    c.w2=0.06440
    c.h2=0.07609
    c.l=0.48354
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def guide_1_3_3():
    c = ChanneledGuide()
    c.short_description = 'guide 1_3_3'
    c.w1=0.06440
    c.h1=0.07609
    c.w2=0.06342
    c.h2=0.07443
    c.l=0.48354
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def t0_chopp():
    c = T0Chopper()
    c.short_description = 'T0 chopper'
    c.len=0.474
    c.w1=0.08
    c.w2=0.101
    c.nu=T0_nu
    c.delta=0.0
    c.tc=phase_T0
    c.ymin=-0.045
    c.ymax=0.045
    return c


def guide_2_1():
    c = ChanneledGuide()
    c.short_description = 'guide 2_1'
    c.w1=0.06136
    c.h1=0.07094
    c.w2=0.06044
    c.h2=0.06936
    c.l=0.40204
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def guide_2_2():
    c = ChanneledGuide()
    c.short_description = 'guide 2_2'
    c.w1=0.06044
    c.h1=0.06936
    c.w2=0.05948
    c.h2=0.06771
    c.l=0.40204
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c
    

def guide_2_3():
    c = ChanneledGuide()
    c.short_description = 'guide 2_3'
    c.w1=0.05948
    c.h1=0.06771
    c.w2=0.05848
    c.h2=0.06598
    c.l=0.40204
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def guide_2_4():
    c = ChanneledGuide()
    c.short_description = 'guide 2_4'
    c.w1=0.05848
    c.h1=0.06598
    c.w2=0.05745
    c.h2=0.06417
    c.l=0.40204
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def guide_2_5():
    c = ChanneledGuide()
    c.short_description = 'guide 2_5'
    c.w1=0.05745
    c.h1=0.06417
    c.w2=0.05637
    c.h2=0.06227
    c.l=0.40204
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c



def fermi_chopp():
    c = FermiChopper()
    c.short_description = 'Fermi chopper'
    c.len=0.10
    c.w=0.060364
    c.ymin=-.0325
    c.ymax=.0325
    c.nu=Fermi_nu
    c.delta=0.0
    c.tc=phasefc1
    c.nchan=nchans
    c.bw=0.00041
    c.blader=nrad
    return c


def tofmonitor1():
    c = TofMonitor()
    c.short_description = 'Monitor #1'
    c.x_min=-0.035
    c.x_max=0.035
    c.y_min=-0.035
    c.y_max=0.035
    c.tmin=tplotmin
    c.tmax=tplotmax
    c.nchan=100
    return c


def guide_3():
    c = ChanneledGuide()
    c.short_description = 'guide 3'
    c.w1=0.05536
    c.h1=0.06046
    c.w2=0.05473
    c.h2=0.05931
    c.l=0.225
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def guide_4_1():
    c = ChanneledGuide()
    c.short_description = 'guide 4_1'
    c.w1=0.05468
    c.h1=0.05924
    c.w2=0.05331
    c.h2=0.05674
    c.l=0.46275
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def guide_4_2():
    c = ChanneledGuide()
    c.short_description = 'guide 4_2'
    c.w1=0.05331
    c.h1=0.05674
    c.w2=0.05187
    c.h2=0.05408
    c.l=0.46275
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c


def guide_5():
    c = ChanneledGuide()
    c.short_description = 'guide 5'
    c.w1=0.05186
    c.h1=0.05405
    c.w2=0.05062
    c.h2=0.05172
    c.l=0.37920
    c.R0=Gu_R
    c.mx=Gu_m
    c.my=Gu_m
    c.Qcx=Gu_Qc
    c.Qcy=Gu_Qc
    c.W=Gu_W
    c.k=1
    c.d=0.0
    c.alphax=Gu_alpha
    c.alphay=Gu_alpha
    return c



def neutron_recorder():
    c = NeutronRecorder()
    c.short_description = 'neutron recorder at sample position of ARCS'
    return c



def tofmonitor2():
    c = TofMonitor()
    c.short_description = 'Monitor #2'
    c.x_min=-0.035
    c.x_max=0.035
    c.y_min=-0.035
    c.y_max=0.035
    c.tmin=0
    c.tmax=0.016
    c.nchan=1600
    return c




def createInstrument(director):
    mod = moderator()
    # the default neutron profile is initd at content/components/initdb/snsmoderatormcsimulateddata.odb
    # this means the snsmoderatormcsimulateddata table should be initd before instruments
    # table
    mod.neutronprofile = director.clerk.orm.load(
        SNSModeratorMCSimulatedData, 'sct521_bu_17_1-ARCS')
    
    from _utils import ccomp, cinstr
    components = [
        ccomp('moderator', mod, ((0,0,0), (0,0,0), '')),
        ccomp('core_ves', core_ves(), ((0,0,1.0106), (0,0,0), '')),
        ccomp('shutter_guide', shutter_guide(), ((0,0,2.26790), (0,0,0), '')),
        ccomp('guide_1_1_1', guide_1_1_1(), ((0,0,4.17230), (0,0,0), '')),
        ccomp('guide_1_1_2', guide_1_1_2(), ((0,0,4.65589), (0,0,0), '')),
        ccomp('guide_1_1_3', guide_1_1_3(), ((0,0,5.13948), (0,0,0), '')),
        ccomp('guide_1_2_1', guide_1_2_1(), ((0,0,5.62331), (0,0,0), '')),
        ccomp('guide_1_2_2', guide_1_2_2(), ((0,0,6.10690), (0,0,0), '')),
        ccomp('guide_1_2_3', guide_1_2_3(), ((0,0,6.59049), (0,0,0), '')),
        ccomp('guide_1_3_1', guide_1_3_1(), ((0,0,7.07433), (0,0,0), '')),
        ccomp('guide_1_3_2', guide_1_3_2(), ((0,0,7.55792), (0,0,0), '')),
        ccomp('guide_1_3_3', guide_1_3_3(), ((0,0,8.04145), (0,0,0), '')),
        ccomp('t0_chopp', t0_chopp(), ((0,0,8.77), (0,0,0), '')),
        ccomp('guide_2_1', guide_2_1(), ((0,0,9.47504), (0,0,0), '')),
        ccomp('guide_2_2', guide_2_2(), ((0,0,9.87713), (0,0,0), '')),
        ccomp('guide_2_3', guide_2_3(), ((0,0,10.27922), (0,0,0), '')),
        ccomp('guide_2_4', guide_2_4(), ((0,0,10.68131), (0,0,0), '')),
        ccomp('guide_2_5', guide_2_5(), ((0,0,11.08340), (0,0,0), '')),
        ccomp('fermi_chopp', fermi_chopp(), ((0,0,11.61), (0,0,0), '')),
        ccomp('tofmonitor1', tofmonitor1(), ((0,0,11.831), (0,0,0), '')),
        ccomp('guide_3', guide_3(), ((0,0,11.84975), (0,0,0), '')),
        ccomp('guide_4_1', guide_4_1(), ((0,0,12.08825), (0,0,0), '')),
        ccomp('guide_4_2', guide_4_2(), ((0,0,12.55105), (0,0,0), '')),
        # ccomp('guide_5', guide_5(), ((0,0,13.01830), (0,0,0), '')),
        ccomp('neutron_recorder', neutron_recorder(), ((0,0,13.5), (0,0,0), '')),
        ccomp('tofmonitor2', tofmonitor2(), ((0,0,18.5), (0,0,0), '')),
        ]


    instrument = cinstr(
        director,
        name = 'ARCS_beam_withmonitor2',
        short_description = 'ARCS instrument down to the sample position',
        long_description = '''ARCS is a wide Angular-Range, direct-geometry, time-of-flight Chopper Spectrometer at the Spallation Neutron Source. It is optimized to provide a high neutron flux at the sample, and a large solid angle of detector coverage.
        This virtual instrument simulates neutrons being emitted from moderator and going through neutron optics of ARCS until they reach the sample position. Those neutrons are then saved and can be used to study inelastic neutron scattering of samples later.
        ''',
        category = 'ins',
        creator = 'vnf',
        date = '08/09/2010',
        components = components
        )
    
    return instrument


# obsolete
"""
    # set up neutron profile for moderator
    orm = director.clerk.orm
    datarecord = orm(moderator_data)
    dds = director.dds
    dest = dds.abspath(datarecord)

    srcdata = orm(SNSModeratorMCSimulatedData())
    srcdata.id = 'sct521_bu_17_1-ARCS'
    src = dds.abspath(srcdata)

    import shutil, os
    # create dest dir if necessary
    if not os.path.exists(dest): os.makedirs(dest)
    # copy files
    for f in srcdata.datafiles:
        shutil.copyfile(os.path.join(src, f), os.path.join(dest, f))
        continue
"""

# version
__id__ = "$Id$"

# End of file 
