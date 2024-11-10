<!-- src/views/About.vue -->
<template>
  <div>
    <h1>Init OPCUA Adapter</h1>
  </div>
  <el-tooltip
    content="初始化MySQL数据库,创建数据库,创建报警数据表"
    placement="top"
  >
    <el-button type="primary" @click="initMySQLBtn"
      >Init MySQL Btn</el-button
    ></el-tooltip
  >
  <el-tooltip
    content="初始化时序数据库,创建数据库，创建超级表，创建数据表"
    placement="top"
  >
    <el-button type="primary" @click="initTdengineBtn"
      >Init Tdengine Btn</el-button
    ></el-tooltip
  >
  <el-divider />
</template>
  
<script setup>
import axios from "../api/axios"; // 引入 Axios 封装
import { ref, onMounted } from "vue";

function initMySQLBtn() {
  try {
    axios.post("/init_mysql").then((response) => {
      if (response.data.status == "success") {
        alert(response.data.message);
      } else {
        alert(response.data.message);
      }
    });
  } catch {
    (error) => {
      console.log(error);
    };
  }
}

function initTdengineBtn() {
  try {
    axios.post("/init_tdengine").then((response) => {
      if (response.data.status == "success") {
        alert(response.data.message);
      } else {
        alert(response.data.message);
      }
    });
  } catch {
    (error) => {
      console.log(error);
    };
  }
}

onMounted(() => {
  // 初始化 JSON 字符串
});
</script>
  