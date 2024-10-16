# MPFUZZ

This document provides the instructions to reproduce 2 experiments of MPFUZZ, namely experiment E1 and experiment E2 as described below. 

For more details of MPFUZZ please refer to the paper "Understanding Ethereum Mempool Security under Asymmetric DoS by Symbolized Stateful Fuzzing" published in USENIX'24: https://www.usenix.org/conference/usenixsecurity24/presentation/wang-yibo. The artifact details is described in USENIX Security ’24 Artifact Appendix: Understanding Ethereum Mempool Security under Asymmetric DoS by Symbolized Stateful Fuzzing. This work is licensed under a Creative Commons Attribution 4.0 International License. To view a copy of this license, visit https://creativecommons.org/licenses/by/4.0/.


## Experiment set-up:

To evaluate the artifact, no specific CPU hardware is required. While the artifact does not have a minimum requirements for memory and storage, higher capacities are advantageous for improving overall performance. (The author uses Intel i7-7700k CPU of 4 cores and 64 GB RAM.)

The artifact is designed to operate on Unix-like operating systems. (The author uses Ubuntu 22.04.)

As the foundational environment for our artifact’s execution, Python version 3.9 or later must be installed. Additionally, a few Python libraries are essential to its operation include web3, numpy, pandas, and graphviz.

1. After downloading all the files in the figshare project https://doi.org/10.6084/m9.figshare.26068909.v5, unzip the key_new.zip, keep the unzipped folder with the same name as ./key_new/

2. unzip the go-ethereum-1.10.11.zip, keep the unzipped folder with the same name as ./go-ethereum-1.10.11/

3. build the author-modified version of Geth via the following command:
$ make -C go-ethereum-1.10.11
$ cp go-ethereum-1.10.11/build/bin/geth ./geth
 
3. Make the start Ethereum script executable via the following command:
$ chmod +x ./start_ethereum.sh
$ chmod +x ./start_ethereum_e2a.sh
$ chmod +x ./start_ethereum_e2b.sh

4. Install the required Python libraries using the pip command:
$ pip3 install web3 numpy pandas graphviz


## Experiment E1: Reproduce the fuzzing results against a 4 slots Ethereum mempool. 

The experimental results validate the Major Claims C1 and C2 described in the USENIX Security ’24 Artifact Appendix: Understanding Ethereum Mempool Security under Asymmetric DoS by Symbolized Stateful Fuzzing. The experiment costs around 15 seconds compute-time.

1. In terminal 1, run the script in the current directory. 

In terminal 1
$./start_ethereum.sh

2. Wait for around 5 seconds to let the Ethereum node start, open a new terminal, say terminal 2, in the current directory to run the python script. It requires you have installed python 3.9 and dependencies, namely numpy, pandas, web3 and graphviz.

In terminal 2
$python3 mpfuzz.py    

After the Python script terminates, a PDF file is generated that reports the experimental results. In the PDF, nodes highlighted in yellow represent the end states of exploits, indicating that these states trigger the bug oracle. The path from the root node to the leaf node that triggers the bug oracle illustrates the exploit transaction sequence. The concrete exploit transaction sequence is also output in the Python console, allowing users to reproduce the attacks. Additionally, the tree structure in the PDF file shows the process that MPFUZZ explores the search space.




## Experiment E2: Reproduce the performance evaluation of detecting the first exploit.

The experimental results validate the Major Claims C3 described in the USENIX Security ’24 Artifact Appendix: Understanding Ethereum Mempool Security under Asymmetric DoS by Symbolized Stateful Fuzzing. The experiment costs less than a minute compute-time.

Experiment E2a: Finding exploit against 6-slot mempool

1. In terminal 1, run the script in the current directory. 

In terminal 1
$./start_ethereum_e2a.sh

2. Wait for around 5 seconds to let the Ethereum node start, open a new terminal, say terminal 2, in the current directory to run the python script.

In terminal 2
$python3 mpfuzz_e2a.py

After the Python script terminates, the concrete exploit transaction sequence of the XT3 exploit found is output in the Python console as well as the time used to find it.    

Experiment E2b: Finding exploit against 16-slot mempool

1. In terminal 1, run the script in the current directory. 

In terminal 1
$./start_ethereum_e2b.sh

2. Wait for around 5 seconds to let the Ethereum node start, open a new terminal, say terminal 2, in the current directory to run the python script.

In terminal 2
$python3 mpfuzz_e2b.py

After the Python script terminates, the concrete exploit transaction sequence of the XT3 exploit found is output in the Python console as well as the time used to find it.  




## MPFUZZ with epsilon configuration: 

Running MPFUZZ with various epsilon under 16 slots mempool. We set a 16-hour time-out for the experiment. Each of the experiment costs around 16 hours compute-time.

1. In terminal 1, run the script in the current directory after making the script executable. 

In terminal 1
$ chmod +x ./start_ethereum_e3.sh
$./start_ethereum_e3.sh

In terminal 2, run the python script with a specific value of epsilon as arguments, e.g., 0.09
$python3 mpfuzz_epsilon.py 0.09

After the Python script terminates, the concrete exploit transaction sequence of the exploit found under the given value of epsilon is output in the Python console.  
