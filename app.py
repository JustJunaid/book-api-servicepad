from bookAPI import db, app


db.create_all()

if __name__ == '__main__':
  app.run(debug=True)
