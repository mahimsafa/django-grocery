# Grocery E-commerce Platform

A full-featured grocery e-commerce platform built with Django.

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- UV Package Manager
- Node.js (for frontend assets if applicable)
- Git

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd django-grocery
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DEBUG=True
DATABASE_URL=postgres://mahim:testpass123@localhost:5432/local_db
```

### 3. Start the Database with Docker Compose

Run the following command to start the PostgreSQL database:

```bash
docker compose up -d 
```

### 4. Set Up Python Environment and Install Dependencies

```bash
# Create and activate virtual environment
uv venv

# Install dependencies
uv sync
```

### 5. Run Database Migrations

```bash
uv run manage.py makemigrations
uv run manage.py migrate
```

### 6. Create a Superuser (Optional)

```bash
uv run manage.py createsuperuser
```

### 7. Seed the Database with Sample Data (Optional)

```bash
uv run manage.py seed_data
```

### 8. Start the Development Server

```bash
uv run manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

## Project Structure

- `grocery_unified/` - Main Django project settings
- `product/` - Product catalog app
- `customer/` - Customer management app
- `cart/` - Shopping cart functionality
- `order/` - Order processing
- `custom_admin/` - Custom admin interface

## Available Management Commands

- `seed_data` - Populate the database with sample data (optional)
- `createsuperuser` - Create an admin user
- `makemigrations` - Create new database migrations
- `migrate` - Apply database migrations


## Stopping the Database

To stop the Docker containers:

```bash
docker compose down
```

## Troubleshooting

- If you encounter port conflicts, make sure no other services are running on ports 8000 (Django) or 5432 (PostgreSQL).
- If the database connection fails, ensure the PostgreSQL container is running and the credentials in `.env` match those in `compose.yml`.