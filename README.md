# Abdel Aziz Mfossa - Personal Portfolio & Custom URL Shortener

<img src="portfolio/static/portfolio/images/landing%20page.png" alt="Portfolio Preview" width="800">

Welcome to the source code of my personal portfolio and blog. I am Abdel Aziz Mfossa, a Google Workspace Engineer, Automation Enthusiast, and Lead of GDG Yaoundé.

This dynamic website is built with **Django** and **Tailwind CSS**, designed to showcase my projects, articles, speaking engagements, and expertise in Cloud Engineering and Automation. It also includes a built-in Custom URL Shortener.

## Key Features

*   **Dynamic Content Management:** Easily manage Skills, Experiences, Projects, Medium Articles, YouTube Videos, and Events directly from the Django Admin Panel.
*   **Custom URL Shortener (`/shortener`):** A custom-built linking tool to create, track, and manage branded short links (e.g., `abdelmfossa.com/spotify`), completely replacing the need for services like Bitly.
*   **Modern UI/UX:** Built with Tailwind CSS, featuring a responsive design, smooth animations, glassmorphism effects, and a fully functional Dark/Light mode toggle.
*   **Integrated Contact Flow:** Features an embedded Google Form for structured lead generation and direct Google Calendar booking integration.
*   **SEO Optimized:** Includes dynamic OpenGraph meta tags for beautiful social media link previews.
*   **Security Focused:** Obfuscated Django Admin URL via environment variables to prevent brute-force attacks on the default `/admin` path.
*   **Production Ready:** Configured with Whitenoise, Gunicorn, python-dotenv, and comes with Nginx and Systemd configuration templates for easy VPS deployment.

## Tech Stack

*   **Backend:** Python 3.11, Django 4.2
*   **Frontend:** HTML5, Tailwind CSS (via CDN), Lucide Icons
*   **Database:** SQLite (Development) / Ready for PostgreSQL (Production)
*   **Deployment:** Gunicorn, Nginx, Systemd, Whitenoise (Static Files)

## Local Development Setup

Follow these steps to run the project locally on your machine.

### Prerequisites
*   Python 3.11+
*   Git

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AbdelMfossa/portfolio.git
    cd portfolio
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Copy the `.env.example` file to create your local `.env` file:
    ```bash
    cp .env.example .env
    ```
    *(Ensure you set a unique path for `ADMIN_URL` and set `DEBUG=True` for local development.)*

5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```

8.  **Access the application:**
    *   Website: `http://127.0.0.1:8000/`
    *   Admin Panel: `http://127.0.0.1:8000/admin/`

## Deployment (Ubuntu VPS)

This project includes configuration files for deploying on an Ubuntu VPS using Nginx and Gunicorn.

Check the `deployment/` directory for detailed configuration templates:
*   `deployment/gunicorn_portfolio.service`: Systemd service configuration
*   `deployment/gunicorn_portfolio.socket`: Systemd socket configuration
*   `deployment/abdelmfossa.com`: Nginx server block configuration
*   `deployment/README.md`: Step-by-step instructions for server configuration and SSL setup (Certbot).

## License

This project is open-source and available under the [MIT License](LICENSE). Feel free to use it as inspiration for your own portfolio!

## Contact & Connections

*   **Website:** [abdelmfossa.com](https://abdelmfossa.com)
*   **LinkedIn:** [linkedin.com/in/AbdelMfossa](https://linkedin.com/in/AbdelMfossa)
*   **YouTube:** [@abdelmfossa](https://youtube.com/@abdelmfossa)
*   **Medium:** [@abdelmfossa](https://medium.com/@abdelmfossa)
*   **GitHub:** [github.com/AbdelMfossa](https://github.com/AbdelMfossa)
*   **Twitter:** [@abdelmfossa](https://twitter.com/abdelmfossa)
