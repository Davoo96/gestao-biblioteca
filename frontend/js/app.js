import { DashboardDetailsPage } from "../components/DashboardDetails.js";
import Router from "../services/Router.js";

window.app = {
  Router,
  currentDeleteAction: null,
  showModal: (message) => {
    document.getElementById("alert-modal").showModal();
    document.querySelector("#alert-modal p").textContent = message;
  },
  closeModal: () => {
    document.getElementById("alert-modal").close();
  },
  confirmDelete: (deleteFunction) => {
    app.currentDeleteAction = deleteFunction;
  },
  executeDelete: () => {
    if (app.currentDeleteAction) {
      app.currentDeleteAction();
      app.currentDeleteAction = null;
    }
    app.closeModal();
  },
};

document.addEventListener("DOMContentLoaded", function () {
  app.Router.init();
});
