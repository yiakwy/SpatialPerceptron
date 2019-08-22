## Installation

| Author | Contact          | Date      | Version | Action  | 
|-------:|-----------------:|----------:|--------:|--------:|
| Yi     | yiak.wy@gmail.com| 2019.5.11 | 0.1     | Created |

### Data

#### Preparation

Before downloading data, we prefer mount a external HDD in a predefined directory and make local soft links to that directory to access data.

I have observed some choatic in daily work, and decided to make it clear and document the work flow so that more poeple can benefit from my description. 

##### Ubuntu

Serveral commands useful:

1. `df` to check your file system spaces usage. Provide `-H` for verbose storage report.
2. `du` to check spaces usage for each file and directory.
3. `lsblk` list connected devices with its mounted path and total storages.
4. `parted`: creates `GPT` paritiions.

Usually we put data in `/data`. Supose this is our mount path which will be recorded in `/etc/fstab` later. GPT partitions are prefered since they have no limits of paritition size. GPT partition bould be larger than 2 TB in contrast with MBR ones created by `fdisk`.

Suppose your devices identifier is '/dev/sda', create partitions by the following instructions:

```shell  
sudo parted /dev/sda
(parted) mklable gpt
(parted) unit TB
(parted) mkpart
Partition name?  []? primary
File system type?  [ext2]? ext4
Start? 0
End? 2
(parted) print
(parted) quit
```

Once successful, you are expected to get a partition `/dev/sda1`. Modern linux filesystem uses Ext4 as data structure. Next we need to format the new partition \(or the HDD disk if you don't have one\) with specified data structure:

```shell
sudo mkfs -t ext4 /dev/sda1
```

To mount it automatically:

```shell
sudo cp /etc/fstab /etc/fstab.bak
sudo blkid /dev/sda1
/dev/sda: LABEL="NewHDD" UUID="6d6c8f68-dcc8-4a91-a510-7bca2aa71521" TYPE="ext4"
echo "
/dev/disk/by-uuid/${UUID} /data auto nosuid,nodev,nofail,x-gvfs-show,x-gvfs-name=${LABEL} 0 0
" > /etc/fstab
sudo mount /dev/sda1 /data
sudo chown -R $USERNAME:$USERNAME /data
```

Details could be found at [InstallingANewHardDrive](https://help.ubuntu.com/community/InstallingANewHardDrive).

##### MacOS Sierra

To list connected blocks using

```shell
$ diskutil list
/dev/disk0 (internal, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                        *500.3 GB   disk0
   1:                        EFI EFI                     209.7 MB   disk0s1
   2:          Apple_CoreStorage Macintosh HD            499.4 GB   disk0s2
   3:                 Apple_Boot Recovery HD             650.0 MB   disk0s3

/dev/disk1 (internal, virtual):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:                  Apple_HFS Macintosh HD           +499.0 GB   disk1
                                 Logical Volume on disk0s2
                                 EB8726F9-F423-445B-A072-3CC212C8C57B
                                 Unlocked Encrypted

/dev/disk2 (external, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
```

Data for software should be prepared in an external disk drive. Suppose the identifier is `disk2s1`. To make software consistant in different systems, we are expected to make a soft link to the data folder and make it visiable in the current file system. Since we are changing the volume name to `/data`, we need to mount it manually.

Suppose the disk is `disk2s1`, and we know that default file system in mac is of "MacOS Extended Format", do :

```shell
(tensorflow) $ diskutil unmount /dev/disk2s1
(tensorflow) $ sudo mount_hfs /dev/disk2s1 /data
(tensorflow) $ cd /data
(tensorlfow) $ ls
MacOSX		User Manual.url	autorun.inf	iphoneX-backup	machines
```

Check 

> df -lh 

to see whether you are successful. To make the mount path permanent, set entry point in `/etc/fstab`

##### Colab

Google Coab uses Ubuntu 18.04.2 LTS \(Binoic Beaver\) OS. By default there are two disks available for data storage:

```txt
Filesystem              Size  Used Avail Use% Mounted on
overlay                 359G   25G  316G   8% /
tmpfs                   6.4G     0  6.4G   0% /dev
tmpfs                   6.4G     0  6.4G   0% /sys/fs/cgroup
tmpfs                   6.4G   16K  6.4G   1% /var/colab
/dev/sda1               365G   30G  336G   8% /opt/bin
shm                     6.0G     0  6.0G   0% /dev/shm
tmpfs                   6.4G     0  6.4G   0% /sys/firmware
```

In case that more data space needed, that it often happens if you want to train different models by exploring different datasets, you need to persistent data, directories and softwares developed in a writable disk.

One of the reomote storages you could use is google driver of which storages is up to 8.0 E. bytes. 

gcloud provides you with oauth2 scheme to authenticate yourself for the google products. Once you successfully connect to the cloud, you are able to mount google drives as oridinary disks.

```jupyter
# mount google driver 

!apt-get install -y -qq software-properties-common python-software-properties module-init-tools
!add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null
!apt-get update -qq 2>&1 > /dev/null
!apt-get -y install -qq google-drive-ocamlfuse fuse

from google.colab import auth
auth.authenticate_user()
from oauth2client.client import GoogleCredentials
creds = GoogleCredentials.get_application_default()
import getpass

!google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL
vcode = getpass.getpass()
!echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}
!mkdir -p drive
!google-drive-ocamlfuse drive
```

Details can be found at [External data: Drive, Sheets, and Cloud Storage](https://colab.research.google.com/notebooks/io.ipynb#scrollTo=c2W5A2px3doP). Run the following command in jupyter 

> !df - h

```txt
Filesystem              Size  Used Avail Use% Mounted on
overlay                 359G   25G  316G   8% /
tmpfs                   6.4G     0  6.4G   0% /dev
tmpfs                   6.4G     0  6.4G   0% /sys/fs/cgroup
tmpfs                   6.4G   12K  6.4G   1% /var/colab
/dev/sda1               365G   30G  336G   8% /opt/bin
shm                     6.0G     0  6.0G   0% /dev/shm
tmpfs                   6.4G     0  6.4G   0% /sys/firmware
google-drive-ocamlfuse  8.0E  1.8G  8.0E   1% /content/drive
```

All the data and codes should be persistent in an HDD, because where the execuation of colab is in a virtual machine which is recycled when idle for a while and cannot live long.

Morover, the default root of working directory `/content` is defined on top of [docker overlay storage driver](https://docs.docker.com/storage/storagedriver/overlayfs-driver/), where the implementation of which is ensured that each time a vm starts, content written onto it is erased and you cannot see it again.

More details of implementation of docker `overlay` storage driver, and `overlay2` storage driver are described in [here](https://docs.docker.com/storage/storagedriver/overlayfs-driver/#how-the-overlay-driver-works) and [here](https://docs.docker.com/storage/storagedriver/overlayfs-driver/#how-the-overlay2-driver-works) respectively

Hence it is highly recommended by google to load data into a persistent storage via colab api.



#### Coco

```shell
git clone https://github.com/cocodataset/cocoapi ${ROOT}/Github/coco
make install -C ${ROOT}/Github/coco/PythonAPI

```

### GPU Resources

#### Local

##### Mac

```
NVIDIA GeForce GT 750M 2048 MB
Intel Iris Pro 1536 MB
```

Intel Iris Pro grpahics card will be considered for Intel  edge computing technology with cpu only devices. The gpu is just served for inference and debug purposes.

For trainnig, see remote GPU resources

##### Z370 HD3 Professional WorkStation

System configuration

| Item         | Brand    | Product Mode    | Number | Reference Price |
|-------------:|---------:|----------------:|-------:|-----------------|
| Mother board | GIGABYTE | Z370 HD3        | 1      | ~               | 
| GPU Card     | NVIDIA   | GTX 1080, 16 GB | 3      | ~               |
| CPU          | Intel    | 8 Cores, 32 GB  | 1      | ~               |
| Power        |          | 16KW            | 1      | ~               |
| Cooler       |          |                 | 1      | ~               |
| Hard Disk    |          | 2 TB            | 2      | ~               |

#### Remote

#### Google Colab

`Edit` -> `Nodebook settings`, select `hardware accelerator` type, check GPU:

> !nvidia-smi

```txt
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 418.56       Driver Version: 410.79       CUDA Version: 10.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Tesla K80           Off  | 00000000:00:04.0 Off |                    0 |
| N/A   37C    P0    70W / 149W |    121MiB / 11441MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
+-----------------------------------------------------------------------------+
```

I have prepared a demo for using Mask RCNN to detect instances in a video using colab. Click [Colab book](https://colab.research.google.com/drive/1A5ZoDc9PhYq_Rgvz8C8gPe8N5bWoo4xk) and [Github](https://github.com/yiakwy/SpatialPerceptron/blob/master/notebooks/prepare_colab.ipynb) to obtain the example running in colab from within chrome. 

#### AIStudio \(PaddlePaddle Team\)

The [AIStudio book](https://aistudio.baidu.com/aistudio/projectdetail/60969) is an anology of Colab book. Since Colab don't support build essentials and dynamic disk mounting, we build softwares manually. To obtain support of Tesla V100 (16GB memory), contact me for invitation code.

### Overview



### Installation

```shell
cd ${Project_Root}/python
pip install --upgrade setuptools
pip install --default-timeout=100 requirements.txt 
```

### Quickstart



#### Train/Test

#### Evaluation

#### Ref

