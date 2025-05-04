from django.core.management.base import BaseCommand
from users.models import CustomUser
from menu.models import MenuItem, Rating, Category
from analytics.models import RatingAnalytics, Feedback, PopularItem, UserActivity
import random
from datetime import datetime, timedelta
import pytz

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **options):
        # Create categories
        categories = [
            {'name': 'Main Course', 'description': 'Hearty main dishes'},
            {'name': 'Appetizers', 'description': 'Starters and snacks'},
            {'name': 'Desserts', 'description': 'Sweet treats'},
            {'name': 'Beverages', 'description': 'Drinks and refreshments'},
        ]

        for category_data in categories:
            Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )

        # Create sample menu items
        menu_items = [
            {'name': 'Paneer Biryani', 'description': 'Fragrant basmati rice with succulent paneer pieces and aromatic spices', 'price': 180, 'category': 'Main Course'},
            {'name': 'Veg Fried Rice', 'description': 'Stir-fried rice with fresh vegetables and a hint of soy sauce', 'price': 120, 'category': 'Main Course'},
            {'name': 'Paneer Butter Masala', 'description': 'Creamy tomato-based curry with soft paneer cubes', 'price': 160, 'category': 'Main Course'},
            {'name': 'Paneer Tikka', 'description': 'Grilled cottage cheese marinated in aromatic spices', 'price': 140, 'category': 'Appetizers'},
            {'name': 'Dal Makhani', 'description': 'Creamy black lentils slow-cooked with butter and cream', 'price': 100, 'category': 'Main Course'},
            {'name': 'Gulab Jamun', 'description': 'Sweet milk dumplings soaked in fragrant sugar syrup', 'price': 40, 'category': 'Desserts'},
            {'name': 'Masala Dosa', 'description': 'Crispy rice crepe with spiced potato filling and coconut chutney', 'price': 80, 'category': 'Main Course'},
            {'name': 'Veg Manchurian', 'description': 'Crispy vegetable balls in tangy sauce', 'price': 150, 'category': 'Appetizers'},
            {'name': 'Mushroom Masala', 'description': 'Fresh mushrooms cooked in rich onion-tomato gravy', 'price': 130, 'category': 'Main Course'},
            {'name': 'Veg Hakka Noodles', 'description': 'Stir-fried noodles with fresh vegetables and oriental spices', 'price': 110, 'category': 'Main Course'},
            {'name': 'Aloo Paratha', 'description': 'Whole wheat flatbread stuffed with spiced potato filling', 'price': 70, 'category': 'Main Course'},
            {'name': 'Veg Burger', 'description': 'Crispy vegetable patty with fresh lettuce and special sauce', 'price': 90, 'category': 'Main Course'},
            {'name': 'Veg Pizza', 'description': 'Thin crust pizza topped with fresh vegetables and mozzarella', 'price': 200, 'category': 'Main Course'},
            {'name': 'Fruit Salad', 'description': 'Fresh seasonal fruits with honey and mint', 'price': 60, 'category': 'Desserts'},
            {'name': 'Veg Spring Roll', 'description': 'Crispy rolls filled with stir-fried vegetables', 'price': 80, 'category': 'Appetizers'},
            {'name': 'Samosa Plate(Bablu Bhai)', 'description': 'Crispy pastry filled with spiced potatoes and peas, served with special chutney', 'price': 30, 'category': 'Appetizers'},
            {'name': 'Vada Pav', 'description': 'Spicy potato fritter in a soft bun with chutneys', 'price': 25, 'category': 'Appetizers'},
            {'name': 'Tiramisu', 'description': 'Classic Italian dessert with coffee and mascarpone', 'price': 120, 'category': 'Desserts'}
        ]

        # Create menu items
        for item_data in menu_items:
            category = Category.objects.get(name=item_data['category'])
            MenuItem.objects.get_or_create(
                name=item_data['name'],
                defaults={
                    'description': item_data['description'],
                    'price': item_data['price'],
                    'is_available': True,
                    'category': category
                }
            )

        # Create sample users if they don't exist
        users = []
        for i in range(1, 6):
            username = f'user{i}'
            email = f'user{i}@example.com'
            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': f'User {i}',
                    'last_name': 'Test',
                    'is_active': True
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)

        # Create sample ratings and analytics
        menu_items = MenuItem.objects.all()
        timezone = pytz.timezone('UTC')
        start_date = datetime.now(timezone) - timedelta(days=30)

        for menu_item in menu_items:
            # Create 20-30 ratings for each menu item
            num_ratings = random.randint(20, 30)
            for _ in range(num_ratings):
                rating = Rating.objects.create(
                    menu_item=menu_item,
                    user=random.choice(users),
                    rating=random.randint(3, 5),
                    comment=random.choice([
                        'Great taste!',
                        'Very delicious',
                        'Perfectly cooked',
                        'Amazing flavor',
                        'Will order again',
                        'Best in the canteen',
                        'Highly recommended',
                        'Fresh and tasty'
                    ]),
                    created_at=start_date + timedelta(
                        days=random.randint(0, 30),
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    )
                )

            # Create analytics entry
            RatingAnalytics.objects.create(
                menu_item=menu_item,
                average_rating=random.uniform(4.0, 4.8),
                total_ratings=num_ratings
            )

            # Create popular item entry
            PopularItem.objects.create(
                menu_item=menu_item,
                view_count=random.randint(50, 200),
                rating_count=num_ratings
            )

            # Create user activities
            for user in users[:2]:  # Create activities for first 2 users
                UserActivity.objects.create(
                    user=user,
                    menu_item=menu_item,
                    action=random.choice(['rated_item', 'viewed_item', 'added_review'])
                )

        # Create sample feedback
        feedback_comments = [
            # Professional Positive Reviews
            'The paneer biryani was perfectly spiced and the paneer was so soft!',
            'Veg fried rice had the perfect balance of vegetables and flavor.',
            'Paneer butter masala was rich and creamy, just like homemade.',
            'The paneer tikka was perfectly grilled with a nice smoky flavor.',
            'Dal makhani was cooked to perfection with just the right amount of cream.',
            'The masala dosa was crispy and the potato filling was well-seasoned.',
            'Veg manchurian had the perfect crunch and the sauce was delicious.',
            'Mushroom masala was flavorful with fresh, well-cooked mushrooms.',
            'Veg hakka noodles were perfectly cooked with a nice wok flavor.',
            'Aloo paratha was soft and the potato filling was well-spiced.',
            
            # Humorous/Mean Complaints
            'Found a cockroach in my misal pav. Extra protein, I guess?',
            'The vada was microwaved and stuffed into the pav. Very unhygenic!',
            'Stupid FE\'s finished all the burnt garlic fried rice, it\'s the only edible thing in our canteen!',
            'The paneer in my butter masala was so hard, I could use it as a cricket ball.',
            'The dal was so watery, I almost went swimming.',
            'The veg burger was so small, I needed a microscope to find it.',
            'The pizza was so greasy, I could use it as a mirror.',
            'The noodles were so overcooked, they could be used as shoelaces.',
            'The ice cream was so melted, it was basically a milkshake.',
            'The fries were so salty, I started growing gills.',
            'The soup was so hot, it could power a small city.',
            'The dessert was so sweet, I got a cavity just looking at it.',
            'The veg spring rolls were so oily, I could use them to lubricate my bike.',
            'The fruit salad had more sugar than a candy store.',
            'The veg manchurian was so spicy, I saw my life flash before my eyes.',
            
            # Constructive Feedback
            'The paneer in my biryani was a bit dry, but the rice was flavorful.',
            'Veg fried rice could use more vegetables and less oil.',
            'Paneer butter masala was good but could be creamier.',
            'The paneer tikka was slightly overcooked but still tasty.',
            'Dal makhani was a bit too thick, but the flavor was good.',
            'Masala dosa was good but the chutney could be spicier.',
            'Veg manchurian sauce was too sweet for my taste.',
            'Mushroom masala had too much gravy, but the mushrooms were fresh.',
            'Veg hakka noodles were a bit too oily but had good flavor.',
            'Aloo paratha was good but could use more filling.',
            
            # Service and General Feedback
            'Service was so slow, I finished my assignment while waiting.',
            'The canteen could use more variety in the menu.',
            'Portion sizes are perfect for a toddler.',
            'The staff is friendly, but the food is a different story.',
            'More variety, please! My taste buds are getting bored.',
            'The food is generally good but could be more consistent.',
            'Prices are reasonable for college canteen food.',
            'The ambiance is clean and comfortable.',
            'Would appreciate more healthy options on the menu.',
            'Good value for money overall.'
        ]

        for comment in feedback_comments:
            Feedback.objects.create(
                user=random.choice(users),
                subject='Food Quality Feedback',
                message=comment,
                is_resolved=random.choice([True, False])
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated sample data')) 