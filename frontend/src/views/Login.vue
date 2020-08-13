<template>
  <div class="home">
    <div class="login" v-if="!show">
      <h3>Vsattech</h3>
      <el-input placeholder="请输入用户名" v-model="username"></el-input>
      <el-input
        style="margin-top:10px;"
        placeholder="请输入密码"
        v-model="password"
        show-password
        @keyup.native.enter="hanlderLogin()"
      ></el-input>
      <el-button
        type="primary"
        style="width:300px;margin-top:10px;"
        @click="hanlderLogin()"
        >Admin Login</el-button
      >
    </div>
  </div>
</template>

<script>
import { setToken } from "@/utils/auth";
import { userLogin } from "@/api/user";
export default {
  name: "home",
  data() {
    return {
      username: "",
      password: "",
      show: false,
    };
  },

  created() {},
  methods: {
    hanlderLogin() {
      userLogin({
        username: this.username,
        password: this.password,
      }).then((response) => {
        setToken(" Bearer " + response.data.access_token);
        this.$message({
          message: "登录成功",
          type: "success",
        });
        this.$router.push({ path: "/list" });
      });
    },
  },
};
</script>

<style scoped>
.login {
  margin-top: 80px;
  width: 300px;
  margin: auto;
}
</style>
