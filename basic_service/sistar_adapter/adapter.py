# pip install pythonnet
import clr
import sys
from pathlib import Path

# 确保.NET Framework路径被包含在系统路径中（如果必要）
sys.path.append(r"Siemens.Sistar.Api.dll")

# 加载Siemens.Sistar.Api.dll
clr.AddReference("Siemens.Sistar.Api")

# 导入DLL中的命名空间
from Siemens.Sistar.Api import WorkOrderService


def submit_work_order(order_details):
    """
    使用Siemens.Sistar.Api.dll提交工单。

    :param order_details: 包含工单详细信息的字典或对象
    """
    try:
        # 假设 WorkOrderService 是工单服务类
        work_order_service = WorkOrderService()

        # 根据 API 文档，创建工单对象并设置其属性
        work_order = work_order_service.CreateNewOrder()
        work_order.Id = order_details["id"]
        work_order.Description = order_details["description"]
        work_order.Quantity = order_details["quantity"]

        # 提交工单
        result = work_order_service.Submit(work_order)

        if result.Success:
            print(f"工单 {order_details['id']} 提交成功!")
        else:
            print(f"工单提交失败: {result.ErrorMessage}")

    except Exception as e:
        print(f"提交工单时发生错误: {e}")


if __name__ == "__main__":
    # 示例工单数据
    order_details = {
        "id": "WO12345",
        "description": "Test work order",
        "quantity": 100
    }

    submit_work_order(order_details)


"""
clr.AddReference("Siemens.Sistar.Api"): 这行代码加载了Siemens.Sistar.Api.dll，以便你可以在Python中使用其中的类和方法。

WorkOrderService类: 假设Siemens.Sistar.Api.dll中有一个名为WorkOrderService的类，用于管理工单。实际情况下，你需要根据API的文档或DLL中的类结构来确定使用的类和方法。

submit_work_order函数: 该函数创建工单并使用Submit方法进行提交。它接受一个包含工单详细信息的字典，并设置工单的属性。

错误处理: 使用try...except块来捕获并处理可能的异常。

在使用pythonnet时，确保你的Python环境与目标.NET版本兼容。例如，pythonnet对于.NET Framework和.NET Core的支持可能有所不同，具体请参考pythonnet的官方文档。如果需要调用复杂的.NET功能，
建议在Windows上使用Python，因为pythonnet对Windows环境支持较好。

DLL文件路径: 确保Siemens.Sistar.Api.dll的路径正确。如果路径不在标准路径中，可以使用绝对路径。

命名空间和类: 在使用pythonnet加载DLL时，需要知道DLL中的命名空间和类名。可以使用dotPeek或ILSpy等反编译工具查看DLL内部的类和方法。

API文档: 通常情况下，第三方API（如Siemens Sistar）的文档中会有如何调用DLL中的类和方法的详细说明。使用之前，建议先查阅API文档。
"""

