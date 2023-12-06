from schemas import Children, GroupByAge, FindSimilarChildrenByAge, LoginUser, Role
from tests.conftest import data_parser, cur, db


def test_create_db():
    # in this case database creation and parser is tested together
    db.create_database()
    data_parser.parse_all_files()
    result = cur.execute("SELECT * FROM roles").fetchall()
    assert len(result) == 2
    result = cur.execute("SELECT * FROM users").fetchall()
    assert len(result) == 4
    result = cur.execute("SELECT * FROM children").fetchall()
    assert len(result) == 7
    result = cur.execute("SELECT created_at FROM users WHERE email=?", ("jwilliams@example.com", )).fetchone()
    assert result[0] == "2023-07-15 21:57:02"
    result = cur.execute("SELECT telephone_number FROM users WHERE email=?", ("briancollins@example.net",)).fetchone()
    assert result[0] == "717279856"


def test_print_all_user(create_db):
    assert db.print_all_accounts() == 4


def test_oldest_account(create_db):
    user = db.print_oldest_account()
    assert user.firstname == "Justin"
    assert user.email == "opoole@example.org"
    assert str(user.created_at) == "2022-11-25 02:19:37"


def test_print_children(create_db):
    children = db.print_children("opoole@example.org")
    assert isinstance(children, Exception)
    children = db.print_children("817730653")
    assert children == [Children(name='Christie', age=13), Children(name='Rebecca', age=11)]


def test_group_by_age(create_db):
    result = db.group_by_age()
    assert result == [GroupByAge(age=1, child_count=1), GroupByAge(age=3, child_count=1),
                      GroupByAge(age=6, child_count=1), GroupByAge(age=11, child_count=1),
                      GroupByAge(age=12, child_count=1), GroupByAge(age=13, child_count=2),]


def test_find_similar_children_by_age(create_db):
    result = db.find_similar_children_by_age("briancollins@example.net")
    assert result == [FindSimilarChildrenByAge(firstname='Russell',
                                               telephone_number='817730653',
                                               children=[Children(name='Christie', age=13),
                                                         Children(name='Rebecca', age=11)])]


def test_login(create_db):
    password = cur.execute("SELECT password FROM users WHERE email=?", ("briancollins@example.net", )).fetchone()
    result = db.login("briancollins@example.net")
    assert result == LoginUser(role=Role.admin,
                               password=password[0])
    result = db.login("briancollins@exampe.net")
    assert isinstance(result, Exception)


