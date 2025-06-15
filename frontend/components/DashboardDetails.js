import { API } from "../services/API.js";

export class DashboardDetailsPage extends HTMLElement {
  async render() {
    const stats = await API.getDashboard();

    const dashboardHTML = `
            <div class="dashboard-grid" id="dashboard-stats">
              <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-book"></i></div>
                <div class="stat-info">
                    <h3>${stats.total_books}</h3>
                    <p>Total de Livros</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-check-circle"></i></div>
                <div class="stat-info">
                    <h3>${stats.available_books}</h3>
                    <p>Livros Disponíveis</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-handshake"></i></div>
                <div class="stat-info">
                    <h3>${stats.loaned_books}</h3>
                    <p>Livros Emprestados</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-user"></i></div>
                <div class="stat-info">
                    <h3>${stats.total_authors}</h3>
                    <p>Autores</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-tags"></i></div>
                <div class="stat-info">
                    <h3>${stats.total_categories}</h3>
                    <p>Categorias</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-clock"></i></div>
                <div class="stat-info">
                    <h3>${stats.active_loans}</h3>
                    <p>Empréstimos Ativos</p>
                </div>
            </div>
          </div>
        `;

    this.innerHTML = dashboardHTML;
  }

  connectedCallback() {
    const template = document.getElementById("dashboard-template");
    const content = template.content.cloneNode(true);
    this.appendChild(content);

    this.render();
  }
}

customElements.define("dashboard-details-page", DashboardDetailsPage);
