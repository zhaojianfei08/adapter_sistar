<template>
  <el-container style="height: 100vh;">
    <!-- 左侧菜单栏 -->
    <el-aside width="200px" style="background-color: #2d3a4b; color: white;">
      <el-menu :default-active="activeMenu" class="el-menu-vertical-demo" background-color="#2d3a4b" text-color="#fff" active-text-color="#ffd04b"  @select="handleSelect">
        <el-menu-item index="/" >
          <i class="el-icon-menu"></i>
          <span>RUN</span>
        </el-menu-item>
        <el-menu-item index="/config">
          <i class="el-icon-setting"></i>
          <span>Config</span>
        </el-menu-item>
        <el-menu-item index="/init">
          <i class="el-icon-setting"></i>
          <span>Init</span>
        </el-menu-item>
        <el-menu-item index="/alarm">
          <i class="el-icon-setting"></i>
          <span>Alarm</span>
        </el-menu-item>
        <el-menu-item index="/log">
          <i class="el-icon-setting"></i>
          <span>Log</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 右侧内容栏 -->
    <el-container>
      <el-header style="background-color: #324157; color: white; padding: 10px;">
        <h2 style="line-height: 100%;">OPCUA Adapter APP</h2>
      </el-header>
      
      <el-main>
        <!-- 通过 Vue Router 渲染的内容 -->
        <router-view></router-view>
      </el-main>
      
      <el-footer style="background-color: #324157; color: white; text-align: center; padding: 10px;">
        泰航智造 © 2024 
      </el-footer>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      activeMenu: '/', // 当前激活的菜单项
    };
  },
  watch: {
    // 监听路由变化，更新菜单的激活状态
    $route(to) {
      this.activeMenu = to.path;
    }
  },
  mounted() {
    // 页面加载时，根据当前路由设置激活的菜单项
    this.activeMenu = this.$route.path;
  },
  methods: {
    // 当选择菜单项时，进行路由跳转
    handleSelect(index) {
      console.log(index)
      this.$router.push(index);
    }
  }
};
</script>

<style scoped>
.el-header {
  background-color: #324157;
  color: white;
}
</style>
