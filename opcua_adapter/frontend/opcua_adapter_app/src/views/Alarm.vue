<!-- src/views/About.vue -->
<template>
  <div>
    <!-- 标题 -->
    <h1>
      Alarm Information
    </h1>
    <!-- 显示内容 -->
    <el-row :gutter="24">
      <!-- 显示OPCUA点 -->
      <el-col :span="24">
        <div class="grid-content ep-bg-purple">
          <el-card style="max-width: 1320px; height: 600px">
            <template #header>
              <div class="card-header">
                <el-row :gutter="24">
                  <el-col :span="12">
                    <span>报警列表</span>
                  </el-col>
                  <el-col :span="4">
                    <!-- <el-button
                      type="danger"
                      @click="deleteAllData('opcuapoints')"
                      >清空数据
                    </el-button> -->
                  </el-col>
                </el-row>
                <el-divider />
              </div>
            </template>
            <el-table :data="alarmData" height="300" style="width: 100%">
              <!-- <el-table-column type="selection" width="55" /> -->
              <el-table-column label="tag_uuid" prop="tag_uuid">
              </el-table-column>
              <el-table-column label="tag_name" prop="tag_name"></el-table-column>
              <el-table-column label="报警信息" prop="alarm_message">
              </el-table-column>
              <el-table-column label="报警限值" prop="alarm_limit">
              </el-table-column>
              <el-table-column label="当前值" prop="value">
              </el-table-column>
              <el-table-column label="发生时间" prop="created_at">
              </el-table-column>
            </el-table>
            <el-pagination
              v-model:currentPage="alarmCurrentPage"
              v-model:page-size="alarmPerPage"
              :size="size"
              :background="background"
              layout="total, prev, pager, next"
              v-model:total="alarmTotal"
              @size-change="handleAlarmSizeChange"
              @current-change="handleAlarmCurrentChange"
            />
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import axios from "../api/axios"; // 引入 Axios 封装
import { ref, onMounted } from "vue";
import { ElMessageBox, ElMessage } from "element-plus";


// OPCUA 设备数据
const alarmData = ref([]);

// OPCUA 点表数据
const alarmCurrentPage = ref(1); // 报警信息的分页
const alarmPerPage = ref(1); // 
const alarmTotal = ref(1); // 

// 分页size
const size = ref("small");
// 分页背景
const background = ref(false);
// 分页
const disabled = ref(false);

// 处理OPCUA点表每个页面大小
const handleAlarmSizeChange = (val) => {
  console.log(`${val} items per page`);
};

// 处理翻页
const handleAlarmCurrentChange = (val) => {
  console.log(`current page: ${val}`);
  alarmCurrentPage.value = val;
  get_alarms(val);
};


// 获取alarms数据
async function get_alarms(page) {
  const params = { page: page };
  try {
    await axios
      .get(`/get_alarms`, { params: params })
      .then((response) => {
        alarmPerPage.value = response.data.data.per_page;
        alarmTotal.value = response.data.data.total;
        alarmCurrentPage.value = response.data.data.page;
        alarmData.value = response.data.data.items;
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


// 组件挂载完成后加载
onMounted(() => {
  get_alarms(1);
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
  