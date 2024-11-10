// src/store/mstable.js
import { defineStore } from 'pinia';

export const OPCUAStore = defineStore('opcua', {
  state: () => ({
    deviceRunPid: {}
  }),
  actions: {
    setdeviceRunPidData(new_data){
       Object.assign(this.deviceRunPid, new_data);
    }
  },
  persist: true  // 启用持久化
});
