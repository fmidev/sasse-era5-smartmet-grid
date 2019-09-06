# Container for Python related contouring tasks
# For using this miniconda image everything done here, 
# is done as the user from miniconda3 image "anaconda"
FROM continuumio/miniconda3:4.7.10-alpine

# The PATH is borked, fix it here, until it is fixed on github
ENV PATH /opt/conda/bin:$PATH

# Use anacondas home directory in order to have 
# write permissions to create a subdir with write permissions
# The subdirectory needs to be writeable by anaconda for pytest 
ARG mydir=/home/anaconda/app
RUN mkdir -p ${mydir}

COPY --chown=anaconda:anaconda . ${mydir}

WORKDIR ${mydir}

# Install proj as a dependency for owslib (in setup.py).
# The proj from pip has issues and problems and horrifying things
# when installing. THe conda version installs without any trouble at all.
# https://proj.org/install.html#conda
RUN conda install -c conda-forge proj4

# Lastly in stall the app itself
RUN pip install .