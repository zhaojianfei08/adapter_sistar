<!-- src/views/About.vue -->
<template>
  <div>
    <!-- 标题 -->
    <h1>
      OPCUA Adapter
      <el-button type="primary" @click="deploy">Deploy</el-button>
    </h1>
    <!-- 显示内容 -->
    <el-row :gutter="24">
      <!-- 显示OPCUA设备 -->
      <el-col :span="8">
        <div class="grid-content ep-bg-purple">
          <el-card style="max-width: 520px">
            <template #header>
              <div class="card-header">
                <el-row :gutter="24">
                  <el-col :span="12">
                    <span> OPCUA 设备 </span>
                  </el-col>
                  <el-col :span="12">
                    <el-button type="primary" @click="openAddDeviceDialog"
                      >ADD OPCUA Device
                    </el-button>
                  </el-col>
                </el-row>
                <el-divider />
                <el-row :gutter="24">
                  <el-col :span="6">
                    <el-button
                      type="primary"
                      @click="dowmloadTemplate('opcua_device_template.xlsx')"
                      >下载模板
                    </el-button>
                  </el-col>
                  <el-col :span="6">
                    <el-upload
                      action="http://127.0.0.1:5003/opcua/upload"
                      :before-upload="beforeUpload"
                      :on-success="handleFileUpSuccess"
                      :on-error="handleFileUpError"
                      v-model:file-list="fileList"
                    >
                      <el-button type="primary">点击上传</el-button>
                    </el-upload>
                  </el-col>
                </el-row>
                <el-divider />
                <el-row :gutter="24">
                  <el-col :span="6">
                    <el-button type="primary" @click="inputDeviceExcelData"
                      >导入Excel
                    </el-button>
                  </el-col>
                  <el-col :span="6">
                    <el-button type="primary" @click="outputExcelData('device')"
                      >导出Excel
                    </el-button>
                  </el-col>
                  <el-col :span="6">
                    <el-button
                      type="danger"
                      @click="deleteAllData('opcuadevices')"
                      >清空数据
                    </el-button>
                  </el-col>
                </el-row>
              </div>
            </template>
            <el-table
              ref="opcuaDeviceRef"
              :data="deviceData"
              @current-change="getDeviceItem"
              highlight-current-row
              style="width: 100%"
            >
              <!-- <el-table-column type="selection" width="55" /> -->
              <el-table-column label="设备ID" prop="id"></el-table-column>
              <el-table-column
                label="设备名称"
                prop="device_name"
              ></el-table-column>
              <el-table-column label="设备URL" prop="url"></el-table-column>
              <!-- 操作列 -->
              <el-table-column label="Actions" width="150">
                <template v-slot="scope">
                  <!-- 编辑按钮 -->
                  <el-button size="small" @click="handleEdit(scope.row)"
                    >Edit
                  </el-button>
                  <!-- 删除按钮 -->
                  <el-button
                    size="small"
                    type="danger"
                    @click="handleDelete(scope.row)"
                    >Delete
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <el-pagination
              v-model:currentPage="deviceCurrentPage"
              v-model:page-size="devicePerPage"
              :size="size"
              :background="background"
              layout="total, prev, pager, next"
              v-model:total="deviceTotal"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </el-card>
        </div>
      </el-col>
      <!-- 显示OPCUA点 -->
      <el-col :span="16">
        <div class="grid-content ep-bg-purple">
          <el-card style="max-width: 1320px; height: 600px">
            <template #header>
              <div class="card-header">
                <el-row :gutter="24">
                  <el-col :span="12">
                    <span>OPCUA 点表</span>
                  </el-col>
                  <el-col :span="12">
                    <el-button type="primary" @click="openAddPointDialog"
                      >ADD OPCUA Point
                    </el-button>
                  </el-col>
                </el-row>
                <el-divider />
                <el-row :gutter="24">
                  <el-col :span="4">
                    <el-button
                      type="primary"
                      @click="dowmloadTemplate('opcua_point_template.xlsx')"
                      >下载模板
                    </el-button>
                  </el-col>
                  <el-col :span="4">
                    <el-upload
                      action="http://127.0.0.1:5003/opcua/upload"
                      :before-upload="beforeUpload"
                      :on-success="handleFileUpSuccess"
                      :on-error="handleFileUpError"
                      v-model:file-list="fileList"
                    >
                      <el-button type="primary">点击上传</el-button>
                    </el-upload>
                  </el-col>
                  <el-col :span="4">
                    <el-button type="primary" @click="inputPointExcelData"
                      >导入Excel
                    </el-button>
                  </el-col>
                  <el-col :span="4">
                    <el-button type="primary" @click="outputExcelData('point')"
                      >导出Excel
                    </el-button>
                  </el-col>
                  <el-col :span="4">
                    <el-button
                      type="danger"
                      @click="deleteAllData('opcuapoints')"
                      >清空数据
                    </el-button>
                  </el-col>
                </el-row>

                <el-divider />
              </div>
            </template>
            <el-table :data="pointData" height="300" style="width: 100%">
              <!-- <el-table-column type="selection" width="55" /> -->
              <el-table-column label="tag_uuid" prop="tag_uuid">
              </el-table-column>
              <el-table-column label="node_id" prop="node_id"></el-table-column>
              <el-table-column label="采集周期" prop="interval">
              </el-table-column>
              <el-table-column label="是否激活" prop="active">
              </el-table-column>
              <el-table-column label="激活报警" prop="active_alarm">
              </el-table-column>
              <el-table-column label="报警上限值" prop="alarm_up">
              </el-table-column>
              <el-table-column label="报警下限值" prop="alarm_down">
              </el-table-column>
              <el-table-column label="报警上限信息" prop="alarm_up_info">
              </el-table-column>
              <el-table-column label="报警下限信息" prop="alarm_down_info">
              </el-table-column>
              <el-table-column
                label="到达报警上限后转换值"
                prop="alarm_up_change"
              >
              </el-table-column>
              <el-table-column
                label="到达报警下限后转换值"
                prop="alarm_down_change"
              >
              </el-table-column>
              <el-table-column label="激活归档" prop="active_archive">
              </el-table-column>
              <el-table-column label="变化时归档" prop="active_onchange">
              </el-table-column>
              <el-table-column label="归档周期" prop="active_interval">
              </el-table-column>
              <el-table-column label="激活缩放" prop="active_scale">
              </el-table-column>
              <el-table-column label="缩放函数" prop="scale_sign">
              </el-table-column>
              <el-table-column label="缩放因子" prop="scale_factor">
              </el-table-column>
              <el-table-column label="mqtt topic" prop="mqtt_topic_name">
              </el-table-column>
              <el-table-column label="单位" prop="unit"></el-table-column>
              <el-table-column label="符号名" prop="comments">
              </el-table-column>
              <el-table-column label="所属设备" prop="device_id">
              </el-table-column>
              <!-- 操作列 -->
              <el-table-column label="Actions" width="150">
                <template v-slot="scope">
                  <!-- 编辑按钮 -->
                  <el-button size="small" @click="handlePointEdit(scope.row)"
                    >Edit
                  </el-button>
                  <!-- 删除按钮 -->
                  <el-button
                    size="small"
                    type="danger"
                    @click="handlePointDelete(scope.row)"
                    >Delete
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <el-pagination
              v-model:currentPage="pointCurrentPage"
              v-model:page-size="pointPerPage"
              :size="size"
              :background="background"
              layout="total, prev, pager, next"
              v-model:total="pointTotal"
              @size-change="handlePointSizeChange"
              @current-change="handlePointCurrentChange"
            />
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
  <!-- OPCUA设备编辑对话框 -->
  <el-dialog v-model="dialogVisible" title="Edit">
    <el-form :model="editForm">
      <el-form-item label="id">
        <el-input v-model="editForm.id" disabled></el-input>
      </el-form-item>
      <el-form-item label="device_name">
        <el-input v-model="editForm.device_name"></el-input>
      </el-form-item>
      <el-form-item label="url">
        <el-input v-model="editForm.url"></el-input>
      </el-form-item>
    </el-form>
    <template v-slot:footer>
      <el-button @click="dialogVisible = false">Cancel</el-button>
      <el-button type="primary" @click="saveEdit">Save</el-button>
    </template>
  </el-dialog>
  <!-- OPCUA 点表编辑对话框 -->
  <el-dialog v-model="pointDialogVisible" title="Edit">
    <el-form :model="pointEditForm">
      <el-form-item label="id">
        <el-input v-model="pointEditForm.id" disabled></el-input>
      </el-form-item>
      <el-form-item label="tag_uuid">
        <el-input v-model="pointEditForm.tag_uuid"></el-input>
      </el-form-item>
      <el-form-item label="node_id">
        <el-input v-model="pointEditForm.node_id"></el-input>
      </el-form-item>
      <el-form-item label="interval">
        <el-input v-model="pointEditForm.interval"></el-input>
      </el-form-item>
      <el-form-item label="active">
        <el-input v-model="pointEditForm.active"></el-input>
      </el-form-item>
      <el-form-item label="active_alarm">
        <el-input v-model="pointEditForm.active_alarm"></el-input>
      </el-form-item>
      <el-form-item label="alarm_up">
        <el-input v-model="pointEditForm.alarm_up"></el-input>
      </el-form-item>
      <el-form-item label="alarm_down">
        <el-input v-model="pointEditForm.alarm_down"></el-input>
      </el-form-item>
      <el-form-item label="alarm_up_info">
        <el-input v-model="pointEditForm.alarm_up_info"></el-input>
      </el-form-item>
      <el-form-item label="alarm_down_info">
        <el-input v-model="pointEditForm.alarm_down_info"></el-input>
      </el-form-item>
      <el-form-item label="alarm_up_change">
        <el-input v-model="pointEditForm.alarm_up_change"></el-input>
      </el-form-item>
      <el-form-item label="alarm_down_change">
        <el-input v-model="pointEditForm.alarm_down_change"></el-input>
      </el-form-item>
      <el-form-item label="active_archive">
        <el-input v-model="pointEditForm.active_archive"></el-input>
      </el-form-item>
      <el-form-item label="active_onchange">
        <el-input v-model="pointEditForm.active_onchange"></el-input>
      </el-form-item>
      <el-form-item label="active_interval">
        <el-input v-model="pointEditForm.active_interval"></el-input>
      </el-form-item>
      <el-form-item label="active_scale">
        <el-input v-model="pointEditForm.active_scale"></el-input>
      </el-form-item>
      <el-form-item label="scale_sign">
        <el-input v-model="pointEditForm.scale_sign"></el-input>
      </el-form-item>
      <el-form-item label="scale_factor">
        <el-input v-model="pointEditForm.scale_factor"></el-input>
      </el-form-item>
      <el-form-item label="mqtt_topic_name">
        <el-input v-model="pointEditForm.mqtt_topic_name"></el-input>
      </el-form-item>
      <el-form-item label="unit">
        <el-input v-model="pointEditForm.unit"></el-input>
      </el-form-item>
      <el-form-item label="comments">
        <el-input v-model="pointEditForm.comments"></el-input>
      </el-form-item>
      <el-form-item label="device_id">
        <el-input v-model="pointEditForm.device_id"></el-input>
      </el-form-item>
    </el-form>
    <template v-slot:footer>
      <el-button @click="pointDialogVisible = false">Cancel</el-button>
      <el-button type="primary" @click="pointSaveEdit">Save</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import axios from "../api/axios"; // 引入 Axios 封装
import { ref, onMounted } from "vue";
import { ElMessageBox, ElMessage } from "element-plus";

const getDeviceItem = (row) => {
  selectDeviceId.value = row.id;
  get_opcua_point(row.id, pointCurrentPage.value);
};

// File List 用于保存上传的文件
const fileList = ref([]);

// 用于处理对文件的验证
const beforeUpload = (file) => {
  // 如果需要在上传前进行一些验证或处理
  console.log("即将上传的文件: ", file);
  return true; // 返回 false 可以阻止上传
};

// OPCUA 设备数据
const deviceData = ref([]);
// OPCUA 点表数据
const pointData = ref([]);

// 当前选择的OPCUA Device ID
const selectDeviceId = ref(1);

// OPCUA设备数据
const deviceCurrentPage = ref(1); // 当前页
const devicePerPage = ref(1); // 每页有几条数据
const deviceTotal = ref(1); // OPCUA设备总页数

// OPCUA 点表数据
const pointCurrentPage = ref(1); // OPCUA点表当前页
const pointPerPage = ref(1); // OPCUA点表每页有几条数据
const pointTotal = ref(1); // OPCUA设备总页数

// 分页size
const size = ref("small");
// 分页背景
const background = ref(false);
// 分页
const disabled = ref(false);
// 控制编辑对话框
const dialogVisible = ref(false);
// 控制新增对话框
const pointDialogVisible = ref(false);

// OPCUA设备当前编辑的数据
const editForm = ref({});

// OPCUA POINT 当前编辑的数据
const pointEditForm = ref({});

// 处理OPCUA设备每个页面大小
const handleSizeChange = (val) => {
  console.log(`${val} items per page`);
};

// 处理OPCUA设备翻页
const handleCurrentChange = (val) => {
  console.log(`current page: ${val}`);
  deviceCurrentPage.value = val;
  get_opcua_device(val);
};

// 处理OPCUA点表每个页面大小
const handlePointSizeChange = (val) => {
  console.log(`${val} items per page`);
};

// 处理OPCUA点表翻页
const handlePointCurrentChange = (val) => {
  console.log(`current page: ${val}`);
  pointCurrentPage.value = val;
  get_opcua_point(selectDeviceId.value, val);
};

// 获取opcua device 数据
async function get_opcua_device(page) {
  const params = { page: page };
  try {
    await axios
      .get("/api/opcuadevices", { params: params })
      .then((response) => {
        devicePerPage.value = response.data.data.per_page;
        deviceTotal.value = response.data.data.total;
        deviceCurrentPage.value = response.data.data.page;
        deviceData.value = response.data.data.items;
      })
      .catch((e) => {
        console.log(e)
        ElMessage({
          showClose: true,
          message: e.response.data.message,
          type: "error",
        });
      });
  } catch {
    (error) => {
      alert(error);
    };
  }
}

// 获取opcua point 数据
async function get_opcua_point(device_id, page) {
  const params = { page: page };
  try {
    await axios
      .get(`/api/opcuapoints/${device_id}`, { params: params })
      .then((response) => {
        pointPerPage.value = response.data.data.per_page;
        pointTotal.value = response.data.data.total;
        pointCurrentPage.value = response.data.data.page;
        pointData.value = response.data.data.items;
      })
      .catch((e) => {
        ElMessage({
          showClose: true,
          message: e.response.data.message,
          type: "error",
        });
      });
  } catch {
    (error) => {
      alert(error);
    };
  }
}

// OPCUA 设备 处理编辑按钮
function handleEdit(row) {
  // 打开对话框并加载数据

  editForm.value = { ...row };
  dialogVisible.value = true;
}

// OPCUA 点表 处理编辑按钮
function handlePointEdit(row) {
  // 打开对话框并加载数据
  pointEditForm.value = { ...row };
  pointDialogVisible.value = true;
}

// OPCUA 设备 保存编辑后的数据
function saveEdit() {
  // 没有id说明是新增数据
  if (!editForm.value.id) {
    addDeviceItem();
  } else {
    // 找到表格中对应的数据并更新
    const index = deviceData.value.findIndex(
      (item) => item.id === editForm.value.id
    );
    if (index !== -1) {
      // deviceData.value[index] = { ...editForm.value };
      // console.log({...editForm.value})
      changeDeviceItem(editForm.value.id);
    }
    dialogVisible.value = false;
  }
}

// OPCUA 点表 保存编辑后的数据
function pointSaveEdit() {
  // 没有id说明是新增数据
  if (!pointEditForm.value.id) {
    addPointItem();
  } else {
    // 找到表格中对应的数据并更新
    const index = pointData.value.findIndex(
      (item) => item.id === pointEditForm.value.id
    );
    if (index !== -1) {
      // deviceData.value[index] = { ...editForm.value };
      // console.log({...editForm.value})
      changePointItem(pointEditForm.value.id);
    }
    pointDialogVisible.value = false;
  }
}

// OPCUA 设备 删除行数据
function handleDelete(row) {
  // 确认删除
  ElMessageBox.confirm("Are you sure to delete this item?", "Warning", {
    confirmButtonText: "Yes",
    cancelButtonText: "No",
    type: "warning",
  })
    .then(() => {
      // 删除操作
      //deviceData.value = deviceData.value.filter((item) => item.id !== row.id);
      deleteDeviceItem(row.id);
      ElMessage({
        type: "success",
        message: "Delete success!",
      });
    })
    .catch(() => {
      ElMessage({
        type: "info",
        message: "Delete canceled",
      });
    });
}

// OPCUA 点表 删除行数据
function handlePointDelete(row) {
  // 确认删除
  ElMessageBox.confirm("Are you sure to delete this item?", "Warning", {
    confirmButtonText: "Yes",
    cancelButtonText: "No",
    type: "warning",
  })
    .then(() => {
      // 删除操作
      //deviceData.value = deviceData.value.filter((item) => item.id !== row.id);
      deletePointItem(row.id);
      ElMessage({
        type: "success",
        message: "Delete success!",
      });
    })
    .catch(() => {
      ElMessage({
        type: "info",
        message: "Delete canceled",
      });
    });
}

// 修改OPCUA设备数据发送ajax
function changeDeviceItem(id) {
  try {
    axios
      .put(`/api/opcuadevices/${id}`, { ...editForm.value })
      .then((response) => {
        if (response.data.status == "success") {
          get_opcua_device(deviceCurrentPage.value);
        } else {
          alert(response.data.message);
        }
      });
  } catch (e) {
    alert(e);
  }
}

// 修改OPCUA点表数据发送ajax
function changePointItem(id) {
  // to do list
  try {
    axios
      .put(`/api/opcuapoints/${selectDeviceId.value}/${id}`, {
        ...pointEditForm.value,
      })
      .then((response) => {
        if (response.data.status == "success") {
          get_opcua_point(selectDeviceId.value, deviceCurrentPage.value);
        } else {
          alert(response.data.message);
        }
      });
  } catch (e) {
    alert(e);
  }
}

// 删除OPCUA设备数据发送ajax
function deleteDeviceItem(id) {
  try {
    axios.delete(`/api/opcuadevices/${id}`).then((response) => {
      if (response.data.status == "success") {
        get_opcua_device(deviceCurrentPage.value);
      } else {
        alert(response.data.message);
      }
    });
  } catch (e) {
    alert(e);
  }
}

// 删除OPCUA点表数据发送ajax
function deletePointItem(id) {
  try {
    axios
      .delete(`/api/opcuapoints/${selectDeviceId.value}/${id}`)
      .then((response) => {
        if (response.data.status == "success") {
          get_opcua_point(selectDeviceId.value, deviceCurrentPage.value);
        } else {
          alert(response.data.message);
        }
      });
  } catch (e) {
    alert(e);
  }
}

// 新增OPCUA设备数据发送ajax
function addDeviceItem() {
  const data = { ...editForm.value };
  data.opcuapoints = [];
  try {
    axios.post(`/api/opcuadevices`, data).then((response) => {
      if (response.data.status == "success") {
        get_opcua_device(deviceCurrentPage.value);
      } else {
        alert(response.data.message);
      }
    });
  } catch (e) {
    alert(e);
  }
}

// 新增OPCUA点表数据发送ajax
function addPointItem() {
  const data = { ...pointEditForm.value };

  try {
    axios
      .post(`/api/opcuapoints/${selectDeviceId.value}`, data)
      .then((response) => {
        if (response.data.status == "success") {
          alert(response.data.message);
          get_opcua_device(deviceCurrentPage.value);
        } else {
          alert(response.data.message);
        }
      });
  } catch (e) {
    alert(e);
  }
}

// 新增OPCUA设备按钮
function openAddDeviceDialog() {
  // 重置表单数据
  editForm.value = { id: null, device_name: "", url: "" };
  dialogVisible.value = true;
}

// 新增OPCUA点表按钮
function openAddPointDialog() {
  // 重置表单数据
  pointEditForm.value = {
    id: null,
    tag_uuid: "",
    node_id: "",
    interval: "",
    active: "",
    active_alarm: "",
    alarm_up: "",
    alarm_down: "",
    alarm_up_info: "",
    alarm_down_info: "",
    alarm_up_change: "",
    alarm_down_change: "",
    active_archive: "",
    active_onchange: "",
    active_interval: "",
    active_scale: "",
    scale_sign: "",
    scale_factor: "",
    mqtt_topic_name: "",
    unit: "",
    comments: "",
    device_id: "",
  };
  pointDialogVisible.value = true;
}

// 处理文件上传成功接口
function handleFileUpSuccess(response, file, fileList) {
  console.log("上传成功：", response);
}

// 处理文件上传失败接口
function handleFileUpError(err, file, fileList) {
  console.log("上传失败：", err);
}

// 下载模板接口
function dowmloadTemplate(filename) {
  const params = { filename: filename };
  try {
    axios
      .get("/download", { params: params, responseType: "blob" })
      .then((response) => {
        // 创建一个下载链接
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", filename); // 设置下载文件名
        document.body.appendChild(link);
        link.click();
        link.remove();
      });
  } catch (e) {
    alert(e);
  }
}

// 清空所有数据
function deleteAllData(table_name) {
  const data = { table_name: table_name };

  try {
    axios
      .post(`/delete_all_data`, data)
      .then((response) => {
        //alert(response.data.message);
        ElMessage({
          showClose: true,
          message: response.data.message,
          type: "success",
        });
        get_opcua_point(deviceData.value, deviceCurrentPage.value);
      })
      .catch((err) => {
        ElMessage({
          showClose: true,
          message: err.message,
          type: "error",
        });
      });
  } catch (e) {
    alert(e);
  }
}

// 导入设备数据，从excel导入到mysql中
function inputDeviceExcelData() {
  // 确认删除
  ElMessageBox.confirm(
    "导入数据前必须清空数据,Are you sure to delete all item?",
    "Warning",
    {
      confirmButtonText: "Yes",
      cancelButtonText: "No",
      type: "warning",
    }
  )
    .then(() => {
      // 删除操作
      //deviceData.value = deviceData.value.filter((item) => item.id !== row.id);
      deleteAllData("opcuadevices");
      try {
        axios
          .post(`/import_device_data`)
          .then((response) => {
            ElMessage({
              showClose: true,
              message: response.data.message,
              type: "success",
            });
          })
          .catch((err) => {
            ElMessage({
              showClose: true,
              message: err.message,
              type: "error",
            });
          });
      } catch (e) {
        alert(e);
      }
    })
    .catch(() => {
      ElMessage({
        type: "info",
        message: "input canceled",
      });
    });
}

// 导入点表数据，从excel导入到mysql中
function inputPointExcelData() {
  // 确认删除
  ElMessageBox.confirm(
    "导入数据前必须清空数据,Are you sure to delete all item?",
    "Warning",
    {
      confirmButtonText: "Yes",
      cancelButtonText: "No",
      type: "warning",
    }
  )
    .then(() => {
      deleteAllData("opcuapoints");
      try {
        axios.post(`/import_point_data`).then((response) => {
          ElMessage({
            showClose: true,
            message: response.data.message,
            type: "success",
          });
        });
      } catch (e) {
        alert(e);
      }
    })
    .catch(() => {
      ElMessage({
        type: "info",
        message: "input canceled",
      });
    });
}

// deploy
function deploy() {
  try {
    axios.post(`/deploy`).then((response) => {
      if (response.data.status == "success") {
        ElMessage({
          showClose: true,
          message: "Deploy success!",
          type: "success",
        });
      } else {
        ElMessage({
          showClose: true,
          message: response.data.message,
          type: "error",
        });
      }
    });
  } catch (e) {
    alert(e);
  }
}

// 导出excel
function outputExcelData(val) {
  const data = { table: val };
  try {
    axios
      .post(`/download_table_data`, data)
      .then((response) => {
        // 创建一个下载链接
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `opcua_${val}_${new Date().getTime()}.xlsx`); // 设置下载文件名
        document.body.appendChild(link);
        link.click();
        link.remove();
      })
      .catch((e) => {
        ElMessage({
          showClose: true,
          message: e.response.data.message,
          type: "error",
        });
      });
  } catch (e) {
    alert(e);
  }
}

// 组件挂载完成后加载
onMounted(() => {
  get_opcua_device(1);
});
</script>


<style scoped>
.demo-table-expand {
  font-size: 0;
}

.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}

.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}
</style>
  