# 概括
本代码为pytorch model 转化 onnx model 工具

## 说明
本包名字为*modelhub*,使用方法包括...

### 打包方法
cd /package
python setup.py sdist
pip install twine
twine upload dist/conversion_onnx-0.0.4.tar.gz

### 安装方法
pip install conversion_onnx

### 使用方法
from conversion.pth2onnx import run_pth2onnx

### 参数说明
1. 直接传入加载好weight的模型去转换onnx(固定size大小，推荐使用)
run_pth2onnx(model, batch_size, onnx_export_path, input_shape)
其中 model：带有网络结构和参数的模型
    batch_size：batch的大小
    onnx_export_path：导出模型的路径
    input_shape：模型的输入

2. 直接传入加载好weight的模型去转换onnx(动态size大小，导出问题较多，较为复杂)
run_dynamic_pth2onnx(model, batch_size, onnx_export_path, input_shape, input_names, output_names, dynamic_axes)
其中 input_names：输入节点重命名
    output_names：输出节点重命名
    dynamic_axes：指定输入/输出的动态轴

3. 先加载模型再转化onnx
load_model_pth2onnx(pth_model_path, batch_size , onnx_export_path, input_shape, network=None)
其中 pth_model_path：pth模型的存放路径
    network：模型的网络结构（不含weight）

4. 评测pth模型和onnx模型的输出差异
do_result_evaluation(batch_size,pth_model_path, onnx_file_path, input_shape, network=None,model=None)

### 错误反馈