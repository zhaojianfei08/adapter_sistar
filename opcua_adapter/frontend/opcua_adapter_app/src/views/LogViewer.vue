<!-- LogViewer.vue -->
<template>
  <div>
    <h2>Log Viewer</h2>
    <div v-if="pagedLogLines.length > 0">
      <ul>
        <li v-for="(line, index) in pagedLogLines" :key="index">{{ line }}</li>
      </ul>
      <!-- 分页控制 -->
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
      </div>
    </div>
    <div v-else>
      <p>No log data available.</p>
    </div>
  </div>
</template>

<script setup>
import axios from "../api/axios"; // 引入 Axios 封装
import { ref, onMounted, computed } from "vue";

const logLines = ref([]);
const currentPage = ref(1); // 当前页码
const itemsPerPage = ref(30); // 每页显示的日志条数

// 根据当前页码和每页显示条数计算当前页的日志条目
const pagedLogLines = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return logLines.value.slice(start, end);
});

// 计算总页数
const totalPages = computed(() =>
  Math.ceil(logLines.value.length / itemsPerPage.value)
);

// 分页控制
const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

async function fetchLogData() {
  try {
    await axios
      .get(`/logs`)
      .then((response) => {
        logLines.value = response.data.data || [];
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

onMounted(() => {
  fetchLogData();
});
</script>

<style scoped>
/* 样式 */
h2 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

ul {
  padding-left: 0;
  list-style-type: none;
  font-family: monospace;
}

li {
  white-space: pre-wrap;
  line-height: 1.4;
}

.pagination {
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
