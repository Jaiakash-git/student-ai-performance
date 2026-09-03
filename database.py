import os

import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv


load_dotenv()


# ==========================================
# MYSQL CONNECTION POOL
# ==========================================

connection_pool = pooling.MySQLConnectionPool(
    pool_name="student_ai_pool",
    pool_size=10,
    pool_reset_session=True,

    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),

    connection_timeout=10
)


# ==========================================
# GET DATABASE CONNECTION
# ==========================================

def get_connection():
    """
    Get a reusable connection from the MySQL pool.

    Calling connection.close() returns the connection
    to the pool instead of creating/destroying it.
    """

    return connection_pool.get_connection()