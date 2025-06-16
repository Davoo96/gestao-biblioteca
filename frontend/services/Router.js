import { API } from "./API.js";

let authors = [];
let categories = [];
let books = [];
let loans = [];

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

function showSection(sectionName) {
  document
    .querySelectorAll(".nav-btn")
    .forEach((btn) => btn.classList.remove("active"));

  document
    .querySelectorAll(".section")
    .forEach((section) => section.classList.remove("active"));

  const activeButton = document.querySelector(
    `[data-section="${sectionName}"]`
  );
  if (activeButton) {
    activeButton.classList.add("active");
  }

  const activeSection = document.getElementById(sectionName);
  if (activeSection) {
    activeSection.classList.add("active");
  }
}

async function loadDashboard() {
  const dashboardElement = document.querySelector("dashboard-details-page");
  if (dashboardElement) {
    await dashboardElement.render();
  }
}

async function loadCategories() {
  try {
    categories = await API.getCategories();

    const tbody = document.getElementById("categories-table");
    if (categories.length === 0) {
      tbody.innerHTML =
        '<tr><td colspan="3">Nenhuma categoria encontrada</td></tr>';
      return;
    }

    tbody.innerHTML = categories
      .map(
        (category) => `
            <tr>
                <td>${category.name}</td>
                <td>${category.description || "-"}</td>
                <td>
                    <button class="btn-delete" data-type="category" data-id="${
                      category.id
                    }">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `
      )
      .join("");
  } catch (error) {
    document.getElementById("categories-table").innerHTML =
      '<tr><td colspan="3">Erro ao carregar categorias</td></tr>';
  }
}

async function loadSelectOptions() {
  try {
    authors = await API.getAuthors();
    categories = await API.getCategories();
    books = await API.getBooks();

    const authorSelects = document.querySelectorAll('select[name="author"]');
    authorSelects.forEach((select) => {
      select.innerHTML =
        '<option value="">Selecione um autor</option>' +
        authors
          .map(
            (author) => `<option value="${author.id}">${author.name}</option>`
          )
          .join("");
    });

    const categorySelects = document.querySelectorAll(
      'select[name="category"]'
    );
    categorySelects.forEach((select) => {
      select.innerHTML =
        '<option value="">Selecione uma categoria</option>' +
        categories
          .map(
            (category) =>
              `<option value="${category.id}">${category.name}</option>`
          )
          .join("");
    });

    const categoryFilter = document.getElementById("book-category-filter");
    if (categoryFilter) {
      categoryFilter.innerHTML =
        '<option value="">Todas as categorias</option>' +
        categories
          .map(
            (category) =>
              `<option value="${category.id}">${category.name}</option>`
          )
          .join("");
    }

    const availableBooks = books.filter((book) => book.status === "available");
    const loanBookSelect = document.querySelector(
      '#loan-form select[name="book"]'
    );
    if (loanBookSelect) {
      loanBookSelect.innerHTML =
        '<option value="">Selecione um livro disponível</option>' +
        availableBooks
          .map((book) => `<option value="${book.id}">${book.title}</option>`)
          .join("");
    }
  } catch (error) {
    console.error("Erro ao carregar opções:", error);
  }
}

async function loadAuthors() {
  try {
    authors = await API.getAuthors();

    const tbody = document.getElementById("authors-table");
    if (authors.length === 0) {
      tbody.innerHTML = '<tr><td colspan="3">Nenhum autor encontrado</td></tr>';
      return;
    }

    tbody.innerHTML = authors
      .map(
        (author) => `
            <tr>
                <td>${author.name}</td>
                <td>${author.nationality || "-"}</td>
                <td>
                    <button class="btn-delete" data-type="author" data-id="${
                      author.id
                    }">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `
      )
      .join("");
  } catch (error) {
    document.getElementById("authors-table").innerHTML =
      '<tr><td colspan="3">Erro ao carregar autores</td></tr>';
  }
}

async function loadBooks() {
  try {
    const search = document.getElementById("book-search")?.value || "";
    const category =
      document.getElementById("book-category-filter")?.value || "";
    const status = document.getElementById("book-status-filter")?.value || "";

    const params = {};
    if (search) params.search = search;
    if (category) params.category = category;
    if (status) params.status = status;

    books = await API.getBooks(params);

    const tbody = document.getElementById("books-table");
    if (books.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6">Nenhum livro encontrado</td></tr>';
      return;
    }

    tbody.innerHTML = books
      .map(
        (book) => `
            <tr>
                <td>${book.title}</td>
                <td>${book.author_name || book.author}</td>
                <td>${book.category_name || book.category}</td>
                <td>
                    <span class="status ${book.status}">
                        ${getStatusText(book.status)}
                    </span>
                </td>
                <td>${book.pages}</td>
                <td>
                    <button class="btn-delete" data-type="book" data-id="${
                      book.id
                    }">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `
      )
      .join("");
  } catch (error) {
    document.getElementById("books-table").innerHTML =
      '<tr><td colspan="6">Erro ao carregar livros</td></tr>';
  }
}

function getStatusText(status) {
  const statusMap = {
    available: "Disponível",
    loaned: "Emprestado",
    maintenance: "Manutenção",
  };
  return statusMap[status] || status;
}

async function deleteBook(id) {
  app.showModal("Tem certeza que deseja excluir este livro?");
  app.confirmDelete(async () => {
    try {
      await API.deleteBook(id);
      API.showMessage("Livro excluído com sucesso!");
      loadBooks();
    } catch (error) {
      API.showMessage("Erro ao excluir livro", "error");
    }
  });
}

async function deleteAuthor(id) {
  app.showModal("Tem certeza que deseja excluir este autor?");
  app.confirmDelete(async () => {
    try {
      await API.deleteAuthor(id);
      API.showMessage("Autor excluído com sucesso!");
      loadAuthors();
      loadSelectOptions();
    } catch (error) {
      API.showMessage("Erro ao excluir autor", "error");
    }
  });
}

async function deleteCategory(id) {
  app.showModal("Tem certeza que deseja excluir esta categoria?");
  app.confirmDelete(async () => {
    try {
      await API.deleteCategory(id);
      API.showMessage("Categoria excluída com sucesso!");
      loadCategories();
      loadSelectOptions();
    } catch (error) {
      API.showMessage("Erro ao excluir categoria", "error");
    }
  });
}

async function loadLoans() {
  try {
    loans = await API.getLoans();
    books = await API.getBooks();

    const tbody = document.getElementById("loans-table");
    if (loans.length === 0) {
      tbody.innerHTML =
        '<tr><td colspan="6">Nenhum empréstimo encontrado</td></tr>';
      return;
    }

    tbody.innerHTML = loans
      .map(
        (loan) => `
            <tr>
                <td>${loan.book_title || "N/A"}</td>
                <td>${loan.borrower_name}</td>
                <td>${formatDate(loan.loan_date)}</td>
                <td>${formatDate(loan.expected_return_date)}</td>
                <td>
                    <span class="status ${
                      loan.returned ? "returned" : "active"
                    }">
                        ${loan.returned ? "Devolvido" : "Ativo"}
                    </span>
                </td>
                <td>
                    ${
                      !loan.returned
                        ? `
                        <button class="btn-return" data-id="${loan.id}">
                            <i class="fas fa-undo"></i> Devolver
                        </button>
                    `
                        : "-"
                    }
                </td>
            </tr>
        `
      )
      .join("");
  } catch (error) {
    document.getElementById("loans-table").innerHTML =
      '<tr><td colspan="6">Erro ao carregar empréstimos</td></tr>';
  }
}

async function returnBook(id) {
  const returnDate = new Date().toISOString().split("T")[0];
  app.showModal(`Confirmar devolução para a data: ${returnDate}`);
  app.confirmDelete(async () => {
    try {
      await API.returnBook(id, returnDate);
      API.showMessage("Livro devolvido com sucesso!");
      loadLoans();
      loadBooks();
    } catch (error) {
      API.showMessage("Erro ao devolver livro", "error");
    }
  });
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString("pt-BR");
}

const Router = {
  currentSection: "dashboard",

  init: () => {
    document.addEventListener("click", async (e) => {
      if (e.target.closest(".btn-delete")) {
        const button = e.target.closest(".btn-delete");
        const type = button.dataset.type;
        const id = button.dataset.id;

        switch (type) {
          case "category":
            await deleteCategory(id);
            break;
          case "author":
            await deleteAuthor(id);
            break;
          case "book":
            await deleteBook(id);
            break;
        }
      }

      if (e.target.closest(".btn-return")) {
        const button = e.target.closest(".btn-return");
        const id = button.dataset.id;

        if (id) {
          await returnBook(id);
        } else {
          console.error("No loan ID found for return button");
        }
      }

      if (e.target.closest("[data-action='filter-books']")) {
        await loadBooks();
      }
    });

    document.querySelectorAll(".nav-btn").forEach((button) => {
      button.addEventListener("click", function () {
        const sectionName = this.getAttribute("data-section");
        if (sectionName) {
          Router.navigate(sectionName);
        }
      });
    });

    loadSelectOptions();

    Router.setupFormListeners();

    const bookSearch = document.getElementById("book-search");
    if (bookSearch) {
      bookSearch.addEventListener("input", debounce(loadBooks, 500));
    }

    Router.navigate("dashboard");
  },

  navigate: (sectionName) => {
    Router.currentSection = sectionName;
    showSection(sectionName);

    switch (sectionName) {
      case "categories":
        loadCategories();
        break;
      case "authors":
        loadAuthors();
        break;
      case "books":
        loadBooks();
        break;
      case "loans":
        loadLoans();
        break;
      case "dashboard":
        loadDashboard();
        break;
    }
  },

  setupFormListeners: () => {
    const bookForm = document.getElementById("book-form");
    if (bookForm) {
      bookForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const data = Object.fromEntries(formData.entries());

        try {
          await API.createBook(data);
          API.showMessage("Livro adicionado com sucesso!");
          this.reset();
          loadBooks();
        } catch (error) {
          API.showMessage("Erro ao adicionar livro", "error");
        }
      });
    }

    const authorForm = document.getElementById("author-form");
    if (authorForm) {
      authorForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const data = Object.fromEntries(formData.entries());

        try {
          await API.createAuthor(data);
          API.showMessage("Autor adicionado com sucesso!");
          this.reset();
          loadAuthors();
          loadSelectOptions();
        } catch (error) {
          API.showMessage("Erro ao adicionar autor", "error");
        }
      });
    }

    const categoryForm = document.getElementById("category-form");
    if (categoryForm) {
      categoryForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const data = Object.fromEntries(formData.entries());

        try {
          await API.createCategory(data);
          API.showMessage("Categoria adicionada com sucesso!");
          this.reset();
          loadCategories();
          loadSelectOptions();
        } catch (error) {
          console.error(error);
          API.showMessage("Erro ao adicionar categoria", "error");
        }
      });
    }

    const loanForm = document.getElementById("loan-form");
    if (loanForm) {
      loanForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const data = Object.fromEntries(formData.entries());

        try {
          await API.createLoan(data);
          API.showMessage("Empréstimo criado com sucesso!");
          this.reset();
          loadLoans();
          loadBooks();
          loadSelectOptions();
        } catch (error) {
          API.showMessage("Erro ao criar empréstimo", "error");
        }
      });
    }
  },

  getCurrentSection: () => Router.currentSection,

  refresh: () => {
    showSection(Router.currentSection);
  },
};

export default Router;
