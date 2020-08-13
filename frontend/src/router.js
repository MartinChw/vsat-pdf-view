import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";
import Login from "./views/Login.vue";
import List from "./views/List.vue";
import PdfLog from "./views/PdfLog.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/auth",
      component: Login,
    },
    {
      path: "/list",
      component: List,
    },
    {
      path: "/pdflog",
      component: PdfLog,
    },
    {
      path: "/:url",
      name: "plan",
      component: Home,
    },
  ],
});
