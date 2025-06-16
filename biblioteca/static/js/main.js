window.app = {
  showModal: (message) => {
    document.getElementById("alert-modal").showModal();
    document.querySelector("#alert-modal p").textContent = message;
  },
  showDeleteModal: (button, message) => {
    const modal = document.getElementById("alert-modal");
    const form = document.getElementById("delete-form");

    modal.querySelector("p").textContent = message;

    form.action = button.getAttribute("data-delete-url");

    modal.showModal();
  },
  closeModal: () => {
    document.getElementById("alert-modal").close();
  },
};
