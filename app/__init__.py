from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import BASE_DIR

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "main.login"


def create_app():
    app = Flask(__name__, template_folder=str(BASE_DIR / "templates"), static_folder=str(BASE_DIR / "static"))
    app.config.from_object("config")

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import User
    with app.app_context():
        db.create_all()
        seed_default_data()

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def seed_default_data():
    from app.models import Category, Product, ProductVariant, User

    if User.query.count() == 0:
        admin = User(username="admin")
        admin.set_password("admin123")
        db.session.add(admin)

    if Category.query.count() == 0:
        categories = [
            ("Whisky", "whisky"),
            ("Vodka", "vodka"),
            ("Beer", "beer"),
            ("Wine", "wine"),
            ("Rum", "rum"),
            ("Brandy", "brandy"),
        ]
        for name, slug in categories:
            db.session.add(Category(name=name, slug=slug))

    if Product.query.count() == 0:
        whisky = Category.query.filter_by(slug="whisky").first()
        vodka = Category.query.filter_by(slug="vodka").first()
        products = [
            {
                "product_name": "Blue Moon",
                "brand": "Blue Moon",
                "category_id": whisky.id,
                "description": "Classic premium whisky",
                "image": "placeholder.svg",
                "status": "active",
                "variants": [
                    {"size": "750ml", "price": 2500, "discount_price": 2400, "stock_status": "Available", "display_order": 1},
                    {"size": "375ml", "price": 1300, "discount_price": 1200, "stock_status": "Available", "display_order": 2},
                    {"size": "180ml", "price": 700, "discount_price": 650, "stock_status": "Available", "display_order": 3},
                ],
            },
            {
                "product_name": "Royal Reserve",
                "brand": "Royal Reserve",
                "category_id": vodka.id,
                "description": "Smooth vodka for all occasions",
                "image": "placeholder.svg",
                "status": "active",
                "variants": [
                    {"size": "750ml", "price": 1800, "discount_price": 1700, "stock_status": "Available", "display_order": 1},
                    {"size": "375ml", "price": 900, "discount_price": 850, "stock_status": "Available", "display_order": 2},
                ],
            },
        ]

        for item in products:
            product = Product(
                product_name=item["product_name"],
                brand=item["brand"],
                category_id=item["category_id"],
                description=item["description"],
                image=item["image"],
                status=item["status"],
            )
            db.session.add(product)
            db.session.flush()
            for variant_data in item["variants"]:
                db.session.add(
                    ProductVariant(
                        product_id=product.id,
                        size=variant_data["size"],
                        price=variant_data["price"],
                        discount_price=variant_data["discount_price"],
                        stock_status=variant_data["stock_status"],
                        display_order=variant_data["display_order"],
                        status="active",
                    )
                )
    db.session.commit()
