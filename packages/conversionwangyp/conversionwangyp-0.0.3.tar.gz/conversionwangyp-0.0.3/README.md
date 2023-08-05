# 概括
本代码为pytorch model 转化 onnx model 工具
## 说明
本包名字为*modelhub*,使用方法包括...

### 打包方法
cd /package
python setup.py sdist
pip install twine
twine upload dist/conversionwangyp-0.0.1.tar.gz

### 安装方法
pip install conversionwangyp

### 使用方法
from conversion.pth2onnx import run_pth2onnx

### 参数说明
1.直接传入加载好weight的模型去转换onnx
run_pth2onnx(model, batch_size, onnx_export_path, input_shape)
其中 model：带有网络结构和参数的模型
    batch_size：batch的大小
    onnx_export_path：导出模型的路径
    input_shape：模型的输入
2.先加载模型再转化onnx
load_model_pth2onnx(pth_model_path, batch_size , onnx_export_path, input_shape, network=None)
其中 pth_model_path：pth模型的存放路径
    network：模型的网络结构（不含weight）
3.评测pth模型和onnx模型的输出差异
do_result_evaluation(batch_size,pth_model_path, onnx_file_path, input_shape, network=None,model=None)

### 错误反馈