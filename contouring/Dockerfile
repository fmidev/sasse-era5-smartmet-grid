# Container for Python related contouring tasks
#
# Miniconda provides the conda dependency manager that handles 
# requirements for scientific packages a bit better than pip
#
# The user name and group "anaconda" is inherited from the
# miniconda3 docker image.
# FROM continuumio/miniconda3:4.7.10
FROM python:3.7.4

# The PATH is borked, fix it here, until it is fixed on github
# https://github.com/ContinuumIO/docker-images/pull/139
# ENV PATH /opt/conda/bin:$PATH


# This is not necessary with miniconda, the environment can handle 
# pyproj installation as a dependency for owslib
# Install proj4 because it is required by a projects dependency owslib (in setup.py).
# The proj from pip has issues and problems and horrifying things
# when installing. The conda version installs without any trouble at all.
# https://proj.org/install.html#conda
# RUN conda install -c conda-forge proj4

# 
# RUN conda install proj4

# RUN addgroup anaconda

# RUN useradd  --uid 10151 --user-group --create-home johnsson
# USER johnsson


# Use anaconda's home directory in order to have 
# write permissions to create a subdir with write permissions
# The subdirectory needs to be writeable by anaconda for
# running pytest
# ARG mydir=/home/johnsson
# RUN mkdir -p ${mydir}

# WORKDIR /home/johnsson

# RUN python3 -m venv myenv

# WORKDIR myenv

ARG mydir=/opt/app
RUN mkdir -p ${mydir}
WORKDIR ${mydir}


# Copy required files incrementally and tests
# Copy without arguments will have files owned by root
COPY setup.py .
COPY src src
COPY tests tests
# COPY --chown=johnsson:johnsson setup.py .
# COPY --chown=johnsson:johnsson src src
# COPY --chown=johnsson:johnsson tests tests

# RUN . ~/myenv/bin/activate && pip install  .
RUN pip install .

# Lastly in stall the app itself
# We are using 'pip' in conda environment and it may be possible that there can
# be some issues. 
# RUN pip install  .

# ENV PATH /home/johnsson/.local/bin:$PATH
# build a virtualenv

# contour_storm --verbose --starttime 2017-08-01T00:00:00 --url http://smartmet-server:8080/wfs  --storedquery_id windgustcoverage --limits 10,15