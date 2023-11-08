from django.test import TestCase
from main_app.models import Restaurant, RestaurantReview
from django.core.exceptions import ValidationError


class RestaurantReviewModelTest(TestCase):
    def setUp(self):
        # Create two restaurant objects
        self.restaurant1 = Restaurant.objects.create(
            name="Restaurant A",
            location="123 Main St.",
            description="A cozy restaurant",
            rating=4.88
        )

        self.restaurant2 = Restaurant.objects.create(
            name="Restaurant B",
            location="456 Elm St.",
            description="Charming restaurant",
            rating=3.59
        )

    def test_create_reviews_and_duplicate_review(self):
        # Create RestaurantReview objects
        RestaurantReview.objects.create(
            reviewer_name="Bob",
            restaurant=self.restaurant1,
            review_content="Good experience overall.",
            rating=4
        )

        RestaurantReview.objects.create(
            reviewer_name="Aleks",
            restaurant=self.restaurant1,
            review_content="Great food and service!",
            rating=5
        )

        RestaurantReview.objects.create(
            reviewer_name="Charlie",
            restaurant=self.restaurant2,
            review_content="It was ok!",
            rating=2
        )

        # Attempt to create a duplicate review for Aleks on Restaurant1
        duplicate_review = RestaurantReview(
            reviewer_name="Aleks",
            restaurant=self.restaurant1,
            review_content="Another great meal!",
            rating=5
        )

        with self.assertRaises(ValidationError) as context:
            duplicate_review.full_clean()

        # Assert the specific validation error message
        self.assertEqual(
            context.exception.message_dict['__all__'][0],
            'Restaurant Review with this Reviewer name and Restaurant already exists.'
        )

        # Query and display all RestaurantReview objects
        reviews = RestaurantReview.objects.all()
        result = ''
        for review in RestaurantReview.objects.all():
            result += f"Reviewer: {review.reviewer_name}, Rating: {review.rating}, Restaurant: {review.restaurant.name}\n"

        self.assertEqual(len(reviews), 3)
        self.assertEqual(result.strip(), """Reviewer: Aleks, Rating: 5, Restaurant: Restaurant A
Reviewer: Bob, Rating: 4, Restaurant: Restaurant A
Reviewer: Charlie, Rating: 2, Restaurant: Restaurant B""")