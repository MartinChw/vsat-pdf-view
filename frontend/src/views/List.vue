<template>
  <div class="home">
    <div class="title"><h1>PDF LIST</h1></div>
    <el-table :data="list" style="width: 100%">
      <el-table-column prop="title" label="title" width="300">
      </el-table-column>
      <el-table-column prop="uuid" label="uuid" width="80"> </el-table-column>
      <el-table-column label="url-prefix">
        <template slot-scope="scope">
          <span class="url-prefix">{{ scope.row.url_prefix }}</span>
        </template>
      </el-table-column>
      <el-table-column label="pwd" width="120">
        <template slot-scope="scope">
          <el-input
            class="table-pwd"
            v-model="scope.row.password"
            style="border:0 !important;"
            show-password
          ></el-input
        ></template>
      </el-table-column>
      <el-table-column label="operation" align="right">
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="openPdf(scope.row)"
            >Open</el-button
          >
          <el-button
            type="primary"
            size="small"
            @click="showUpdatePdf(scope.row)"
            >Update</el-button
          >
          <el-button type="primary" size="small" @click="infoCopy(scope.row)"
            >Copy</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <div style="margin-top:20px">
      <el-button
        type="primary"
        size="small"
        style="float:left"
        @click="showCreatePdf()"
        >Create</el-button
      >
      <el-pagination
        background
        layout="prev, pager, next"
        :current-page.sync="page"
        @current-change="hanlderListPdf()"
        :page-size.sync="size"
        :total="count"
        style="float:right"
      >
      </el-pagination>
    </div>
    <el-dialog
      title="Create/Update PDF"
      :visible.sync="dialogVisible"
      width="700px"
    >
      <el-form ref="form" v-model="pdf" label-width="120px">
        <el-form-item label="title" required>
          <el-input v-model="pdf.title"></el-input>
        </el-form-item>
        <template v-if="action == 'update'">
          <el-form-item label="password" required>
            <el-input v-model="pdf.password" show-password></el-input>
          </el-form-item>
        </template>
        <template v-if="!upload">
          <el-form-item label="uuid" required>
            <el-input v-model="pdf.uuid"></el-input>
          </el-form-item>
          <el-form-item label="url_prefix" required>
            <el-input
              type="textarea"
              :autosize="{ minRows: 2, maxRows: 4 }"
              v-model="pdf.url_prefix"
            ></el-input>
          </el-form-item>
          <el-form-item label="page_size" required>
            <el-input v-model="pdf.page_size"></el-input>
          </el-form-item>
        </template>
        <el-form-item label="pdf-file" align="left" v-if="action == 'create'">
          <el-switch v-model="upload" active-text="Upload File"> </el-switch>
          <el-upload
            v-if="upload"
            class="upload-demo"
            action="https://jsonplaceholder.typicode.com/posts/"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :on-change="bindFile"
            :before-remove="beforeRemove"
            :limit="1"
            :on-exceed="handleExceed"
            :file-list="fileList"
            :auto-upload="false"
          >
            <el-button size="small" type="primary">Click Upload</el-button>
          </el-upload>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button
          type="primary"
          @click="action == 'create' ? handleCreatePdf() : handleUpdatePdf()"
          >Save</el-button
        >
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { setToken } from "@/utils/auth";
import { listPdf, createPdf, updatePdf } from "@/api/pdf";
export default {
  name: "home",
  data() {
    return {
      action_map: {
        update: "update",
        create: "create",
      },
      action: "create",
      show: false,
      upload: true,
      list: [],
      dialogVisible: false,
      fileList: [],
      title: "测试文件",
      pdf: {
        title: "",
        uuid: "",
        url_prefix: "",
        page_size: 0,
      },
      count: 0,
      page: 0,
      size: 10,
      file: null,
    };
  },

  created() {
    this.hanlderListPdf();
  },
  methods: {
    hanlderListPdf() {
      listPdf({ page: this.page, limit: this.size }).then((res) => {
        this.list = res.data.items;
        this.count = res.data.count;
      });
    },
    handleRemove(file, fileList) {},
    handlePreview(file) {},
    infoCopy(row) {
      let str =
        "标题： " +
        row.title +
        "\n" +
        "链接： http://pdf.vsattech.com/" +
        row.uuid +
        "\n" +
        "密码： " +
        row.password;
      this.copyToClipboard(str + "");
    },
    openPdf(row) {
      this.$router.push({
        path: "/" + row.uuid,
        query: { pwd: row.password },
      });
    },
    bindFile(files, fileList) {
      //绑定文件
      this.file = fileList[0];
    },
    handleExceed(files, fileList) {
      this.$message.warning(
        `当前限制选择 1 个文件，本次选择了 ${
          files.length
        } 个文件，共选择了 ${files.length + fileList.length} 个文件`
      );
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },
    copyToClipboard(text) {
      if (text.indexOf("-") !== -1) {
        let arr = text.split("-");
        text = arr[0] + arr[1];
      }
      var textArea = document.createElement("textarea");
      textArea.style.position = "fixed";
      textArea.style.top = "0";
      textArea.style.left = "0";
      textArea.style.width = "2em";
      textArea.style.height = "2em";
      textArea.style.padding = "0";
      textArea.style.border = "none";
      textArea.style.outline = "none";
      textArea.style.boxShadow = "none";
      textArea.style.background = "transparent";
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();

      try {
        var successful = document.execCommand("copy");
        var msg = successful
          ? "成功复制到剪贴板"
          : "该浏览器不支持点击复制到剪贴板";
        //alert(msg);
        this.$message({
          message: msg,
          type: "success",
        });
      } catch (err) {
        //alert('该浏览器不支持点击复制到剪贴板');
        this.$message({
          message: "该浏览器不支持点击复制到剪贴板",
          type: "error",
        });
      }

      document.body.removeChild(textArea);
    },
    handleCreatePdf() {
      let formData = new FormData();
      formData.append("title", this.pdf.title);

      if (this.upload && this.file) {
        formData.append("file", this.file.raw);
      } else {
        formData.append("uuid", this.pdf.uuid);
        formData.append("url_prefix", this.pdf.url_prefix);
        formData.append("page_size", this.pdf.page_size);
      }
      createPdf(formData).then((res) => {
        this.$message({
          message: "SUCCESS",
          type: "success",
        });
        this.hanlderListPdf();
        this.dialogVisible = false;
      });
    },
    showUpdatePdf(row) {
      this.pdf = row;
      this.dialogVisible = true;
      this.action = "update";
      this.upload = false;
    },
    showCreatePdf() {
      this.dialogVisible = true;
      this.action = "create";
      this.upload = true;
    },
    handleUpdatePdf() {
      updatePdf(this.pdf).then((res) => {
        this.$message({
          message: "SUCCESS",
          type: "success",
        });
        this.hanlderListPdf();
        this.dialogVisible = false;
      });
    },
  },
};
</script>

<style scoped>
.home {
  margin-top: 80px;
  width: 1000px;
  margin: auto;
}
.table-pwd >>> input {
  border: 0 !important;
  background-color: transparent !important;
}

.home >>> .url-prefix {
  vertical-align: middle;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>
