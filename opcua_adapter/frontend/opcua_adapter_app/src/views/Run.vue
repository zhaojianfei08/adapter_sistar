<!-- src/views/Home.vue -->
<template>
  <div>
    <h1>Run Engine</h1>
    <el-table :data="opcuaInfoCompute" style="width: 100%">
      <el-table-column label="设备ID" prop="device_id"> </el-table-column>
      <el-table-column label="设备名称" prop="device_name"></el-table-column>
      <el-table-column label="设备URL" prop="url"> </el-table-column>
      <el-table-column label="设备点位数量" prop="pointCount">
      </el-table-column>
      <!-- 操作列 -->
      <el-table-column label="Actions" width="240">
        <template v-slot="scope">
          <el-button size="small" @click="startTask(scope.row)"
            >Start</el-button
          >
          <el-button size="small" type="danger" @click="stopTask(scope.row)"
            >Stop</el-button
          >
          <el-button
            size="small"
            type="danger"
            @click="forceStopTask(scope.row)"
            >Force Stop</el-button
          >
        </template>
      </el-table-column>
      <el-table-column label="PID" prop="pid"></el-table-column>
      <el-table-column label="状态" prop="pid_status"></el-table-column>
    </el-table>
  </div>
</template>
  
<script setup>
import axios from "../api/axios"; // 引入 Axios 封装
import { ref, onMounted, computed, onBeforeUnmount } from "vue";
import { OPCUAStore } from "../store/opcua";
import { ElMessageBox, ElMessage } from "element-plus";

// 获取状态信号
const opcuastore = OPCUAStore();
const opcuaInfo = ref([]);
const pidInfo = ref({});
let intervalId = null;

const pidStatus = ref({});

const opcuaInfoCompute = computed(() => {
  const temp = [];
  opcuaInfo.value.forEach((item) => {
    temp.push({
      device_id: item.id,
      device_name: item.device_name,
      url: item.url,
      pointCount: item.opcua_points.length,
      pid: pidInfo.value[item.id] || opcuastore.deviceRunPid[item.id],
      pid_status: pidStatus.value[item.id],
    });
  });
  return temp;
});

// delpoy后，需要将设备数据和点位数据存入到redis缓存中，方便采集任务调用
async function get_deploy_data() {
  try {
    await axios.post("/get_deploy_data").then((response) => {
      if ((response.data.status = "success")) {
        opcuaInfo.value = response.data.data;
        ElMessage({
          showClose: true,
          message: "Get Deploy Data success!",
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
  } catch {
    (error) => {
      console.log(error);
      ElMessage({
        showClose: true,
        message: error,
        type: "error",
      });
      console.log(error);
    };
  }
}

// 启动任务
function startTask(row) {
  const data = { device_id: row.device_id };
  try {
    axios.post("/task/start", data).then((response) => {
      if (response.data.status == "success") {
        pidInfo.value[row.device_id] = response.data.data;
        opcuastore.setdeviceRunPidData(pidInfo.value);
        ElMessage({
          showClose: true,
          message: response.data.message,
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
    console.log(e);
    ElMessage({
      showClose: true,
      message: e,
      type: "error",
    });
  }
}

// 停止任务
function stopTask(row) {
  const data = {
    device_id: row.device_id,
    pid: opcuastore.deviceRunPid[row.device_id],
  };
  try {
    axios
      .post("/task/stop", data)
      .then((response) => {
        if (response.data.status == "success") {
          ElMessage({
            showClose: true,
            message: response.data.message,
            type: "success",
          });
        } else {
          ElMessage({
            showClose: true,
            message: response.data.message,
            type: "error",
          });
        }
      })
      .catch((e) => {
        console.log(e);
        ElMessage({
          showClose: true,
          message: e.response.data.message,
          type: "error",
        });
      });
  } catch (e) {
    alert("停止引擎失败：" + e);
  }
}

// 停止任务
function forceStopTask(row) {
  const data = { device_id: row.device_id, force_shutdown: true };
  try {
    axios
      .post("/task/stop", data)
      .then((response) => {
        console.log(response);
        alert(response.data.message);
      })
      .catch((e) => {
        ElMessage({
          showClose: true,
          message: e.response.data.message,
          type: "error",
        });
      });
  } catch (e) {
    alert("停止引擎失败：" + e);
  }
}

// 定义获取数据的函数
async function fetchMonitorData() {
  const data = { pid_info: opcuastore.deviceRunPid };
  try {
    await axios
      .post("/get_monitor_data", data)
      .then((response) => {
        pidStatus.value = response.data.data;
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
      console.log(error);
    };
  }
}
onMounted(() => {
  get_deploy_data();
  intervalId = setInterval(fetchMonitorData, 3000); // 每10秒请求一次
});

// 组件卸载前清除定时器
onBeforeUnmount(() => {
  clearInterval(intervalId);
});
</script>
  

<style scoped>
</style>