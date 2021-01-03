from flask import Flask, request, jsonify
import pymysql
import shortuuid

app = Flask(__name__,  template_folder='Frontend/templates/')


def get_connection():
    connection = pymysql.connect(host="localhost", user="root", password="",
                                 db="urlshortener", charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    return connection


@app.route('/shorten', methods=["POST"])
def shorten():
    # Check if "link" paramenter exists
    if request.json and request.json['link']:
        link = request.json['link']

        # Get MySQL connection
        con = get_connection()
        cur = con.cursor()

        # Generate unique url for length 7
        short_url = shortuuid.ShortUUID().random(length=7)

        # Insert "link" and "short_url" in the table "urls"
        query = "INSERT INTO urls (link, short_url) VALUES (%s, %s)"
        cur.execute(query, (link, short_url))
        con.commit()
        cur.close()
        con.close()

        # Return shortened URL
        return jsonify({"short_url": short_url}), 201

    # Return error if "links" is not provided in json request
    return jsonify({"error": "Please proive an URL to shorten."}), 400


@app.route('/link/<short_url>')
def getlink(short_url):

    # Get the connection
    con = get_connection()
    cur = con.cursor()

    # Fetch row of the provided "short_url" from table "urls"
    query = "SELECT * FROM urls WHERE short_url = %s"
    cur.execute(query, (short_url))
    data = cur.fetchone()

    # Check if the query returned any data
    if data:

        # If yes then  returnt the data
        return jsonify(data), 200
    cur.close()
    con.close()

    # If no data has been found, return a 404
    return jsonify({"error": "No data found"}), 404


@app.route('/visit/<short_url>', methods=["POST"])
def visit(short_url):

    # Get the connection
    con = get_connection()
    cur = con.cursor()

    # Update visitor count to current_count+1 if the short_url exists
    try:
        query = "UPDATE urls SET visitors=visitors+1 WHERE short_url = %s"
        cur.execute(query, (short_url))
        con.commit()

    # If short_url doesnt exists then return an error
    except:
        return jsonify({"error": "Please check the short_url."}), 400

    # Fetch latest visitor count
    query = "SELECT visitors FROM urls WHERE short_url = %s"
    cur.execute(query, (short_url))
    visitors = cur.fetchone()['visitors']
    cur.close()
    con.close()

    # Return the latest visitor count
    return jsonify({"visitors": visitors}), 200


@app.route('/getUrls')
def getUrls():

    # Get the connection
    con = get_connection()
    cur = con.cursor()

    # Get all the data from table "urls"
    query = "SELECT * FROM urls"
    cur.execute(query)
    data = cur.fetchall()

    # if there is any data return the data
    if data:
        return jsonify(data), 200
    cur.close()
    con.close()

    # Return error if the table is empty
    return jsonify({"error": "No data found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')
