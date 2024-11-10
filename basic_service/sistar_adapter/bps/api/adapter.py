import os
import clr  # 导入 pythonnet 提供的 clr 模块
from typing import Any
from func_timeout import func_set_timeout
from func_timeout.exceptions import FunctionTimedOut

# 加载 DLL 文件
current_path = os.getcwd()
dll_path = os.path.join(current_path, "Siemens.Sistar.Api.dll")  # DLL 文件的路径
clr.AddReference(dll_path)

# 导入 C# 命名空间中的类
from Siemens.Sistar.Api import SistarBatch

# 实例化类
sistar_batch_instance = SistarBatch('python_web_api_batch')
sistar_batch_params_instance = SistarBatch.ParameterList()

from System import UInt16, UInt32, Double, Boolean, DateTime, String, Int32

BatchStartMode = {
    'Immediate': SistarBatch.BatchStartMode.Immediate,
    'StartTime': SistarBatch.BatchStartMode.StartTime,
    'ByEvent': SistarBatch.BatchStartMode.ByEvent,
    'StartTimeAuto': SistarBatch.BatchStartMode.StartTimeAuto
}

BatchStatus = {
    'Locked': SistarBatch.BatchStatus.Locked,
    'ReadyForRelease': SistarBatch.BatchStatus.ReadyForRelease,
    'Released': SistarBatch.BatchStatus.Released
}


@func_set_timeout(3)
def create_batch(site: int,
                 area: int,
                 year: int,
                 order: int,
                 batch: int,
                 recipeCategory: int,
                 recipe: int,
                 line: int,
                 productId: int,
                 size: float,
                 useDefaultSize: bool,
                 startMode: str,
                 plannedStartTimeYear: int,
                 plannedStartTimeMonth: int,
                 plannedStartTimeDay: int,
                 plannedStartTimeHour: int,
                 plannedStartTimeMin: int,
                 plannedStartTimeSec: int,
                 status: str,
                 parameterList: Any,
                 useDefaultParameterValues: bool,
                 errorMessage: str,
                 doRepeat: bool
                 ):
    """
    创建工单
    :param site: 1
    :param area: 1
    :param year: 2024
    :param order: 1
    :param batch:115
    :param recipeCategory:1
    :param recipe:9
    :param line:1
    :param productId:0
    :param size:100
    :param useDefaultSize:True
    :param startMode: 'Immediate'
    :param plannedStartTimeYear: 2024
    :param plannedStartTimeMonth: 12
    :param plannedStartTimeDay: 1
    :param status: 'ReadyForRelease'
    :param parameterList:  sistar_batch_params_instance
    :param useDefaultParameterValues: True
    :param errorMessage: ''
    :param doRepeat: False
    :return:
    """
    error_message = errorMessage

    result = sistar_batch_instance.CreateBatch(UInt16(site), UInt16(area), UInt16(year), UInt32(order), UInt32(batch),
                                               UInt32(recipeCategory),
                                               UInt32(recipe),
                                               UInt32(line),
                                               UInt32(productId), Double(size), Boolean(useDefaultSize),
                                               BatchStartMode[startMode],
                                               DateTime(Int32(plannedStartTimeYear), Int32(plannedStartTimeMonth),
                                                        Int32(plannedStartTimeDay), Int32(plannedStartTimeHour),
                                                        Int32(plannedStartTimeMin), Int32(plannedStartTimeSec)),
                                               BatchStatus[status],
                                               parameterList, Boolean(useDefaultParameterValues), String(error_message),
                                               Boolean(doRepeat)
                                               )

    return result


def create_batch_ex(site: int,
                    area: int,
                    year: int,
                    order: int,
                    batch: int,
                    recipeCategory: int,
                    recipe: int,
                    line: int,
                    productId: int,
                    useDefaultProductId: bool,
                    size: float,
                    useDefaultSize: bool,
                    startMode: str,
                    plannedStartTimeYear: int,
                    plannedStartTimeMonth: int,
                    plannedStartTimeDay: int,
                    plannedStartTimeHour: int,
                    plannedStartTimeMin: int,
                    plannedStartTimeSec: int,
                    status: str,
                    parameterList: Any,
                    useDefaultParameterValues: bool,
                    batcName: str,
                    errorMessage: str,
                    doRepeat: bool
                    ):
    """
    创建工单Ex
    :param site: 1
    :param area: 1
    :param year: 2024
    :param order: 1
    :param batch:115
    :param recipeCategory:1
    :param recipe:9
    :param line:1
    :param productId:0
    :param size:100
    :param useDefaultSize:True
    :param startMode: 'Immediate'
    :param plannedStartTimeYear: 2024
    :param plannedStartTimeMonth: 12
    :param plannedStartTimeDay: 1
    :param status: 'ReadyForRelease'
    :param parameterList:  sistar_batch_params_instance
    :param useDefaultParameterValues: True
    :param errorMessage: ''
    :param doRepeat: False
    :return:
    """
    error_message = errorMessage

    result = sistar_batch_instance.CreateBatchEx(UInt16(site), UInt16(area), UInt16(year), UInt32(order), UInt32(batch),
                                                 UInt32(recipeCategory),
                                                 UInt32(recipe),
                                                 UInt32(line),
                                                 UInt32(productId), Boolean(useDefaultProductId), Double(size),
                                                 Boolean(useDefaultSize),
                                                 BatchStartMode[startMode],
                                                 DateTime(Int32(plannedStartTimeYear), Int32(plannedStartTimeMonth),
                                                          Int32(plannedStartTimeDay), Int32(plannedStartTimeHour),
                                                          Int32(plannedStartTimeMin), Int32(plannedStartTimeSec)),
                                                 BatchStatus[status],
                                                 parameterList, Boolean(useDefaultParameterValues), String(batcName),
                                                 String(error_message),
                                                 Boolean(doRepeat)
                                                 )

    return result


def delete_batch(site: int,
                 area: int,
                 year: int,
                 order: int,
                 batch: int,
                 recipeCategory: int,
                 errorMessage: str,
                 doRepeat: bool
                 ):
    error_message = errorMessage

    result = sistar_batch_instance.DeleteBatch(UInt16(site), UInt16(area), UInt16(year), UInt32(order), UInt32(batch),
                                               UInt32(recipeCategory),
                                               String(error_message),
                                               Boolean(doRepeat)
                                               )

    return result


def get_last_error():
    result = sistar_batch_instance.GetLastError()
    return result


def get_last_full_error_string():
    result = sistar_batch_instance.GetLastFullErrorString()
    return result


def set_batch_parameters(site: int,
                         area: int,
                         year: int,
                         order: int,
                         batch: int,
                         recipeCategory: int,
                         parameterList: Any,
                         errorMessage: str,
                         doRepeat: bool
                         ):
    error_message = errorMessage

    result = sistar_batch_instance.SetBatchParameters(UInt16(site), UInt16(area), UInt16(year), UInt32(order),
                                                      UInt32(batch),
                                                      UInt32(recipeCategory), parameterList,
                                                      String(error_message),
                                                      Boolean(doRepeat)
                                                      )

    return result


def set_batch_size(site: int,
                   area: int,
                   year: int,
                   order: int,
                   batch: int,
                   recipeCategory: int,
                   size: float,
                   errorMessage: str,
                   doRepeat: bool
                   ):
    error_message = errorMessage

    result = sistar_batch_instance.SetBatchSize(UInt16(site), UInt16(area), UInt16(year), UInt32(order), UInt32(batch),
                                                UInt32(recipeCategory), Double(size),
                                                String(error_message),
                                                Boolean(doRepeat)
                                                )

    return result


def set_batch_start_data(site: int,
                         area: int,
                         year: int,
                         order: int,
                         batch: int,
                         recipeCategory: int,
                         startMode: str,
                         plannedStartTimeYear,
                         plannedStartTimeMonth,
                         plannedStartTimeDay,
                         plannedStartTimeHour: int,
                         plannedStartTimeMin: int,
                         plannedStartTimeSec: int,
                         errorMessage: str,
                         doRepeat: bool
                         ):
    error_message = errorMessage

    result = sistar_batch_instance.SetBatchStartData(UInt16(site), UInt16(area), UInt16(year), UInt32(order),
                                                     UInt32(batch),
                                                     UInt32(recipeCategory), BatchStartMode[startMode],
                                                     DateTime(Int32(plannedStartTimeYear), Int32(plannedStartTimeMonth),
                                                              Int32(plannedStartTimeDay), Int32(plannedStartTimeHour),
                                                              Int32(plannedStartTimeMin), Int32(plannedStartTimeSec)),
                                                     String(error_message),
                                                     Boolean(doRepeat)
                                                     )

    return result


def set_batch_status(site: int,
                     area: int,
                     year: int,
                     order: int,
                     batch: int,
                     recipeCategory: int,
                     status: str,
                     errorMessage: str,
                     doRepeat: bool
                     ):
    error_message = errorMessage

    result = sistar_batch_instance.SetBatchStatus(UInt16(site), UInt16(area), UInt16(year), UInt32(order),
                                                  UInt32(batch),
                                                  UInt32(recipeCategory), BatchStatus[status],
                                                  String(error_message),
                                                  Boolean(doRepeat)
                                                  )

    return result


def set_timeout(timeout: int):
    result = sistar_batch_instance.SetTimeout(UInt16(timeout))
    return result


def add_parameter(paramNumber: int, paramValue: str):
    result = sistar_batch_params_instance.AddParameter(UInt16(paramNumber), String(paramValue))
    return result


def get_number_at(index: int):
    result = sistar_batch_params_instance.GetNumberAt(UInt32(index))
    return result


def get_size():
    result = sistar_batch_params_instance.GetSize()
    return result


def get_value_at(index: int):
    result = sistar_batch_params_instance.GetValueAt(UInt32(index))
    return result



def fff():
    try:
        return create_batch(1,1,1,1,1,1,1,1,1,1,False,"Immediate",2024,10,13,1,1,1,"Locked",1,False,"",False)
    except FunctionTimedOut:
        return 'timeout'


if __name__ == '__main__':
    f = fff()