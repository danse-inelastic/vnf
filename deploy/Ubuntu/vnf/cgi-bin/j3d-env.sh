J3D_LIBDIR=/home/linjiao/Downloads/java3d-1_5_0-linux-i586/lib
export CLASSPATH=.:$J3D_LIBDIR/ext/j3dcore.jar:$J3D_LIBDIR/ext/j3dutils.jar:$J3D_LIBDIR/ext/vecmath.jar:$CLASSPATH
export LD_LIBRARY_PATH=$J3D_LIBDIR/i386:$LD_LIBRARY_PATH
EXPORT_ROOT=/home/vnf/dv/danse/buildInelast/web-vnf/EXPORT
export CLASSPATH=$EXPORT_ROOT/java:$CLASSPATH
