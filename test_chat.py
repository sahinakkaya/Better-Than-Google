import unittest
from unittest import mock
from parser import Chat, Line
import io
from datetime import datetime

class TestChat(unittest.TestCase):
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('builtins.input')
    def test_group_chat(self,fake_stdin, fake_stdout):
        fake_stdin.return_value = "Şahin Akkaya"
        self.chat = Chat("chats/itu")
        self.assertEqual(self.chat.title_history[-1],"ITU COMPUTER 17-18")
        self.assertEqual(self.chat.type,"Group Chat")
        self.assertEqual(self.chat.right_side_person,"Şahin Akkaya")
        self.assertEqual(len(self.chat.persons['Şahin Akkaya'].existence),2)
        # self.assertTrue(all(self.chat.persons[p].existence[0][0] is not None for p in self.chat.persons))
        # self.assertTrue(all(self.chat.persons[p].existence[-1][1] is not None for p in self.chat.persons))

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('builtins.input')
    def test_single_chat(self, fake_stdin, fake_stdout):
        fake_stdin.return_value = "Babam"
        self.chat = Chat("chats/babam")
        self.assertEqual(self.chat.title_history[-1], "Şahin Akkaya")
        self.assertEqual(self.chat.type, "2 Person Chat")
        self.assertEqual(self.chat.right_side_person, "Babam")
        self.assertListEqual(self.chat.persons['Babam'].existence, [[None,None]])



    def test_create(self):
        line = Line('9/16/17, 9:06 PM - ‪+90 534 317 04 77‬ created group "İTÜ BİLGİSAYAR 17-18"‬‬')
        self.assertEqual(line.text, '9/16/17, 9:06 PM - +90 534 317 04 77 created group "İTÜ BİLGİSAYAR 17-18"')
        self.assertEqual(line.operation, "CreateGroup")
        self.assertEqual(line.time, datetime(2017, 9, 16, 21, 6))
        self.assertSetEqual(line.affected_persons, set())
        self.assertSetEqual(line.main_persons, {"+90 534 317 04 77"})


    def test_send_message(self):
        line = Line("10/6/17, 6:11 PM - ‪+90 506 369 83 17‬: Merhaba")
        self.assertEqual(line.text,"10/6/17, 6:11 PM - +90 506 369 83 17: Merhaba")
        self.assertEqual(line.operation,"SendMessage")
        self.assertEqual(line.time,datetime(2017,10,6,18,11))
        self.assertSetEqual(line.slice_to_person(line.text,"right"),set())
        self.assertSetEqual(line.slice_to_person(line.text,),{"+90 506 369 83 17"})

    def test_add(self):
        line = Line("4/10/18, 15:54 - ‪+90 554 643 08 24‬ added ‪+90 531 226 92 68‬ and ‪+90 544 534 33 90‬‬")
        self.assertEqual(line.text, "4/10/18, 15:54 - +90 554 643 08 24 added +90 531 226 92 68 and +90 544 534 33 90")
        self.assertEqual(line.operation, "AddPerson")
        self.assertEqual(line.time, datetime(2018, 4, 10, 15, 54))
        self.assertSetEqual(line.affected_persons, {"+90 531 226 92 68","+90 544 534 33 90"})
        self.assertSetEqual(line.main_persons, {"+90 554 643 08 24"})

        line = Line("4/10/18, 15:54 - Şahin Akkaya‬ added person name with colon : (Weird person)‬")
        self.assertEqual(line.operation, "AddPerson")
        self.assertSetEqual(line.main_persons, {"Şahin Akkaya"})
        self.assertSetEqual(line.affected_persons, {"person name with colon : (Weird person)"})


    def test_remove(self):
        line = Line("10/26/17, 2:42 PM - ‪+90 534 317 04 77‬ removed ‪+90 546 402 31 26‬")
        self.assertEqual(line.text, "10/26/17, 2:42 PM - +90 534 317 04 77 removed +90 546 402 31 26")
        self.assertEqual(line.operation, "RemovePerson")
        self.assertEqual(line.time, datetime(2017, 10, 26, 14, 42))
        self.assertSetEqual(line.affected_persons,{"+90 546 402 31 26"})
        self.assertSetEqual(line.main_persons, {"+90 534 317 04 77"})

    def test_left(self):
        line = Line("10/8/17, 4:51 PM - ‪+90 534 857 69 22‬ left‬")
        self.assertEqual(line.operation, "LeftGroup")
        self.assertEqual(line.time, datetime(2017, 10, 8, 16, 51))
        self.assertSetEqual(line.affected_persons, set())
        self.assertSetEqual(line.main_persons, {"+90 534 857 69 22"})

    def test_joined(self):
        line = Line("10/6/17, 6:06 PM - You joined using this group's invite link‬")
        self.assertEqual(line.operation, "JoinedGroup")
        self.assertEqual(line.time, datetime(2017, 10, 6, 18, 6))
        self.assertSetEqual(line.affected_persons, set())
        self.assertSetEqual(line.main_persons, {"You"})




if __name__ == '__main__':
    unittest.main()
