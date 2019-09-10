# Container for Python related contouring tasks
#
# Miniconda provides the conda dependency manager that handles 
# requirements for scientific packages a bit better than pip
#
# The user name and group "anaconda" is inherited from the
# miniconda3 docker image.
FROM continuumio/miniconda3:4.7.10-alpine

# The PATH is borked, fix it here, until it is fixed on github
# https://github.com/ContinuumIO/docker-images/pull/139
ENV PATH /opt/conda/bin:$PATH

# Install proj as a dependency for owslib (in setup.py).
# The proj from pip has issues and problems and horrifying things
# when installing. THe conda version installs without any trouble at all.
# https://proj.org/install.html#conda
RUN conda install -c conda-forge proj4

# Use anaconda's home directory in order to have 
# write permissions to create a subdir with write permissions
# The subdirectory needs to be writeable by anaconda for
# running pytest
ARG mydir=/home/anaconda/app
RUN mkdir -p ${mydir}
WORKDIR ${mydir}

# Copy required files incrementally and tests
COPY --chown=anaconda:anaconda setup.py .
COPY --chown=anaconda:anaconda src src
COPY --chown=anaconda:anaconda tests tests

# Lastly in stall the app itself
RUN pip install .
