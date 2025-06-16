export const API = {
  baseURL: "http://localhost:8000/api",
  getDashboard: async () => {
    return await API.fetch("/dashboard");
  },
  getBook: async (id) => {
    return API.fetch(`/books/${id}`);
  },
  getBooks: async (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return API.fetch(`/books/${query ? "?" + query : ""}`);
  },
  createBook: async (data) => {
    return API.fetch("/books/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
  updateBook: async (id, data) => {
    return API.fetch(`/books/${id}/`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },
  deleteBook: async (id) => {
    return API.fetch(`/books/${id}/`, {
      method: "DELETE",
    });
  },
  getAuthors: async () => {
    return API.fetch("/authors/");
  },
  createAuthor: async (data) => {
    return API.fetch("/authors/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
  deleteAuthor: async (id) => {
    return API.fetch(`/authors/${id}/`, {
      method: "DELETE",
    });
  },
  getCategories: async () => {
    return API.fetch("/categories/");
  },
  createCategory: async (data) => {
    return API.fetch("/categories/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
  deleteCategory: async (id) => {
    return API.fetch(`/categories/${id}/`, {
      method: "DELETE",
    });
  },
  getLoans: async () => {
    return API.fetch("/loans/");
  },
  createLoan: async (data) => {
    return API.fetch("/loans/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
  returnBook: async (id, returnDate) => {
    return API.fetch(`/loans/${id}/return_book/`, {
      method: "POST",
      body: JSON.stringify({ return_date: returnDate }),
    });
  },
  fetch: async (serviceName, options = {}) => {
    try {
      const config = {
        headers: { "Content-Type": "application/json" },
        ...options,
      };

      const response = await fetch(`${API.baseURL}${serviceName}`, config);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const contentType = response.headers.get("content-type");
      const hasContent = response.status !== 204;

      if (
        hasContent &&
        contentType &&
        contentType.includes("application/json")
      ) {
        return await response.json();
      } else {
        return { success: true };
      }
    } catch (error) {
      console.error("API Error:", error);
      throw error;
    }
  },
};
