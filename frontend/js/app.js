import { DashboardDetailsPage } from "../components/DashboardDetails.js";
import Router from "../services/Router.js";

window.app = {
  Router,
  showMessage: (message, type = "success") => {
    const messagesDiv = document.getElementById("messages");
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = `
            <span>${message}</span>
            <button class="btn-message" onclick="this.parentElement.remove()">&times;</button>
        `;
    messagesDiv.appendChild(messageDiv);

    setTimeout(() => {
      if (messageDiv.parentElement) {
        messageDiv.remove();
      }
    }, 5000);
  },
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
