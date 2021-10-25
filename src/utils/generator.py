import random
import string


def generate_code():
    return random.randrange(100000, 999999)


def random_string():
   letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
   return ''.join(random.choice(letters) for i in range(64))
