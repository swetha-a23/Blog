from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(
    host='database-2.c9zljavouvdq.us-east-1.rds.amazonaws.com',
    port='5432',
    database='blog',
    user='postgres',
    password='rama1234'
)
cursor = conn.cursor()

try:
    cursor.execute("""
          CREATE TABLE IF NOT EXISTS blog (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            description VARCHAR(300) NOT NULL,
            image_url VARCHAR(255) NOT NULL,
            username VARCHAR(50) NOT NULL,
            tags TEXT[],
            public BOOLEAN NOT NULL,
            private BOOLEAN NOT NULL,
            user_id INTEGER NOT NULL
        )
    """)
    conn.commit()
except psycopg2.Error as e:
    print("Error while creating the blog table:", e)

# POST /blog
@app.route('/blog', methods=['POST'])
def add_blog():
    try:
        blog = request.get_json()
        title = blog.get('title')
        content = blog.get('content')
        description = blog.get('description')
        image_url = blog.get('image_url')
        username = blog.get('username')
        tags = blog.get('tags', [])
        public = blog.get('public', False)
        private = blog.get('private', False)

        
        user_id = blog.get('user_id')

        query = "INSERT INTO blog (title, content, description, image_url, username, tags, public, private, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (title, content, description, image_url, username, tags, public, private, user_id)
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'message': 'Blog added successfully'})
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': 'Failed to add blog', 'message': str(e)}), 500

# GET /blog
@app.route('/blog', methods=['GET'])
def get_all_blogs():
    try:
        query = "SELECT * FROM blog"
        cursor.execute(query)
        blogs = cursor.fetchall()
        blog_list = []
        for blog in blogs:
            blog_data = {
                'id': blog[0],
                'title': blog[1],
                'content': blog[2],
                'description': blog[3],
                'image_url': blog[4],
                'username': blog[5],
                'tags': blog[6],
                'public': blog[7],
                'private': blog[8]
            }
            blog_list.append(blog_data)
        return jsonify(blog_list)
    except psycopg2.Error as e:
        return jsonify({'error': 'Failed to fetch blogs', 'message': str(e)}), 500

# GET /blog/<int:blog_id>
@app.route('/blog/<int:blog_id>', methods=['GET'])
def get_blog_by_id(blog_id):
    try:
        query = "SELECT * FROM blog WHERE id = %s"
        value = (blog_id,)
        cursor.execute(query, value)
        blog = cursor.fetchone()
        if blog:
            blog_data = {
                'id': blog[0],
                'title': blog[1],
                'content': blog[2],
                'description': blog[3],
                'image_url': blog[4],
                'username': blog[5],
                'tags': blog[6],
                'public': blog[7],
                'private': blog[8]
            }
            return jsonify(blog_data)
        return jsonify({'message': 'Blog not found'}), 404
    except psycopg2.Error as e:
        return jsonify({'error': 'Failed to fetch the blog', 'message': str(e)}), 500

# GET /blog/user/<username>
@app.route('/blog/user/<username>', methods=['GET'])
def get_blogs_by_username(username):
    try:
        query = "SELECT * FROM blog WHERE username = %s"
        value = (username,)
        cursor.execute(query, value)
        blogs = cursor.fetchall()
        blog_list = []
        for blog in blogs:
            blog_data = {
                'id': blog[0],
                'title': blog[1],
                'content': blog[2],
                'description': blog[3],
                'image_url': blog[4],
                'username': blog[5],
                'tags': blog[6],
                'public': blog[7],
                'private': blog[8]
            }
            blog_list.append(blog_data)
        return jsonify(blog_list)
    except psycopg2.Error as e:
        return jsonify({'error': 'Failed to fetch blogs', 'message': str(e)}), 500

@app.route('/blog/tags/<tag>', methods=['GET'])
def get_blogs_by_tags(tag):
    try:
        query = "SELECT * FROM blog WHERE tags LIKE %s"
        value = (tag,)
        cursor.execute(query, value)
        blogs = cursor.fetchall()
        blog_list = []
        for blog in blogs:
            blog_data = {
                'id': blog[0],
                'title': blog[1],
                'content': blog[2],
                'description': blog[3],
                'image_url': blog[4],
                'username': blog[5],
                'tags': blog[6],
                'public': blog[7],
                'private': blog[8]
            }
            blog_list.append(blog_data)
        return jsonify(blog_list)
    except psycopg2.Error as e:
        return jsonify({'error': 'Failed to fetch blogs', 'message': str(e)}), 500

# PUT /blog/<int:blog_id>
@app.route('/blog/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    try:
        blog = request.get_json()
        title = blog.get('title')
        content = blog.get('content')
        description = blog.get('description')
        image_url = blog.get('image_url')
        tags = blog.get('tags', [])
        public = blog.get('public', False)
        private = blog.get('private', False)

        user_id = blog.get('user_id')

    
        query = "SELECT * FROM blog WHERE id = %s AND user_id = %s"
        values = (blog_id, user_id)
        cursor.execute(query, values)
        blog_post = cursor.fetchone()

        if not blog_post:
            return jsonify({'message': 'Blog not found or you are not authorized to update'}), 404

        query = "UPDATE blog SET title = %s, content = %s, description = %s, image_url = %s, tags = %s, public = %s, private = %s WHERE id = %s"
        values = (title, content, description, image_url, tags, public, private, blog_id)
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'message': 'Blog updated successfully'})
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': 'Failed to update blog', 'message': str(e)}), 500

# DELETE /blog/<int:blog_id>
@app.route('/blog/<int:blog_id>', methods=['DELETE'])
def remove_blog(blog_id):
    try:
        blog = request.get_json()

        
        user_id = blog.get('user_id')

        query = "SELECT * FROM blog WHERE id = %s AND user_id = %s"
        values = (blog_id, user_id)
        cursor.execute(query, values)
        blog_post = cursor.fetchone()

        if not blog_post:
            return jsonify({'message': 'Blog not found or you are not authorized to delete'}), 404

        query = "DELETE FROM blog WHERE id = %s"
        value = (blog_id,)
        cursor.execute(query, value)
        conn.commit()
        return jsonify({'message': 'Blog removed successfully'})
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': 'Failed to delete blog', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
