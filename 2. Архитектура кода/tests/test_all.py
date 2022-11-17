from doctor.test import TestDoctor
from user.test import TestUser
from user_not_foud.test import TestUserNotFound

TestUser().test_all()
print("TestUser passed")
TestDoctor().test_all()
print("TestDoctor passed")
TestUserNotFound().test_all()
print("TestUserNotFound passed")
