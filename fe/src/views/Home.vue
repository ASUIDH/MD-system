<template>

  <div class="home">
    <el-container>
      <div class ="head_1">Windows恶意软件相似性度量平台</div>
      <el-header >
        <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          @select="handleSelect"
          active-text-color="rgb(53,167,89)"
          router
        >

          <el-menu-item index="/1"><img src="../assets/imgs/icon-test.png" alt="" style="width:25px"/>&nbsp;软件检测</el-menu-item>
          <el-menu-item index="/2"><img src="../assets/imgs/sousuo.png" alt="" style="width:20px"/>&nbsp;检测搜索</el-menu-item>
          <el-menu-item index="/3"><img src="../assets/imgs/wenbenxiangsixing-4.png" alt="" style="width:20px"/>&nbsp;相似性度量</el-menu-item>
          
        </el-menu>

        <div v-if="!isLogin" class="sign">
          <el-button
            style="margin-right: 20px"
            round
            size="small"
            type="primary"
            @click="editDialogVisible = true"
            >登陆 | 注册</el-button
          >
        </div>

        <div v-else>
          <el-dropdown @command="handleCommand" style="margin-right: 20px">
            <el-button type="success">
              {{ name }}<i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="history">历史记录</el-dropdown-item>
              <el-dropdown-item command="logout">退出</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
      <!-- <el-footer>Footer</el-footer> -->

      <el-dialog
        :visible.sync="editDialogVisible"
        width="35%"
        @close="reset(activeName)"
        class="dialog"
        modal
      >
        <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
          <el-tab-pane label="登陆" name="login">
            <el-form
              :model="editForm"
              :rules="editFormRules"
              ref="login"
              label-width="70px"
            >
              <el-form-item label="邮箱" prop="email">
                <el-input
                  :style="{ width: cORp ? '62%' : '100%' }"
                  v-model="editForm.email"
                  placeholder="请输入邮箱"
                  clearable
                ></el-input>
                <el-button
                  v-if="cORp"
                  type="primary"
                  size="mini"
                  @click="sendEmail('login')"
                  :disabled="isDisabled_l"
                  :style="{ marginLeft: '50px' }"
                  >{{
                    isDisabled_l ? `${clock_l}s后可重新发送` : "发送验证码"
                  }}</el-button
                >
              </el-form-item>
              <el-form-item label="验证码" prop="code" v-if="cORp">
                <el-input
                  v-model="editForm.code"
                  placeholder="请输入验证码"
                ></el-input>
              </el-form-item>
              <el-form-item label="密码" prop="password" v-else>
                <el-input
                  v-model="editForm.password"
                  placeholder="请输入密码"
                ></el-input>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="注册" name="register">
            <el-form
              :model="editForm"
              :rules="editFormRules"
              ref="register"
              label-width="70px"
            >
              <el-form-item label="邮箱" prop="email" class="email">
                <el-input
                  style="width: 62%"
                  v-model="editForm.email"
                  placeholder="请输入邮箱"
                  clearable
                >
                </el-input>

                <el-button
                  type="primary"
                  size="mini"
                  @click="sendEmail('register')"
                  :disabled="isDisabled_r"
                  :style="{ marginLeft: '50px' }"
                  >{{
                    isDisabled_r ? `${clock_r}s后可重新发送` : "发送验证码"
                  }}</el-button
                >
              </el-form-item>
              <el-form-item label="昵称" prop="username">
                <el-input
                  v-model="editForm.username"
                  placeholder="请输入昵称"
                  clearable
                ></el-input>
              </el-form-item>
              <el-form-item label="密码" prop="password">
                <el-input
                  v-model="editForm.password"
                  placeholder="请输入密码"
                  clearable
                ></el-input>
              </el-form-item>
              <el-form-item label="验证码" prop="code">
                <el-input
                  v-model="editForm.code"
                  placeholder="请输入验证码"
                ></el-input>
              </el-form-item> </el-form
          ></el-tab-pane>
        </el-tabs>

        <div slot="footer" class="dialog-footer">
          <div v-if="activeName === 'login'" class="text">
            <el-link @click="cORp = !cORp" type="primary">
              {{ cORp ? "密码登陆" : "验证码登陆" }}
            </el-link>
          </div>
          <div>
            <el-button type="primary" @click="sign">{{
              activeName === "login" ? "登陆" : "注册"
            }}</el-button>
            <el-button @click="reset(activeName)">取 消</el-button>
          </div>
        </div>
      </el-dialog>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      clock_r: 5,
      clock_l: 5,
      isDisabled_r: false,
      isDisabled_l: false,

      cORp: true, // 验证码还是密码登录  true 为验证码
      activeName: "login",
      activeIndex: "/1",
      dropdown: -1,
      isLogin: false,
      editDialogVisible: false,
      name: "",
      editForm: {
        username: "",
        password: "",
        code: "",
        email: "",
        csrf_token: "",
      },
      email: "",
      realCode: "",
      editFormRules: {
        email: [{ required: true, message: "请输入邮箱", trigger: "blur" }],
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
        code: [{ required: true, message: "请输入验证码", trigger: "blur" }],
      },
    };
  },
  async created() {
    const { data } = await this.$http.get("/user/session");
    if (data.code) {
      this.isLogin = true;
      this.name = data.data;
      this.email = data.email;
    }
    this.activeIndex = this.$route.path;
  },

  methods: {
    toast(txt) {
      this.$alert(txt, "提示", {
        confirmButtonText: "确定",
        callback: () => {},
      });
    },
    async sendEmail(lORr) {
      if (this.editForm.email === "") {
        this.$message.error("邮箱不能为空!");
        return;
      }
      await this.initCSRF();
      const { data } = await this.$http.post(
        `/email/${this.activeName}`,
        this.editForm
      );
      if (data.status === "OK") {
        this.realCode = data.data;
        if (lORr === "login") {
          this.isDisabled_l = true;
          this.clock_l === 5; // 复原倒计时
          let timer = setInterval(() => {
            if (this.clock_l === 1) {
              this.isDisabled_l = false;
              clearInterval(timer);
            }
            this.clock_l--;
          }, 1000);
        } else {
          this.isDisabled_r = true;
          this.clock_r = 5;
          let timer = setInterval(() => {
            if (this.clock_r === 1) {
              this.isDisabled_r = false;
              clearInterval(timer);
            }
            this.clock_r--;
          }, 1000);
        }
      } else if (data.status === "EXIST") {
        this.toast("该邮箱已注册，请直接登陆");
      } else if (data.status === "NOTEXIST") {
        this.toast("该邮箱未注册，请注册");
      } else {
        this.$message.error("出错了，请重新发送");
      }
    },

    async initCSRF() {
      await this.$http.get("/csrf");
      this.editForm.csrf_token = this.getCookie("csrf_token");
    },
    getCookie(name) {
      let r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
      return r ? r[1] : undefined;
    },
    reset(formName) {
      this.$refs[formName].resetFields();
      this.editDialogVisible = false;
    },

    // 登陆/注册
    async sign() {
      this.$refs[this.activeName].validate(async (valid) => {
        if (!valid) return;
        await this.initCSRF();

        // 注册 或者 验证码登陆时要 检验验证码对不对
        if (
          this.activeName === "register" ||
          (this.activeName === "login" && this.cORp)
        ) {
          if (this.editForm.code !== this.realCode) {
            this.toast("验证码不正确");
            return;
          }
        }
        if (
          this.activeName === "login" &&
          !this.cORp &&
          this.editForm.email === "admin" &&
          this.editForm.password === "admin"
        ) {
          this.$router.push("/admin_home");
          return;
        }
        let url = `/user/register`;
        if (this.activeName === "login") {
          url = `/user/login/${this.cORp}`; // 告诉后端是哪种登陆方式
        }

        const { data: res } = await this.$http.post(url, this.editForm);
        if (this.activeName === "login") {
          if (res.code) {
            this.$message.success("登陆成功");
            this.isLogin = true;
            this.name = res.data; // 点登陆后会清空editForm
            this.email = res.email;

            this.editDialogVisible = false;
          } else {
            this.toast(res.data);
            this.$refs["login"].resetFields();
          }
        } else {
          if (res.code) {
            this.isLogin = true;
            this.name = res.data; // 点登陆后会清空editForm
            this.email = res.email;
            this.editDialogVisible = false;
          }
        }
      });
    },
    handleClick(tab, event) {
      this.$refs[
        this.activeName === "login" ? "register" : "login"
      ].resetFields();
    },
    handleSelect(key, keyPath) {
      console.log(keyPath);

      this.activeIndex = keyPath[0];
    },
    async handleCommand(command) {
      if (command === "logout") {
        await this.$http.get("/user/logout");
        this.isLogin = false;
        this.initCSRF();
      } else if (command === "history") {
        this.activeIndex = "";
        this.$router.push(`/history/${this.email}`);
      }
    },
  },
};
</script>


<style scoped>

.el-footer,
.el-header {
  display: flex;
  justify-content: space-between;
  align-content: center;
  color: rgb(48, 230, 57);
  text-align: center;
  line-height: 60px;
  padding:0px 0px 0px 85px;
  height: 60px;
  box-shadow: 10px 10px 5px #888888;
  background:  rgb(53,167,89);

}

.el-main {
  height: 900px;
  color: rgb(0, 0, 0);
  text-align: center;
  position: relative;
  padding: 0;
  background-color: rgb(236, 240, 244);
  background-image:url( "../assets/imgs/beijing1.png");
  background-repeat:no-repeat;
  background-position: 128% 0%;
  box-shadow: 10px 10px 5px #888888;

}
.el-icon-arrow-down {
  font-size: 12px;
}

.sign {
  animation: signs 1s linear infinite;
}

@keyframes signs {
  50% {
    transform: scale(1.1);
  }
}
.dialog-footer {
  position: relative;
  margin-top: -30px;
  width: 100%;
}
.text {
  position: absolute;
  top: 8px;
  left: 15px;
}

.dialog {
  background: url(../assets/imgs/meadow-3743023_1280.jpg);
}

/* .el-dropdown {
  position: absolute;
  top: 15px;
  right: 20px;
} */
.el-menu-item{

  font-size:16px;
  background:  rgb(53,167,89);
  color: rgb(255,255,255);
  border-bottom-color:rgb(32,246,132);
}
.el-menu-item:hover{
    outline: 0 !important;

    background: rgb(255,255,255) !important;
    color:rgb(32,246,132);
}
.head_1{
  background:rgb(40,40,40);
  color:rgb(255,255,255);
  height:45px;
  font-size:36px;
  text-align:center;
  padding:0px 0px 0px 100px;
}
</style>
