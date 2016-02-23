#! /usr/bin/env python3

"""Random Recipe Selector

Run this program to help pick out recipes without the work of actually making a
choice yourself. The database of recipes is organized by chapter and comes into
completion when it is built at the bottom of the chapter divisions. The program
entry point contains few lines of code, but the code that does most of the work
can be found in a class at the very bottom of the program. Enjoy your meals!"""

import bisect
import functools
import itertools
import random

# Chapter Recipes
A_GOOD_START = \
    {'Buttermilk Pancakes': dict(weight=4),
     'Buckwheat Blueberry Pancakes': dict(weight=1),
     'Lemon Ricotta Pancakes': dict(weight=1),
     'Crêpes with Lemon and Sugar': dict(weight=1),
     'Buttermilk Waffles': dict(weight=1),
     'Blueberry Muffins': dict(weight=1),
     'Cranberry-Orange Pecan Muffins': dict(weight=1),
     'Millet-Cherry Almond Muffins': dict(weight=0),
     'Pumpkin Bread': dict(weight=1),
     'Banana Bread': dict(weight=5),
     'Coffee Cake': dict(weight=5),
     'Almond Granola with Dried Fruit': dict(weight=0),
     '10-Minute Steel-Cut Oatmeal': dict(weight=1),
     'Millet Porridge with Maple Syrup': dict(weight=1),
     'Hot Quinoa Breakfast Cereal with Blueberries and Almonds':
         dict(weight=0)}
GRAINS = \
    {'Basmati Rice Pilaf': dict(weight=1),
     'Hearty Baked Brown Rice with Onions and Roasted Red Peppers':
         dict(weight=1),
     'Wild Rice Pilaf with Pecans and Cranberries': dict(weight=1),
     'Almost Hands-Free Risotto with Parmesan and Herbs': dict(weight=1),
     'Creamy Parmesan Polenta': dict(weight=1),
     'Quinoa Pilaf with Herbs and Lemon': dict(weight=1),
     'Quinoa Salad with Red Bell Peppers and Cilantro': dict(weight=1),
     'Quinoa Patties with Spinach and Sun-Dried Tomatoes': dict(weight=1),
     'Kasha Pilaf with Caramelized Onions': dict(weight=1),
     'Creamy Cheesy Millet': dict(weight=1),
     'Curried Millet Pilaf': dict(weight=1),
     'Buckwheat Tabbouleh': dict(weight=1),
     'Oat Berry Pilaf with Walnuts and Gorgonzola': dict(weight=1),
     'Oat Berry, Chickpea, and Arugula Salad': dict(weight=1)}
PASTA = \
    {'Fresh Pasta': dict(weight=1),
     'Sauces for Fresh Pasta': dict(weight=1),
     'Penne with Spiced Butter, Cauliflower, and Pine Nuts': dict(weight=1),
     'Fusilli with Basil Pesto': dict(weight=1),
     'Fusilli with Spring Vegetable Cream Sauce': dict(weight=1),
     'Spaghetti with Puttanesca Sauce': dict(weight=1),
     'Spaghetti and Meatballs': dict(weight=1),
     'Penne with Sausage and Red Pepper Ragu': dict(weight=1),
     'Penne with Weeknight Meat Sauce': dict(weight=1),
     'Soba Noodles with Pork, Shiitakes, and Bok Choy': dict(weight=1),
     'Soba Noodles with Roasted Eggplant and Sesame': dict(weight=1),
     'Drunken Noodles with Chicken': dict(weight=1),
     'Singapore Noodles with Shrimp': dict(weight=1),
     'Pad Thai with Shrimp': dict(weight=1),
     'Spicy Basil Noodles with Crispy Tofu, Snap Peas, and Bell Pepper':
         dict(weight=1)}
COMFORT_FOODS = \
    {'Lasagna with Hearty Tomato-Meat Sauce': dict(weight=1),
     'Spinach and Tomato Lasagna': dict(weight=1),
     'Eggplant Parmesan': dict(weight=1),
     'Easy Stovetop Macaroni and Cheese': dict(weight=1),
     'Baked Macaroni and Cheese': dict(weight=1),
     'All-American Meatloaf': dict(weight=1),
     'Fried Chicken': dict(weight=2),
     'Crispy Pen-Fried Pork Chops': dict(weight=1),
     'Crispy Chicken Fingers': dict(weight=1),
     "Shepherd's Pie": dict(weight=1),
     'Chicken Pot Pie': dict(weight=1),
     'Cheese Quiche': dict(weight=1),
     'Tamale Pie': dict(weight=1),
     'Golden Cornbread and Sausage Stuffing': dict(weight=1),
     'Wild Rice Dressing': dict(weight=1)}
YEAST_BREADS_SAVORY_LOAVES_AND_PIZZA = \
    {'Classic Sandwich Bread': dict(weight=5),
     'Multigrain Sandwich Bread': dict(weight=1),
     'Cinnamon-Raisin Bread': dict(weight=3),
     'Hearty Country Flax Bread': dict(weight=1),
     'Olive-Rosemary Bread': dict(weight=1),
     'Dinner Roles': dict(weight=5),
     'English Muffins': dict(weight=1),
     'Cheddar Cheese Bread': dict(weight=1),
     'Skillet Cornbread': dict(weight=1),
     'Light and Fluffy Biscuits': dict(weight=1),
     'Pizza': dict(weight=5),
     'Socca (Chickpea Flatbreads)': dict(weight=1),
     'Corn Tortillas': dict(weight=1),
     'Arepas (Corn Cakes)': dict(weight=1),
     'Pupusas (Stuffed Corn Tortillas)': dict(weight=1),
     'Brazilian Cheese Bread Rolls': dict(weight=1)}
COOKIES_AND_BARS = \
    {'Chocolate Chip Cookies': dict(weight=5),
     'Chocolate Cookies': dict(weight=5),
     'Oatmeal-Raisin Cookies': dict(weight=1),
     'Chewy Sugar Cookies': dict(weight=1),
     'Peanut Butter Cookies': dict(weight=0),
     'Pignoli': dict(weight=1),
     'Shortbread': dict(weight=1),
     'Florentine Lace Cookies': dict(weight=1),
     'Holiday Cookies': dict(weight=1),
     'Fudgy Brownies': dict(weight=5),
     'Raspberry Streusel Bars': dict(weight=1),
     'Lemon Bars': dict(weight=1),
     'Granola Bars': dict(weight=1)}
PIES_FRUIT_DESSERTS_AND_TARTS = \
    {'Pie Dough': dict(weight=1),
     'Pumpkin Pie': dict(weight=1),
     'Deep-Dish Apple Pie': dict(weight=5),
     'Blueberry Pie': dict(weight=1),
     'Fresh Strawberry Pie': dict(weight=5),
     'Individual Blueberry-Almond Buckles': dict(weight=0),
     'Individual Fresh Berry Gratins with Zabaglione': dict(weight=1),
     'Individual Pavlovas with Tropical Fruit': dict(weight=1),
     'Peach Cobbler with Cornmeal Biscuits': dict(weight=1),
     'Apple Crisp': dict(weight=5),
     'Tart Shell': dict(weight=1),
     'Rustic Walnut Tart': dict(weight=1),
     'Nutella Tart': dict(weight=1),
     'Lemon Tart': dict(weight=1),
     'Fresh Fruit Tart': dict(weight=1)}
CAKES = \
    {'Yellow Layer Cake': dict(weight=1),
     'Birthday Cupcakes': dict(weight=1),
     'Chocolate Layer Cake': dict(weight=1),
     'Dark Chocolate Cupcakes': dict(weight=1),
     'Red Velvet Cupcakes': dict(weight=1),
     'Carrot Sheet Cake': dict(weight=1),
     'Gingerbread Cake': dict(weight=1),
     'Applesauce Snack Cake': dict(weight=1),
     'Rustic Plum Torte': dict(weight=1),
     'Lemon Pound Cake': dict(weight=1),
     'Almond Cake': dict(weight=0),
     'Flourless Chocolate Cake': dict(weight=1)}

# Main Database
CONTENTS = \
    {'A Good Start': dict(weight=2, recipes=A_GOOD_START),
     'Grains': dict(weight=0, recipes=GRAINS),
     'Pasta': dict(weight=0, recipes=PASTA),
     'Comfort Foods': dict(weight=5, recipes=COMFORT_FOODS),
     'Yeast Breads, Savory Loaves, and Pizza':
         dict(weight=5, recipes=YEAST_BREADS_SAVORY_LOAVES_AND_PIZZA),
     'Cookies and Bars': dict(weight=5, recipes=COOKIES_AND_BARS),
     'Pies, Fruit Desserts, and Tarts':
         dict(weight=5, recipes=PIES_FRUIT_DESSERTS_AND_TARTS),
     'Cakes': dict(weight=1, recipes=CAKES)}

# This is an example of giving new weights to chapters based on recipe count.
# for value in CONTENTS.values():
#     value['weight'] = len(value['recipes'])


def main():
    """Select a recipe from a database having weighted entries."""
    chapter, metadata = next(WeightedRandomDictionary(CONTENTS))
    title, _ = next(WeightedRandomDictionary(metadata['recipes']))
    print('{}: {}'.format(chapter, title))


class WeightedRandomDictionary:

    """WeightedRandomDictionary(dictionary) -> New Class Instance"""

    def __init__(self, dictionary):
        """Initialize a new instance of the class."""
        self.__dictionary = dictionary
        keys, weights = [], []
        for key, value in dictionary.items():
            keys.append(key)
            weights.append(value['weight'])
        self.__keys = tuple(keys)
        self.__weights = tuple(itertools.accumulate(weights))
        self.__selector = functools.partial(random.SystemRandom().randrange,
                                            self.__weights[-1])

    def __iter__(self):
        """An instance acts as an iterator, so just return self."""
        return self

    def __next__(self):
        """Select a key according to the weights and return the pair."""
        key = self.__keys[bisect.bisect(self.__weights, self.__selector())]
        return key, self.__dictionary[key]


if __name__ == '__main__':
    main()
