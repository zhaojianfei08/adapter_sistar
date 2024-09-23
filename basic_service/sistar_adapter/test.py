import clr  # 导入 pythonnet 提供的 clr 模块
import os

# 加载 DLL 文件
dll_path = r"E:\TH\core\basic_service\sistar_adapter\Siemens.Sistar.Api.dll"  # DLL 文件的路径
clr.AddReference(dll_path)

# 导入 C# 命名空间中的类
from Siemens.Sistar.Api import SistarBatch

# 实例化类
my_instance = SistarBatch('ins')
ins2 = SistarBatch.ParameterList()

from System import UInt16, UInt32, Double, Boolean, DateTime, String, Int32

message = ''

result = my_instance.CreateBatch(UInt16(1), UInt16(1), UInt16(2024), UInt32(1), UInt32(115), UInt32(1), UInt32(9),
                                 UInt32(1),
                                 UInt32(0), Double(100), Boolean(True), SistarBatch.BatchStartMode.Immediate,
                                 DateTime(Int32(2024), Int32(12), Int32(1)), SistarBatch.BatchStatus.ReadyForRelease,
                                 ins2, Boolean(True), String(message), Boolean(False)
                                 )

print(f"Result of CreateBatch method: {result}")
