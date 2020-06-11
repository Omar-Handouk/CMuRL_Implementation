# Congestion management using reinforcement learning
### Preface
This project is aimed to studying the possibility of utilizing reinforcement learning to handle network congestion.

We use a version of [TCP Cubic](https://www.cs.princeton.edu/courses/archive/fall16/cos561/papers/Cubic08.pdf) in which
has it parameters exposed _Beta, TCP Friendliness, Fast Convergence_ with an additional _alpha_ parameter.

We utilize [Proximal Policy Optimization](https://arxiv.org/abs/1707.06347) to fine tune these parameters to handle
congestion conditions.
___
### Perquisites

- Ubuntu Server 16.04, Linux Kernel 4.4 (One for server and one for client)
  - Machine must have at least 15 GB of storage and 2 GB of RAM
- OpenMPI
- Miniconda 3
- TCPTuner
- WonderShaper
- Git
- iperf3
___
### How to setup environment

- Update Ubuntu server
```shell script
$ sudo apt update && sudo apt upgrade
```
- Install Git, Linux kernel headers, Build-essentials, libsm6, libxrender1, libfontconfig1, OpenMPI & iperf3
```shell script
$ sudo apt install git linux-headers-$(uname -r) build-essential libsm6 libxrender1 libfontconfig1 openmpi-bin openmpi-doc libopenmpi-dev iperf3
```
- Install Miniconda and add Miniconda bin to path
```shell script
$ cd ~
$ mkdir miniInstall
$ cd miniInstall
$ curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh --output Miniconda3-latest-Linux-x86_64.sh
$ chmod 755 Miniconda3-latest-Linux-x86_64.sh
$ ./Miniconda3-latest-Linux-x86_64.sh
$ echo 'PATH=$HOME/miniconda3/bin:$PATH' >> ~/.bashrc
```
- Install TCPTuner and set congestion algorithm to tuner
```shell script
$ cd ~
$ git clone https://github.com/Gasparila/TCPTuner
$ cd TCPTuner
$ cd module/
$ make
$ sudo rmmod tcp_tuner.ko
$ sudo insmod tcp_tuner.ko
$ sudo sysctl -w net.ipv4.tcp_congestion_control=tuner
```
___
### Setting up CMuRL

- Cloning repo
```shell script
$ git clone ssh://git@github.com:Omar-Handouk/CMuRL_Implementation.git
```
- Creating a new Anaconda Environment
```shell script
$ conda create --name CMuRL python=3.7
```
- Installing requirements
```shell script
$ pip install -r requirment.txt
```
___
### Running the experiment

- Run an iperf server on a remote machine
```shell script
$ iperf3 -s
```
- Run client on host machine
```shell script
$ ./scripts/client.sh
```
- Train the model and run it
```shell script
$ python main.py
```