import logging
from config import NUMBER_OF_USERS, MAX_POSTS_PER_USER, MAX_LIKES_PER_USER
from utils import generate_user_access_tokens, create_dummy_posts, create_random_likes_for_posts

logging.basicConfig(level=logging.INFO)


def create_dummy_data(number_of_users: int, max_posts_per_user: int, max_likes_per_user: int) -> None:
    logging.info("Generating user tokens...")
    users_tokens = generate_user_access_tokens(number_of_users)
    logging.info('Creating posts...')
    posts = create_dummy_posts(users_tokens, max_posts_per_user)
    logging.info('Creating likes...')
    create_random_likes_for_posts(users_tokens, posts, max_likes_per_user)


if __name__ == '__main__':
    create_dummy_data(NUMBER_OF_USERS, MAX_POSTS_PER_USER, MAX_LIKES_PER_USER)
