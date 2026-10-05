# Liquor Shop Rate List & Product Catalog

A Flask-based liquor shop product catalog and admin dashboard for managing product variants, stock status, bulk import, and public pricing displays.

## Features

- Admin authentication using Flask-Login with password hashing
- Product and category management
- Product variants with size/price data
- Product image handling and upload validation
- CSV / Excel / JSON import with preview and validation
- Duplicate and grouping checks for product variants
- Public responsive rate list with search and category filters
- CSV, Excel, JSON, and PDF export
- Print-friendly rate list view
- SQLite default for local development, with MySQL support via DATABASE_URL environment variable

## Stack

- Python
- Flask
- SQLAlchemy
- MySQL-ready configuration
- Jinja2 templates
- Bootstrap 5
- Pandas + OpenPyXL
- reportlab

## Quick Start

1. Clone or open the project directory.
2. Create a virtual environment (optional but recommended).
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   python app.py
   ```

5. Open in browser:

   - Public rate list: http://localhost:5000/
   - Admin login: http://localhost:5000/admin/login

## Admin Login

- Username: `admin`
- Password: `admin123`

## Environment Variables

```bash
export SECRET_KEY="change-me"
export DATABASE_URL="mysql+pymysql://user:password@localhost/liquor_shop"
```

If `DATABASE_URL` is not set, the app falls back to a local SQLite database file named `rate_list.db`.

## Sample Files

Sample import data is available in the `sample_data/` folder:

- `rate_list.csv`
- `rate_list.json`

## Production Notes

- Store uploaded images in a persistent `uploads/` directory or cloud storage.
- For production, configure MySQL and secure the admin credentials.
- Add deployment-specific WSGI setup as needed for your hosting platform.

## Testing

Run the built-in validation tests:

```bash
python -m unittest discover -s tests
```
