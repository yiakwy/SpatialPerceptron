#!/bin/bash

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}"  )/.." && pwd )"

pwd
echo "ROOT: $ROOT"

# install huawei cloud modelarts SDK
# https://support.huaweicloud.com/sdkreference-modelarts/modelarts_04_0004.html
SDK="modelarts-1.1.1-py2.py3-none-any.whl"
if [ ! -f $SDK ]; then
wget https://modelarts-sdk.obs.cn-north-1.myhwclouds.com/modelarts-1.1.1-py2.py3-none-any.whl
fi

pip3 install Cython
pip3 install -U setuptools
pip3 install $SDK

# import libraries
source "utils.sh"

function Init_SDK() {
 info "initiating ModelArts SDK env ..."
 mkdir -p ~/.modelarts/config
 PYTHON_PKG=$( python3 -m site --user-site )
 info "modelarts installed in $PYTHON_PKG."
 info "copying config.json to ~/.modelarts/config"
 cp $PYTHON_PKG/modelarts/config/config.json ~/.modelarts/config
 info "done"

}

Init_SDK

