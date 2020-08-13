<template>
  <div>
    <div class="home" v-if="loading">
      <div class="login" v-if="!show">
        <h3>Vsattech</h3>
        <el-input
          placeholder="请输入密码"
          v-model="pwd"
          show-password
          @keyup.native.enter="login()"
        ></el-input>
        <el-button
          type="primary"
          style="width:300px;margin-top:10px;"
          @click="login()"
          >Login</el-button
        >
      </div>
      <div class="pdf" v-if="show">
        <div class="img" v-for="item in pdf.page_size">
          <img
            :src="pdf.url_prefix + item + '.jpg?x-oss-process=style/logo'"
            alt
            width="100%"
            height="100%"
          />
        </div>
      </div>
    </div>
    <div v-if="no_file">
      <h1>NO FILE!</h1>
    </div>
  </div>
</template>

<script>
import md5 from "js-md5";
import { getPdf } from "@/api/pdf";

export default {
  name: "home",
  data() {
    return {
      pwd: "",
      url: "",
      show: false,
      no_file: false,
      loading: false,
      password: "",
    };
  },

  created() {
    document.oncontextmenu = function() {
      event.returnValue = false;
    };
    var url = this.$route.params.url;
    this.pwd = this.$route.query.pwd ? this.$route.query.pwd : "";
    this.handlerGetPdf(url);
  },
  methods: {
    async handlerGetPdf(uuid) {
      let res = await getPdf({ uuid: uuid });
      if (res.data) {
        this.pdf = res.data;
        this.loading = true;
        if (this.pwd == this.pdf.password) {
          this.show = true;
        }
      } else {
        this.no_file = true;
      }
    },
    login() {
      if (this.pwd == this.pdf.password) {
        this.show = true;
      } else {
        this.$message.error("密码错误");
      }
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
.pdf {
  background-color: gray;
  width: 100%;
  height: 100%;
}
.img {
  margin-bottom: 5px;
}
</style>
