# Photon identification with the FASER upgraded preshower
# Introduction 
The particle that composes light, the **photon**, is a particle that does not carry any mass but interacts with matter.  
There are several reasons to think that there might be a new particle (often referred to as ALP) that decays (this is the way we call when a particle *converts itself*) into two photons. 
The current FASER detector, located at CERN, is not capable of identifying separately two photons, therefore a detector upgrade (*preshower upgrade*), was designed to achieve this goal.  
The preshower upgrade is essentialy a (silicon) detector with high granularity. In this way, the detector will be able to *count* photons.  
There are other processes in physics that may *fake* a real two photon signal, which I will call backgrounds. The main background is composed of neutrinos (another type of particle). These neutrinos can interact with the detector and leave signals that may mimic the ones left by two photons. 
The goal of the project is to develop a machine learning approach to be able to distinguish between photons and 

# Basic physics to understand the problem 
Photons ($\gamma$) interact with matter in a different way depending on their energy. At the energies of interest the photons will mainly interact via photon conversion. In this reaction, a photon interacts with the nuclei of the target material and converts into an electron ($e^-$) and positron (the antiparticle of the electron, $e^+$). These electrons and positrons can further emit photons, which will again convert into e+e- pairs, and thus creating a chain reaction. This is an example of a particle shower. An sketch of the production of this shower can be seen in the following image. 

![alt text](https://github.com/sabateri/photon_identification_FASER/images/photon_shower.png "Particle shower created by a photon")  

A neutrino may also create one of these particle showers, mimicking 