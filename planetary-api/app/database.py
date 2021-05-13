from app import app, db, models

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    mercury = models.Planet(name='Mercury', type='Class D', home_star='Sol', mass=3.258e23, radius=1516, distance=35.98e6)
    venus = models.Planet(name='Venus', type='Class K', home_star='Sol', mass=4.867e24, radius=3760, distance=67.24e6)
    earth = models.Planet(name='Earth', type='Class M', home_star='Sol', mass=5.972e24, radius=3959, distance=92.96e6)
    test_user = models.User(first_name='William', last_name='Herschel', email='test@test.com', password='123')

    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)
    db.session.add(test_user)
    db.session.commit()
    
    print('Database seeded!')