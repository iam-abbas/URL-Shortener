from flask import Flask, request, jsonify, render_template, redirect
import pymysql
import shortuuid

application = app = Flask(__name__,  template_folder='Frontend/templates/')


def get_connection():
    connection = pymysql.connect(host="mysql-db", user="root", password="root",
                                 db="urlshortener", port=3306, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    return connection


@app.route('/shorten', methods=["POST"])
def shorten():
    if request.json and request.json['link']:
        link = request.json['link']
        con = get_connection()
        cur = con.cursor()
        short_url = shortuuid.ShortUUID().random(length=7)
        query = "INSERT INTO urls (link, short_url) VALUES (%s, %s)"
        cur.execute(query, (link, short_url))
        con.commit()
        cur.close()
        con.close()
        return jsonify({"short_url": short_url}), 201
    return jsonify({"error": "Please proive an URL to shorten."}), 400


@app.route('/link/<short_url>')
def getlink(short_url):
    con = get_connection()
    cur = con.cursor()
    query = "SELECT * FROM urls WHERE short_url = %s"
    cur.execute(query, (short_url))
    data = cur.fetchone()
    if data:
        return jsonify(data), 200
    cur.close()
    con.close()
    return jsonify({"error": "No data found"}), 404


@app.route('/visit/<short_url>', methods=["POST"])
def visit(short_url):
    con = get_connection()
    cur = con.cursor()
    try:
        query = "UPDATE urls SET visitors=visitors+1 WHERE short_url = %s"
        cur.execute(query, (short_url))
        con.commit()
    except:
        return jsonify({"error": "Please check the short_url."}), 400
    query = "SELECT visitors FROM urls WHERE short_url = %s"
    cur.execute(query, (short_url))
    visitors = cur.fetchone()['visitors']
    cur.close()
    con.close()
    return jsonify({"visitors": visitors}), 200


@app.route('/getUrls')
def getUrls():
    con = get_connection()
    cur = con.cursor()
    query = "SELECT * FROM urls"
    cur.execute(query)
    data = cur.fetchall()
    if data:
        return jsonify(data), 200
    cur.close()
    con.close()
    return jsonify({"error": "No data found"}), 404


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
