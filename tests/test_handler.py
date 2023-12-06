from unittest.mock import MagicMock

from exceptions import ForbiddenException, InvalidCredentials


def test_login(handler_instance):
    # invalid credentials
    args = MagicMock(login='admin', password='password', command='print-all-accounts')
    result = handler_instance.print_all_accounts(args)
    assert isinstance(result, InvalidCredentials)
    # success email
    args = MagicMock(login='briancollins@example.net', password='R9AjA5nb$!', command='print-all-accounts')
    result = handler_instance.print_all_accounts(args)
    assert result == 4
    # success telephone number
    args = MagicMock(login='717279856', password='R9AjA5nb$!', command='print-all-accounts')
    result = handler_instance.print_all_accounts(args)
    assert result == 4
    # no permission
    args = MagicMock(login='tamara37@example.com', password='jQ66IIlR*1', command='print-all-accounts')
    result = handler_instance.print_all_accounts(args)
    assert isinstance(result, ForbiddenException)
    # admin for user
    args = MagicMock(login='817730653', password='4^8(Oj52C+', command='print-all-accounts')
    result = handler_instance.print_children(args)
    assert result == 'Christie, 13\nRebecca, 11\n'


def test_print_all_accounts(handler_instance):
    args = MagicMock(login='briancollins@example.net', password='R9AjA5nb$!', command='print-all-accounts')
    result = handler_instance.print_all_accounts(args)
    assert result == 4


def test_print_children(handler_instance):
    args = MagicMock(login='briancollins@example.net', password='R9AjA5nb$!', command='print-children')
    result = handler_instance.print_children(args)
    assert result == 'Andrew, 3\nNicholas, 13\n'


def test_print_oldest_account(handler_instance):
    args = MagicMock(login='briancollins@example.net', password='R9AjA5nb$!', command='print-oldest-account')
    result = handler_instance.print_oldest_account(args)
    assert result == 'name: Justin\nemail_address: opoole@example.org\ncreated_at: 2022-11-25 02:19:37'


def test_group_by_age(handler_instance):
    args = MagicMock(login='briancollins@example.net', password='R9AjA5nb$!', command='group-by-age')
    result = handler_instance.group_by_age(args)
    print(result)
    assert result == """age: 1, count: 1\nage: 3, count: 1\nage: 6, count: 1\nage: 11, count: 1\nage: 12, count: 1\nage: 13, count: 2\n"""


def test_find_similar_children_by_age(handler_instance):
    args = MagicMock(login='briancollins@example.net', password='R9AjA5nb$!', command='find-similar-children-by-age')
    result = handler_instance.find_similar_children_by_age(args)
    assert result == 'Russell, 817730653: Christie, 13; Rebecca, 11\n'
