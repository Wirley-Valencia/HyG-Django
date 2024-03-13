from django.test import TestCase
from categories.models import Category, Product

class CategoryTestCase(TestCase):
    def test_create_category(self):
       
        product = Product.objects.create(
            title='Test Product',
            description='This is a test product',
            price=10.99,
            image='products/test.jpg'
        )
        category = Category.objects.create(
            title='Test Category',
            description='This is a test category'
        )
        category.products.add(product)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(category.title, 'Test Category')
        self.assertEqual(category.description, 'This is a test category')
        self.assertEqual(category.products.count(), 1)
        self.assertTrue(product in category.products.all())

    def test_edit_category(self):
        category = Category.objects.create(
            title='Initial Category',
            description='This is an initial category'
        )

        category.title = 'Modified Category'
        category.description = 'This is a modified category'
        category.save()
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(category.title, 'Modified Category')
        self.assertEqual(category.description, 'This is a modified category')