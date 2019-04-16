FROM centos:7.6.1810

LABEL maintainer "Teemu Sirviö <teemu.sirvio@fmi.fi>"

RUN yum clean all 
RUN rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm 
RUN rpm -ivh https://download.postgresql.org/pub/repos/yum/9.5/redhat/rhel-7-x86_64/pgdg-centos95-9.5-3.noarch.rpm 
RUN rpm -ivh https://download.fmi.fi/smartmet-open/rhel/7/x86_64/smartmet-open-release-17.9.28-1.el7.fmi.noarch.rpm 
RUN yum -y update 
RUN yum -y install unzip
RUN yum -y install smartmet-server
RUN yum -y install smartmet-engine-grid 
RUN yum -y install smartmet-engine-observation 
RUN yum -y install smartmet-plugin-backend
RUN yum -y install smartmet-plugin-admin
RUN yum -y install smartmet-plugin-gribtimeseries
RUN yum -y install smartmet-plugin-grid-admin
RUN yum -y install smartmet-plugin-grid-gui
# For installing filesys2smartmet which  is used to load grib-files to redis
RUN yum -y install smartmet-tools-grid
RUN yum clean all 

HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl -f http://localhost/admin?what=qengine || exit 1

# wms.conf defines imagecache. timeseriescache's use is yet to be found.
RUN mkdir -p /var/smartmet/timeseriescache /var/smartmet/imagecache

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["smartmetd"]