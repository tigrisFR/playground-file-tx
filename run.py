from app import create_app, db

app = create_app()

if __name__ == '__main__':
  
    app.run(host='0.0.0.0', port=3000)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
