import unittest

import cereal.cython.log as cython_log
from cereal import car, log


class TestStruct(unittest.TestCase):
  def test_struct(self):
    cs = car.CarState.new_message()
    cs.brake = 10.1
    cs.gasPressed = True

    b = cs.to_bytes()
    cs_cython = cython_log.CarState(b)

    self.assertAlmostEqual(cs.brake, cs_cython.brake)
    self.assertTrue(cs_cython.gasPressed)

  def test_nested_struct(self):
    cs = car.CarState.new_message()
    cs.cruiseState.enabled = True
    cs.cruiseState.speed = 1234.5

    b = cs.to_bytes()
    cs_cython = cython_log.CarState(b)

    self.assertAlmostEqual(cs.cruiseState.speed, cs_cython.cruiseState.speed)
    self.assertTrue(cs_cython.cruiseState.enabled)

  def test_enum(self):
    cs = car.CarState.new_message()
    cs.gearShifter = car.CarState.GearShifter.drive

    b = cs.to_bytes()
    cs_cython = cython_log.CarState(b)
    self.assertEqual(cs_cython.gearShifter, car.CarState.GearShifter.drive)

  def test_union(self):
    l = log.Event.new_message()
    l.init('thermal')
    l.thermal.cpu0 = 100

    b = l.to_bytes()
    l_cython = cython_log.Event(b)

    self.assertEqual(l_cython.which(), l.which())
    self.assertEqual(l_cython.thermal.cpu0, l.thermal.cpu0)


  def test_list_of_primitive(self):
    cs = car.CarState.new_message()
    cs.canMonoTimes = [0, 1, 2, 3, 4]

    b = cs.to_bytes()
    cs_cython = cython_log.CarState(b)
    self.assertEqual(cs_cython.canMonoTimes, list(cs.canMonoTimes))


  def test_list_of_struct(self):
    cs = car.CarState.new_message()
    cs.init('events', 3)
    cs.events[0].enable = True
    cs.events[2].enable = True

    b = cs.to_bytes()
    cs_cython = cython_log.CarState(b)

    enables = [c.enable for c in cs_cython.events]
    self.assertEqual(enables, [True, False, True])

  def test_list_of_union(self):
    cs = car.CarState.new_message()
    cs.errorsDEPRECATED = ["wrongGear", "doorOpen"]

    b = cs.to_bytes()
    cs_cython = cython_log.CarState(b)
    self.assertEqual(cs_cython.errorsDEPRECATED, [car.CarEvent.EventName.wrongGear, car.CarEvent.EventName.doorOpen])


  def test_text(self):
    cp = car.CarParams.new_message()
    cp.carName = "mock"

    b = cp.to_bytes()
    cp_cython = cython_log.CarParams(b)
    self.assertEqual(cp_cython.carName, cp.carName)

  def test_data(self):
    can = log.CanData.new_message()
    can.dat = b"\x01\x02\x00\x03"

    b = can.to_bytes()
    can_cython = cython_log.CanData(b)
    self.assertEqual(can_cython.dat, can.dat)