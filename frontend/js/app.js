import { DashboardDetailsPage } from "../components/DashboardDetails.js";
import Router from "../services/Router.js";

window.app = { Router };

document.addEventListener("DOMContentLoaded", function () {
  app.Router.init();
});
